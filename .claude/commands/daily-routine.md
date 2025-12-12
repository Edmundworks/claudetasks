---
description: Execute complete daily routine including Granola notes processing, CRM updates, email triage, planning, and standup notes.
allowed-tools: Task, Bash(date:*), Bash(ls:*), Read, Edit, mcp__mcp-gsuite__*, mcp__notion-mcp__*, mcp__granola__*
---

# Daily Routine Command - MANDATORY EXECUTION PROTOCOL

**CRITICAL**: This is a MANDATORY step-by-step execution protocol. Each step MUST be completed and verified before proceeding to the next. DO NOT skip any steps. DO NOT proceed if a step fails.

Execute Edmund's complete daily routine by running Granola notes processing, CRM updates, email triage, daily planning, and standup notes generation in sequence.

## Execution Rules

1. **SEQUENTIAL EXECUTION**: Complete each step fully before moving to next
2. **MANDATORY VERIFICATION**: After each step, explicitly report completion status
3. **STOP ON FAILURE**: If any step fails, STOP and report the failure - do not continue
4. **NO SKIPPING**: Every step must execute - there are no optional steps
5. **CHECKPOINT CONFIRMATION**: Confirm each checkpoint before proceeding

## Current Context

- Today's date: !`date +"%Y-%m-%d"`
- Day of week: !`date +"%A"`
- Active files in root: !`ls -la *.md 2>/dev/null | grep -E "(email_summaries|newsletter_digest|daily_schedule|standup_notes)" || echo "No daily files found"`

## MANDATORY EXECUTION CHECKLIST

Execute each step in order. Report completion after each step using the checkpoint format.

---

### CHECKPOINT 1: Environment Setup

**Actions:**
1. Get current date and time
2. Determine if workday (Monday-Friday)
3. Check `last_summarized.md` in `.claude/skills/fetch-granola-notes/` for Granola timestamps

**Verification:**
```
CHECKPOINT 1 COMPLETE
- Date: [YYYY-MM-DD]
- Workday: [YES/NO]
- Granola last summarized: Sales=[date], Onboarding=[date]
```

**STOP GATE**: Do not proceed until this checkpoint is confirmed.

---

### CHECKPOINT 2: Current Sprint Detection

**Actions:**
1. Query Sprint Database: `19dc548c-c4ff-80db-a687-fade4b6cc149`
2. Filter by "Is Current" formula property
3. Extract current sprint ID (NEVER use cached IDs)
4. Store sprint ID for all subsequent task creation

**Verification:**
```
CHECKPOINT 2 COMPLETE
- Sprint Name: [Week X]
- Sprint ID: [full-uuid]
- Date Range: [start] to [end]
- Sprint ready for task creation: YES
```

**STOP GATE**: Do not proceed without valid sprint ID.

---

### CHECKPOINT 3: Fetch & Summarize Granola Notes

**Actions:**
1. Follow the `fetch-granola-notes` skill workflow (see `.claude/skills/fetch-granola-notes/SKILL.md`)
2. Use `granola-note-reader` agent for each meeting to summarize
3. Update `last_summarized.md` after all sub-agents complete

**Verification:**
```
CHECKPOINT 3 COMPLETE
- Sales calls fetched: [X] new since [last_summarized_date]
- Onboarding calls fetched: [Y] new since [last_summarized_date]
- Summaries created: [Z] files in meeting_summaries/
- Timestamp file updated: last_summarized.md
```

**STOP GATE**: Do not proceed until all meeting summaries are created.

---

### CHECKPOINT 4: CRM Update from Meeting Summaries

**Actions:**
1. Follow the `crm-update` skill workflow (see `.claude/skills/crm-update/SKILL.md`)

**Verification:**
```
CHECKPOINT 4 COMPLETE
- Meeting summaries processed: [X] files
- New CRM entries created: [Y] companies
- Status updates: [Z] (e.g., Sales Call -> Onboarding)
- Contextual notes added: [N] pages updated
```

**STOP GATE**: Do not proceed until CRM updates are complete.

---

### CHECKPOINT 5: Email Processing

**Actions:**
1. Launch `email-preprocessor` agent (Task tool) with instruction: "Process today's emails"
2. Launch `daily-email-triage` agent with sprint ID
3. Verify files created: `email_summaries_YYYY_MM_DD.md`, `newsletter_digest_YYYY_MM_DD.md`

