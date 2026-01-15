---
name: crm-update
description: Update the Job Pipeline CRM in Notion based on summarized Granola meeting notes. Reads the latest sales and onboarding summaries, cross-references with CRM, and proposes updates. Also supports manual CRM operations.
---

# CRM Update Skill

Manage the Job Pipeline CRM in Notion - create leads, update statuses, track sources, and maintain accurate sales pipeline data based on summarized meeting notes.

## When to Use This Skill

- Processing new meeting summaries to update CRM
- Adding a new lead or opportunity to the pipeline
- Updating deal status (Lead → Sales Call → Onboarding → In progress, etc.)
- Setting or changing the source of an opportunity
- Updating customer feedback, metrics, or other fields
- Marking deals as won (Filled by us) or lost (closed lost, Not a fit)

## Database Schema

See `@crm_schema.md` (co-located with this skill) for full database schema including:
- All field definitions and types
- Status options and transitions
- Source type options
- Related databases

**Database ID**: `20ac548c-c4ff-80ee-9628-e09d72900f10`

---

## API Approach: Direct Notion API vs MCP

**IMPORTANT**: Use direct Notion API calls via curl for **creating pages**. The Notion MCP has a bug where the `parent` parameter gets double-stringified, causing page creation to fail.

### What Works with MCP
- `mcp__notion-mcp__API-post-search` - Search for pages/databases
- `mcp__notion-mcp__API-patch-page` - Update existing page properties
- `mcp__notion-mcp__API-patch-block-children` - Append content to pages
- `mcp__notion-mcp__API-retrieve-a-page` - Get page details

### What Requires Direct API (curl)
- **Creating new pages** (`POST /v1/pages`) - MCP bug with `parent` parameter
- **Moving pages** (`POST /v1/pages/{id}`) - Same `parent` parameter bug

### Environment Setup
The Notion token is stored in `/Users/edmund/MyAssistant/.env`:
```bash
# Load token before API calls
export $(grep NOTION_TOKEN /Users/edmund/MyAssistant/.env | xargs)
```

---

## Primary Workflow: Update CRM from Meeting Summaries

This is the main workflow for keeping the CRM in sync with sales activity.

### Step 1: Check Last Summarized Timestamps

Read the timestamp file to find when meetings were last summarized:

**File**: `/Users/edmund/MyAssistant/.claude/skills/fetch-granola-notes/last_summarized.md`

Look for the `Last Summarized` column for these categories:
- `Sales - Call 1` → maps to `meeting_summaries/sales_call_1/`
- `Onboarding - Call 2` → maps to `meeting_summaries/onboarding_call_2/`

### Step 2: Find New Meeting Summaries

Based on the timestamps, scan the meeting summaries directories for new files:

```
/Users/edmund/MyAssistant/meeting_summaries/
├── sales_call_1/
│   └── {YYYY-MM-DD}/
│       └── {company-name}.md
└── onboarding_call_2/
    └── {YYYY-MM-DD}/
        └── {company-name}.md
```

**Process**:
1. List date directories in `sales_call_1/` and `onboarding_call_2/`
2. Filter to dates on or after the last summarized timestamp
3. Read each `.md` file in those date directories

### Step 3: Extract CRM-Relevant Data from Summaries

From each meeting summary, extract:

| Field | Source in Summary |
|-------|-------------------|
| Company | `**Company**:` field |
| Contact | `**Contact**:` field (name and role) |
| Date | `**Date**:` field or directory date |
| Referral Source | `### Referral Source` section |
| Onboarding Status | `### Onboarding Status` section |
| Onboarding Date | `**Scheduled Date**:` if specified |

### Step 4: Cross-Reference with CRM

Use MCP to search for existing entries:

```javascript
mcp__notion-mcp__API-post-search({
  query: "<company-name>",
  filter: { property: "object", value: "page" }
})
```

Determine action for each company:
- **Not found**: Create new entry (use curl)
- **Found at "Lead"**: Update to "Sales Call" (use MCP)
- **Found at "Sales Call"**: Check if onboarding discussed → update to "Onboarding"
- **Found at "Onboarding"**: No status change needed (unless progressing further)

### Step 5: Apply CRM Updates

#### Creating New Entries (USE CURL - MCP has bug)

```bash
# Load environment and create new CRM entry
export $(grep NOTION_TOKEN /Users/edmund/MyAssistant/.env | xargs) && \
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer ${NOTION_TOKEN}" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  --data-raw '{
    "parent": {"database_id": "20ac548c-c4ff-80ee-9628-e09d72900f10"},
    "properties": {
      "Name": {"title": [{"text": {"content": "Company Name"}}]},
      "Status": {"status": {"name": "Sales Call"}},
      "Owner": {"people": [{"id": "6ae517a8-2360-434b-9a29-1cbc6a427147"}]},
      "Source Type": {"select": {"name": "VC"}},
      "Source": {"select": {"name": "VC - Phil - Ardent"}}
    }
  }' | jq '.id'
```

