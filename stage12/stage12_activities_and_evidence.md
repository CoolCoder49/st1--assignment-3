# Stage 12 activities and evidence

BLANK student response template. Supplied from the beginning in stage12/ in your EXISTING repository; complete it only when you reach Stage 12 after the previous applicable stage is integrated, verified and recorded; preserve project/, tests, earlier records and Git history. UG/common and PG/extended scope must be explicit. Use concise results and versioned links, not copied logs or source. No staff answers or fabricated approvals.

Group/tutorial: Tuesday 1:30-3:30, Group 2
Members and UG/PG applicability: Alex Marek (UG) and Kreesha Singh (UG).


## A Release scope and starting SHA

Release label/version and requirements baseline:

SmartCare Stage 12 Undergraduate Final Release, using SmartCare A3 Requirements Baseline 2026, revision 2. The release covers the completed functionality from Stages 6-9, including patient and practitioner registration and lookup, appointment booking, conflict prevention, cancellation, retained appointment history, practitioner appointment listing, filtering, sorting and the interactive console. The application uses session-only in-memory storage. The final release SHA will be confirmed after all Stage 12 verification and integration activities are complete.

Common starting SHA / branch / applicable members:

The common starting commit is `89d106fecbd1671a184728f233c3e669ea0a7957` on `main`. This commit includes the completed Stage 9 implementation and its final evidence record. The Stage 12 work is being completed on the separate `release/stage12-common` branch, created from the same commit. Both Alex and Kreesha are included in the undergraduate common release.

PG starting SHA / branch / applicable members or not applicable:

Not applicable. Both group members are undergraduate students, so no PG extension branch or separate PG release candidate is required. Stages 10 and 11 are not part of our assessed project.

Working-state review and approved integration:

Before beginning Stage 12, I checked the local repository and its GitHub connection using Git commands. The working tree was clean, and the local `main` branch matched `origin/main`, with zero commits ahead and zero commits behind.

Stage 9 was merged into `main` through Pull Request #10 at commit `1b2c48f`, followed by the Stage 9 evidence update at `89d106f`. However, the Stage 9 pull request was merged without my recorded independent review. I did not complete this review before merging, and I will not report it as an earlier approval. I will check the integrated code independently during Stage 12.

I then ran the complete automated test suite from the `project/` directory using `python -m pytest -q`. The result was **61 passed in 0.08 seconds**, using Python 3.14.6 and pytest 9.2.0. This confirms that the current integrated application passes all 61 available tests in my local environment. The final release will still require further verification, including the interactive console, documentation, code quality and reproducibility checks.

Protected common candidate and PG differences:

The starting common candidate is commit `89d106fecbd1671a184728f233c3e669ea0a7957`. This version has been retained on `main`, while Stage 12 work is being carried out on `release/stage12-common` to avoid changing the existing integrated application unnecessarily.

There is no PG extension or alternative PG candidate because both group members are undergraduate students. The final common release SHA will be recorded after all required Stage 12 checks and any necessary reviewed corrections are complete.

Feature freeze / owner / verifier:

Optional feature development has been stopped for Stage 12. The remaining work will focus on checking the existing application, verifying requirements, completing release documentation, reviewing code quality, and correcting any genuine release blockers identified. No new database, persistence system, rescheduling feature or unnecessary dependency will be introduced.

Alex is responsible for preparing the Stage 12 release evidence and coordinating final verification. Kreesha is the proposed independent verifier, subject to confirmation and completion of an actual review. Final approval and release readiness have not yet been established and will be recorded after the required checks are complete.


## B Requirements and release readiness matrix

Tutorial activity 1: All tests pass, README setup is incomplete, one dependency is unreviewed and a known limitation is undocumented. Decide Release / Release with conditions / Do not release and justify:

Do not release yet.

Although all automated tests pass, the application is not fully ready for release. In the example, the README setup instructions are incomplete, a dependency hasn't been reviewed, and a known limitation hasn't been documented. These issues could prevent another developer from running the application correctly or understanding its limitations.

Before approving the release, the team should complete the README with accurate setup and testing instructions, review the dependency to confirm that it is required and appropriate, and document the known limitation. Another group member should then verify that the application can be set up and run using the supplied instructions.

Passing tests show that the tested functionality works, but release readiness also requires complete documentation, reviewed dependencies, reproducibility, and an informed decision about remaining risks. Do not release the application until these issues have been addressed and verified.

