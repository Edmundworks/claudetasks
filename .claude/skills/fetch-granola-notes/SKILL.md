---
name: fetch-granola-notes
description: Comprehensive manual for working with the Granola MCP. Covers meeting categories, company name extraction, finding transcripts, and all available operations. Reference this skill whenever working with Granola meeting data.
---

# Granola MCP Manual

Complete reference for working with Granola meeting data via MCP.

## Default Behavior

**If no date range is specified**, assume we are only fetching meetings since the last fetch. Check `last_summarized.md` (in this skill's directory) to get the timestamp for the relevant meeting category, then use that as `start_date`.

---

## Meeting Categories (Folders)

### Discovering Categories

**ALWAYS call `list_folders` first** to get current folder IDs. Never hardcode folder IDs - they can change.

```
mcp__granola__list_folders()
```

Returns:
- Folder ID
- Folder name
- Document count
- Date range of meetings

### Known Categories (as of Dec 2025)

| Category | Folder Name | Purpose |
|----------|-------------|---------|
| Sales Calls | `Sales - Call 1` | Initial sales conversations |
| Onboarding | `Onboarding - Call 2` | Customer onboarding sessions |
| Customer Calls | `Customer calls` | Ongoing customer conversations |
| VC Calls | `VC Calls` | Investor meetings |
| 1st Interviews | `1st Interview - Edmund` | Candidate screenings |
| Team Meetings | `Team meetings` | Internal discussions |
| Product Feedback | `Cap Product Feedback` | Product feedback sessions |
| Closing Prep | `Closing Candidate Prep` | Candidate closing preparation |
| Vendors | `vendors` | Vendor/partner calls |

### Category Aliases

Map user requests to folder names:

| User Says | Folder Name |
|-----------|-------------|
| "sales", "prospects" | `Sales - Call 1` |
| "onboarding" | `Onboarding - Call 2` |
| "customer", "client" | `Customer calls` |
| "investor", "vc" | `VC Calls` |
| "interviews" | `1st Interview - Edmund` |
| "team", "internal" | `Team meetings` |

### Directory Slug Mapping

For saving files locally:

| Folder Name | Directory Slug |
|-------------|----------------|
| Sales - Call 1 | `sales_call_1` |
| Onboarding - Call 2 | `onboarding_call_2` |
| Customer calls | `customer_calls` |
| VC Calls | `vc_calls` |
| 1st Interview - Edmund | `1st_interview_edmund` |
| Team meetings | `team_meetings` |
| Cap Product Feedback | `cap_product_feedback` |
| Closing Candidate Prep | `closing_candidate_prep` |
| vendors | `vendors` |

---

## Available MCP Tools

### list_folders

List all Granola folders with document counts.

```
mcp__granola__list_folders()
```

**Use when**: Starting any Granola operation, need to discover categories.

### get_folder_meetings

Get meetings from a specific folder with optional date filtering.

```
mcp__granola__get_folder_meetings({
  folder_name: "Sales",      // Partial match supported
  folder_id: "...",          // Or use exact ID
  start_date: "YYYY-MM-DD",  // Optional
  end_date: "YYYY-MM-DD",    // Optional
  limit: 50                  // Default 50
})
```

**Returns**: Meeting list with IDs, URLs, titles, dates, participants (with emails).

### get_meeting_details

Get metadata for a specific meeting.

```
mcp__granola__get_meeting_details({ meeting_id: "..." })
```

**Returns**: Title, date, URL, folder, participants with emails and companies.

### get_meeting_transcript

Get the full transcript of a meeting.

```
mcp__granola__get_meeting_transcript({ meeting_id: "..." })
```

**Returns**: Full transcript text, speakers list.

### get_meeting_documents

Get notes/documents associated with a meeting.

```
mcp__granola__get_meeting_documents({ meeting_id: "..." })
```

**Returns**: Meeting notes, overview, summary.

### search_meetings

Search across all meetings by keyword.

```
mcp__granola__search_meetings({ query: "keyword", limit: 10 })
```

**Use when**: Looking for specific content across all meetings.

### analyze_meeting_patterns

Analyze patterns across meetings.

```
mcp__granola__analyze_meeting_patterns({
  pattern_type: "topics" | "participants" | "frequency",
  date_range: { start_date: "...", end_date: "..." }
})
```

---

## Meeting URLs

Each meeting includes a clickable URL to view it in the Granola web app.

**Format**: `https://granola.ai/note/{meeting_id}`

The URL is returned by:
- `get_folder_meetings` - for each meeting in the list
- `get_meeting_details` - in the meeting details

**Usage**: Include the URL in summaries and reports so users can quickly access the original meeting in Granola.

---

## Company Name Extraction

### Extraction Priority

1. **participant.company** from MCP response (if available)
2. **Email domain** - extract and clean
3. **Meeting title** - parse if format is "Call with [Company]"
4. **Transcript** - search for company mentions

### Cleaning Rules

**NEVER return raw URLs or email domains. NEVER use person's name as company name.**

#### Remove Domain Suffixes

`.com`, `.ai`, `.io`, `.co`, `.org`, `.net`, `.gg`, `.app`, `.dev`, `.xyz`, `.health`, `.chat`, `.tech`, `.cloud`, `.finance`, `.capital`

#### Remove Common Prefixes

| Prefix | Example | Result |
|--------|---------|--------|
| `join` | joinhexagon.com | Hexagon |
| `get` | getdbt.com | dbt |
| `try` | trymaverick.com | Maverick |
| `use` | usepylon.com | Pylon |
| `meet` | meetcleo.com | Cleo |
| `hello` | helloworld.com | World |
| `hi` | himarley.com | Marley |
| `with` | withpersona.com | Persona |
| `go` | gohenry.com | Henry |
| `my` | myfitnesspal.com | FitnessPal |
| `the` | theorg.com | Org |

#### Capitalization

- Title case: `hexagon` → `Hexagon`
- Preserve acronyms: `dbt`, `ai`, `ml`
- Handle camelCase: Keep as-is

### Examples

| Raw Input | Cleaned Output |
|-----------|----------------|
| `tunde@joinhexagon.com` | Hexagon |
| `victoria@paceapp.ai` | Pace App |
| `ben@heater.gg` | Heater |
| `ayoola@astronaut.chat` | Astronaut |
| `salman@astrada.co` | Astrada |

---

## Finding Transcripts

### By Meeting ID

```
mcp__granola__get_meeting_transcript({ meeting_id: "..." })
```

### By Search

```
mcp__granola__search_meetings({ query: "company name or topic" })
// Then get transcript for each result
```

### By Folder + Date

```
mcp__granola__get_folder_meetings({ folder_name: "Sales", start_date: "2025-12-01" })
// Then get transcript for each meeting
```

---

## Meeting Summaries

### Finding Existing Summaries

**From MCP** (Granola's notes):

```
mcp__granola__get_meeting_documents({ meeting_id: "..." })
```

Returns Granola's notes/overview/summary fields.

**Local Summaries** (our processed summaries):

```
/Users/edmund/MyAssistant/meeting_summaries/{category_slug}/{YYYY-MM-DD}/{company-name}.md
```

### Saving New Summaries

#### Directory Structure

```
/Users/edmund/MyAssistant/meeting_summaries/
├── sales_call_1/
│   └── {YYYY-MM-DD}/
│       └── {company-name}.md
├── onboarding_call_2/
│   └── {YYYY-MM-DD}/
│       └── {company-name}.md
├── customer_calls/
├── vc_calls/
├── 1st_interview_edmund/
├── team_meetings/
├── cap_product_feedback/
├── closing_candidate_prep/
└── vendors/
```

#### File Naming Convention

- **Directory**: Use the category slug from the mapping table above
- **Date subdirectory**: `YYYY-MM-DD` format (meeting date)
- **Filename**: `{company-name}.md` in lowercase, hyphenated
  - Clean the company name (remove spaces, special chars)
  - Example: `victoria-pu.md`, `hexagon.md`, `pace-app.md`

#### Creating the Summary File

1. **Create date directory** if it doesn't exist:
   ```bash
   mkdir -p /Users/edmund/MyAssistant/meeting_summaries/{category_slug}/{YYYY-MM-DD}
   ```

2. **Write the summary file** using the appropriate template below

### Summary Templates

#### Sales Call Template

```markdown
# Sales Call Summary

**Category**: Sales - Call 1
**Company**: {cleaned company name}
**Contact**: {participant name} <{email}>
**Date**: {YYYY-MM-DD}
**Meeting ID**: {meeting_id}
**Granola URL**: https://granola.ai/note/{meeting_id}

## Referral Source
{How they found us - VC referral, personal referral, inbound, etc.}

## Role Details
- **Title**: {job title}
- **Salary**: {range}
- **Location**: {location/remote}
- **Experience**: {years}
- **Ideal Profile**: {key qualifications}
- **Hard Requirements**: {must-haves, deal-breakers}

## Discussion Summary
{2-3 paragraph narrative of the call - what was discussed, their pain points, our pitch}

## Key Product Feedback
{Numbered list of product feedback or feature requests mentioned}

## Current Recruiting Setup
{How they currently hire - internal, agencies, platforms}

## Competition
{Who else they're using or considering}

## Next Steps
{Specific action items with dates}

## Onboarding Status
- **Discussed**: Yes/No
- **Scheduled Date**: {date and time if scheduled}

## Deal Temperature
**{HOT/WARM/COLD}** - {1-2 sentence assessment}
```

#### Onboarding Call Template

```markdown
# Onboarding Call Summary

**Category**: Onboarding - Call 2
**Company**: {cleaned company name}
**Contact**: {participant name} <{email}>
**Date**: {YYYY-MM-DD}
**Meeting ID**: {meeting_id}
**Granola URL**: https://granola.ai/note/{meeting_id}

## Account Setup
- **Account Created**: Yes/No
- **Roles Added**: {number and titles}
- **Initial Candidates**: {number sent or reviewed}

## Role Requirements Discussed
{Detailed requirements captured during onboarding}

## Discussion Summary
{Narrative of the onboarding call}

## Action Items
{Specific next steps for both parties}

## Account Status
**{ACTIVE/PENDING/BLOCKED}** - {brief status note}
```

#### Customer Call Template

```markdown
# Customer Call Summary

**Category**: Customer calls
**Company**: {company name}
**Contact**: {participant name} <{email}>
**Date**: {YYYY-MM-DD}
**Meeting ID**: {meeting_id}
**Granola URL**: https://granola.ai/note/{meeting_id}

## Call Purpose
{Why the call was scheduled}

## Discussion Summary
{What was discussed}

## Feedback / Issues
{Any feedback, complaints, or issues raised}

## Action Items
{Next steps}

## Account Health
**{GREEN/YELLOW/RED}** - {assessment}
```

### Workflow: Summarize New Meetings

1. **Fetch meetings** since last summarized:
   ```
   get_folder_meetings({ folder_name: "Sales", start_date: "<last_summarized>" })
   ```

2. **For each meeting**:
   - `get_meeting_details({ meeting_id })` → get participants, company
   - `get_meeting_transcript({ meeting_id })` → get transcript
   - Extract company name (see Company Name Extraction rules)
   - Create summary using appropriate template
   - Save to correct directory

3. **Update timestamp** in `last_summarized.md`

---

## Timestamp Tracking

**File**: `.claude/skills/fetch-granola-notes/last_summarized.md`

Tracks when meetings were last processed per category. Use to determine which meetings are new.

### Format

```markdown
| Category | Last Summarized | Meetings Processed |
|----------|-----------------|-------------------|
| Sales - Call 1 | 2025-12-15 13:25 | 5 |
| Onboarding - Call 2 | 2025-12-15 13:25 | 3 |
```

### Usage

1. Read timestamp for target category
2. Use as `start_date` when fetching meetings
3. After processing, update timestamp

---

## Common Workflows

### List all meetings in a category

1. `list_folders()` → get folder ID
2. `get_folder_meetings({ folder_name: "..." })`

### Get full details for a meeting

1. `get_meeting_details({ meeting_id: "..." })`
2. `get_meeting_transcript({ meeting_id: "..." })`
3. `get_meeting_documents({ meeting_id: "..." })`

### Find new meetings since last run

1. Read `last_summarized.md` for category timestamp
2. `get_folder_meetings({ folder_name: "...", start_date: "<timestamp>" })`

### Search for a specific topic

1. `search_meetings({ query: "topic" })`
2. Get details/transcript for relevant results
