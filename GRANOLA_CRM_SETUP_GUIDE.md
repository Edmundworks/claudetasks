

# Granola → Meeting Summaries → Notion CRM

A complete guide to automating meeting transcript summarization with Claude Code, syncing to a Notion CRM.

**Time to set up**: ~15 minutes
**Prerequisites**: Granola desktop app, Notion account, Claude Code CLI

---

## Quick Start

Paste this file into an empty directory, then run Claude Code and say:

```
Help me set up my Granola → CRM integration
```

Claude will create all necessary files and walk you through configuration.

---

## What This Does

1. **Fetches meetings** from Granola by category (Sales, Follow-ups, Customer calls, etc.)
2. **Summarizes transcripts** using AI with structured templates
3. **Saves summaries** as markdown files organized by date/company
4. **Updates your Notion CRM** with new leads, deal status changes, and contextual notes

---

## Architecture Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Granola MCP    │────▶│  Claude Code     │────▶│  Notion MCP     │
│  (meetings)     │     │  (skills/agents) │     │  (CRM updates)  │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌──────────────────┐
                        │  Local Files     │
                        │  (summaries)     │
                        └──────────────────┘
```

**Components:**
- **Skills** - Reference documents Claude reads to understand workflows
- **Agents** - Specialized sub-agents for specific tasks (summarizing meetings)
- **MCPs** - External integrations (Granola for meetings, Notion for CRM)

---

## Prerequisites

### 1. Granola Desktop App + MCP Server

Install [Granola](https://granola.ai) desktop app, then set up the MCP server.

**Install the Granola MCP Server:**

```bash
# Clone to home directory (not Documents - causes permission issues)
cd ~
git clone https://github.com/proofgeist/granola-ai-mcp-server
cd granola-ai-mcp-server

# Install dependencies (requires Python 3.12+ and uv)
uv sync

# Test it works
uv run python test_server.py
```

> **Need uv?** Install with: `curl -LsSf https://astral.sh/uv/install.sh | sh`

**Add to your Claude Desktop config** (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "granola": {
      "command": "/Users/YOUR_USERNAME/granola-ai-mcp-server/.venv/bin/granola-mcp-server",
      "args": [],
      "env": {}
    }
  }
}
```

> **Important:** Replace `YOUR_USERNAME` with your actual macOS username.

See the [Granola MCP Server repo](https://github.com/proofgeist/granola-ai-mcp-server) for troubleshooting.

### 2. Notion Integration + MCP Server

**Get your Notion API token:**

1. Go to https://www.notion.so/my-integrations
2. Click **"+ New integration"**
3. Name it (e.g., "CRM Sync" - can't include the word "notion")
4. Select your workspace
5. Click **"Submit"**
6. Copy the **"Internal Integration Secret"** (starts with `ntn_`)

**Share your CRM database with the integration:**

1. Open your CRM database in Notion
2. Click **"..."** in the top right → **"Connections"**
3. Find and add your integration

**Add to your Claude Desktop config:**

```json
{
  "mcpServers": {
    "notion-mcp": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "OPENAPI_MCP_HEADERS": "{\"Authorization\": \"Bearer ntn_YOUR_TOKEN_HERE\", \"Notion-Version\": \"2022-06-28\"}"
      }
    }
  }
}
```

> **Note:** The server name `notion-mcp` is used in tool calls throughout this guide (e.g., `mcp__notion-mcp__API-post-search`). If you use a different name, adjust accordingly.

> **Important:** Replace `ntn_YOUR_TOKEN_HERE` with your actual token.

See the [Official Notion MCP Server](https://github.com/makenotion/notion-mcp-server) and [Notion MCP Docs](https://developers.notion.com/docs/mcp) for more details.

**Restart Claude Desktop** after updating the config:
```bash
osascript -e 'quit app "Claude"' && open -a "Claude"
```

### 3. Environment File

During setup, Claude will create a `.env` file and prompt you to add your Notion token.

> **Why a .env file?** The Notion MCP has a bug with page creation. We use MCP for queries/updates and direct API calls (curl) for creating new pages. The `.env` file stores your token for curl commands.

---

## Directory Structure

Create this structure in your project:

```
your-project/
├── .env                                    # Notion token
├── .claude/
│   ├── skills/
│   │   ├── fetch-granola-notes/
│   │   │   ├── SKILL.md                   # Granola reference manual
│   │   │   └── last_summarized.md         # Timestamp tracking
│   │   └── crm-update/
│   │       ├── SKILL.md                   # CRM operations manual
│   │       └── crm_schema.md              # Your CRM schema
│   └── agents/
│       └── granola-note-reader.md         # Meeting summarizer agent
└── meeting_summaries/                      # Output directory
    ├── sales_call_1/
    ├── follow_up_calls/
    ├── customer_calls/
    └── [other categories]/
