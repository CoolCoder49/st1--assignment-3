# Stage 12 activities and evidence

Group/tutorial: Tuesday 1:30-3:30, Group 2
Members and UG/PG applicability: Alex Marek (UG) and Kreesha Singh (UG).


## A Release scope and starting SHA

Release label/version and requirements baseline:

SmartCare Stage 12 Undergraduate Final Release, using SmartCare A3 Requirements Baseline 2026, revision 2. The release covers the completed functionality from Stages 6-9, including patient and practitioner registration and lookup, appointment booking, conflict prevention, cancellation, retained appointment history, practitioner appointment listing, filtering, sorting and the interactive console. The application uses session-only in-memory storage. The final release SHA will be confirmed after all Stage 12 verification and integration activities are complete.

Common starting SHA / branch / applicable members:

The common starting commit is `89d106fecbd1671a184728f233c3e669ea0a7957` on `main`. This commit includes the completed Stage 9 implementation and its final evidence record. Stage 12 work was prepared on the separate release/stage12-common branch, created from the starting commit. Kreesha approved PR #11, which was then merged into main. Both Alex and Kreesha are included in the undergraduate common release.

PG starting SHA / branch / applicable members or not applicable:

Not applicable. Both group members are undergraduate students, so no PG extension branch or separate PG release candidate is required. Stages 10 and 11 are not part of our assessed project.

Working-state review and approved integration:

Before beginning Stage 12, I checked the local repository and its GitHub connection using Git commands. The working tree was clean, and the local `main` branch matched `origin/main`, with zero commits ahead and zero commits behind.

Stage 9 was merged into `main` through Pull Request #10 at commit `1b2c48f`, followed by the Stage 9 evidence update at `89d106f`. However, the Stage 9 pull request was merged without my recorded independent review. I did not complete this review before merging, and I will not report it as an earlier approval. I will check the integrated code independently during Stage 12.

I then ran the complete automated test suite from the `project/` directory using `python -m pytest -q`. The result was **61 passed in 0.08 seconds**, using Python 3.14.6 and pytest 9.2.0. This confirms that the current integrated application passes all 61 available tests in my local environment. The final release will still require further verification, including the interactive console, documentation, code quality and reproducibility checks.

Protected common candidate and PG differences:

The starting common candidate is commit `89d106fecbd1671a184728f233c3e669ea0a7957`. This starting version remains recoverable through Git history. Stage 12 changes were developed separately on release/stage12-common before independent review and integration into main.

There is no PG extension or alternative PG candidate because both group members are undergraduate students. The final common release SHA will be recorded after all required Stage 12 checks and any necessary reviewed corrections are complete.

Feature freeze / owner / verifier:

Optional feature development has been stopped for Stage 12. The remaining work will focus on checking the existing application, verifying requirements, completing release documentation, reviewing code quality, and correcting any genuine release blockers identified. No new database, persistence system, rescheduling feature or unnecessary dependency will be introduced.

Alex is responsible for preparing the Stage 12 release evidence and coordinating final verification. Kreesha independently reviewed and approved Pull Request #11 before it was merged into `main`. The merged application passed all 61 tests using Python 3.13.17 and pytest 8.3.5. Final submission packaging and fresh-copy verification are still pending.

## B Requirements and release readiness matrix

Tutorial activity 1: All tests pass, README setup is incomplete, one dependency is unreviewed and a known limitation is undocumented. Decide Release / Release with conditions / Do not release and justify:

Do not release yet.

Although all automated tests pass, the application is not fully ready for release. In the example, the README setup instructions are incomplete, a dependency hasn't been reviewed, and a known limitation hasn't been documented. These issues could prevent another developer from running the application correctly or understanding its limitations.

Before approving the release, the team should complete the README with accurate setup and testing instructions, review the dependency to confirm that it is required and appropriate, and document the known limitation. Another group member should then verify that the application can be set up and run using the supplied instructions.

Passing tests show that the tested functionality works, but release readiness also requires complete documentation, reviewed dependencies, reproducibility, and an informed decision about remaining risks. Do not release the application until these issues have been addressed and verified.

Tutorial activity 2 and actual readiness matrix. Add exact requirement/acceptance IDs, evidence and reviewer; distinguish common/PG applicability.