#### Updating Existing Entries (MCP works fine)

```javascript
mcp__notion-mcp__API-patch-page({
  page_id: "<page-id>",
  properties: {
    "Status": { status: { name: "Sales Call" } },
    "Owner": { people: [{ id: "6ae517a8-2360-434b-9a29-1cbc6a427147" }] },
    "Source Type": { select: { name: "VC" } },
    "Source": { select: { name: "VC - Phil - Ardent" } }
  }
})
```

### Step 6: Add Contextual Notes to Page Content

After creating/updating the CRM entry, **append contextual notes** to the page body (MCP works for this):

```javascript
mcp__notion-mcp__API-patch-block-children({
  block_id: "<page-id>",  // The page ID acts as the parent block
  children: [
    {
      type: "paragraph",
      paragraph: {
        rich_text: [
          { type: "text", text: { content: "📅 2025-12-11 - Sales Call Notes" } }
        ]
      }
    },
    {
      type: "paragraph",
      paragraph: {
        rich_text: [
          { type: "text", text: { content: "<contextual notes from meeting summary>" } }
        ]
      }
    }
  ]
})
```

#### What to Include in Contextual Notes

Extract from the meeting summary and write notes that help the next person:

| Include | Example |
|---------|---------|
| **Contact & Role** | "Spoke with Jane Smith (Head of Engineering)" |
| **Company Context** | "Series B startup, 50 engineers, scaling backend team" |
| **Pain Points** | "Struggling to find senior Go developers, tried 3 agencies" |
| **What They're Looking For** | "2 senior backend engineers, remote OK, $180-220k range" |
| **Referral Context** | "Referred by Phil at Ardent - Phil worked with Jane at previous company" |
| **Key Discussion Points** | "Discussed our AI matching approach, showed demo of candidate pipeline" |
| **Next Steps** | "Onboarding call scheduled for Dec 15 to set up account" |
| **Red Flags / Notes** | "Budget approved but timeline is Q1, may need to follow up in Jan" |

#### Note Format Template

```markdown
📅 2025-12-11 - Sales Call Notes

**Contact**: Jane Smith, Head of Engineering
**Referral**: Phil at Ardent Ventures (worked together at previous startup)

**Context**: Series B fintech startup, 50-person engineering team scaling to 80.
Struggled with traditional recruiters who don't understand technical roles.

**Looking For**: 2 senior backend engineers (Go/Python), remote-friendly, $180-220k

**Discussion**: Walked through our AI matching approach. Jane was impressed by
the technical depth of candidate profiles. Main concern was timeline - they need
hires by end of Q1.

**Next Steps**: Onboarding call Dec 15 at 2pm to set up account and review initial candidates.
```

---

## Manual CRM Operations

### Create New Lead (CURL)

```bash
export $(grep NOTION_TOKEN /Users/edmund/MyAssistant/.env | xargs) && \
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer ${NOTION_TOKEN}" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  --data-raw '{
    "parent": {"database_id": "20ac548c-c4ff-80ee-9628-e09d72900f10"},
    "properties": {
      "Name": {"title": [{"text": {"content": "Company Name"}}]},
      "Status": {"status": {"name": "Lead"}},
      "Owner": {"people": [{"id": "6ae517a8-2360-434b-9a29-1cbc6a427147"}]},
      "Source Type": {"select": {"name": "VC"}},
      "Source": {"select": {"name": "VC - Phil - Ardent"}}
    }
  }' | jq '.id'
```

### Create Entry at Sales Call Stage (CURL)

```bash
export $(grep NOTION_TOKEN /Users/edmund/MyAssistant/.env | xargs) && \
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer ${NOTION_TOKEN}" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  --data-raw '{
    "parent": {"database_id": "20ac548c-c4ff-80ee-9628-e09d72900f10"},
    "properties": {
      "Name": {"title": [{"text": {"content": "Company Name"}}]},
      "Status": {"status": {"name": "Sales Call"}},
      "Owner": {"people": [{"id": "6ae517a8-2360-434b-9a29-1cbc6a427147"}]}
    }
  }' | jq '.id'
```

### Update Deal Status (MCP)

```javascript
mcp__notion-mcp__API-patch-page({
  page_id: "<page-id>",
  properties: {
    "Status": { status: { name: "Sales Call" } }
  }
})
```

### Progress to Onboarding (MCP)

```javascript
mcp__notion-mcp__API-patch-page({
  page_id: "<page-id>",
  properties: {
    "Status": { status: { name: "Onboarding" } }
  }
})
```

### Mark as Won (MCP)

```javascript
mcp__notion-mcp__API-patch-page({
  page_id: "<page-id>",
  properties: {
    "Status": { status: { name: "Filled by us" } },
    "Filled": { date: { start: "2025-12-11" } }
  }
})
```

### Mark as Lost (MCP)

```javascript
mcp__notion-mcp__API-patch-page({
  page_id: "<page-id>",
  properties: {
    "Status": { status: { name: "closed lost" } }
  }
})
```

### Update Metrics (MCP)

