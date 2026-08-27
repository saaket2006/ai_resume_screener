import re

with open("backend/routers/recruiter.py", "r") as f:
    content = f.read()

old_loop = """        # Save each parsed candidate resume and scan result
        for cand in results.get("results", []):
            # Skip invalid/error files from saving
            if cand.get("email") == "N/A" and cand.get("name") in ("Unsupported/Invalid File", "File Too Large (>5MB)"):
                continue

            fn = cand.get("filename", "unknown_file")
            ext = fn.split(".")[-1].lower() if "." in fn else "unknown"
            from backend.services.pipeline import PersistenceStage
            persist_stage = PersistenceStage(db)

            # Pass context down to persistence stage so metrics get saved
            pipeline_ctx = cand["pipeline_context"]

            persistence_result = persist_stage.execute(
                pipeline_ctx,
                candidate_id=None,
                version=1,
                label=None,
                label_source="SYSTEM",
                job_description_id=jd_model.id,
                ats_score=cand["similarity_score"],
                elapsed_ms=0
            )
            if persistence_result.status != "success":
                raise HTTPException(status_code=500, detail=persistence_result.error_message)

        db.commit()
        logger.info("Screening persisted successfully for job description ID %d", jd_model.id)"""

new_code = """        # Save each parsed candidate resume and scan result
        from backend.services.pipeline import PersistenceStage
        persist_stage = PersistenceStage(db)

        batch_args = []
        for cand in results.get("results", []):
            # Skip invalid/error files from saving
            if cand.get("email") == "N/A" and cand.get("name") in ("Unsupported/Invalid File", "File Too Large (>5MB)"):
                continue

            pipeline_ctx = cand["pipeline_context"]

            batch_args.append({
                "arg": pipeline_ctx,
                "kwargs": {
                    "candidate_id": None,
                    "version": 1,
                    "label": None,
                    "label_source": "SYSTEM",
                    "job_description_id": jd_model.id,
                    "ats_score": cand["similarity_score"],
                    "elapsed_ms": 0
                }
            })

        if batch_args:
            batch_results = persist_stage.execute_batch(batch_args)
            for res in batch_results:
                # If it's a context, the event is nested
                event = res.event if hasattr(res, 'event') else res
                if event.status != "success":
                    raise HTTPException(status_code=500, detail=event.error_message)

        db.commit()
        logger.info("Screening persisted successfully for job description ID %d", jd_model.id)"""

new_content = content.replace(old_loop, new_code)

with open("backend/routers/recruiter.py", "w") as f:
    f.write(new_content)

print("Patched recruiter.py")
