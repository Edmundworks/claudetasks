---
description: Execute complete daily routine including email triage, planning, and standup notes
allowed-tools: Task, Bash(date:*), Bash(ls:*), Read, MultiEdit, mcp__mcp-gsuite__*, mcp__notion-mcp__*
---

# Daily Routine Command - MANDATORY EXECUTION PROTOCOL

**CRITICAL**: This is a MANDATORY step-by-step execution protocol. Each step MUST be completed and verified before proceeding to the next. DO NOT skip any steps. DO NOT proceed if a step fails.

Execute [YOUR_NAME]'s complete daily routine by running email triage, daily planning, and standup notes generation in sequence.

## ⚠️ EXECUTION RULES

1. **SEQUENTIAL EXECUTION**: Complete each step fully before moving to next
2. **MANDATORY VERIFICATION**: After each step, explicitly report completion status
3. **STOP ON FAILURE**: If any step fails, STOP and report the failure - do not continue
4. **NO SKIPPING**: Every step must execute - there are no optional steps
5. **CHECKPOINT CONFIRMATION**: Confirm each checkpoint before proceeding

## Current Context

- Today's date: !`date +"%Y-%m-%d"`
- Day of week: !`date +"%A"`
- Active files in root: !`ls -la *.md 2>/dev/null | grep -E "(email_summaries|newsletter_digest|daily_schedule|standup_notes)" || echo "No daily files found"`
- Archive status: !`ls -la archive/ 2>/dev/null | head -5 || echo "Archive directory not found"`

## MANDATORY EXECUTION CHECKLIST

Execute each step in order. Report completion after each step using the checkpoint format.

---

### ✅ CHECKPOINT 1: Environment Setup & State Check

**Actions:**
1. Get current date and time
2. Determine if workday (Monday-Friday)
3. Run: `source venv/bin/activate && python scripts/assistant_state.py summary`
4. Report which agents need processing and date ranges

**Verification:**
```
✅ CHECKPOINT 1 COMPLETE
- Date: [YYYY-MM-DD]
- Workday: [YES/NO]
- State status: [Summary of what needs processing]
```

**⛔ STOP GATE**: Do not proceed until this checkpoint is confirmed.

---

### ✅ CHECKPOINT 2: Current Sprint Detection

**Actions:**
1. Query Sprint Database: `19dc548c-c4ff-80db-a687-fade4b6cc149`
2. Filter by "Is Current" formula property
3. Extract current sprint ID (NEVER use cached IDs)
4. Store sprint ID for all subsequent task creation

**Verification:**
```
✅ CHECKPOINT 2 COMPLETE
- Sprint Name: [Week X]
- Sprint ID: [full-uuid]
- Date Range: [start] to [end]
- Sprint ready for task creation: YES
```

**⛔ STOP GATE**: Do not proceed without valid sprint ID.

---

### ✅ CHECKPOINT 3: Email Processing

**Actions:**
1. Launch `email-preprocessor` agent (Task tool)
2. Wait for completion and capture: date range, emails processed/archived/remaining
3. Launch `daily-email-triage` agent with sprint ID (Task tool)
4. Wait for completion and capture: tasks created, newsletter insights
5. Verify files created: `email_summaries_YYYY_MM_DD.md`, `newsletter_digest_YYYY_MM_DD.md`

**Verification:**
```
✅ CHECKPOINT 3 COMPLETE
- Date range processed: [start] to [end]
- Work emails: [X] processed, [Y] archived, [Z] remaining
- Notion tasks from emails: [X] tasks created
- Newsletter insights: [X] items extracted
- Files created: [list filenames]
```

**⛔ STOP GATE**: Do not proceed until both agents complete successfully.

---

### ✅ CHECKPOINT 4: Daily Tasks Creation ⚠️ CRITICAL - DO NOT SKIP

**Actions:**
1. Launch `daily-tasks-agent` with current sprint ID (Task tool)
2. Agent must process Current Daily Todos page: `26fc548c-c4ff-80c7-87bf-cac0369bec44`
3. Wait for agent to complete Two-Pass System
4. Agent must report verification status
5. Capture: direct tasks count, derived tasks count, verification status

**Verification:**
```
✅ CHECKPOINT 4 COMPLETE
- Direct tasks created: [X] tasks (from numbered list)
- Derived tasks created: [Y] tasks (from workflows)
- Verification status: ✅ COMPLETE / ❌ INCOMPLETE
- Total tasks in sprint: [TOTAL]
```

**⛔ CRITICAL STOP GATE**:
- If verification status is ❌ INCOMPLETE, STOP HERE
- Report missing tasks and DO NOT PROCEED
- If verification status is ✅ COMPLETE, proceed to next checkpoint

**THIS STEP CANNOT BE SKIPPED UNDER ANY CIRCUMSTANCES**

---

### ✅ CHECKPOINT 5: Daily Planning

**Actions:**
1. Launch `daily-planning` agent (Task tool)
2. Agent pulls calendar events from work calendar
3. Agent runs task analyzer
4. Agent integrates email insights
5. Verify file created: `daily_schedule_YYYY-MM-DD.md`

