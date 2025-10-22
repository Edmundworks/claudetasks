---
description: Execute complete daily routine including email triage, planning, and standup notes
allowed-tools: Task, Bash(date:*), Bash(ls:*), Read, MultiEdit, mcp__mcp-gsuite__*, mcp__notion-mcp__*
---

# Daily Routine Command

Execute [YOUR_NAME]'s complete daily routine by running email triage, daily planning, and standup notes generation in sequence.

## Current Context

- Today's date: !`date +"%Y-%m-%d"`
- Day of week: !`date +"%A"`
- Active files in root: !`ls -la *.md 2>/dev/null | grep -E "(email_summaries|newsletter_digest|daily_schedule|standup_notes)" || echo "No daily files found"`
- Archive status: !`ls -la archive/ 2>/dev/null | head -5 || echo "Archive directory not found"`

## Process Flow

### 1. Environment Setup & Date Verification
- Get current date and time
- Determine if it's a workday (Monday-Friday)
- Store date in format YYYY-MM-DD for file operations

### 2. Current Sprint Detection (MOVED BEFORE EMAIL PROCESSING)
- **CRITICAL**: Query Sprint Database (19dc548c-c4ff-80db-a687-fade4b6cc149) to get current active sprint
- **Filter**: Use "Is Current" formula property to find today's active sprint
- **Dynamic ID**: Extract current sprint ID for use in all task creation (NEVER use cached IDs)
- **Purpose**: Ensure all daily tasks are created in the actual current sprint
- **IMPORTANT**: Sprint ID must be retrieved BEFORE email processing to enable task creation from emails

### 3. Email Processing (WITH TASK CREATION)
- Use Agent: `daily-email-triage` and `email-preprocessor`
- Processes both work and personal emails
- Use `email-preprocessor` first to do the initial sweep, then pass the context AND current sprint ID to `daily-email-triage` for detailed triaging
- Archives routine/marketing emails
- Applies manual labels to important emails
- **NEW: Creates Notion tasks for actionable emails with Gmail deep links**
- Extracts newsletter content
- Outputs:
  - `email_summaries_YYYY_MM_DD.md` (includes Notion tasks created)
  - `newsletter_digest_YYYY_MM_DD.md`
  - Notion tasks in Work Task Database with email links

### 4. Daily Todo Processing - Use Daily Tasks Agent

- **Use Agent**: `daily-tasks-agent`
- **Purpose**: Execute Enhanced Two-Pass System for creating daily tasks with 100% adherence
- **Input**: Current date and sprint context
- **Process**: The agent handles all task creation including:
  - Section-by-section parsing of Current Daily Todos page
  - 1:1 mapping of direct daily tasks (numbered list items)
  - Workflow execution for derived tasks (chase-ups, enrollment checks)
  - Comprehensive verification with mandatory reporting
- **Output**: All daily tasks created in Work Task Database with proper properties
- **Success Criteria**: 100% task adherence with ✅ COMPLETE verification status

### 5. Daily Planning
- Use Agent: `daily-planning`
- Pulls calendar events from both calendars
- Runs task analyzers for work and personal tasks
- Integrates email insights and client tasks
- Creates comprehensive daily schedule
- Output: `daily_schedule_YYYY-MM-DD.md`

### 7. Sprint Information Update
- Sprint information already retrieved in Step 3 (current sprint detection)
- If today is Tuesday, execute standup notes using `sprint-planning-agent`
- Update CLAUDE.md if outdated with:
  - Sprint name and ID (from Step 3 dynamic query)
  - Sprint date range
  - Sprint goal

### 8. Standup Notes Generation (Workdays Only)
- If today is Monday, Wednesday, Thursday, Friday, execute standup notes using `daily-standup-notes-agent`
- Uses daily schedule and previous day's completions as context
- Includes client follow-up tasks in standup agenda
- Generates formatted standup notes
- Output: `standup_notes_YYYY-MM-DD.md`

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