| Release claim / requirement / scope | Evidence | Location/link and SHA | Reviewer | Sufficient? | Gap/action |
|---|---|---|---|---|---|
| Cancellation history works | Automated tests and an interactive demonstration confirmed that cancelled appointments remain retrievable and repeated cancellations are rejected. | `project/tests/`; Section D; `0a4d764` | Alex; PR #11 approved by Kreesha | Yes | None |
| Architecture responsibilities are appropriate | Domain, store, services, queries and console responsibilities reviewed. | `project/smartcare/`; Section E; `0a4d764` | Alex; PR #11 approved by Kreesha | Yes | None identified |
| Rescheduling is safe — PG only | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| AI use is responsible | Stage 8 Copilot evidence and Stage 12 AI decisions documented and human-verified. | `stage08/`, Sections E and N | Alex | Yes | Stage 9 missing independent PR review disclosed |
| System is maintainable | Module responsibilities, naming, imports and code structure reviewed. Missing import corrected. | `project/smartcare/`; Section E; `0a4d764` | Alex; PR #11 approved by Kreesha | Yes | Production-scale assurance excluded |
| FR-01–03 register/find and validation | Tests and interactive demonstration confirmed registration, lookup, duplicate-ID rejection and unknown-ID handling. | `project/tests/`; Section D; `0a4d764` | Alex | Yes | None |
| FR-04–05 booking/conflict rules | Tests and console demonstration confirmed successful bookings, conflict rejection and different-practitioner bookings. | `project/tests/`; Section D; `0a4d764` | Alex | Yes | None |
| FR-06–08 cancellation/history/find | Tests and console demonstration confirmed cancellation, retained history and appointment lookup. | `project/tests/`; Section D; `0a4d764` | Alex | Yes | None |
| FR-09 and QRY/FP listing/filter/order/purity | Automated query tests and console demonstration confirmed filtering, sorting and correct appointment listings. | `project/tests/test_queries.py`; Section D; `0a4d764` | Alex | Yes | None |
| UI full console sequence and error recovery | Registration, booking, cancellation, listing, invalid-input recovery and restart behaviour demonstrated. | `project/smartcare/console.py`; Section D | Alex | Yes | None |
| Session-only scope / FR-10 retired | Session data was lost after restart, as required. Limitation documented in both README and release notes. | `project/smartcare/data_store.py`; Section G | Alex | Yes | Intentional session-only limitation |
| PG RES and assurance integration | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |


## C Full regression results

| Suite/scope | Environment/version | Working directory and command | Tested SHA | Actual result | Evidence link |
|---|---|---|---|---|---|
| Complete common | Python 3.14.6, pytest 9.2.0, PyCharm | `project/` - `python -m pytest -q` | `89d106fecbd1671a184728f233c3e669ea0a7957` | 61 passed in 0.08s | Local PyCharm terminal output; `project/tests/` |
| Complete PG if applicable | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Affected focused checks after correction | Python 3.14.6, pytest 9.2.0 | `project/` - `python -m pytest -q` | Stage 12 branch, uncommitted correction | 61 passed in 0.07s after adding the missing `datetime` import. | PyCharm terminal output; `git diff -- smartcare/services.py` |
| Full integrated recheck | Python 3.13.17, pytest 8.3.5 | `project/` - `python -m pytest -q` | `0a4d76429ca42ce5cab4b67dce0c9adc9d014a17` | 61 passed in 0.06s after merging PR #11. | PyCharm terminal output; `project/tests/`; PR #11 |

Prior assertions preserved / reviewed test diff:

All six existing test files were preserved. No test assertions were changed or removed during Stage 12. The only Python correction was adding `from datetime import datetime` to `services.py`. All 61 tests passed on both Python versions after the correction.

Remaining failure / limitation:

No automated test failures remain. The interactive demonstration and invalid-input recovery checks passed. Kreesha independently approved PR #11, and all 61 tests passed on the merged commit using Python 3.13.17 and pytest 8.3.5. Session-only storage remains an intentional limitation. Fresh-copy and submission ZIP verification are still pending.

## D Console and end to end demonstration