**Verification:**
```
CHECKPOINT 5 COMPLETE
- Work emails: [X] processed, [Y] archived, [Z] remaining
- Notion tasks from emails: [X] tasks created
- Newsletter insights: [X] items extracted
- Files created: [list filenames]
```

**STOP GATE**: Do not proceed until both agents complete successfully.

---

### CHECKPOINT 6: Daily Planning

**Actions:**
1. Launch `daily-planning` agent (Task tool)
2. Agent pulls calendar events from work calendar
3. Agent integrates email insights
4. Verify file created: `daily_schedule_YYYY-MM-DD.md`

**Verification:**
```
CHECKPOINT 6 COMPLETE
- Calendar events: [X] events from work calendar
- Time blocks: [Y] blocks allocated
- File created: daily_schedule_YYYY-MM-DD.md
```

**STOP GATE**: Do not proceed until daily schedule is generated.

---

### FINAL CHECKPOINT: Execution Summary

**Actions:**
1. Compile metrics from all checkpoints
2. Generate formatted execution summary using template
3. Report total execution time
4. List any warnings or issues

**Verification:**
```
ALL CHECKPOINTS COMPLETE

[Full execution summary as per template]
```

## File Management

### Active Files (Root Directory - Today Only)
- `email_summaries_YYYY_MM_DD.md`
- `newsletter_digest_YYYY_MM_DD.md`
- `daily_schedule_YYYY-MM-DD.md`

### Meeting Summaries Structure
```
/meeting_summaries/
├── sales_call_1/
│   └── {YYYY-MM-DD}/
│       └── {company-name}.md
├── onboarding_call_2/
└── ...
```

### Archive Structure
```
/archive/
├── email_summaries/
├── newsletter_digests/
└── daily_schedules/
```

## Execution Order - CHECKPOINT SYSTEM

**Checkpoint Flow:**
1. Environment Setup
2. Current Sprint Detection (STOP GATE)
3. Fetch & Summarize Granola Notes (STOP GATE)
4. CRM Update from Meeting Summaries (STOP GATE)
5. Email Processing (STOP GATE)
6. Daily Planning (STOP GATE)
7. Final Execution Summary

## Time Considerations
- **Best Run Time**: 9:00am-10:00am ET

## Error Handling

**CRITICAL**: Steps do not continue on failure

- **If any checkpoint fails**: STOP execution immediately
- **Report failure**: State which checkpoint failed and why
- **Do not proceed**: Wait for manual intervention

## Success Criteria

Success is measured by checkpoint completion:

- All checkpoints completed successfully (1-6)
- Each checkpoint verification reported
- All stop gates passed
- Execution summary provided at end with all metrics
- All expected files created

## Execution Summary Output

After completing the daily routine, provide a comprehensive summary:

```
══════════════════════════════════════════════════════════════════
           DAILY ROUTINE EXECUTION SUMMARY
           [DATE] - [DAY OF WEEK]
══════════════════════════════════════════════════════════════════

GRANOLA NOTES PROCESSED:
  - Sales calls summarized: [X] new
  - Onboarding calls summarized: [Y] new
  - Files created in meeting_summaries/

CRM UPDATES:
  - New entries created: [X] companies
  - Status updates: [Y] progressions
  - Contextual notes added: [Z] pages

EMAIL PROCESSING:
  - Work inbox: [X] emails processed, [Y] archived, [Z] remaining
  - Notion tasks created: [X] tasks from actionable emails
  - Newsletter insights: [X] items extracted
  - Files: email_summaries_YYYY_MM_DD.md, newsletter_digest_YYYY_MM_DD.md

DAILY SCHEDULE:
  - Calendar events: [X] events from work calendar
  - Time blocks allocated: [Y] blocks
  - Files: daily_schedule_YYYY-MM-DD.md

CURRENT SPRINT:
  - Sprint: Week [X]
  - Sprint ID: [ID]
  - Date range: [START] to [END]

WARNINGS/ISSUES:
  - [List any errors, conflicts, or items needing attention]
  - [Or "None" if all clean]

ROUTINE COMPLETED: [HH:MM:SS] elapsed
Next routine recommended: [TOMORROW'S DATE]
```