```

---

## Step 1: Create the Granola Skill

Create `.claude/skills/fetch-granola-notes/SKILL.md`:

```markdown
---
name: fetch-granola-notes
description: Reference manual for working with Granola meeting data via MCP. Covers meeting categories, company name extraction, and summary templates.
---

# Granola MCP Manual

## Default Behavior

If no date range is specified, fetch meetings since the last fetch. Check `last_summarized.md` for the timestamp.

---

## Meeting Categories (Folders)

### Discovering Categories

**ALWAYS call `list_folders` first** - folder IDs can change.

```
mcp__granola__list_folders()
```

### Category to Directory Mapping

| Folder Name | Directory Slug |
|-------------|----------------|
| Sales - Call 1 | `sales_call_1` |
| Follow-up Calls | `follow_up_calls` |
| Customer calls | `customer_calls` |
| VC Calls | `vc_calls` |

> Customize this table to match your Granola folders.

---

## Available MCP Tools

### list_folders
List all Granola folders with document counts.
```
mcp__granola__list_folders()
```

### get_folder_meetings
Get meetings from a folder with optional date filtering.
```
mcp__granola__get_folder_meetings({
  folder_name: "Sales",
  start_date: "YYYY-MM-DD",
  end_date: "YYYY-MM-DD",
  limit: 50
})
```

### get_meeting_details
Get metadata for a specific meeting.
```
mcp__granola__get_meeting_details({ meeting_id: "..." })
```

### get_meeting_transcript
Get the full transcript.
```
mcp__granola__get_meeting_transcript({ meeting_id: "..." })
```

### get_meeting_documents
Get Granola's notes/summary.
```
mcp__granola__get_meeting_documents({ meeting_id: "..." })
```

### search_meetings
Search across all meetings.
```
mcp__granola__search_meetings({ query: "keyword", limit: 10 })
```

---

## Company Name Extraction

### Priority Order
1. `participant.company` from MCP response
2. Email domain (cleaned)
3. Meeting title
4. Transcript mentions

### Cleaning Rules

**Remove domain suffixes:**
`.com`, `.ai`, `.io`, `.co`, `.org`, `.net`, `.app`, `.dev`, `.xyz`

**Remove common prefixes:**

| Prefix | Example | Result |
|--------|---------|--------|
| `join` | joinhexagon.com | Hexagon |
| `get` | getdbt.com | dbt |
| `try` | trymaverick.com | Maverick |
| `use` | usepylon.com | Pylon |
| `with` | withpersona.com | Persona |

**Examples:**
- `alex@joinacme.com` → Acme
- `sam@rocketapp.ai` → Rocket App

---

## Summary Templates

### Sales Call Template

```markdown
# Sales Call Summary

**Category**: Sales - Call 1
**Company**: {company name}
**Contact**: {name} <{email}>
**Date**: {YYYY-MM-DD}
**Meeting ID**: {meeting_id}
**Granola URL**: https://notes.granola.ai/d/{meeting_id}

## Referral Source
{How they found you}

## Opportunity Details
- **Product/Service Interest**: {what they're interested in}
- **Budget**: {range or TBD}
- **Timeline**: {when they need it}
- **Decision Maker**: {yes/no, who else is involved}

## Discussion Summary
{2-3 paragraph narrative}

## Next Steps
{Action items with dates}

## Deal Temperature
**{HOT/WARM/COLD}** - {assessment}
```

### Customer Call Template

```markdown
# Customer Call Summary

**Category**: Customer calls
**Company**: {company name}
**Contact**: {name} <{email}>
**Date**: {YYYY-MM-DD}
**Meeting ID**: {meeting_id}
**Granola URL**: https://notes.granola.ai/d/{meeting_id}

## Call Purpose
{Why the call was scheduled}

## Discussion Summary
{What was discussed}

## Action Items
{Next steps}

## Account Health
**{GREEN/YELLOW/RED}** - {assessment}
```

---

## Saving Summaries

### Directory Structure
```
meeting_summaries/{category_slug}/{YYYY-MM-DD}/{company-name}.md
```

### File Naming
- Lowercase, hyphenated company name
- Example: `meeting_summaries/sales_call_1/2025-12-15/hexagon.md`

---

## Timestamp Tracking