| Demo step | Synthetic setup/input | Expected requirement | Observed result | Evidence/link |
|---|---|---|---|---|
| Problem and stakeholders | SmartCare appointment management for patients and practitioners. | Manage registration, booking, cancellation and lookup. | PASS: Interactive menu launched successfully. | `project/main.py`, `project/smartcare/console.py` |
| Register and find Patient and two Practitioners | Register P1 (John Doe), D1 (Dr John Doe, General Practice) and D2 (Dr John Smith, Neurology). Look up P1 and D2. | FR-01-03: Register and retrieve participants. | PASS: All registered and retrieved successfully. | Console demonstration |
| Valid booking | Book A1: P1 with D1, `2026-12-01 09:00`. | FR-04: Book a valid SCHEDULED appointment. | PASS: A1 booked successfully. | Console demonstration |
| Same practitioner exact-time conflict rejected | Attempt A2 with D1 at the same time as A1. | FR-05: Reject conflicting bookings. | PASS: Conflict error displayed. | Console demonstration |
| Different practitioner same time allowed | Book A2 with D2 at `2026-12-01 09:00`. | FR-05: Allow different practitioners at the same time. | PASS: A2 booked successfully. | Console demonstration |
| Cancel SCHEDULED and retain/find CANCELLED object | Cancel A1 and retrieve it. | FR-06-08: Cancel and retain appointment history. | PASS: A1 remained retrievable with CANCELLED status. | Console demonstration |
| Invalid/repeated cancellation rejected | Attempt to cancel A1 again. | FR-06: Only SCHEDULED appointments can be cancelled. | PASS: Repeated cancellation rejected. | Console demonstration |
| Default all-status listing | List D1 appointments without a status filter. | FR-09, QRY-01-02: Include all statuses. | PASS: A1 and A3 displayed after rebooking. | Console demonstration |
| Explicit filtering / empty vs unknown / deterministic order | Filter D1 by scheduled; search D99; list A1 and A3. | QRY-01-04: Correct filtering, errors and ordering. | PASS: Correct filtered results, unknown practitioner error and A1-before-A3 ordering. | Console demonstration |
| Invalid date/status/menu/lookup recovery and continued operation | Invalid dates, status `schedulled`, menu inputs `99` and `abc`, unknown IDs and duplicate registration. | UI-02: Reject invalid inputs without corrupting records. | PASS: Errors displayed; rejected appointments absent; valid operations still worked. | Console demonstration |
| Session-only limitation and normal exit | Exit, restart and search for A3. | Session data is not persistent. | PASS: A3 was not found after restart. | Console demonstration |
| One meaningful requirement-linked pytest test explained | Appointment workflow tests. | Verify booking, conflict prevention and cancellation. | PASS: Full suite: 61 tests passed in 0.08s. Workflow tests cover these behaviours. | `project/tests/test_workflows.py` |
| Architecture and one actual AI decision / known limitation | Module responsibilities and Stage 9 AI evidence. | Separate responsibilities and evaluate AI suggestions. | Domain, store, services, queries and console have separate responsibilities. Stage 9 records rejecting unnecessary permanent storage. | `project/smartcare/`, Stage 9 evidence |
| PG reschedule identity/participants/time and no-op | Not applicable | Not applicable | Not applicable | Stage 12 handout |
| PG conflict/invalid status/failure non-mutation | Not applicable | Not applicable | Not applicable | Stage 12 handout |
| PG old slot / current lookup/list ordering / assurance risks | Not applicable | Not applicable | Not applicable | Stage 12 handout |

Stable demo owner / fresh process / command: Alex, `python main.py --interactive` from `project/`, Python 3.14.6, starting SHA `89d106fecbd1671a184728f233c3e669ea0a7957`. Demonstrated scenarios passed.

PG demonstrations through service/tests or not applicable: Not applicable


## E Final code quality and AI review

