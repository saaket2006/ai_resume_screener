import re

with open("backend/services/pipeline.py", "r") as f:
    content = f.read()

batch_execute = """
    def execute_batch(self, args_list: list, **common_kwargs) -> list:
        \"\"\"Batch executes persistence for multiple items, optimizing N+1 database queries.\"\"\"
        if not args_list:
            return []

        outputs = []
        valid_items = []

        # Prepare Resumes
        for item in args_list:
            arg = item.get("arg")
            kwargs = item.get("kwargs", {})
            # Merge common kwargs with specific kwargs
            merged_kwargs = {**common_kwargs, **kwargs}

            is_context = isinstance(arg, AnalysisContext)
            event = arg.event if is_context else arg

            output = PersistenceEvent(event)
            outputs.append(output)

            if output.status != "success":
                if is_context:
                    arg.event = output
                continue

            try:
                candidate_id = merged_kwargs.get("candidate_id")
                version = merged_kwargs.get("version", 1)
                label = merged_kwargs.get("label")
                label_source = merged_kwargs.get("label_source", "SYSTEM")
                job_description_id = merged_kwargs.get("job_description_id")
                ats_score = merged_kwargs.get("ats_score", 0.0)
                elapsed_ms = merged_kwargs.get("elapsed_ms", 0)

                scoring = event.explanation.scoring
                extraction = scoring.matching.skills.extraction

                meta = event.explanation.analysis_metadata
                meta["score"]["overall"] = ats_score
                meta["engine"]["processing_time_ms"] = elapsed_ms

                if is_context:
                    meta["pipeline_metrics"] = arg.metrics

                resume = Resume(
                    candidate_id=candidate_id,
                    extracted_text=extraction.raw_text,
                    original_filename=extraction.filename,
                    file_type=extraction.file_ext,
                    version=version,
                    label=label,
                    label_source=label_source,
                    status=ResumeStatus.ACTIVE
                )
                valid_items.append({
                    "resume": resume,
                    "meta": meta,
                    "job_description_id": job_description_id,
                    "ats_score": ats_score,
                    "output": output
                })
            except Exception as e:
                logger.error("Error preparing persistence for item: %s", e)
                output.status = "error"
                output.error_message = f"Data preparation failed: {str(e)}"
                if is_context:
                    arg.event = output

        if not valid_items:
            return outputs

        try:
            # Batch insert Resumes
            resumes_to_add = [item["resume"] for item in valid_items]
            self.db.add_all(resumes_to_add)
            self.db.flush()

            # Batch insert ScanResults
            scan_results_to_add = []
            for item in valid_items:
                resume = item["resume"]
                scan_result = ScanResult(
                    resume_id=resume.id,
                    job_description_id=item["job_description_id"],
                    ats_score=item["ats_score"],
                    analysis_metadata=item["meta"]
                )
                scan_results_to_add.append(scan_result)
                item["scan_result"] = scan_result

            self.db.add_all(scan_results_to_add)
            self.db.flush()

            # Finalize outputs
            for item in valid_items:
                resume = item["resume"]
                scan_result = item["scan_result"]
                output = item["output"]

                output.resume_id = resume.id
                output.scan_result_id = scan_result.id
                output.recommendation.explanation.scoring.similarity_score = item["ats_score"]

            logger.info("Pipeline batch persisted %d Resumes and ScanResults successfully", len(valid_items))
        except Exception as e:
            self.db.rollback()
            logger.error("Batch persistence failed: %s", e)
            for item in valid_items:
                output = item["output"]
                output.status = "error"
                output.error_message = f"Database batch persistence failed: {str(e)}"

        # Make sure the context events are updated as well for the ones that were successfully run
        for i, item in enumerate(args_list):
            arg = item.get("arg")
            is_context = isinstance(arg, AnalysisContext)
            if is_context:
                # the outputs array corresponds 1:1 with args_list
                arg.event = outputs[i]
                outputs[i] = arg

        return outputs
"""

new_content = content.replace("    def execute(self, arg: Any, **kwargs) -> PersistenceEvent:", batch_execute + "\n    def execute(self, arg: Any, **kwargs) -> PersistenceEvent:")

with open("backend/services/pipeline.py", "w") as f:
    f.write(new_content)

print("Patched pipeline.py")
