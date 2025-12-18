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

### Step 5: Extract Meeting Details & Company Names

For each meeting found, get details and transcript:

```
mcp__granola__get_meeting_details({ meeting_id: "..." })
mcp__granola__get_meeting_transcript({ meeting_id: "..." })
```

The MCP now returns `participant_details` with emails and companies. Extract:

1. **Company name** (see "Company Name Rules" section below):
   - Use `participant.company` if available
   - Otherwise clean the email domain (remove `.com`, `join` prefix, etc.)
   - **NEVER use person's name as company name**
2. **Contact person** - the external attendee (not Edmund)
3. **Contact email** - from participant_details
4. **Call context** - from transcript

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

## Company Name Rules (CRITICAL)

### FORBIDDEN: Using Person's Name as Company Name

**NEVER create CRM entries using a person's name as the company name.**

Bad examples (DO NOT DO):
- ❌ "Victoria Pu" as company name
- ❌ "Satish Nagpal" as company name
- ❌ "Tunde Adeyinka" as company name

The only exception is when the company is literally named after a person (e.g., "John Deere", "Goldman Sachs").

### Company Name Extraction (Use fetch-granola-notes Rules)

Follow the company name cleaning rules from `fetch-granola-notes` skill:

1. **Use participant.company** if available from MCP response
2. **Extract from email domain** and apply cleaning:
   - Remove suffixes: `.com`, `.ai`, `.io`, `.co`, `.org`, `.net`, `.gg`, `.app`, `.dev`
   - Remove prefixes: `join`, `get`, `try`, `use`, `meet`, `hello`, `hi`, `with`, `go`, `my`, `the`
   - Title case the result

### Extraction Examples

| Participant Email | Company Name |
|-------------------|--------------|
| `tunde@joinhexagon.com` | Hexagon |
| `victoria@paceapp.ai` | Pace App |
| `satish@astrada.co` | Astrada |
| `ben@heater.gg` | Heater |
| `ayoola@astronaut.chat` | Astronaut |

### Validation Before CRM Creation

Before creating or updating a CRM entry:

1. **Verify company name is NOT a person's name**
   - Check if it matches `FirstName LastName` pattern
   - Check if it matches the participant's name
   - If it does, STOP and extract from email domain instead

2. **Verify company name is cleaned**
   - No `.com`, `.ai`, etc. suffixes
   - No `join`, `get`, etc. prefixes
   - Properly capitalized

3. **If company name cannot be determined**
   - Flag for manual review
   - Do NOT create entry with person's name as fallback

### Client Identification Priority

1. **Company field** from Granola MCP participant_details (highest priority)
2. **Email domain** - cleaned using the rules above
3. **Transcript mentions** - look for company name in transcript
4. **Meeting title** - parse company name if format is "Call with [Company]"
5. **Manual review** - if none of above work, flag for human input

### Cross-Reference Rules

- Cross-reference against CRM for exact matches
- Use fuzzy matching for Inc./Corp./LLC variations
- Match by email domain (john@company.com matches sarah@company.com)

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

### [Date]: [Company Name] (cleaned from email/participant data)
- **Company**: [Cleaned company name - NOT person's name]
- **Contact**: [Name] <[email]>
- **Company Source**: [participant.company / email domain / transcript]
- **CRM Status**: [New/Existing]
- **Onboarding**: [Detected on DATE / Not detected]
- **Proposed Action**: [Create new / Update to Onboarding]
- **Status**: Sales Call | **Source**: [inferred or unknown]

### Proposed Changes (Awaiting Approval)
1. Create "Hexagon" (from tunde@joinhexagon.com)
2. Update "Astrada" status to Onboarding

### Warnings
- [Any ambiguous matches]
- [Companies that could not be identified - require manual review]
```

**CRITICAL**: The CRM entry title MUST be the cleaned company name, NOT the person's name.

## Available Granola MCP Tools

| Tool | Purpose |
|------|---------|
| `list_folders` | List all folders with document counts |
| `get_folder_meetings` | Get meetings with date filtering |
| `get_meeting_details` | Get meeting metadata |
| `get_meeting_transcript` | Get full transcript |
| `get_meeting_documents` | Get meeting notes |
| `search_meetings` | Search by query |
