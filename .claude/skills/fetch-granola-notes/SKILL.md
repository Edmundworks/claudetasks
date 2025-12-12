---
name: fetch-granola-notes
description: Quickly fetch and list Granola meetings by category/folder. Use when you need to see what meetings exist in a specific category (Sales, Onboarding, Customer calls, VC Calls, etc.) without fetching full meeting content. Returns meeting titles, dates, and IDs for further drilling down.
---

# FetchGranolaNotes - Fast Granola Meeting Lookup

Quickly list Granola meetings by category/folder. This skill is for **listing meetings only** - it does NOT fetch full meeting content or transcripts. Use this when you need a quick overview of meetings in a category.

## When to Use This Skill

- Listing all meetings in a specific category (e.g., "show me all Sales calls")
- Getting a quick count of meetings by category
- Finding meeting IDs for further investigation
- Overview of recent activity by meeting type
- Answering "what meetings do we have in X folder?"

## When NOT to Use This Skill

- Fetching full meeting transcripts or summaries (use `granola-note-reader` agent)
- Detailed meeting analysis (use `sales-pipeline-tracker`)
- Searching across all meetings by keyword (use `search_meetings`)

## Granola Meeting Categories

**ALWAYS call `list_folders` first** to get current folder IDs - never hardcode them.

### Current Categories (as of Dec 2025)

| Category | Folder Name | Purpose |
|----------|-------------|---------|
| **Sales Calls** | `Sales - Call 1` | Initial sales conversations with prospects |
| **Onboarding** | `Onboarding - Call 2` | Customer onboarding sessions |
| **Customer Calls** | `Customer calls` | Ongoing customer conversations |
| **VC Calls** | `VC Calls` | Investor and VC meetings |
| **1st Interviews** | `1st Interview - Edmund` | Candidate interview screenings |
| **Team Meetings** | `Team meetings` | Internal team discussions |
| **Product Feedback** | `Cap Product Feedback` | Product feedback sessions |
| **Closing Prep** | `Closing Candidate Prep` | Candidate closing preparation |
| **Vendors** | `vendors` | Vendor/partner calls |

### Category Aliases

When the user asks for meetings, map their request to the correct folder:

| User Says | Map To Folder |
|-----------|---------------|
| "sales", "sales calls", "prospects" | `Sales - Call 1` |
| "onboarding", "onboarding calls" | `Onboarding - Call 2` |
| "customer", "customers", "client calls" | `Customer calls` |
| "investor", "vc", "fundraising" | `VC Calls` |
| "interviews", "1st interview", "screening" | `1st Interview - Edmund` |
| "team", "internal", "standup" | `Team meetings` |
| "feedback", "product feedback" | `Cap Product Feedback` |
| "vendors", "partners" | `vendors` |

## Workflow

### Step 1: Discover Folders (Always First)

```
mcp__granola__list_folders()
```

This returns all folders with:
- Folder ID
- Folder Name
- Document count
- Date range of meetings

### Step 2: Fetch Meetings from Category

Use `get_folder_meetings` with optional date filtering:

```
mcp__granola__get_folder_meetings({
  folder_name: "Sales",  // Partial match supported
  start_date: "2025-12-01",  // Optional: YYYY-MM-DD
  end_date: "2025-12-11",    // Optional: YYYY-MM-DD
  limit: 50                   // Default 50, max configurable
})
```

Or use folder_id for exact match:

```
mcp__granola__get_folder_meetings({
  folder_id: "b515c9e5-a860-493f-b5a6-cb4f2db97f35",
  start_date: "2025-12-01"
})
```

### Step 3: Return Meeting List

Return a concise list with:
- **Meeting category** (folder name)
- Meeting title
- Date/time
- Meeting ID (for further lookup)
- Attendee count or key attendee

## Output Format

### Category Overview (All Categories)

```markdown
## Granola Meeting Categories

| Category | Meetings | Latest |
|----------|----------|--------|
| Sales - Call 1 | 89 | Dec 9, 2025 |
| Onboarding - Call 2 | 69 | Dec 9, 2025 |
| VC Calls | 68 | Dec 10, 2025 |
| Customer calls | 6 | Dec 8, 2025 |
| Team meetings | 21 | Dec 9, 2025 |
| 1st Interview - Edmund | 25 | Dec 11, 2025 |
| Cap Product Feedback | 8 | Nov 6, 2025 |
| vendors | 3 | Nov 13, 2025 |
| Closing Candidate Prep | 1 | Nov 18, 2025 |
```

### Single Category Listing