| Review area | Code/evidence location | Finding or no finding | Correction/no change and recheck |
|---|---|---|---|
| OOP responsibilities and pure-query boundaries | `project/smartcare/` | Domain, data store, services, queries and console have separate responsibilities. Queries do not modify source records. | No further change required from Alex's inspection. Kreesha independently reviewed and approved PR #11. |
| PascalCase and snake_case naming | SmartCare Python modules | Classes use PascalCase; functions and variables use snake_case. | No significant naming issue identified. |
| Useful type hints and meaningful docstrings | `services.py` and other modules | A missing `datetime` import was identified in `services.py`. | Added `from datetime import datetime`. Full suite: 61 passed in 0.07s. |
| Four-space indentation and imports/layout | SmartCare Python modules | Code is readable; standard-library import was missing from `services.py`. | Added missing import. |
| Focused methods / duplication / dead or commented code | `project/smartcare/` | No major structural problem identified during initial inspection. | Final repository review pending. |
| Globals / leakage / unnecessary inheritance or frameworks | `data_store.py`, `services.py`, `console.py` | Services share one session data store. No unnecessary framework was identified. | No change required. |
| No SQLite/persistence/repository ABCs/speculative features | `data_store.py` | Records use session-only in-memory storage as required. | No change required. |
| Synthetic data / secrets / dependencies / provenance | Console demonstration; `requirements-dev.txt` | Synthetic data was used during testing. | Final repository and dependency checks pending. |
| Significant common Copilot contributions and human verification | Stage 8 and Stage 9 evidence records | Stage 8 includes recorded Copilot diagnoses and human checks. Stage 9 independent PR review was missed. | Disclose the missing review. |
| PG plan/diff/test approvals and Stage 11 VERIFY/TRUST | Not applicable | Not applicable | Not applicable. |

| AI claim | Affected requirement/code | Human check | Accept/Modify/Reject and reason | Actual outcome/action or no change |
|---|---|---|---|---|
| Incorrect practitioner comparison caused conflict failures. | FR-05; `data_store.py` | Alex inspected the condition and regression tests during Stage 8. | Accept: `!=` incorrectly allowed conflicting bookings. | Changed to `==`; regression tests passed. |
| Cancelled-status filtering prevented appointment lookup. | FR-07; `data_store.py` | Alex inspected the stored appointment and lookup condition during Stage 8. | Accept: cancelled appointments must remain retrievable. | Removed the incorrect filter; regression tests passed. |
| Permanent storage should not be added. | Session-only requirement | Stage 9 evidence records rejecting unnecessary persistence. | Reject additional storage: outside project scope. | No database or file persistence added. |
| Missing `datetime` import could affect compatibility. | `services.py` | Alex applied the import and ran the full test suite. | Accept: the annotation requires the import for Python 3.13. | Added the missing import. All 61 tests passed using Python 3.13.17 and pytest 8.3.5, including 61 passed in 0.06s on the merged commit. |

Access route or approved equivalent / limitations: GitHub Copilot was used through PyCharm during Stage 8. Saved evidence is available in `stage08/copilot_f8_01_diagnosis.md` and `stage08/copilot_f8_02_diagnosis.md`. Stage 9 AI review details are recorded in its evidence file, but the independent PR review was not completed.

Available AI evidence and missing evidence honestly disclosed: Stage 8 includes recorded AI prompts, diagnoses, human decisions and test results. ChatGPT assisted with Stage 12 documentation and identifying the missing import; Alex applied the correction and verified the tests. The missing independent review of Stage 9 remains disclosed. Kreesha independently approved Stage 12 PR #11 before merging. Final release packaging and approval are still pending.


## F README and reproducibility check

| README item | Location | Verifier | Result/gap |
|---|---|---|---|
| Purpose and included common/PG scope | `README.md`, `project/README.md` | Alex | Updated. Common UG scope documented; PG stages marked not applicable. |
| Out-of-scope capabilities and known limitations | `project/README.md` | Alex | Session-only storage and excluded production features documented. |
| Confirmed teaching Python version and dependency installation | `project/README.md`, `requirements-dev.txt` | Alex | PASS: Python 3.13.17 and pytest 8.3.5 verified. |
| Working directory / demo / interactive / test commands | `project/README.md` | Alex | PASS: All three commands executed successfully. |
| Repository structure and architecture responsibilities | `project/README.md` | Alex | Updated with module responsibilities. |
| Responsible AI summary / synthetic-data rule | Both README files | Alex | Documented. |
| Release label/version and SHA links | Both README files | Alex | Stage 12 UG release identified. Final release SHA pending. |

Root README index and project/README verified:

Both README files were updated with the SmartCare features, setup instructions, architecture, requirements and limitations. Kreesha independently reviewed and approved the Stage 12 changes through PR #11. Fresh-copy reproducibility verification is still pending.

Fresh clone or extracted ZIP / candidate identity:

PR #11 was merged into main at commit 0a4d76429ca42ce5cab4b67dce0c9adc9d014a17. All 61 tests passed on this merged commit using Python 3.13.17 and pytest 8.3.5. Testing from a freshly extracted submission ZIP is still pending.

Verifier and clean environment / actual version:

Alex created a separate Python 3.13 virtual environment outside the repository. Python 3.13.17 and pytest 8.3.5 were verified. Kreesha's independent verification remains pending.

Setup/run/test commands and observed results:

From the repository root, dependencies were installed using `-m pip install -r project/requirements-dev.txt` with the separate Python 3.13 interpreter.

From `project/`, the following were verified:

- `python main.py` - PASS.
- `python main.py --interactive` - PASS.
- `python -m pytest -q` - 61 passed in 0.11s.

All commands used Python 3.13.17. The tests used pytest 8.3.5.

Missing local file or setup gap / remedy and recheck:

No setup or test failures were identified. Kreesha's independent PR review and integration are complete. Final ZIP verification, fresh-copy testing, and confirmation of the submitted commit SHA remain pending.


## G Known limitations debt and release notes

Delivered features:

SmartCare supports patient and practitioner registration and lookup; appointment booking; same-practitioner, same-time conflict prevention; cancellation with retained appointment history; practitioner appointment listing, status filtering and deterministic sorting; and an interactive console with input validation and error recovery.

Important fixes:

Stage 8 corrected conflict detection and cancelled-appointment lookup. Stage 12 added the missing `datetime` import in `services.py`. All 61 tests passed after this correction on Python 3.13.17 with pytest 8.3.5.

Architecture/quality improvements:

The application separates domain validation and state, in-memory storage, service coordination, pure appointment queries and console interaction. Existing regression tests were retained.

Known limitations:

All records are session-only and disappear on exit. The application is an educational appointment-management prototype, not a production healthcare system.

AI-assisted development note:

GitHub Copilot suggestions were evaluated against code and tests during Stage 8. ChatGPT assisted with Stage 12 documentation and identifying the missing import; Alex applied and tested the correction. Stage 9's missing independent pull-request review is disclosed, and final Stage 12 approval remains pending.


| Debt item | Impact | Priority | Future action | Accepted? / release rationale |
|---|---|---|---|---|
| Session-only storage | Records are lost when the application exits. | Low for coursework | Add persistence only if future requirements change. | Accepted design limit; restart persistence is not required. |
| No timezone policy | Appointment times are entered to minute precision without multi-timezone support. | Low for coursework | Define timezone handling if deployed across locations. | Accepted prototype limitation. |
| No production healthcare integrations or security controls | Not suitable for handling real clinical or patient data. | High for production | Design authentication, authorisation, privacy, and integrations before any real deployment. | Outside the undergraduate assignment scope; not accepted for production use. |
| Limited operational assurance | No demonstrated production-scale concurrency, monitoring or accessibility assessment. | Medium for future development | Conduct dedicated performance, operations, and usability testing. | Accepted for the course prototype, subject to final review. |

Session-only synthetic data and minute-precision local time:

The demonstration used synthetic patients and practitioners. Records remain in memory only until program exit. Appointment times use minute-precision input; no cross-timezone policy has been implemented.

Production auth/roles, portal, notifications, billing/insurance, clinical AI exclusions:

These are not delivered features.

Scale/concurrency, timezone policy, operations/monitoring, accessibility/usability limitations:

These areas have not been verified to production standards and would require separate requirements, development and testing before deployment.

Difference between accepted scope limit and unresolved required behaviour:

SmartCare includes the features required for our undergraduate assignment. Some features, such as permanent storage, online payments and patient portals, are not required and have intentionally been left out. These are known limitations rather than faults in the application.

PG assurance residual risks / owner / status or not applicable:

Not applicable.


## H Release findings and corrective action

| Requirement/claim | Reproduction/observation | Impact/severity | Owner/action | Corrective diff | Focused/full recheck | Residual limit |
|---|---|---|---|---|---|---|
| Python 3.13 compatibility and code quality | During code review, `services.py` was found to use `datetime` in a type hint without importing it. A failure on Python 3.13 before the fix was not directly tested. | Compatibility risk | Alex added the missing import. | Added `from datetime import datetime` to `project/smartcare/services.py`. | 61 passed in 0.07s on Python 3.14.6; 61 passed in 0.11s on Python 3.13.17; 61 passed in 0.06s on the merged commit. | Kreesha approved PR #11. No test failures remain. Fresh-copy and ZIP verification are pending. |
Justified no-change conclusion if no defect found:

One code issue was identified and corrected. No other defects requiring code changes were found during the completed checks. Existing test files and assertions were preserved.

Release blockers still open / status:

Kreesha's independent review and Git integration are complete. The merged application passed all 61 tests using Python 3.13.17 and pytest 8.3.5. No automated test failures are currently known. Final documentation, fresh-copy verification, ZIP creation and submission checks remain outstanding.

## I Git review and integration evidence

Issue / PR / diff links and reviewed SHA:

Stage 12 release candidate: c192bf6781f26298ef652e35d84cb183e46f4e22.

Pull Request #11: https://github.com/CoolCoder49/st1--assignment-3/pull/11

The pull request included both README updates, the Stage 12 evidence record and the missing datetime import in services.py.

Independent reviewer / feedback / response:

Kreesha independently reviewed and approved PR #11 before it was merged. No additional review comments or requested changes have been reported. The earlier missing Stage 9 review remains disclosed in Section A.

Integration commit / full recheck:

PR #11 was merged into main at 0a4d76429ca42ce5cab4b67dce0c9adc9d014a17.

Alex pulled the merged commit and ran the complete test suite using Python 3.13.17 and pytest 8.3.5. All 61 tests passed in 0.06 seconds.

Tracked and untracked file inspection / cleanliness:

Before committing, Git showed exactly four modified files and no errors from git diff --check. After merging and pulling, git status --short --branch confirmed that local main was clean and synced with origin/main.

Secrets/staff material/caches/tool-metadata exclusion check:

Final source ZIP and repository-content exclusion checks remain pending. These will confirm that no secrets, real patient data, staff solutions, virtual environments or unnecessary generated files are included.

Candidate recovery plan / known-good SHA:

The previous integrated version is 89d106fecbd1671a184728f233c3e669ea0a7957. The reviewed release candidate is c192bf6781f26298ef652e35d84cb183e46f4e22, and the tested merge commit is 0a4d76429ca42ce5cab4b67dce0c9adc9d014a17. Git history allows the earlier version to be recovered if necessary.

Named substantive contributions:

Alex completed Stages 6 and 8 and prepared the Stage 12 release, including documentation, the Python compatibility correction and final testing. Kreesha completed Stages 7 and 9 and independently approved the Stage 12 pull request.


## J Human release decision

Decision — READY FOR COURSE RELEASE / READY WITH DOCUMENTED LIMITATIONS / NOT YET READY:

NOT YET READY

Approver / date / rationale and evidence:

Kreesha independently reviewed and approved PR #11 before it was merged. Alex verified the merged commit 0a4d76429ca42ce5cab4b67dce0c9adc9d014a17 using Python 3.13.17 and pytest 8.3.5, with 61 tests passing in 0.06 seconds. Final release approval has not yet been recorded.

What risks remain / conditions / owners:

Alex must finish the Stage 12 evidence, create and verify the submission ZIP, confirm its contents match the intended Git commit, and complete the submission checklist. Fresh-copy verification remains outstanding.

Can the team explain the system:

Yes.

Can a change be recovered:

Yes.

Common decision / PG decision where different:

The undergraduate common release is awaiting final packaging and verification. The PG extension is not applicable.


## K Final tested release SHA

Exact common tested SHA:

0a4d76429ca42ce5cab4b67dce0c9adc9d014a17

Exact PG tested SHA or not applicable:

Not applicable

Final submitted SHA / repository URL:

https://github.com/CoolCoder49/st1--assignment-3

Evidence-only later commit and difference explanation:

The Stage 12 documentation changes will be committed separately after the tested application merge 0a4d764. No further executable changes have been made.

Executable changes after testing and re-verification:

No executable code changes have been made since the merged application passed all 61 tests. Any further executable changes would require another full test run.

Source ZIP name / SHA correspondence / extracted comparison:

Planned ZIP: SmartCare-Assignment3-Final-Submission.zip. The ZIP will contain the complete Assignment 3 repository contents required for our undergraduate pathway, including the application, tests, stage evidence, root README, and .gitignore. Creation from the final Git commit and extracted-copy verification are pending.