Tutorial activity 2 and actual readiness matrix. Add exact requirement/acceptance IDs, evidence and reviewer; distinguish common/PG applicability.

| Release claim / requirement / scope | Evidence | Location/link and SHA | Reviewer | Sufficient? | Gap/action |
|---|---|---|---|---|---|
| Cancellation history works | Service, regression and workflow tests check that cancellation changes the status to CANCELLED, retains the original appointment and rejects repeated cancellation. | `project/tests/test_services.py`, `test_regressions.py`, `test_workflows.py`; starting SHA `89d106f` | Kreesha | No | Confirm the same behaviour through the final interactive console demonstration. |
| Architecture responsibilities are appropriate | Domain classes handle validation and appointment state. The data store manages session records, services coordinate operations, pure queries filter and sort appointments, and the console handles user interaction. | `project/smartcare/domain.py`, `data_store.py`, `services.py`, `queries.py`, `console.py`; `89d106f` | Alex | No | Complete the Stage 12 code quality and architecture review. |
| Rescheduling is safe — PG only | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| AI use is responsible — common recheck / PG assurance | Stage 8 records include human-first debugging hypotheses, actual GitHub Copilot prompts, evaluated suggestions and verification against the code and tests. Stage 9 records its query and integration review decisions. | `stage08/stage08_activities_and_evidence.md`, `stage08/copilot_f8_01_diagnosis.md`, `stage08/copilot_f8_02_diagnosis.md`, `stage09/stage09_activities_and_evidence.md` | Alex | Yes | None |
| System is maintainable | The application separates responsibilities across modules, uses named functions and domain classes, and includes accumulated automated tests. Stage 8 also records a small refactoring from a hardcoded appointment status string to the existing enum. | `project/smartcare/`, `project/tests/`, Stage 8 evidence; `89d106f` | Alex | No | Check naming, type hints, docstrings, duplication, unnecessary complexity, and code readability during the final quality review. |
| FR-01–03 register/find and validation |  Domain and service tests check valid patient and practitioner registration, retrieval, duplicate IDs, blank values, and unknown identifiers. | `project/tests/test_domain.py`, `test_services.py`, `test_starter.py`; `89d106f` | Alex | Yes | Demonstrate registration, lookup and error recovery through the final console. |
| FR-04–05 booking/conflict rules | Service, regression and workflow tests check valid booking, registered participants, rejection of same-practitioner exact-time conflicts, different-practitioner bookings and unchanged records after rejection. | `project/tests/test_services.py`, `test_regressions.py`, `test_workflows.py`; `89d106f` | Alex | Yes | Repeat the important booking and conflict scenarios during the final demonstration. |
| FR-06–08 cancellation/history/find | Tests confirm that a scheduled appointment can be cancelled, remains retrievable using its original ID and cannot be cancelled a second time. Appointment lookup is also tested. | `project/tests/test_services.py`, `test_regressions.py`, `test_workflows.py`; `89d106f` | Alex | Yes | Demonstrate cancellation, retained history, repeated cancellation rejection, and appointment lookup in one session. |
| FR-09 and QRY/FP listing/filter/order/purity | Query tests check practitioner filtering, status filtering, chronological ordering, equal-time appointment ID ordering, fresh result lists and source non-mutation. Workflow tests check service listing and error handling. | `project/smartcare/queries.py`, `project/tests/test_queries.py`, `test_workflows.py`; `89d106f` | Alex | No | Review query purity and demonstrate the listing and filtering behaviour. |
| UI full console sequence and error recovery | Stage 9 documentation records a successful main menu workflow, including registration, booking, conflict rejection, cancellation, listing and freed-slot booking. However, it states that the complete invalid-input recovery sequence was not manually demonstrated. | `project/smartcare/console.py`, `project/main.py`, `stage09/stage09_activities_and_evidence.md`; `89d106f` | Alex | No | Confirm that rejected operations preserve existing data and the menu remains usable. |
| Session-only scope / FR-10 retired | SmartCare uses one in-memory data store. Patient, practitioner and appointment records remain available during the session but are lost when the program exits. Restart persistence is not required. | `project/smartcare/data_store.py`, `project/README.md`, Assignment 3 revision 2 requirements; `89d106f` | Alex | Yes | Make sure the final README and release notes explain the session-only limitation clearly. |
| PG RES and assurance integration | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |


## C Full regression results

| Suite/scope | Environment/version | Working directory and command | Tested SHA | Actual result | Evidence link |
|---|---|---|---|---|---|
| Complete common | Python 3.14.6, pytest 9.2.0, PyCharm | `project/` - `python -m pytest -q` | `89d106fecbd1671a184728f233c3e669ea0a7957` | 61 passed in 0.08s | Local PyCharm terminal output; `project/tests/` |
| Complete PG if applicable | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Affected focused checks after correction | Python 3.14.6, pytest 9.2.0 | `project/` - `python -m pytest -q` | Stage 12 branch, uncommitted correction | 61 passed in 0.07s after adding the missing `datetime` import. | PyCharm terminal output; `git diff -- smartcare/services.py` |
| Full integrated recheck | Python 3.13.17, pytest 8.3.5 | `project/` - `python -m pytest -q` using the separate Python 3.13 environment | Stage 12 branch, uncommitted correction | 61 passed in 0.11s. | PyCharm terminal output; `project/tests/` |

Prior assertions preserved / reviewed test diff:

All six existing test files were preserved. No test assertions were changed or removed during Stage 12. The only Python correction was adding `from datetime import datetime` to `services.py`. All 61 tests passed on both Python versions after the correction.

Remaining failure / limitation:

No automated test failures remain. The interactive demonstration and invalid-input recovery checks passed. Session-only storage is an intentional limitation. Final testing against the committed release SHA and independent review are still pending.


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
| OOP responsibilities and pure-query boundaries | `project/smartcare/` | Domain, data store, services, queries and console have separate responsibilities. Queries do not modify source records. | No change required from initial inspection. Independent review pending. |
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
| Missing `datetime` import could affect compatibility. | `services.py` | Alex applied the import and ran the full test suite. | Accept: the annotation requires the import for Python 3.13. | Added import; 61 tests passed on Python 3.14.6. Python 3.13 verification pending. |

Access route or approved equivalent / limitations: GitHub Copilot was used through PyCharm during Stage 8. Saved evidence is available in `stage08/copilot_f8_01_diagnosis.md` and `stage08/copilot_f8_02_diagnosis.md`. Stage 9 AI review details are recorded in its evidence file, but the independent PR review was not completed.

Available AI evidence and missing evidence honestly disclosed: Stage 8 includes recorded prompts, diagnoses, human decisions and test results. ChatGPT assisted with documentation and identifying the missing import; Alex applied the correction and verified the tests. Stage 9 independent review and final Stage 12 release approval remain outstanding.


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

Root README index and project/README verified: [response]

Both README files were updated to describe the completed SmartCare application, current commands, group information, requirements baseline and limitations. Final independent review is pending.

Fresh clone or extracted ZIP / candidate identity:

Pending. The current Stage 12 branch is `release/stage12-common`, based on commit `89d106fecbd1671a184728f233c3e669ea0a7957`, with uncommitted release changes. A fresh copy of the final release candidate will be verified after integration.

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

No setup or test failures were identified in the current checkout. Fresh-copy reproducibility testing, independent review and final SHA verification remain pending.



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
| Python 3.13 compatibility and code quality | During code review, `services.py` was found to use `datetime` in a type hint without importing it. A failure on Python 3.13 before the fix was not directly tested. | Compatibility risk | Alex added the missing import. | Added `from datetime import datetime` to `project/smartcare/services.py`. | Full suite: 61 passed in 0.07s using Python 3.14.6; 61 passed in 0.11s using Python 3.13.17 and pytest 8.3.5. | No test failures observed after the correction. Final independent review remains pending. |

Justified no-change conclusion if no defect found:

One code issue was identified and corrected. No other defects requiring code changes were found during the completed checks. Existing test files and assertions were preserved.

Release blockers still open / status:

Kreesha's independent review, final Git integration, testing against the final release commit, and fresh-copy/ZIP verification are still pending. No automated test failures are currently known.


## I Git review and integration evidence

Issue / PR / diff links and reviewed SHA: [response]
Independent reviewer / feedback / response: [response]
Integration commit / full recheck: [response]
Tracked and untracked file inspection / cleanliness: [response]
Secrets/staff material/caches/tool-metadata exclusion check: [response]
Candidate recovery plan / known-good SHA: [response]
Named substantive contributions: [response]