```javascript
mcp__notion-mcp__API-patch-page({
  page_id: "<page-id>",
  properties: {
    "Candidates sent": { number: 5 },
    "Interviews": { number: 3 },
    "# of roles": { number: 2 }
  }
})
```

### Set Follow-Up Date (MCP)

```javascript
mcp__notion-mcp__API-patch-page({
  page_id: "<page-id>",
  properties: {
    "Follow-Up Date": { date: { start: "2025-12-15" } }
  }
})
```

### Add Customer Feedback (MCP)

```javascript
mcp__notion-mcp__API-patch-page({
  page_id: "<page-id>",
  properties: {
    "Customer Feedback": {
      rich_text: [{ text: { content: "Great experience, fast turnaround" } }]
    }
  }
})
```

---

## Query Operations

### Find Lead by Name (MCP)

```javascript
mcp__notion-mcp__API-post-search({
  query: "Company Name",
  filter: { property: "object", value: "page" }
})
```

### Get Page Details (MCP)

```javascript
mcp__notion-mcp__API-retrieve-a-page({
  page_id: "<page-id>"
})
```

---

## Batch Operations (CURL)

### Create Multiple CRM Entries

For creating multiple entries efficiently, run curl commands in parallel:

```bash
# Create multiple entries - run in parallel
export $(grep NOTION_TOKEN /Users/edmund/MyAssistant/.env | xargs)

# Company 1
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer ${NOTION_TOKEN}" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  --data-raw '{"parent":{"database_id":"20ac548c-c4ff-80ee-9628-e09d72900f10"},"properties":{"Name":{"title":[{"text":{"content":"Company1"}}]},"Status":{"status":{"name":"Sales Call"}},"Owner":{"people":[{"id":"6ae517a8-2360-434b-9a29-1cbc6a427147"}]}}}' | jq '.id'

# Company 2 (can run in parallel)
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer ${NOTION_TOKEN}" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  --data-raw '{"parent":{"database_id":"20ac548c-c4ff-80ee-9628-e09d72900f10"},"properties":{"Name":{"title":[{"text":{"content":"Company2"}}]},"Status":{"status":{"name":"Sales Call"}},"Owner":{"people":[{"id":"6ae517a8-2360-434b-9a29-1cbc6a427147"}]}}}' | jq '.id'
```

---

## Source Inference from Meeting Summaries

When creating CRM entries from meeting summaries, infer source from the `### Referral Source` section:

| Pattern in Summary | Source Type | Source Value |
|--------------------|-------------|--------------|
| "referred by [Name] at [VC Fund]" | `VC` | `VC - [Name] - [Fund]` |
| "referred by [Name] from [Company]" | `Referral` | `Referral - [Name] - [Company]` |
| "existing customer [Name]" | `Customer` | `Customer - [Name] - [Company]` |
| "met at [Event]" | `Event` | `Event - [Event Name]` |
| "inbound inquiry" / "reached out" | `Inbound` | Leave blank |
| Unknown/unclear | `Other` | Leave blank |

---

## Best Practices

1. **Always set Owner** when creating new leads (Edmund's ID: `6ae517a8-2360-434b-9a29-1cbc6a427147`)
2. **Always set Source Type and Source** when known
3. **Check for existing entry** before creating to avoid duplicates
4. **Update Status promptly** based on meeting summaries
5. **Track onboarding progression** - if onboarding is scheduled, update status
6. **Use curl for page creation** - MCP has a bug with the `parent` parameter
7. **Use MCP for updates** - `API-patch-page` and `API-patch-block-children` work correctly

---

## Troubleshooting

### MCP Page Creation Fails
**Error**: `body.parent should be an object or undefined, instead was "{"database_id": "..."}"`

**Cause**: The Notion MCP has a bug where the `parent` parameter gets double-stringified.

**Solution**: Use curl for page creation instead:
```bash
export $(grep NOTION_TOKEN /Users/edmund/MyAssistant/.env | xargs) && \
curl -s -X POST "https://api.notion.com/v1/pages" ...
```

### Token Not Found
**Error**: `curl: option : blank argument where content is expected`

**Cause**: NOTION_TOKEN environment variable not loaded.

**Solution**: Ensure you're loading from .env:
```bash
export $(grep NOTION_TOKEN /Users/edmund/MyAssistant/.env | xargs)
```

---

## Related Files

- **Schema**: `crm_schema.md` (co-located)
- **Meeting Summaries**: `/Users/edmund/MyAssistant/meeting_summaries/`
- **Timestamps**: `/Users/edmund/MyAssistant/.claude/skills/fetch-granola-notes/last_summarized.md`
- **Environment**: `/Users/edmund/MyAssistant/.env` (contains NOTION_TOKEN)

## Related Skills & Agents

- **fetch-granola-notes**: Lists meetings by category, manages summarization timestamps
- **granola-note-reader**: Summarizes individual meetings to markdown files
- **sales-pipeline-tracker**: Automated pipeline tracking (alternative workflow)
