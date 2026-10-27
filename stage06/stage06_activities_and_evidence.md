# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: Tue 1:30 - 3:30 Group 2
- Members, GitHub usernames and cohorts: Alex Marek (UG), Kreesha Singh (UG), CoolCoder49, 
- Repository URL: https://github.com/CoolCoder49/st1--assignment-3
- Starting SHA: 54c50924b75cebfff7e9b762cf225f9a69be1936

## A Requirement to issue activities

### FR-02 Patient Search

- Title: FR-02: Find a registered patient using their patient ID
- Context: The program already has a Patient class, a patient collection, and a working registration function. However, the starter code does not complete the PatientService.find_patient() function. The search must use the existing stored patient rather than creating a new object with the same information.
- Requirement: Implement PatientService.find_patient(patient_id) to return the actual registered Patient object. A patient ID that does not exist must raise LookupError, while an empty, whitespace-only, or non-string ID must raise ValueError. IDs remain case-sensitive, and the existing validation removes surrounding spaces.
- Acceptance criteria: AC-02.1: Searching for a registered patient returns the same object held in the data store, including when the ID has spaces around it. AC-02.2: Searching for an unknown ID raises LookupError without creating a new patient.
- Scope: Only implement PatientService.find_patient() and add its related tests.
- Definition of Done: The function meets the acceptance criteria, the original and new tests pass, and the Git diff contains no unrelated changes. The issue must be linked to a PR, reviewed by the other team member, and approved after implementing any feedback. Check the final merged version again.
- Owner: Kreesha
- Actual issue link: https://github.com/CoolCoder49/st1--assignment-3/issues/1#issue-6034797916

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: FR-06/FR-07: Cancel an appointment without deleting its history
- Context: The Appointment class already has a cancel() method that checks whether an appointment is SCHEDULED before allowing its status to become CANCELLED. The service should use this method rather than repeating the status checks. The cancelled appointment must remain in the data store so it can still be found later in the same session.
- Requirement: Implement AppointmentService.cancel_appointment(appointment_id) to find the registered appointment, call its cancel() method and return the same object. Unknown appointment IDs raise LookupError, while invalid IDs and illegal status changes raise ValueError. A rejected cancellation must not change the stored appointment.
- Acceptance criteria: AC-05.1: A SCHEDULED appointment changes to CANCELLED. AC-05.2: The same appointment remains stored and can still be found using its ID, with its patient, practitioner and date/time unchanged. AC-05.3: Trying to cancel the same appointment again raises ValueError and leaves it CANCELLED. A COMPLETED appointment also cannot be cancelled. The original booking time becomes available again because only SCHEDULED appointments cause a conflict, but the cancelled record is not deleted.
- Scope: Only implement AppointmentService.cancel_appointment() and its related tests.
- Definition of Done: Successful and rejected cancellations have been tested, with specific assertions proving that the object and its history are retained. The change must have its own issue and a focused PR, be reviewed by another member, have feedback resolved, and pass tests after merging.
- Owner: Kreesha
- Actual issue link: https://github.com/CoolCoder49/st1--assignment-3/issues/2#issue-6034871146

## B Commit quality