**Verification:**
```
✅ CHECKPOINT 5 COMPLETE
- Calendar events: [X] events from work calendar
- Time blocks: [Y] blocks allocated
- File created: daily_schedule_YYYY-MM-DD.md
```

**⛔ STOP GATE**: Do not proceed until daily schedule is generated.

---

### ✅ CHECKPOINT 6: Sprint Information Update (Conditional)

**Actions:**
- If Tuesday: Launch `sprint-planning-agent` (Task tool)
- If not Tuesday: Skip to Checkpoint 7
- Update CLAUDE.md if sprint info is outdated

**Verification:**
```
✅ CHECKPOINT 6 COMPLETE
- Day: [Day of week]
- Sprint planning: [RAN / SKIPPED - not Tuesday]
- CLAUDE.md: [UPDATED / NO UPDATE NEEDED]
```

---

### ✅ CHECKPOINT 7: Standup Notes (Workdays Only)

**Actions:**
- If Monday/Wednesday/Thursday/Friday: Launch `daily-standup-notes-agent` (Task tool)
- If Tuesday/Weekend: Skip (handled by sprint planning or not needed)
- Verify file created: `standup_notes_YYYY-MM-DD.md`

**Verification:**
```
✅ CHECKPOINT 7 COMPLETE
- Day: [Day of week]
- Standup generated: [YES / NO - not a standup day]
- File created: [filename or N/A]
```

---

### ✅ FINAL CHECKPOINT: Execution Summary

**Actions:**
1. Compile metrics from all checkpoints
2. Generate formatted execution summary using template
3. Report total execution time
4. List any warnings or issues

**Verification:**
```
✅ ALL CHECKPOINTS COMPLETE

[Full execution summary as per template]
```

## File Management

### Active Files (Root Directory - Today Only)
- `email_summaries_YYYY_MM_DD.md`
- `newsletter_digest_YYYY_MM_DD.md`
- `daily_schedule_YYYY-MM-DD.md`
- `standup_notes_YYYY-MM-DD.md`

### Archive Structure
```
/archive/
├── email_summaries/
├── newsletter_digests/
├── daily_schedules/
└── standup_notes/
```

## Execution Order - CHECKPOINT SYSTEM

The workflow is now enforced through mandatory checkpoints (see above). Each checkpoint must complete before proceeding to the next.

**Checkpoint Flow:**
1. ✅ Environment Setup & State Check
2. ✅ Current Sprint Detection (⛔ STOP GATE)
3. ✅ Email Processing (⛔ STOP GATE)
4. ✅ Daily Tasks Creation (⛔ CRITICAL STOP GATE - CANNOT BE SKIPPED)
5. ✅ Daily Planning (⛔ STOP GATE)
6. ✅ Sprint Information Update (Conditional)
7. ✅ Standup Notes (Conditional)
8. ✅ Final Execution Summary

## Time Considerations
- **Best Run Time**: 9:00am-10:00am ET
- **Standup Timing**: 11:00am-11:30am (Tuesdays: 11:00am-12:00pm for sprint planning)

## Error Handling - NEW STOP GATE PROTOCOL

**CRITICAL CHANGE**: Steps no longer continue on failure

- **If any checkpoint fails**: STOP execution immediately
- **Report failure**: State which checkpoint failed and why
- **Do not proceed**: Wait for manual intervention
- **Exception**: Conditional checkpoints (6, 7) can be skipped if not applicable
- **Checkpoint 4 is MANDATORY**: Daily tasks creation cannot be skipped under any circumstances

## Success Criteria - CHECKPOINT BASED

Success is measured by checkpoint completion:

- ✅ All 7 checkpoints completed successfully
- ✅ Each checkpoint verification reported
- ✅ All stop gates passed
- ✅ **Checkpoint 4 verification status: COMPLETE** (most critical)
- ✅ No checkpoints skipped
- ✅ Execution summary provided at end with all metrics
- ✅ All expected files created (emails, schedule, standup if applicable)

## Checkpoint 4 Verification Details

The daily-tasks-agent will provide its own verification report. You must capture this report and include it in Checkpoint 4 verification.

**Agent should report**:
- Direct tasks created from numbered list
- Derived tasks from workflow instructions
- Verification status (COMPLETE/INCOMPLETE)
- Any discrepancies or missing tasks

**Your responsibility**:
- Wait for agent completion
- Capture verification metrics
- Report in Checkpoint 4 format
- STOP if verification is INCOMPLETE

## Execution Summary Output

After completing the daily routine, provide a comprehensive summary in this format:

```
╔════════════════════════════════════════════════════════════════╗
║           DAILY ROUTINE EXECUTION SUMMARY                      ║
║           [DATE] - [DAY OF WEEK]                              ║
╚════════════════════════════════════════════════════════════════╝

📊 STATE TRACKING STATUS:
  • email_preprocessor: Last run [X] days ago
  • sales_pipeline_tracker: Last run [X] days ago
  • granola_meeting_summarizer: Last run [X] days ago

📧 EMAIL PROCESSING (Date range: YYYY-MM-DD to YYYY-MM-DD):
  • Work inbox: [X] emails processed, [Y] archived, [Z] remaining
  • Notion tasks created: [X] tasks from actionable emails
  • Newsletter insights: [X] items extracted
  • Files: email_summaries_YYYY_MM_DD.md, newsletter_digest_YYYY_MM_DD.md

📅 MEETINGS PROCESSED (Date range: YYYY-MM-DD to YYYY-MM-DD):
  • Meetings found: [X] meetings across [Y] days
  • Action items extracted: [X] items
  • Files: meetings_summary_YYYY-MM-DD_to_YYYY-MM-DD.md

💼 SALES PIPELINE (Date range: YYYY-MM-DD to YYYY-MM-DD):
  • Sales calls tracked: [X] calls
  • New opportunities: [X] added to CRM
  • Progression detected: [X] moved to onboarding
  • CRM updates: [X] rows modified

✅ DAILY TASKS CREATED:
  • Direct tasks from Daily Todos: [X] tasks
  • Workflow-derived tasks: [Y] tasks
  • Email-based tasks: [Z] tasks
  • Total tasks in today's sprint: [TOTAL] tasks
  • Verification: ✅ COMPLETE / ❌ INCOMPLETE

📆 DAILY SCHEDULE:
  • Calendar events: [X] events from work calendar
  • Time blocks allocated: [Y] blocks
  • Files: daily_schedule_YYYY-MM-DD.md

📝 STANDUP NOTES ([If applicable]):
  • Generated: [YES/NO]
  • Files: standup_notes_YYYY-MM-DD.md

🎯 CURRENT SPRINT:
  • Sprint: Week [X]
  • Sprint ID: [ID]
  • Date range: [START] to [END]
  • Theme: [THEME]

⚠️  WARNINGS/ISSUES:
  • [List any errors, conflicts, or items needing attention]
  • [Or "None" if all clean]

🎉 ROUTINE COMPLETED: [HH:MM:SS] elapsed

Next routine recommended: [TOMORROW'S DATE]
```

## How to Execute This Command

When you run `/daily-routine`, follow the **MANDATORY EXECUTION CHECKLIST** above.

### Execution Protocol

1. **Read each checkpoint** carefully
2. **Execute actions** listed for that checkpoint
3. **Wait for completion** before proceeding
4. **Report verification** using the exact format provided
5. **Check stop gate** - only proceed if verification is complete
6. **Move to next checkpoint** only after stop gate passes

### Example Checkpoint Execution

```
EXECUTING CHECKPOINT 4: Daily Tasks Creation

Actions:
1. Launching daily-tasks-agent with sprint ID: 277c548c-c4ff-81bd...
2. Agent processing Current Daily Todos page: 26fc548c-c4ff-80c7...
3. Waiting for agent completion...
4. Agent completed - capturing results

✅ CHECKPOINT 4 COMPLETE
- Direct tasks created: 8 tasks (from numbered list)
- Derived tasks created: 5 tasks (from workflows)
- Verification status: ✅ COMPLETE
- Total tasks in sprint: 13

⛔ STOP GATE PASSED - Proceeding to Checkpoint 5
```

### If a Checkpoint Fails

```
❌ CHECKPOINT 4 FAILED
- Direct tasks created: 5 tasks (expected 8)
- Derived tasks created: 3 tasks (expected 5)
- Verification status: ❌ INCOMPLETE
- Missing: 3 direct tasks, 2 derived tasks

⛔ CRITICAL STOP GATE FAILED
Reason: daily-tasks-agent did not create all required tasks
Action: STOPPING EXECUTION - Manual intervention required
```

**Key Enhancement**: Checkpoint system ensures NO STEPS CAN BE SKIPPED and failures are caught immediately.

## Execution Instructions

### Track Metrics Throughout Execution

As you execute each phase, **track and accumulate** the following metrics:

1. **Start Time**: Record when routine begins
2. **State Status**: Run `python scripts/assistant_state.py summary` at start
3. **Each Agent Output**: Capture key metrics from each agent's final report:
   - Email preprocessor: date range, emails processed/archived/remaining, tasks created
   - Email triage: newsletter insights count
   - Meetings: date range, meetings found, action items extracted
   - Sales pipeline: calls tracked, CRM updates
   - Daily tasks: direct tasks, derived tasks, verification status
   - Daily planning: calendar events, time blocks
   - Standup: generated yes/no
4. **Sprint Info**: Current sprint details
5. **Warnings**: Any errors, conflicts, or attention items
6. **End Time**: Record when routine completes

### Final Summary Generation

After ALL phases complete, generate the execution summary using the template above with actual values. This summary is the **final output** shown to the user and should be the last thing printed to the command line.

### Summary Storage

Optionally save the summary to: `execution_summary_YYYY-MM-DD.md` for reference.