## L Submission package verification

- [x] Feature freeze and scoped requirements traced.
- [x] Applicable full regressions, integrated demo and invalid paths verified.
- [ ] Architecture/code quality and final AI/dependency checks complete.
- [ ] Root README and project/README reproduced by another verifier.
- [x] Release notes, technical debt and limitations visible.
- [ ] Independent human review, integration and release decision recorded.
- [ ] Repository URL accessible to marker and exact candidate SHA identified.
- [ ] One source ZIP from submitted commit with root README.md and .gitignore.
- [ ] project/ source and all accumulated applicable tests included.
- [ ] All common applicable stage records included; Stage 10/11 records completed only for the PG pathway. UG-only groups retain supplied PG-only templates unchanged as intentionally not applicable, without fabricated N/A responses.
- [ ] No .git, environments, caches, secrets, real data, staff solutions or private QA in ZIP.
- [ ] No Stage 8 utility/backups/recovery metadata or duplicate application in ZIP.
- [x] Mixed-group common protection and candidate upload routing checked.
- [ ] Group reflection, confidential individual peer forms and common team viva routed separately.

Confirmed assessment item/upload route:

Canvas → Group Assignment 3 → Website URL submission. One submission applies to the entire group. The assignment requires a complete source ZIP, a public GitHub repository URL, the full submitted commit SHA and the tested SHA. The repository URL is https://github.com/CoolCoder49/st1--assignment-3. The exact ZIP delivery method is not specified on the Canvas submission page and still needs confirmation.

Deadline/timezone:

9 Nov by 23:59 (GMT+11)

Repository access arrangement:

The repository must be public and accessible to teachers.

Mixed-candidate upload arrangement:

Not applicable.

Oral/video recording/accessibility arrangements:

The oral recording will be completed through Cadmus.

Remaining administration or release dependency:

Final evidence commit, source ZIP creation, extracted-copy verification, Canvas submission, group reflection, and peer review.


## M Formative questions

1. What is a release candidate?

A version of the software with its intended features completed, being checked for final release. It still needs testing, review and approval.

2. What is feature freeze and why is it used?

Feature freeze means stopping new feature development so the team can focus on fixing defects, testing and preparing the release. It reduces the risk of introducing new problems.

3. What is regression testing in a release context?

Regression testing checks that existing functionality still works after changes. For SmartCare, I ran all 61 automated tests after the Stage 12 correction and again after merging.

4. What is a known limitation?

A known limitation is something the software does not support or cannot do fully. SmartCare stores records only during the current session, and they disappear when the application closes.

5. What is technical debt?

Technical debt is work that may need improvement later, such as simplifying code, improving tests, or adding operational safeguards. It should be documented so future developers understand the risks.

6. What are release notes?

Release notes summarise the features delivered, important fixes, improvements and known limitations of a software version.

7. What is software maintenance?

Software maintenance involves correcting defects, improving code and adapting software when requirements or environments change after development.

8. What is the purpose of the individual demonstration/viva?

The viva checks that each student understands the system, can explain their own contribution and decisions throughout the project, and can demonstrate their knowledge about the code and tests.

9. What should the final responsible-AI check establish before release?

It should establish which AI suggestions were used, whether a human checked their outputs, whether the resulting code was tested, and whether any AI-related risks or limitations remain. AI-generated suggestions should not be treated as automatically correct.

10. What is the main course conclusion about AI and the role of the software engineer?

AI can help developers write, explain and debug code. Still, software engineers remain responsible for understanding requirements, evaluating suggestions, testing behaviour, reviewing changes and deciding whether software is ready for release.


## N Reflection viva and handover

Strongest evidence SmartCare is ready:

All 61 automated tests passed on the final integrated commit (Python 3.13.17, pytest 8.3.5). The interactive console was walked through with valid bookings, conflicts, cancellations, filtering, invalid inputs and session only. Kreesha approved PR #11 independently prior to integration.

Weakest area:

The application has not been tested for production use, and fresh-copy/ZIP verification is still pending. Its session-only storage is an intentional assignment limitation.

How AI use changed from Stage 1 to Stage 12:

As the project went on the AI assistance went from being used to generate suggestions to being used to review and check the work that we'd already done. In stage 8 I was comparing the Copilot diagnoses against the code and the regression tests. In stage 12 ChatGPT was used to spot a missing import and to draft the documentation, which I then applied and verified myself.

