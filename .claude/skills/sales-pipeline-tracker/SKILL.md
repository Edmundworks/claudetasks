---
name: sales-pipeline-tracker
description: Track sales pipeline progression from initial calls to onboarding by analyzing Granola meeting records and updating the Notion CRM. Use when asked about sales calls, pipeline updates, CRM tracking, or when processing yesterday's meetings for sales opportunities.
---

# Sales Pipeline Tracker

Automatically track sales progression from initial calls to onboarding by analyzing Granola call records and calendar events, then updating the Job Pipeline CRM in Notion.

## When to Use This Skill

- Checking if sales calls have progressed to onboarding
- Processing yesterday's sales activity
- Updating the pipeline CRM with new opportunities
- Tracking sales call progression over time

## Granola Folder Discovery (CRITICAL)

**ALWAYS call `list_folders` first** - never hardcode folder IDs.

Folders may be added, renamed, or reorganized at any time. Look for folders by name pattern:
- Sales calls: usually contains "Sales" in the name
- Onboarding: usually contains "Onboarding" in the name
- Customer calls: usually contains "Customer" in the name

The `get_folder_meetings` tool also accepts `folder_name` for partial matching.

## Notion CRM Database

**Job Pipeline Database ID**: `20ac548c-c4ff-80ee-9628-e09d72900f10`

**Schema**:
- **Name** (title): Company name
- **Status** (status): "Sales Call" or "Onboarding"
- **Owner** (people): Edmund's ID `6ae517a8-2360-434b-9a29-1cbc6a427147`
- **Source** (select): Origin of opportunity (e.g., `VC - Phil - Ardent`, `Referral - Vince - Plastic Labs`)

## Workflow

### Step 1: Determine Date Range

Get the date range from state tracking:

```bash
source venv/bin/activate && python -c "from scripts.assistant_state import get_date_range_since_last_run; start, end = get_date_range_since_last_run('sales_pipeline_tracker'); print(f'{start}|{end}')"
```

### Step 2: Discover Granola Folders

**ALWAYS run this first** to get current folder IDs:

```
mcp__granola__list_folders()
```

Parse the response to find Sales and Onboarding folders by name.

### Step 3: Fetch Sales Calls

Use `mcp__granola__get_folder_meetings` with native date filtering:

```
mcp__granola__get_folder_meetings({
  folder_name: "Sales",  // or use folder_id from list_folders
  start_date: "YYYY-MM-DD",
  end_date: "YYYY-MM-DD"
})
```

### Step 4: Check Onboarding Folder

```
mcp__granola__get_folder_meetings({
  folder_name: "Onboarding",  // or use folder_id from list_folders
  start_date: "YYYY-MM-DD",
  end_date: "YYYY-MM-DD"
})
```

### Step 5: Extract Meeting Details

For each meeting found, get details and transcript:

```
mcp__granola__get_meeting_details({ meeting_id: "..." })
mcp__granola__get_meeting_transcript({ meeting_id: "..." })
```

Extract:
- Company name from attendee email domains
- Contact person and email
- Call context from transcript

### Step 6: Check for Onboarding Progression

Search calendar for upcoming onboarding meetings:
- Check current week + next 2 weeks
- Look for: 30-45 min duration, "onboarding" in title
- Match by email domain (john@company.com matches sarah@company.com)

### Step 7: Prepare CRM Updates

Cross-reference against CRM database to find existing entries:

```
mcp__notion-mcp__API-post-database-query({
  database_id: "20ac548c-c4ff-80ee-9628-e09d72900f10"
})
```

### Step 8: Propose Changes (Await Approval)

Present proposed changes:
- New entries to create
- Status updates (Sales Call → Onboarding)
- Source labels when inferable

**NEVER write to Notion without explicit approval.**

### Step 9: Apply Changes & Update State

After approval:

```javascript
// Create new entry
mcp__notion-mcp__API-post-page({
  parent: { database_id: "20ac548c-c4ff-80ee-9628-e09d72900f10" },
  properties: { title: [{ text: { content: "Company Name" } }] }
})

// Update with properties
mcp__notion-mcp__API-patch-page({
  page_id: "...",
  properties: {
    "Status": { status: { name: "Sales Call" } },
    "Owner": { people: [{ id: "6ae517a8-2360-434b-9a29-1cbc6a427147" }] }
  }
})
```

Update state after success:

```bash
source venv/bin/activate && python -c "from scripts.assistant_state import update_last_run; update_last_run('sales_pipeline_tracker')"
```

## Client Identification Rules

1. Extract company name from attendee email domains
2. Check Granola transcript for company mentions
3. Cross-reference against CRM for exact matches
4. Use fuzzy matching for Inc./Corp./LLC variations

## Source Label Inference

Infer source from transcript and calendar:
- **VC referral**: `VC - <first name> - <fund>`
- **Personal referral**: `Referral - <first name> - <company>`
- **Platform/community**: Just the org name (e.g., `Betaworks`)

If unknown, mark as `Source: (unknown, leave blank)`

## Output Format

```markdown
## Sales Pipeline Analysis

**Date Range**: [start] to [end] ([N] days)
**Sales Calls Found**: [count]

### [Date]: [Company Name]
- **Contact**: [Name] ([email])
- **Evidence**: [domain/transcript snippet]
- **CRM Status**: [New/Existing]
- **Onboarding**: [Detected on DATE / Not detected]
- **Proposed Action**: [Create new / Update to Onboarding]
- **Status**: Sales Call | **Source**: [inferred or unknown]

### Proposed Changes (Awaiting Approval)
1. [Action for Company A]
2. [Action for Company B]

### Warnings
- [Any ambiguous matches]
```

## Available Granola MCP Tools

| Tool | Purpose |
|------|---------|
| `list_folders` | List all folders with document counts |
| `get_folder_meetings` | Get meetings with date filtering |
| `get_meeting_details` | Get meeting metadata |
| `get_meeting_transcript` | Get full transcript |
| `get_meeting_documents` | Get meeting notes |
| `search_meetings` | Search by query |