```markdown
## Sales Calls (Last 7 Days)

| Date | Meeting | ID |
|------|---------|-----|
| Dec 9 | Acme Corp - Initial Call | `abc123` |
| Dec 8 | Beta Inc - Sales Discovery | `def456` |
| Dec 5 | Gamma Ltd - Intro Call | `ghi789` |

**Total**: 3 meetings
**Date Range**: Dec 5-9, 2025
```

## Available Granola MCP Tools

| Tool | Purpose | Use in This Skill |
|------|---------|-------------------|
| `list_folders` | List all folders with counts | YES - always first |
| `get_folder_meetings` | Get meetings with date filter | YES - main tool |
| `get_meeting_details` | Get meeting metadata | NO - out of scope |
| `get_meeting_transcript` | Get full transcript | NO - out of scope |
| `search_meetings` | Search by keyword | NO - use directly |

## Examples

### "Show me all sales calls this week"

1. Call `list_folders()` to get Sales folder ID
2. Call `get_folder_meetings(folder_name: "Sales", start_date: "2025-12-09", end_date: "2025-12-11")`
3. Return formatted list of meetings

### "How many VC calls have we had?"

1. Call `list_folders()`
2. Return the document count for "VC Calls" folder (68 as of Dec 2025)

### "List recent customer meetings"

1. Call `list_folders()` to get Customer calls folder ID
2. Call `get_folder_meetings(folder_name: "Customer", limit: 10)`
3. Return formatted list of recent meetings

### "What meeting categories do we have?"

1. Call `list_folders()`
2. Return the category overview table with all folders and counts

## Integration Notes

- This skill is **read-only** - it only lists meetings
- For CRM updates based on meetings, use `sales-pipeline-tracker`
- For detailed meeting content and summaries, use `granola-note-reader` agent with the meeting ID
- Folder structure may change - always call `list_folders` first

## Related Agent

**granola-note-reader**: Use this agent to get structured summaries of specific meetings. Pass the meeting ID from this skill's output to get detailed summaries tailored to the meeting type (Sales Call, Onboarding, etc.).

## Summary Timestamp Tracking

**File**: `last_summarized.md` (co-located with this skill at `.claude/skills/fetch-granola-notes/last_summarized.md`)

This file tracks when meetings were last fetched and summarized for each category. Use it to:
- Determine which meetings are new since last summary run
- Filter meetings by date to only process unsummarized ones
- Track how many meetings were processed per category

### Reading the Timestamp File

Before summarizing meetings, read `last_summarized.md` to get the last summarized date for the target category. Use that date as `start_date` when fetching meetings to only get new ones.

### Batch Summarization Workflow

When summarizing multiple meetings:

1. **Fetch meetings** from the category using date filter (start from last summarized timestamp)
2. **Launch `granola-note-reader` sub-agents** to summarize each meeting
   - Each sub-agent saves its summary to `/Users/edmund/MyAssistant/meeting_summaries/`
   - Sub-agents return: file path, key fields, and meeting ID
3. **WAIT for ALL sub-agents to complete** before proceeding
4. **Only after ALL sub-agents finish**, update `last_summarized.md`

### Updating the Timestamp File (CRITICAL - Main Agent Responsibility)

**The main agent using this skill is responsible for updating timestamps.**

**IMPORTANT**: Do NOT update `last_summarized.md` until ALL `granola-note-reader` sub-agents have completed their work.

**Update process:**
1. Confirm all sub-agents have returned successfully
2. Read the current `last_summarized.md` file
3. Find the row for the category you just processed
4. Update:
   - **Last Summarized**: Current date/time (format: `YYYY-MM-DD HH:MM`)
   - **Meetings Processed**: Count of meetings successfully summarized in this run
5. Write the updated file

**Example update** (after all 5 Sales call sub-agents complete on Dec 11, 2025 at 3:30 PM):

```markdown
| Sales - Call 1 | 2025-12-11 15:30 | 5 |
```

### Timestamp File Format

```markdown
# Granola Meeting Summary Timestamps

Last time meetings were fetched and summarized by category.

| Category | Last Summarized | Meetings Processed |
|----------|-----------------|-------------------|
| Sales - Call 1 | 2025-12-11 15:30 | 5 |
| Onboarding - Call 2 | Never | 0 |
| ... | ... | ... |
```

### Summary Output Location

Sub-agents save meeting summaries to a structured directory:

```
/Users/edmund/MyAssistant/meeting_summaries/
├── sales_call_1/
│   └── {YYYY-MM-DD}/
│       └── {company-name}.md
├── onboarding_call_2/
├── customer_calls/
├── vc_calls/
├── 1st_interview_edmund/
├── team_meetings/
├── cap_product_feedback/
├── closing_candidate_prep/
└── vendors/
```

**Path format**: `meeting_summaries/{category_slug}/{date}/{company_or_title}.md`

This structure allows easy identification of which dates have summaries and which are missing.