**File**: `last_summarized.md` (in this skill's directory)

### Format
```markdown
| Category | Last Summarized | Meetings Processed |
|----------|-----------------|-------------------|
| Sales - Call 1 | 2025-12-15 13:25 | 5 |
| Follow-up Calls | 2025-12-15 13:25 | 3 |
```

### Usage
1. Read timestamp for target category
2. Use as `start_date` when fetching
3. Update timestamp after processing
```

---

## Step 2: Create the Timestamp Tracker

Create `.claude/skills/fetch-granola-notes/last_summarized.md`:

```markdown
# Granola Meeting Summary Timestamps

Last time meetings were fetched and summarized by category.

| Category | Last Summarized | Meetings Processed |
|----------|-----------------|-------------------|
| Sales - Call 1 | Never | 0 |
| Follow-up Calls | Never | 0 |
| Customer calls | Never | 0 |
| VC Calls | Never | 0 |
```

---

## Step 3: Create the Meeting Reader Agent

Create `.claude/agents/granola-note-reader.md`:

```markdown
---
name: granola-note-reader
description: Summarize a specific Granola meeting transcript. Produces structured summaries tailored to meeting type.
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
4. If there are action items with specific dates, include them prominently
5. Save to file following skill's directory structure
6. Return: file path, company name, contact, meeting ID

**Note**: Do NOT update timestamp tracking files. The parent handles that.
```

---

## Step 4: Create the CRM Schema

Create `.claude/skills/crm-update/crm_schema.md`:

```markdown
# CRM Schema

**Database ID**: `SETUP_REQUIRED` <!-- Run: "Help me set up my Granola → CRM integration" -->

<!--
This file is AUTO-GENERATED during setup.
Claude will read your actual Notion CRM database and populate the schema below.
-->

## Fields

<!-- Fields will be populated automatically from your Notion database -->

## Status Options

<!-- Status options will be populated automatically -->

## Select Options

<!-- Select field options will be populated automatically -->
```

> **Note**: This file is auto-generated. During setup, Claude reads your actual Notion CRM database schema and populates this file with your real fields, status options, and select values.

---

## Step 5: Create the CRM Update Skill

Create `.claude/skills/crm-update/SKILL.md`:

```markdown
---
name: crm-update
description: Update CRM in Notion based on meeting summaries. Cross-references with existing entries and proposes updates.
---

# CRM Update Skill

Manage your Notion CRM - create leads, update statuses, and track pipeline.

## Database Reference

See `crm_schema.md` for field definitions.

**Database ID**: `SETUP_REQUIRED` <!-- Run: "Help me set up my Granola → CRM integration" -->

---

## API Approach

**Use MCP for**: Searching, updating pages, appending content
**Use curl for**: Creating new pages (MCP has a bug with `parent` parameter)

### Environment Setup
```bash
export $(grep NOTION_TOKEN .env | xargs)
```

---

## Workflow: Update CRM from Meeting Summaries

### Step 1: Check Timestamps

Read `.claude/skills/fetch-granola-notes/last_summarized.md` for when meetings were last processed.

### Step 2: Find New Summaries

Scan `meeting_summaries/` for files newer than the timestamp:
```
meeting_summaries/
├── sales_call_1/{YYYY-MM-DD}/{company}.md
└── follow_up_calls/{YYYY-MM-DD}/{company}.md
```

### Step 3: Extract CRM Data

From each summary, extract:
- Company name
- Contact name and email
- Meeting date
- Referral source
- Deal temperature

### Step 4: Cross-Reference

Search for existing CRM entries:
```javascript
mcp__notion-mcp__API-post-search({
  query: "<company-name>",
  filter: { property: "object", value: "page" }
})
```

**Actions:**
- Not found → Create new entry (curl)
- Found → Update status to next pipeline stage based on meeting type (MCP)
- Already up-to-date → Just add meeting notes

### Step 5: Create New Entries (curl)

```bash
# IDs and status values come from your crm_schema.md
export $(grep NOTION_TOKEN .env | xargs) && \
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer ${NOTION_TOKEN}" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  --data-raw '{
    "parent": {"database_id": "<your-crm-database-id>"},
    "properties": {
      "Name": {"title": [{"text": {"content": "Company Name"}}]},
      "Status": {"status": {"name": "<status-from-your-schema>"}},
      "Owner": {"people": [{"id": "<your-notion-user-id>"}]}
    }
  }'
```

### Step 6: Update Existing Entries (MCP)

```javascript
mcp__notion-mcp__API-patch-page({
  page_id: "<page-id>",
  properties: {
    "Status": { status: { name: "<next-status-from-your-schema>" } }
  }
})
```

### Step 7: Add Meeting Notes to Page

```javascript
mcp__notion-mcp__API-patch-block-children({
  block_id: "<page-id>",
  children: [
    {
      type: "paragraph",
      paragraph: {
        rich_text: [
          { type: "text", text: { content: "📅 2025-12-11 - Meeting Notes\n\n<summary from meeting>" } }
        ]
      }
    }
  ]
})
```

---

## Source Inference

| Pattern in Summary | Source Type | Source Value |
|--------------------|-------------|--------------|
| "referred by [Name] at [VC]" | `VC` | `VC - [Name] - [Fund]` |
| "referred by [Name] from [Company]" | `Referral` | `Referral - [Name] - [Company]` |
| "inbound inquiry" | `Inbound` | - |
| Unknown | `Other` | - |

---

## Best Practices

1. Always check for existing entries before creating
2. Update status based on meeting progression
3. Use curl for page creation (MCP bug)
4. Use MCP for updates and queries
5. Include contextual notes with each status change
```

---

## Step 6: Interactive Setup (Run Once)

After pasting this guide into your project directory, just ask:

```
Help me set up my Granola → CRM integration
```

Claude will automatically:

1. **Create all directories and files** from the templates in this guide
2. **Create `.env`** with placeholder and instructions for your Notion token
3. **Wait for you to add your token**, then verify it works
4. **Ask for your CRM URL** and extract the database ID
5. **Read your CRM schema** directly from Notion
6. **Generate `crm_schema.md`** based on YOUR actual database fields
7. **Ask which user** should be the default CRM owner
8. **Test the connection** to both Granola and Notion

### What You'll Need Ready

- Your **Notion API token** (Claude will show you where to get it)
- Your **CRM database URL** (just copy the link from Notion)

### URL Format Reference

Claude can extract IDs from these Notion URL formats:
```
https://www.notion.so/myworkspace/abc123def456...?v=...
https://notion.so/abc123def456...?v=...
https://www.notion.so/abc123def456...
```

The 32-character hex string is the database ID. Claude converts it to UUID format automatically:
`abc123def456...` → `abc123de-f456-...`

---

## Usage

### Summarize New Meetings

Ask Claude:
```
Summarize my sales calls from the last week
```

Claude will:
1. Read the `fetch-granola-notes` skill
2. Check `last_summarized.md` for the last run
3. Fetch new meetings from Granola
4. Use the `granola-note-reader` agent for each
5. Save summaries to `meeting_summaries/`
6. Update the timestamp

### Update CRM

Ask Claude:
```
Update the CRM with the latest meeting summaries
```

Claude will:
1. Read the `crm-update` skill
2. Find new summaries since last CRM update
3. Cross-reference with existing CRM entries
4. Create or update entries as needed
5. Add contextual notes to each page

### One Command

Ask Claude:
```
Process yesterday's sales calls and update the CRM
```

---

## Customization

### Add New Meeting Categories

1. Create the Granola folder in the Granola app
2. Add the mapping to `fetch-granola-notes/SKILL.md`:
   - Add to the Category table
   - Add the directory slug
3. Create a summary template for the category
4. Add to `last_summarized.md`

### Customize Summary Templates

Edit the templates in `fetch-granola-notes/SKILL.md` to match your needs. Add or remove sections as relevant to your business.

### Customize CRM Schema

Update `crm_schema.md` to match your Notion database structure. Add any custom fields your CRM uses.

---

## Troubleshooting

### "MCP not found" errors

Ensure your Claude Desktop config has the MCP servers configured and restart Claude Desktop.

### "parent should be an object" error

Use curl for page creation instead of MCP:
```bash
curl -X POST "https://api.notion.com/v1/pages" ...
```

### Meetings not showing up

1. Check Granola desktop app is running
2. Run `mcp__granola__list_folders()` to verify connection
3. Check the folder names match your skill configuration

### CRM updates failing

1. Verify your database is shared with the Notion integration
2. Check the database ID format (should have dashes)
3. Verify field names match exactly (case-sensitive)

---

## Full Example Session

```
You: Process my sales calls from the last 3 days and update the CRM

Claude: I'll process your recent sales calls. Let me:

1. Check the last summarized timestamp...
   → Last processed: 2025-12-12

2. Fetch meetings since then...
   → Found 3 new sales calls: Acme Corp, Beta Inc, Gamma Ltd

3. Summarizing each meeting...
   → Saved: meeting_summaries/sales_call_1/2025-12-15/acme-corp.md
   → Saved: meeting_summaries/sales_call_1/2025-12-14/beta-inc.md
   → Saved: meeting_summaries/sales_call_1/2025-12-13/gamma-ltd.md

4. Updating CRM...
   → Acme Corp: Created new entry
   → Beta Inc: Updated status, added meeting notes
   → Gamma Ltd: Added meeting notes

5. Updated timestamp to 2025-12-15 14:30

Done! 3 meetings processed, 1 new CRM entry, 2 updated.
```

---

## Setup Instructions for Claude

When a user asks to set up the integration, follow this flow:

### 1. Create Directory Structure
Create all necessary directories and files:

```bash
mkdir -p .claude/skills/fetch-granola-notes
mkdir -p .claude/skills/crm-update
mkdir -p .claude/agents
mkdir -p meeting_summaries
```

Then create the skill and agent files from the templates in this guide.

### 2. Create .env File
Create `.env` with a placeholder:

```
# Notion API Token
# Get yours at: https://www.notion.so/my-integrations
# 1. Create a new integration
# 2. Copy the "Internal Integration Secret"
# 3. Paste it below (replace the placeholder)
NOTION_TOKEN=paste-your-token-here
```

Also create `.gitignore` to protect the token:
```
.env
```

Then tell the user:
```
I've created a .env file. Please:

1. Open .env in your editor
2. Replace "paste-your-token-here" with your Notion token

To get your token:
→ Go to https://www.notion.so/my-integrations
→ Click "+ New integration" (or use existing)
→ Copy the "Internal Integration Secret"

Let me know when you've added your token!
```

**Wait for user confirmation before proceeding.**

### 4. Get CRM Database URL
Ask the user:
```
Please paste the URL of your Notion CRM database.

To get this:
1. Open your CRM database in Notion
2. Click the "..." menu in the top right
3. Click "Copy link"
4. Paste it here
```

**Extract the ID from the URL:**
- URL: `https://www.notion.so/workspace/a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4?v=...`
- Raw ID: `a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4` (32 hex characters)
- Formatted: `a1b2c3d4-e5f6-a1b2-c3d4-e5f6a1b2c3d4` (add dashes at positions 8, 12, 16, 20)

### 5. Read the CRM Schema from Notion
Fetch the database schema:
```
mcp__notion-mcp__API-retrieve-a-data-source({ data_source_id: "<database-id>" })
```

**Parse the response and extract:**
- All property names and types
- Status field options (groups and values)
- Select/multi-select options
- People fields
- Date fields
- Number fields

### 6. Generate the Schema File
Write the schema to `.claude/skills/crm-update/crm_schema.md`:

```markdown
# CRM Schema

**Database ID**: `<extracted-database-id>`

## Fields

| Field | Type | Description |
|-------|------|-------------|
| **Name** | title | Company/deal name |
| **Status** | status | Pipeline stage |
| ... (all fields from database) ...

## Status Options

**Group 1:**
- `Option 1` - description
- `Option 2` - description
... (all status options from database) ...

## Select Options

### Field Name
- `Option 1`
- `Option 2`
... (all select options) ...
```

### 7. Get User ID
Query Notion for users:
```
mcp__notion-mcp__API-get-users()
```

Present the list and ask:
```
I found these users in your Notion workspace:
1. Alice Smith (alice@company.com)
2. Bob Jones (bob@company.com)

Which one should be the default CRM owner? (Enter the number)
```

### 8. Update Skill Files
Use the Edit tool to:
- Update database ID in `.claude/skills/crm-update/crm_schema.md`
- Update database ID in `.claude/skills/crm-update/SKILL.md`
- Store the default owner user ID

### 9. Verify Setup
- Test the Notion connection by searching for an entry
- Test the Granola connection by listing folders
- Report success or troubleshoot issues

### 10. Offer Next Steps
```
Setup complete! Would you like me to:
1. List your Granola meeting folders
2. Check your CRM for existing entries
3. Process a recent meeting as a test
```

---

## Related Resources

- [Granola](https://granola.ai) - Meeting transcription app
- [Granola MCP Server](https://github.com/proofgeist/granola-ai-mcp-server) - MCP server for Granola
- [Notion MCP Server](https://github.com/makenotion/notion-mcp-server) - Official Notion MCP server
- [Notion MCP Docs](https://developers.notion.com/docs/mcp) - Notion MCP documentation
- [Notion API Docs](https://developers.notion.com) - Full Notion API reference
- [Claude Code](https://claude.ai/code) - Claude CLI
- [MCP Documentation](https://modelcontextprotocol.io) - Model Context Protocol docs