## Execution Order & Dependencies - SIMPLIFIED WORKFLOW
1. **Current Sprint Detection** → Query Sprint Database for active sprint ID (needed by email triage)
2. **Email Triage** → Uses sprint ID to create tasks from actionable emails, produces email + newsletter files + Notion tasks
3. **Daily Todo Processing** → Use `daily-tasks-agent` with Enhanced Two-Pass System
4. **Daily Planning** → Reads email summary + ALL verified tasks (including email tasks), produces schedule file
5. **Sprint Update** → Sprint info already retrieved in step 1
6. **Standup Notes** → Reads schedule file, produces standup notes

## Time Considerations
- **Best Run Time**: 9:00am-10:00am ET
- **Standup Timing**: 11:00am-11:30am (Tuesdays: 11:00am-12:00pm for sprint planning)

## Error Handling
- Each component is atomic - if one fails, others can continue
- Failed email triage: Use previous day's context
- Failed calendar sync: Use cached events
- Failed Notion query: Use CLAUDE.md as fallback

## Success Criteria - ENHANCED
- All components execute successfully
- No duplicate calendar events created  
- Email inbox properly triaged
- Daily schedule reflects accurate state
- Standup notes ready before 11:00am on workdays
- **CRITICAL**: Two-pass task creation verification shows ✅ COMPLETE before proceeding
- **Enhanced Parsing**: Section-by-section analysis completed with verification checkpoint
- **Task Adherence**: All direct daily tasks created 1:1 from numbered list
- **Workflow Execution**: All workflow instructions executed with correct derived task counts

## Validation & Reporting - ENHANCED VERIFICATION
**MANDATORY**: After completing Daily Todo Processing Phase 3, provide comprehensive verification:

### Enhanced Task Creation Report Format:
```
DAILY TODO PROCESSING - VERIFICATION REPORT:
============================================

PHASE 1 - PARSING VERIFICATION:
📋 Direct daily tasks found: X (numbered items 1-X)
🔄 Workflow instructions found: Y
📊 Total expected individual tasks: X + (estimated derived)

PHASE 2 - TASK CREATION RESULTS:
PASS 1 - DIRECT TASKS (1:1 mapping):
- Expected: X direct tasks
- Created: Y direct tasks
- Status: ✅ COMPLETE / ❌ INCOMPLETE [STOP HERE IF INCOMPLETE]

PASS 2 - WORKFLOW EXECUTION:
- Workflow 1 "Chase up clients": Created A of B expected ✅/❌
- Workflow 2 "Check enrollments": Created C of D expected ✅/❌

PHASE 3 - COMPREHENSIVE VERIFICATION:
- Total expected tasks: X + B + D = TOTAL
- Total created tasks: Y + A + C = ACTUAL  
- Verification status: ✅ COMPLETE / ❌ INCOMPLETE
- Adherence score: ACTUAL/TOTAL = XX%

ERRORS/DISCREPANCIES (if any):
[List any missing or incorrect tasks]

STOP-GATE DECISION:
✅ PROCEED to Daily Planning (verification complete)
❌ HALT (fix discrepancies before proceeding)
```

## Example Execution

When you run this command, I will execute the **Simplified Agent-Based Workflow**:

### Phase 1: Foundation Setup
1. Query **Sprint Database** to get current active sprint ID (never use cached values)
2. Run **`email-preprocessor`** then **`daily-email-triage-agent`** (with sprint ID) to:
   - Process inbox and extract newsletter content
   - Create Notion tasks for actionable emails with Gmail deep links
   - Archive routine emails

### Phase 2: Daily Todo Processing  
3. Run **`daily-tasks-agent`** to execute Enhanced Two-Pass System with:
   - Section-by-section parsing of Current Daily Todos page
   - 1:1 mapping of direct daily tasks (numbered list items)
   - Workflow execution for derived tasks (chase-ups, enrollment checks)
   - Comprehensive verification with mandatory reporting
   - 100% task adherence with ✅ COMPLETE verification status

### Phase 3: Schedule Generation & Coordination  
4. Run **`daily-planning-agent`** to generate daily schedule incorporating ALL verified tasks
5. Update sprint information using **`sprint-planning-agent`** if Tuesday
6. Run **`daily-standup-notes-agent`** if Monday/Wednesday/Thursday/Friday

**Key Enhancement**: Modular agent architecture prevents complexity overflow and ensures reliable task creation.