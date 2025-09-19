---
description: Create daily tasks using Enhanced Two-Pass System with comprehensive verification
allowed-tools: Task, mcp__notion-mcp__*, Read
---

# Daily Tasks Agent

Execute the Enhanced Two-Pass System for creating daily tasks from the Current Daily Todos Notion page with mandatory verification and 100% task adherence.

## Enhanced Two-Pass System Overview

This agent implements a robust task creation system that achieved 100% task adherence compared to the previous 21% failure rate. The system uses section-aware parsing, mandatory verification checkpoints, and comprehensive reporting.

## Critical Database IDs

- **Work Task Database**: `181c548c-c4ff-80ba-8a01-f3ed0b4a7fef` (all tasks go here)
- **Current Daily Todos Page**: `26fc548cc4ff80c787bfcac0369bec44`
- **Job Pipeline Database**: `20ac548cc4ff80ee9628e09d72900f10`
- **Edmund User ID**: `6ae517a8-2360-434b-9a29-1cbc6a427147`
- **Xiang Li User ID**: `1bad872b-594c-8117-b3e5-0002d3edb7d3`

## PHASE 1: Section-by-Section Parsing

### Objective
Parse the Current Daily Todos Notion page into distinct sections to distinguish between direct tasks and workflow instructions.

### Process
1. **Read the Current Daily Todos page** (`26fc548cc4ff80c787bfcac0369bec44`)
2. **Identify Section 1**: "Create daily tasks" (numbered list items 1-N) → DIRECT TASKS
3. **Identify Section 2**: "Follow these workflows" → WORKFLOW INSTRUCTIONS
4. **Output Parsing Verification**:
   ```
   PARSING VERIFICATION REPORT:
   📋 Found X direct daily tasks (items 1-X)
   🔄 Found Y workflow instructions  
   📊 Expected total individual tasks: X + (estimated derived tasks from workflows)
   ```

### Critical Rules
- **1:1 Mapping**: Each numbered item in Section 1 becomes exactly ONE task
- **Exact Text**: Use the exact text from numbered items as task names
- **No Interpretation**: Do not modify or interpret the task names

## PHASE 2: Two-Pass Task Creation

### PASS 1: Direct Task Creation (1:1 Mapping)

**Objective**: Create exactly ONE task for each numbered item in the "Create daily tasks" section.

**Process**:
1. **For each numbered item** (1, 2, 3, etc.) in Section 1:
   - Create task with **exact text** as task name
   - **Person**: Edmund (`6ae517a8-2360-434b-9a29-1cbc6a427147`) unless task specifies "as Li" (then Xiang Li)
   - **Tags**: Appropriate tag based on content:
     - Prospecting/LinkedIn/Sales: "Sell"
     - Customer service: "Serve" 
     - Development: "Build"
     - Administrative: "Admin"
   - **Sprint**: Current sprint ID (get dynamically - NEVER use cached values)
   - **Due Date**: Today's date
   - **Status**: "Not started"

**Assignment Rules**:
- Default: Edmund Cuthbert (`6ae517a8-2360-434b-9a29-1cbc6a427147`)
- If task contains "as Li": Xiang Li (`1bad872b-594c-8117-b3e5-0002d3edb7d3`)

### PASS 2: Workflow Execution (Database Queries → Multiple Tasks)

**Objective**: Execute workflow instructions to create multiple derived tasks from database queries.

**Common Workflows**:

1. **"Chase up clients"**:
   - Query Job Pipeline for status "Onboarding" OR "Activating"
   - Create individual "Chase up [Company]" task for each result
   - Tags: "Serve", Person: Edmund, Due: Today

2. **"Check enrollments"**:
   - Query Job Pipeline for status "In Progress"
   - Create individual "Check enrollment [Company]" task for each result
   - Tags: "Serve", Person: Edmund, Due: Today

**Query Filters**:
- Onboarding/Activating: `{"or": [{"property": "Status", "status": {"equals": "Onboarding"}}, {"property": "Status", "status": {"equals": "Activating"}}]}`
- In Progress: `{"property": "Status", "status": {"equals": "In Progress"}}`

## PHASE 3: Comprehensive Verification

### Mandatory Verification Report

**Format**:
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
- Status: ✅ COMPLETE / ❌ INCOMPLETE

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
✅ PROCEED (verification complete)
❌ HALT (fix discrepancies before proceeding)
```

### Success Criteria
- **100% Task Adherence**: ACTUAL = TOTAL tasks
- **Proper Properties**: All tasks have Person, Tags, Sprint, Due Date
- **1:1 Mapping**: Direct tasks exactly match numbered list items
- **Complete Workflows**: All database queries executed and derived tasks created

## Current Sprint Detection

**Critical**: Always get current sprint ID dynamically - NEVER use cached values.

1. **Query All Sprints Database**: `19dc548c-c4ff-80db-a687-fade4b6cc149`
2. **Filter**: Use "Is Current" formula property to find today's active sprint
3. **Extract ID**: Use the returned sprint ID for all task creation
4. **Purpose**: Ensure all daily tasks are created in the actual current sprint

## Error Handling

### Common Issues
1. **Missing Properties**: Ensure all tasks have Person, Tags, Sprint, Due Date
2. **Wrong Sprint**: Always query for current sprint dynamically
3. **Incomplete Workflows**: Verify database queries return expected results
4. **Text Mismatch**: Use exact text from numbered items, no interpretation

### Recovery Actions
- If database query fails: Retry with correct filter syntax
- If task creation fails: Check all required properties are provided
- If verification fails: List specific missing/incorrect tasks
- If count mismatch: Report exact discrepancy and halt

## Deep Links for Tasks

Include relevant deep links in task descriptions:
- **LinkedIn connections**: https://www.linkedin.com/mynetwork/invite-connect/connections/
- **LinkedIn messages**: https://www.linkedin.com/messaging/
- **Apollo prospecting**: https://app.apollo.io/#/tasks?dateRange[max]=YYYY-MM-DD&sortByField=task_due_at&sortAscending=true
- **Email follow-ups**: https://mail.google.com/mail/u/0/#inbox
- **Company-specific tasks**: Include Job Pipeline page URL from query results

## Usage Instructions

### Input Required
- Current date (YYYY-MM-DD format)
- Current sprint context (if known, otherwise will be queried)

### Expected Output
- Comprehensive verification report
- All tasks created with proper properties
- 100% adherence confirmation
- Ready for daily planning integration

### Integration Points
- Called by daily-routine.md after email processing
- Outputs feed into daily-planning agent
- Results used in standup notes generation

## Example Execution Flow

1. **Parse** Current Daily Todos page → Find 11 direct tasks + 2 workflows
2. **Create** 11 direct tasks with exact text mapping
3. **Execute** "Chase up clients" → Query Job Pipeline → Create 7 chase-up tasks
4. **Execute** "Check enrollments" → Query Job Pipeline → Create 8 enrollment tasks
5. **Verify** 26 total tasks created (11 + 7 + 8) = 100% adherence
6. **Report** comprehensive verification with ✅ COMPLETE status

This Enhanced Two-Pass System eliminates the systematic task omission problem and maintains the Notion document as the single source of truth while ensuring perfect adherence through mandatory verification.