| Original example | Strong or Weak | Reason |
|---|---|---|
| changes | Weak | It doesn't explain what was changed or which requirement the commit relates to, making it difficult for someone else to review. |
| final version | Weak | This only tells us the work is supposedly finished and does not explain what was actually implemented. |
| Add patient search by ID | Strong | It clearly identifies the function being added and the behaviour expected from the change. |
| fix stuff | Weak | It doesn't identify the problem that was fixed, so another group member would need to open the code just to understand the purpose of the commit. |
| Prevent cancellation of completed appointments | Strong | It explains a specific rule that can be tested. |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: I would not approve this PR in its current form because it includes changes that have nothing to do with appointment cancellation. Renaming patient fields and restructuring other functions makes the change unnecessarily large and introduces the risk of breaking code that already works. The new dependency is also outside the requirements of this small application.
- Responsibility and architecture concerns: The Appointment class is responsible for protecting its own status transitions, while the service is responsible for finding the appointment and calling the appropriate operation. Moving these rules around or putting unrelated functionality in the same PR could create excessive coupling and lower cohesion. 
- Testing and review concerns:  Even if the tests pass, it doesn't mean the unrelated changes are correct or that all cancellation cases have been tested. I would check the actual Git diff, then verify that a scheduled appointment can be cancelled, the record remains stored, repeated cancellation raises ValueError, and completed appointments cannot be cancelled. I would also confirm that unsuccessful operations leave the original data unchanged.
- Changes to remove or separate, with reasons:  I would ask the author to remove the unrelated patient-field changes, unnecessary restructuring and new dependency from this PR. If any of those changes are actually required, they should have their own issue and PR. The cancellation PR should only contain cancel_appointment() and its tests so the reviewer can clearly check the requirement against the implementation.

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: This is not enough information to approve the PR because it doesn't explain which requirements were checked, what the tests actually covered, or whether the code introduced any unnecessary changes. Copilot also hasn't shown the test command, output or commit being reviewed. A passing test result on its own does not prove that the correct rules were implemented.
- Follow-up review question 1: Did the service use the existing Appointment.cancel() method, or did it duplicate the status rules inside services.py?
- Follow-up review question 2: Which tests prove that cancelling an appointment changes its status to CANCELLED without deleting the original object or changing its patient, practitioner and time?
- Follow-up review question 3: Were repeated cancellations, completed appointments, unknown IDs and invalid IDs tested, and do the rejected operations leave the original records unchanged?
- Follow-up review question 4: What test command was run, which Python and pytest versions were used, and which exact code commit was tested?
- Follow-up review question 5: Does the actual Git diff include unrelated changes, new dependencies, persistence or functions that belong in later stages?
- Additional questions if useful: [response]

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | We will use feature/stage06-<short-description> for focused issue branches, for example feature/stage06-patient-lookup, feature/stage06-practitioner-lookup and feature/stage06-cancellation. Every branch starts from an updated main branch.  |
| Commit message convention | Commit messages will briefly explain the actual change using a clear action, such as Implement patient lookup by ID. We will avoid vague descriptions such as changes or final version. |
| PR size | Each PR should only contain one focused issue and its relevant tests. Unrelated refactoring or new features should be separated so that each change can be reviewed properly. |
| Another-member review requirement | The member who did not implement the feature will check its code, requirements and tests. They must record their own observations before using GitHub Copilot. The author cannot approve their own PR. |
| Merge rule | We will only merge when the issue is linked, the relevant tests pass, all review comments are resolved, and the other member has approved the actual diff. Afterwards, both members will update main and check the integrated code again. |
| Significant Copilot disclosure rule | We will follow the required human-first order, then use GitHub Copilot chat with the Part H review prompt, the actual issue and diff. For significant output we will record the prompt, recommendation, human check, Accept/Modify/Reject decision and evidence. Copilot cannot replace human approval or claim an unobserved test. |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|---|---|---|---|---|
| https://github.com/CoolCoder49/st1--assignment-3/issues/1#issue-6034797916 | FR-02 | Kreesha | AC-02.1/AC-02.2: known ID returns the same stored Patient, unknown ID raises LookupError. Public contract: blank/non-string ID raises ValueError; trimmed and case-sensitive IDs; no mutation. | Open |
| https://github.com/CoolCoder49/st1--assignment-3/issues/3#issue-6035515993 | FR-03 | Kreesha | find_practitioner() returns the original stored Practitioner; trimmed and case-sensitive IDs; blank/non-string IDs raise ValueError; valid unknown IDs raise LookupError; no new object or mutation. | Open |
| https://github.com/CoolCoder49/st1--assignment-3/issues/2#issue-6034871146 | FR-06 and FR-07 | Kreesha | AC-05.1/05.2/05.3: SCHEDULED → CANCELLED; same object remains retrievable; repeated cancellation rejected. Public contract: COMPLETED cancellation and invalid/unknown IDs rejected without mutation. | Open |

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

- PR link and title: [response]
- Linked issue and requirement: [response]
- Feature branch: [response]
- Changed behaviour: [response]
- Meaningful commits: [links]
- Test command, directory and observed result: [response]
- Another-member reviewer: [response]
- Human observations recorded before Copilot: [link and time]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [response]
- Key feedback: [response]
- Author response/change and verification: [response]
- Reviewer recheck and approval: [link]
- Merge outcome and SHA: [response]
- Significant Copilot assistance: [summary or none]
- Linked issue closure: [response]
- Each member updated main: [member and confirmation]
- Integrated verification after merge: [command, directory, result and code SHA]

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: [response]
- Prompt/purpose and relevant issue/diff: [response]
- Summary of output: [response]
- Human check against actual code, requirements and tests: [response]
- Decision — Accept / Modify / Reject: [select]
- Reason: [response]
- Verification/evidence: [link and result]

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: [response]
- Copilot noticed: [response]
- Overlap: [response]
- What did the human reviewer notice that Copilot did not: [response]
- What did Copilot identify that the human reviewer initially missed: [response]
- Unsupported or incorrect Copilot suggestion: [response or none identified with explanation]
- Human judgement accepted, modified or rejected, and why: [response]
- Which evidence justified merge approval: [response]

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: [response]
- Implementation: [work and evidence]
- Testing: [work and evidence]
- Review: [work and evidence]
- Issue refinement: [work and evidence]
- Design and responsibility discussion: [work and evidence]
- Debugging or integration: [work and evidence]
- Documentation or team support: [work and evidence]

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

[response]

## L Stage 6 formative questions

1. What is version control?

[response]

2. Why is a feature branch useful?

[response]

3. What makes a commit a good engineering commit?

[response]

4. What is a pull request?

[response]

5. What is the purpose of code review?

[response]

6. What does a Git diff show?

[response]

7. What is a Definition of Done?

[response]

8. What is the appropriate role of GitHub Copilot in pull-request review?

[response]

9. Why should individual contribution not be judged only by commit count?

[response]

10. What is the Stage 6 engineering rule?

[response]

## M Completion and handover

- Starting SHA: 54c50924b75cebfff7e9b762cf225f9a69be1936
- Final Stage 6 code SHA: [response]
- Test command: [response]
- Working directory: [response]
- Observed result: [response]
- PR and another-member reviewer: [links]
- Unresolved issue or none: [response]
- Stage 7 handover status: [ready for tutor checkpoint / unresolved work]
- Final submitted SHA if later than tested SHA: [response and evidence-only difference]

- [ ] Three Stage 6 service targets completed and checked.
- [ ] Original supplied tests retained and passing.
- [ ] At least two focused issues link requirements and acceptance criteria.
- [ ] Feature work reviewed by another member using the actual diff.
- [ ] Human-first review and required Copilot comparison recorded.
- [ ] Feedback resolved and approval recorded before merge.
- [ ] Everyone pulled main and integrated checks passed.
- [ ] Required activities, quiz responses and contribution notes completed.
- [ ] Only synthetic data included; confidential peer material kept out.
- [ ] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.
