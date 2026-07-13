from backend.services.skills.extractor import SkillExtractor
from backend.services.semantic.matcher import SemanticMatcher
from backend.services.semantic.resolver import resolve_relationship

e = SkillExtractor()
jd_skills = e.extract("We need a Frontend Developer with HTML, CSS, React, and Flask experience.")
print("JD skills:")
for s in jd_skills:
    print(f"  {s.id}: {s.canonical_name} (cat={s.category}, sub={s.subcategory}, family={s.technology_family})")

# Simulate candidate skills from the frontend resume
cand_skills = e.extract("Skills: HTML, CSS, JavaScript, React, frontend, angular, vue, next.js, bootstrap, tailwind, sass, less, node.js")
print("\nCandidate skills:")
for s in cand_skills:
    print(f"  {s.id}: {s.canonical_name} (cat={s.category}, sub={s.subcategory}, family={s.technology_family})")

print("\n--- Semantic Matching ---")
matcher = SemanticMatcher()
results = matcher.match_skills(jd_skills, cand_skills)
for r in results:
    print(f"  Required: {r.required_skill.canonical_name} -> Candidate: {r.candidate_skill.canonical_name} | Type: {r.match_type} | Weight: {r.weight} | Reason: {r.reason}")

# Debug: direct HTML -> HTML resolution
print("\n--- Direct HTML -> HTML resolution ---")
html_jd = next(s for s in jd_skills if s.id == "html")
html_cand = next((s for s in cand_skills if s.id == "html"), None)
if html_cand:
    t, c, w, r = resolve_relationship(html_jd, html_cand)
    print(f"  HTML -> HTML: type={t}, weight={w}, reason={r}")
else:
    print("  HTML not found in candidate skills!")
