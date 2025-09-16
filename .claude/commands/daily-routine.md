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

### 4. Daily Todo Processing
- **Source**: Query Current Daily Todos Notion page (26fc548cc4ff80c787bfcac0369bec44)
- **Process**: Read all todos from the page content and interpret as workflow instructions
- **Workflow Execution**: For each todo item, execute the instruction to create specific actionable tasks:
  - **Example Input**: "Go through all jobs in job pipeline, for those in Onboarding or Activating create a todo for me to chase them and mention the company name"
  - **Example Output**: Multiple tasks like "Chase up Newton", "Chase up GigaML", "Chase up Blocksight" etc.
  - **Direct Tasks**: Simple todos like "Send 50 LinkedIn connections" create one task as written
  - **Workflow Tasks**: Complex instructions get executed to create multiple specific tasks
- **EXECUTION PROTOCOL**:
  1. **Pre-execution Count**: For workflow instructions, query source database first to determine expected task count
  2. **Execute**: Create individual tasks as specified
  3. **Post-execution Verification**: Count created tasks and verify against expected count
  4. **Report**: Log "Created X of Y expected tasks" for each workflow instruction
  5. **Error Handling**: If count mismatch, report discrepancy and list what was/wasn't created
- **Create Tasks**: For each specific actionable task, create individual work task in Work Task Database (181c548c-c4ff-80ba-8a01-f3ed0b4a7fef):
  - Task name: [Specific actionable task name, NOT the instruction text]
  - **Include relevant deep links in task description**:
    - LinkedIn connections: https://www.linkedin.com/mynetwork/invite-connect/connections/
    - LinkedIn messages: https://www.linkedin.com/messaging/
    - Apollo prospecting: https://app.apollo.io/#/tasks?dateRange[max]=YYYY-MM-DD&sortByField=task_due_at&sortAscending=true (replace YYYY-MM-DD with today's date)
    - Email follow-ups: https://mail.google.com/mail/u/0/#inbox
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

## Execution Order & Dependencies
1. **Email Triage** → No dependencies, produces email + newsletter files
2. **Current Sprint Detection** → Query Sprint Database for active sprint ID
3. **Daily Todo Processing** → Uses dynamic sprint ID from step 2, creates individual work todos
4. **Client Task Generation** → Uses dynamic sprint ID from step 2, creates work todos
5. **Daily Planning** → Reads email summary + daily todos + client tasks, produces schedule file
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

## Success Criteria
- All components execute successfully
- No duplicate calendar events created
- Email inbox properly triaged
- Daily schedule reflects accurate state
- Standup notes ready before 11:00am on workdays
- **Task Creation Verification**: All workflow instructions executed with correct task counts
- **Execution Summary**: Clear report of what was created vs expected

## Validation & Reporting
After completing all workflow instructions, provide an execution summary:

### Task Creation Report Format:
```
DAILY TODO EXECUTION SUMMARY:
================================

Workflow Instructions Processed: X
Direct Tasks Created: Y
Database Tasks Created: Z

DETAILED BREAKDOWN:
- Job Pipeline Chase-ups: Created 11 of 11 expected tasks ✅
- LinkedIn Connections: Created 1 of 1 expected tasks ✅  
- [Other workflows]: Created X of Y expected tasks ✅/❌

TOTAL VERIFICATION:
- Expected tasks: XX
- Created tasks: YY  
- Status: ✅ COMPLETE / ❌ INCOMPLETE

ERRORS (if any):
- [List any count mismatches or failed creations]
```

## Example Execution

When you run this command, I will:

1. First, run **`email-preprocessor`** agent then **`daily-email-triage-agent`** agent to process your inbox and extract newsletter content
2. Query the **Sprint Database** to get the current active sprint ID (never use cached values)
3. Query your **Current Daily Todos** Notion page and create individual work tasks for each todo in the current sprint
4. Query Job Pipeline database for "Activating" and "Onboarding" clients and create follow-up tasks
5. Then, run **`daily-planning-agent`** agent to generate your daily schedule incorporating urgent emails, daily todos, and client follow-ups
6. Update sprint information by using **`sprint-planning-agent`** if it's Tuesday
7. Finally, run **`daily-standup-notes-agent`** if it's a Monday, Wednesday, Thursday and Friday (includes all tasks in agenda)