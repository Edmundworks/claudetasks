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

### 2. Email Processing
- Use Agent: `daily-email-triage` and `email-preprocessor`
- Processes both work and personal emails
- Use `email-preprocessor` first to do the inital sweap, then pass the context to `daily-email-triage` for detailed triaging
- Archives routine/marketing emails
- Applies manual labels to important emails
- Extracts newsletter content
- Outputs:
  - `email_summaries_YYYY_MM_DD.md`
  - `newsletter_digest_YYYY_MM_DD.md`

### 3. Current Sprint Detection
- **CRITICAL**: Query Sprint Database (19dc548c-c4ff-80db-a687-fade4b6cc149) to get current active sprint
- **Filter**: Use "Is Current" formula property to find today's active sprint
- **Dynamic ID**: Extract current sprint ID for use in all task creation (NEVER use cached IDs)
- **Purpose**: Ensure all daily tasks are created in the actual current sprint

### 4. Daily Todo Processing - ENHANCED TWO-PASS SYSTEM

#### **PHASE 1: SECTION-BY-SECTION PARSING**
- **Source**: Query Current Daily Todos Notion page (26fc548cc4ff80c787bfcac0369bec44)
- **Enhanced Content Analysis**: Parse page content into distinct sections:
  - **SECTION 1**: "Create daily tasks" (numbered list items 1-N) → DIRECT TASKS (1:1 creation)
  - **SECTION 2**: "Follow these workflows" → WORKFLOW INSTRUCTIONS (execute to create multiple derived tasks)
- **Verification Checkpoint**: Before proceeding, output parsing summary:
  ```
  PARSING VERIFICATION REPORT:
  📋 Found X direct daily tasks (items 1-X)
  🔄 Found Y workflow instructions  
  📊 Expected total individual tasks: X + (estimated derived tasks from workflows)
  ```

#### **PHASE 2: TWO-PASS TASK CREATION**

**PASS 1: DIRECT TASK CREATION (1:1 Mapping)**
- **Input**: Numbered list items from "Create daily tasks" section
- **Process**: Create exactly ONE task for each numbered item, using the EXACT text as task name
- **Examples**: 
  - "Send LinkedIn connections to 50 prospects in Apollo" → 1 task with that exact name
  - "Comment on post as Li" → 1 task with that exact name
- **Verification**: Count created tasks = count of numbered items in section 1

**PASS 2: WORKFLOW EXECUTION (Database Queries → Multiple Tasks)**
- **Input**: Instructions from "Follow these workflows" section
- **Process**: Execute each workflow instruction to create multiple derived tasks
- **Examples**:
  - "Chase up clients" → Query Job Pipeline (Onboarding/Activating) → Create individual "Chase up [Company]" tasks
  - "Check enrollments" → Query Job Pipeline (In Progress) → Create individual "Check enrollment [Company]" tasks
- **Pre-execution Protocol**: For each workflow, query source database first to determine expected task count
- **Post-execution Verification**: Count created tasks and verify against expected count

#### **PHASE 3: COMPREHENSIVE VERIFICATION**
- **Task Count Audit**: 
  ```
  TASK CREATION VERIFICATION REPORT:
  ================================
  PHASE 1 - DIRECT TASKS:
  - Expected: X (from parsing)
  - Created: Y 
  - Status: ✅ COMPLETE / ❌ INCOMPLETE

  PHASE 2 - WORKFLOW TASKS:
  - Workflow 1 "Chase up clients": Created Z of W expected ✅/❌
  - Workflow 2 "Check enrollments": Created A of B expected ✅/❌
  
  TOTAL VERIFICATION:
  - Total expected: X + W + B = TOTAL
  - Total created: Y + Z + A = ACTUAL
  - Status: ✅ COMPLETE / ❌ INCOMPLETE
  
  ERRORS (if any): [List discrepancies]
  ```
