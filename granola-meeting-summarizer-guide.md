# Granola Meeting Summarizer - Replication Guide

A complete guide for setting up automated meeting transcript summarization using Claude Code, the Granola MCP, and a skill/agent architecture.

---

## What This Does

This system automatically:
1. Connects to Granola.ai's local meeting cache via MCP
2. Fetches new meetings by category (Sales, Onboarding, Customer calls, etc.)
3. Reads full transcripts and extracts key information
4. Generates structured markdown summaries tailored to meeting type
5. Saves summaries to organized directories
6. Tracks timestamps to only process new meetings

---

## Prerequisites

### 1. Granola.ai Desktop App
- Install Granola from [granola.ai](https://granola.ai)
- Granola must be running and recording meetings
- Cache file location: `~/Library/Application Support/Granola/cache-v3.json`

### 2. Granola MCP Server
The MCP server reads from Granola's local cache. You can find/clone a Granola MCP implementation or build your own.

**Claude Desktop Config** (`~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "granola": {
      "command": "uv",
      "args": ["--directory", "/path/to/granola-mcp", "run", "granola-mcp-server"],
      "env": {}
    }
  }
}
```

### 3. Claude Code Directory Structure
Create this folder structure in your Claude Code project:
```
your-project/
├── .claude/
│   ├── skills/
│   │   └── fetch-granola-notes/
│   │       ├── SKILL.md
│   │       └── last_summarized.md
│   └── agents/
│       └── granola-note-reader.md
└── meeting_summaries/
    ├── sales_call_1/
    ├── onboarding_call_2/
    ├── customer_calls/
    └── ... (other categories)
```

---

## File 1: The Skill (SKILL.md)

**Location**: `.claude/skills/fetch-granola-notes/SKILL.md`

This skill defines all the rules for working with Granola data - folder names, company extraction, templates, etc.

```markdown
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
| Team meetings | `team_meetings` |

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

---

## Meeting URLs

Each meeting includes a clickable URL: `https://granola.ai/note/{meeting_id}`

Include in summaries so users can access the original in Granola.

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

`.com`, `.ai`, `.io`, `.co`, `.org`, `.net`, `.gg`, `.app`, `.dev`, `.xyz`, `.health`, `.chat`, `.tech`, `.cloud`

#### Remove Common Prefixes

| Prefix | Example | Result |
|--------|---------|--------|
| `join` | joinhexagon.com | Hexagon |
| `get` | getdbt.com | dbt |
| `try` | trymaverick.com | Maverick |
| `use` | usepylon.com | Pylon |
| `meet` | meetcleo.com | Cleo |
| `hello` | helloworld.com | World |
| `with` | withpersona.com | Persona |
| `go` | gohenry.com | Henry |
| `my` | myfitnesspal.com | FitnessPal |

#### Capitalization

- Title case: `hexagon` -> `Hexagon`
- Preserve acronyms: `dbt`, `ai`, `ml`
- Handle camelCase: Keep as-is

### Examples

| Raw Input | Cleaned Output |
|-----------|----------------|
| `tunde@joinhexagon.com` | Hexagon |
| `victoria@paceapp.ai` | Pace App |
| `ben@heater.gg` | Heater |
| `salman@astrada.co` | Astrada |

---

## Meeting Summaries

### Directory Structure

```
/meeting_summaries/
├── sales_call_1/
│   └── {YYYY-MM-DD}/
│       └── {company-name}.md
├── onboarding_call_2/
│   └── {YYYY-MM-DD}/
│       └── {company-name}.md
├── customer_calls/
├── vc_calls/
└── team_meetings/
```

### File Naming Convention

- **Directory**: Use the category slug from the mapping table
- **Date subdirectory**: `YYYY-MM-DD` format (meeting date)
- **Filename**: `{company-name}.md` in lowercase, hyphenated

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
{2-3 paragraph narrative of the call}

## Key Product Feedback
{Numbered list of product feedback or feature requests}

## Current Recruiting Setup
{How they currently hire}

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

---

## Timestamp Tracking

**File**: `.claude/skills/fetch-granola-notes/last_summarized.md`

Tracks when meetings were last processed per category.

### Format

```markdown
# Granola Meeting Summary Timestamps

Last time meetings were fetched and summarized by category.

| Category | Last Summarized | Meetings Processed |
|----------|-----------------|-------------------|
| Sales - Call 1 | 2025-12-15 13:25 | 5 |
| Onboarding - Call 2 | 2025-12-15 13:25 | 3 |
| Customer calls | Never | 0 |
```

### Usage

1. Read timestamp for target category
2. Use as `start_date` when fetching meetings
3. After processing, update timestamp

---

## Common Workflows

### List all meetings in a category

1. `list_folders()` -> get folder ID
2. `get_folder_meetings({ folder_name: "..." })`

### Get full details for a meeting

1. `get_meeting_details({ meeting_id: "..." })`
2. `get_meeting_transcript({ meeting_id: "..." })`
3. `get_meeting_documents({ meeting_id: "..." })`

### Find new meetings since last run

1. Read `last_summarized.md` for category timestamp
2. `get_folder_meetings({ folder_name: "...", start_date: "<timestamp>" })`
```

---

## File 2: The Agent (granola-note-reader.md)

**Location**: `.claude/agents/granola-note-reader.md`

This agent is spawned to process individual meetings.

```markdown
---
name: granola-note-reader
description: Use this agent to read and summarize a specific Granola meeting transcript given a meeting ID. Produces structured summaries tailored to the meeting type (currently supports Sales Calls). Use when you need to extract key information from a specific meeting after finding its ID via fetch-granola-notes or search.

<example>
Context: User has found a meeting ID from fetch-granola-notes and wants details.

user: "Summarize the sales call with Acme Corp"

assistant: "I'll use the granola-note-reader agent to read and summarize that meeting."

<commentary>
The user wants a structured summary of a specific meeting. Use granola-note-reader to fetch the transcript and produce a tailored summary based on meeting type.
</commentary>
</example>
model: sonnet
---

You are a meeting transcript analyst for Granola meetings.

## Required Reading

Before processing, read the `fetch-granola-notes` skill at `.claude/skills/fetch-granola-notes/SKILL.md`. Follow all rules defined there.

## Input

A **meeting ID** (string).

## Task

1. Fetch meeting details and transcript using the Granola MCP
2. Extract company name following skill rules
3. Generate structured summary based on meeting category
4. Save to file following skill's directory structure
5. Return: file path, company name, contact, meeting ID

**Note**: Do NOT update timestamp tracking files. The parent handles that.
```

---

## File 3: Timestamp Tracker (last_summarized.md)

**Location**: `.claude/skills/fetch-granola-notes/last_summarized.md`

Initialize with your categories:

```markdown
# Granola Meeting Summary Timestamps

Last time meetings were fetched and summarized by category.

| Category | Last Summarized | Meetings Processed |
|----------|-----------------|-------------------|
| Sales - Call 1 | Never | 0 |
| Onboarding - Call 2 | Never | 0 |
| Customer calls | Never | 0 |
| VC Calls | Never | 0 |
| Team meetings | Never | 0 |
```

---

## How to Use

### Manual: Summarize a specific meeting

```
User: "Summarize my sales call with Acme Corp"

Claude:
1. Reads the skill file
2. Searches for the meeting: mcp__granola__search_meetings({ query: "Acme Corp" })
3. Gets transcript: mcp__granola__get_meeting_transcript({ meeting_id: "..." })
4. Generates summary using the sales call template
5. Saves to: meeting_summaries/sales_call_1/YYYY-MM-DD/acme-corp.md
```

### Automated: Process new meetings since last run

```
User: "Fetch and summarize new sales calls"

Claude:
1. Reads last_summarized.md -> Sales - Call 1 last processed 2025-12-15
2. Fetches: mcp__granola__get_folder_meetings({ folder_name: "Sales", start_date: "2025-12-15" })
3. For each meeting, spawns granola-note-reader agent
4. Updates last_summarized.md with new timestamp
```

### Background Processing with Agents

For multiple meetings, spawn agents in parallel:

```javascript
// In parent Claude
Task({
  subagent_type: "granola-note-reader",
  prompt: "Summarize meeting ID: abc-123-def for Sales - Call 1 category",
  run_in_background: true
})

Task({
  subagent_type: "granola-note-reader",
  prompt: "Summarize meeting ID: ghi-456-jkl for Sales - Call 1 category",
  run_in_background: true
})

// Later, collect results
TaskOutput({ task_id: "...", block: true })
```

---

## Customization

### Adding New Meeting Categories

1. Add to the skill's category tables (Folder Name, Alias, Directory Slug)
2. Create a new summary template for the category
3. Add row to `last_summarized.md`
4. Create the directory: `meeting_summaries/{new_category_slug}/`

### Modifying Templates

Edit the templates in the skill file to match your needs:
- Add/remove fields
- Change formatting
- Add new sections

### Integration with CRM/Task Systems

After generating summaries, you can:
- Update a CRM (Notion, Salesforce, etc.)
- Create follow-up tasks
- Send notifications
- Update pipeline tracking

---

## Troubleshooting

### "Cache file not found"
- Ensure Granola.ai is installed and running
- Check cache exists: `ls -la "~/Library/Application Support/Granola/cache-v3.json"`

### "No meetings found"
- Check folder names match exactly (use `list_folders()` to verify)
- Ensure date range includes meetings that exist
- Verify Granola has recorded meetings in that category

### "Company name not extracted"
- Check participant email domains
- Review meeting title format
- Fallback: use participant name or "Unknown Company"

### "Agent not creating files"
- Verify directory exists
- Check file permissions
- Ensure agent has Write tool access

---

## Summary

This system provides:
- **Skill file**: Rules, templates, and MCP tool reference
- **Agent file**: Individual meeting processor
- **Timestamp tracker**: Prevents duplicate processing
- **Directory structure**: Organized storage by category/date

The architecture separates concerns:
- Parent orchestrator: Finds new meetings, tracks progress, updates timestamps
- Child agents: Process individual meetings in parallel
- Skill reference: Single source of truth for rules and templates