Start doing — engineering and AI use:

Complete independent reviews prior to merging any pull request and test the changes in the required Python environment as early as possible.

Stop doing — engineering and AI use:

Stop treating passing tests alone as sufficient release evidence, and avoid merging changes before the required independent review.

Continue doing — engineering and AI use:

Continue using focused tests, maintaining clear Git evidence, checking AI suggestions manually and documenting decisions honestly.

What worked / caused rework / future delivery improvement:

The separate domain, store, services, queries and console modules all went a long way to keeping the app understandable. Regression tests were useful in identifying and verifying the fixes. The missed Stage 9 pull request review and the missing 'datetime' import were good reminders as to why code review and environment compatibility checks are important. In future I would definitely use a consistent review and release checklist throughout the development cycle.

One paragraph — If AI can write code why do we still need software engineers:

Software engineers are still absolutely required as writing code is only one element of the process of building reliable software. You need the engineer to understand the requirements of the stakeholders, to pick the right design, to identify the risks, to test the real behaviour and to maintain the system. AI can generate code or generate explanations, but that output may be wrong or inappropriate. The engineer has to assess that output, verify that it works and then take ownership of the software that results.

| Preparation item | Own explanation and evidence link |
|---|---|
| Problem and stakeholders | SmartCare helps manage patient, practitioner and appointment information. Its main users are staff managing appointments. See `project/README.md`. |
| Two requirements and acceptance criteria | FR-05: Prevent two scheduled appointments for the same practitioner at the same time. FR-07: Keep cancelled appointments retrievable. See `project/tests/test_regressions.py`. |
| Domain model and architecture | `domain.py` defines entities and validation; `data_store.py` stores session records; `services.py` coordinates workflows; `queries.py` filters and sorts; `console.py` handles interaction. |
| Design trade-off | We use simple in-memory storage rather than a database because persistence is outside the current requirements. This simplifies the application but loses records on exit. |
| Meaningful test and its limits / 100 percent coverage | Conflict tests verify that an occupied practitioner timeslot is rejected. Even 100% code coverage would not prove that every requirement and input combination works. See `test_regressions.py`. |
| Diagnosed defect and verification | Stage 8 corrected an incorrect practitioner comparison in conflict detection. The related regression tests passed after correction. |
| Shared store and session-state/query responsibilities | The shared data store holds the current session's records. Services perform operations, while queries return filtered and ordered appointments without changing the source data. |
| What would break if session-state lookup/query responsibilities changed? | If queries modified stored records or filtered cancelled appointments incorrectly, appointment history and listing results could become unreliable. |
| Why cancellation is domain behaviour / conflict coordination is service behaviour | Cancellation changes an appointment's status according to its lifecycle rules. Conflict checking requires comparing a proposed booking with other stored appointments, so services coordinate it. |
| FR-07 retained history test | After cancellation, the appointment keeps its original ID and remains retrievable with CANCELLED status. See `test_regressions.py` and `test_workflows.py`. |
| Actual AI change rejected/modified or honestly accepted with verification | Stage 8 Copilot diagnoses were checked against the code and tests. Stage 12's missing `datetime` import was corrected and verified with all 61 tests passing. |
| Unresolved limitation / future production work | Session-only data, no production authentication, no billing integrations and no production-scale operational assurance. |
| Personal implementation contribution | Alex completed Stage 6 and Stage 8 work and the Stage 12 compatibility correction. See the corresponding stage evidence and PR #11. |
| Personal test/review/design/integration contribution | Alex ran the interactive demonstration, verified all 61 tests on Python 3.13, prepared release documentation and coordinated PR #11. |
| PG agentic change and rescheduling verification | Not applicable |
| PG responsible-AI risk/remediation or supported no finding | Not applicable |

Optional bounded-change practice only: validation rule, focused test, safe error-message change, explicit-input query or agreed status rule with test. Explain expected impact before editing, make a small change, run the test, and identify evidence to inspect if unsure. No live AI unless explicitly permitted. Preserve the submitted candidate.

Practice question/change and reasoning: Not undertaken.

Separate reflection / peer / common team viva evidence links and routing: The separate reflection report and peer review still needs to be completed through canvas.
No further coding stage. Later corrections use the published assessment process.