- **Stop-gate**: Do NOT proceed to daily planning until verification shows ✅ COMPLETE
- **Error Handling**: If count mismatch, report discrepancy and list what was/wasn't created
- **Create Tasks**: For each specific actionable task, create individual work task in Work Task Database (181c548c-c4ff-80ba-8a01-f3ed0b4a7fef):
  - Task name: [Specific actionable task name, NOT the instruction text]
  - **Include relevant deep links in task description**:
    - LinkedIn connections: https://www.linkedin.com/mynetwork/invite-connect/connections/
    - LinkedIn messages: https://www.linkedin.com/messaging/
    - Apollo prospecting: https://app.apollo.io/#/tasks?dateRange[max]=YYYY-MM-DD&sortByField=task_due_at&sortAscending=true (replace YYYY-MM-DD with today's date)
    - Email follow-ups: https://mail.google.com/mail/u/0/#inbox
    - **Company-specific tasks**: When creating tasks like "Chase up [Company]", include the company's Job Pipeline page URL from the query results
  - Tag: Appropriate tag based on content (Build, Serve, Sell, Admin, etc.)
  - Assign to Edmund (6ae517a8-2360-434b-9a29-1cbc6a427147)
  - Link to current sprint: **USE DYNAMIC SPRINT ID FROM STEP 3**
  - Due date: Today (unless specified otherwise in todo)
  - Status: "Not started"
- **Integration**: Include these executed daily todo tasks in daily planning context

### 5. Client Task Generation
- Query Job Pipeline database (20ac548cc4ff80ee9628e09d72900f10) for clients in "Activating" and "Onboarding" status
- For each active client, create work todo in Work Task Database (181c548c-c4ff-80ba-8a01-f3ed0b4a7fef):
  - Task name: "Follow up with [Client Name] - [Status]"
  - Tag: "Serve" (customer service)
  - Assign to Edmund (6ae517a8-2360-434b-9a29-1cbc6a427147)
  - Link to current sprint: **USE DYNAMIC SPRINT ID FROM STEP 3**
  - Due date: Today + 1 day
  - Status: "Not started"
- Include these client tasks in daily planning context

### 6. Daily Planning
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

## Execution Order & Dependencies - ENHANCED WORKFLOW
1. **Email Triage** → No dependencies, produces email + newsletter files
2. **Current Sprint Detection** → Query Sprint Database for active sprint ID
3. **Daily Todo Processing - ENHANCED TWO-PASS SYSTEM**:
   - **PHASE 1: Section-by-Section Parsing** → Parse Daily Todos page into sections
   - **PHASE 2: Two-Pass Task Creation**:
     - **PASS 1**: Direct Task Creation (1:1 mapping from numbered list)
     - **PASS 2**: Workflow Execution (database queries → multiple derived tasks)
   - **PHASE 3: Comprehensive Verification** → Verify all tasks created before proceeding
   - **STOP-GATE**: Do NOT proceed to step 4 until verification shows ✅ COMPLETE
4. **Client Task Generation** → DEPRECATED (now handled in Daily Todo Processing Phase 2)
5. **Daily Planning** → Reads email summary + ALL verified tasks, produces schedule file
6. **Sprint Update** → Sprint info already retrieved in step 2
7. **Standup Notes** → Reads schedule file, produces standup notes

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

## Example Execution - ENHANCED WORKFLOW

When you run this command, I will execute the **Enhanced Two-Pass System**:

### Phase 1: Foundation Setup
1. Run **`email-preprocessor`** then **`daily-email-triage-agent`** to process inbox and extract newsletter content
2. Query **Sprint Database** to get current active sprint ID (never use cached values)

### Phase 2: Enhanced Daily Todo Processing
3. **PHASE 1: Section-by-Section Parsing**
   - Parse **Current Daily Todos** page into distinct sections
   - Output verification checkpoint with task counts
4. **PHASE 2: Two-Pass Task Creation**
   - **PASS 1**: Create direct tasks 1:1 from numbered list (exact text mapping)
   - **PASS 2**: Execute workflow instructions to create derived tasks from database queries  
5. **PHASE 3: Comprehensive Verification**
   - Verify all tasks created against expected counts
   - Generate detailed verification report
   - **STOP-GATE**: Halt if verification fails

### Phase 3: Schedule Generation & Coordination  
6. Run **`daily-planning-agent`** to generate daily schedule incorporating ALL verified tasks
7. Update sprint information using **`sprint-planning-agent`** if Tuesday
8. Run **`daily-standup-notes-agent`** if Monday/Wednesday/Thursday/Friday

**Key Enhancement**: The new system prevents task omission through mandatory verification checkpoints and section-aware parsing.