## J Human release decision

Decision — READY FOR COURSE RELEASE / READY WITH DOCUMENTED LIMITATIONS / NOT YET READY: [response]
Approver / date / rationale and evidence: [response]
What risks remain / conditions / owners: [response]
Can the team explain the system: [response]
Can a change be recovered: [response]
Common decision / PG decision where different: [response]


## K Final tested release SHA

Exact common tested SHA: [response]
Exact PG tested SHA or not applicable: [response]
Final submitted SHA / repository URL: [response]
Evidence-only later commit and difference explanation: [response]
Executable changes after testing and re-verification: [response]
Source ZIP name / SHA correspondence / extracted comparison: [response]


## L Submission package verification

- [ ] Feature freeze and scoped requirements traced.
- [ ] Applicable full regressions, integrated demo and invalid paths verified.
- [ ] Architecture/code quality and final AI/dependency checks complete.
- [ ] Root README and project/README reproduced by another verifier.
- [ ] Release notes, technical debt and limitations visible.
- [ ] Independent human review, integration and release decision recorded.
- [ ] Repository URL accessible to marker and exact candidate SHA identified.
- [ ] One source ZIP from submitted commit with root README.md and .gitignore.
- [ ] project/ source and all accumulated applicable tests included.
- [ ] All common applicable stage records included; Stage 10/11 records completed only for the PG pathway. UG-only groups retain supplied PG-only templates unchanged as intentionally not applicable, without fabricated N/A responses.
- [ ] No .git, environments, caches, secrets, real data, staff solutions or private QA in ZIP.
- [ ] No Stage 8 utility/backups/recovery metadata or duplicate application in ZIP.
- [ ] Mixed-group common protection and candidate upload routing checked.
- [ ] Group reflection, confidential individual peer forms and common team viva routed separately.

Confirmed assessment item/upload route: [response]
Deadline/timezone: [response]
Repository access arrangement: [response]
Mixed-candidate upload arrangement: [response]
Oral/video recording/accessibility arrangements: [response]
Remaining administration or release dependency: [response]


## M Formative questions

1. What is a release candidate? [response]

2. What is feature freeze and why is it used? [response]

3. What is regression testing in a release context? [response]

4. What is a known limitation? [response]

5. What is technical debt? [response]

6. What are release notes? [response]

7. What is software maintenance? [response]

8. What is the purpose of the individual demonstration/viva? [response]

9. What should the final responsible-AI check establish before release? [response]

10. What is the main course conclusion about AI and the role of the software engineer? [response]


## N Reflection viva and handover

Strongest evidence SmartCare is ready: [response]
Weakest area: [response]
How AI use changed from Stage 1 to Stage 12: [response]
Start doing — engineering and AI use: [response]
Stop doing — engineering and AI use: [response]
Continue doing — engineering and AI use: [response]
What worked / caused rework / future delivery improvement: [response]
One paragraph — If AI can write code why do we still need software engineers: [response]

| Preparation item | Own explanation and evidence link |
|---|---|
| Problem and stakeholders | [response] |
| Two requirements and acceptance criteria | [response] |
| Domain model and architecture | [response] |
| Design trade-off | [response] |
| Meaningful test and its limits / 100 percent coverage | [response] |
| Diagnosed defect and verification | [response] |
| Shared store and session-state/query responsibilities | [response] |
| What would break if session-state lookup/query responsibilities changed? | [response] |
| Why cancellation is domain behaviour / conflict coordination is service behaviour | [response] |
| FR-07 retained history test | [response] |
| Actual AI change rejected/modified or honestly accepted with verification | [response] |
| Unresolved limitation / future production work | [response] |
| Personal implementation contribution | [response] |
| Personal test/review/design/integration contribution | [response] |
| PG agentic change and rescheduling verification | [response] |
| PG responsible-AI risk/remediation or supported no finding | [response] |

Optional bounded-change practice only: validation rule, focused test, safe error-message change, explicit-input query or agreed status rule with test. Explain expected impact before editing, make a small change, run the test, and identify evidence to inspect if unsure. No live AI unless explicitly permitted. Preserve the submitted candidate.

Practice question/change and reasoning: [response or not undertaken]
Separate reflection / peer / common team viva evidence links and routing: [response]
No further coding stage. Later corrections use the published assessment process.
