# Software Technology 1 Assignment 3

One group repository and one evolving SmartCare application.

Requirements baseline: SmartCare A3 2026, revision 2. The common undergraduate functionality from Stages 6-9 has been implemented. Stage 12 final release verification is in progress.

## Group index

- Group and tutorial: Tuesday 1:30-3:30, Group 2
- Member names, GitHub usernames and UG/PG cohorts: Alex Marek (UG) — CoolCoder49; Kreesha Singh (UG) — kreesha-12
- Shared repository URL: [https://github.com/CoolCoder49/st1--assignment-3](https://github.com/CoolCoder49/st1--assignment-3)
- Latest completed stage: 9 (Stage 12 in progress)
- Verified common starting SHA: `89d106fecbd1671a184728f233c3e669ea0a7957`
- Test command, working directory and observed result: `python -m pytest -q` from `project/` - 61 passed in 0.07s after the Stage 12 import correction, using Python 3.14.6 and pytest 9.2.0.
- Final submitted SHA, if different from tested code SHA: Pending final verification, commit and integration.

Do not put student IDs, private peer ratings, credentials or personal contact details here.

## Complete package and stage sequence

All Assignment 3 materials were supplied at the beginning, including the Overview, Git/GitHub Group Guide, Stage 6-12 handouts, SmartCare starter, activity/evidence records and assessment instructions/forms.

The project was developed continuously through the applicable stages:

UG: 6 → 7 → 8 → 9 → 12

PG: 6 → 7 → 8 → 9 → 10 → 11 → 12

Our group follows the UG pathway. Stages 6-9 have been completed and integrated into the common project. Stage 12 focuses on final testing, documentation, review and release.

One group repository and one evolving `project/` directory have been used throughout. Previous code, tests, evidence records and Git history are retained.

Stages 10 and 11 are PG-only and are not applicable to our group. Their supplied templates remain unchanged.

The Stage 8 preparation utility is a controlled teaching asset and is not included in the final project submission.

The final Stage 12 record will include verification results, review evidence, the exact submitted SHA and the final source ZIP.

## Application and evidence

- [Application setup and commands](project/README.md)
- [Stage 6 activities and evidence](stage06/stage06_activities_and_evidence.md)
- [Stage 7 activities and evidence](stage07/stage07_activities_and_evidence.md)
- [Stage 8 activities and evidence](stage08/stage08_activities_and_evidence.md)
- [Stage 9 activities and evidence](stage09/stage09_activities_and_evidence.md)
- [Stage 10 PG activities and evidence](stage10_pg/stage10_activities_and_evidence.md)
- [Stage 11 PG activities and evidence](stage11_pg/stage11_activities_and_evidence.md)
- [Stage 12 activities and evidence](stage12/stage12_activities_and_evidence.md)

Git commands run from the repository root. Application commands run from `project/`:

```powershell
cd project
python -m pip install -r requirements-dev.txt
python main.py
python main.py --interactive
python -m pytest -q
cd ..
```

The teaching baseline is Python 3.13 with pytest 8.3.5. The Stage 12 tests have passed using Python 3.14.6 and pytest 9.2.0. Final release verification remains pending.

SmartCare uses session-only in-memory storage, so records are lost when the application exits. Only synthetic data must be used.

GitHub Copilot was used during development, with significant suggestions and human decisions documented in the stage evidence records. ChatGPT also assisted with documentation and identifying a missing import. Final independent review and release approval remain pending.