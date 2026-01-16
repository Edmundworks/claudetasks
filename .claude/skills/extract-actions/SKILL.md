---
name: extract-actions
description: Extract scheduled action items from meeting summaries and organize by action date. Also retrieves today's action items for daily planning and removes them after inclusion.
---

# Extract Actions Skill

Two-mode skill for managing scheduled action items:
1. **Extract Mode**: Extract action items from meeting summaries → write to `scheduled_action_items.md`
2. **Retrieve Mode**: Get today's action items for daily planning → delete after inclusion

## Skill Modes

### Mode 1: Extract (used by daily-routine Checkpoint 4.5)
- **When**: After processing Granola meeting summaries
- **Action**: Extract action items from meeting summaries, parse dates, write to `scheduled_action_items.md`
- **See**: "Extraction Workflow" section below

### Mode 2: Retrieve Today's Items (used by Daily Planning)
- **When**: During daily plan generation
- **Action**: Read `scheduled_action_items.md`, return today's items with full context, delete them from file
- **See**: "Retrieve Today's Items Workflow" section below

---

## When to Use This Skill

**Mode 1 (Extract):**
- After running fetch-granola-notes to process new meeting summaries
- When reviewing action items across multiple meetings
- To build a consolidated follow-up schedule

**Mode 2 (Retrieve):**
- During daily planning to get today's scheduled action items
- To include meeting follow-ups in the daily plan

---

## Finding Today's Meeting Summaries

Process summaries **created today** (based on timestamps), not just summaries dated today.

### Step 1: Check Timestamps

Read `/Users/edmund/MyAssistant/.claude/skills/fetch-granola-notes/last_summarized.md` to find when meetings were last summarized per category.

Look for the `Last Summarized` column:
- `Sales - Call 1` → maps to `meeting_summaries/sales_call_1/`
- `Onboarding - Call 2` → maps to `meeting_summaries/onboarding_call_2/`
- `Customer calls` → maps to `meeting_summaries/customer_calls/`

### Step 2: Scan Meeting Summary Directories

Based on timestamps, scan these directories for new files:

```
/Users/edmund/MyAssistant/meeting_summaries/
├── sales_call_1/{YYYY-MM-DD}/*.md
├── onboarding_call_2/{YYYY-MM-DD}/*.md
├── customer_calls/{YYYY-MM-DD}/*.md
├── vc_calls/{YYYY-MM-DD}/*.md
├── team_meetings/{YYYY-MM-DD}/*.md
└── vendors/{YYYY-MM-DD}/*.md
```

### Step 3: Identify New Summaries

Find `.md` files in date directories **on or after** the last summarized timestamp:

1. List date directories in each category (e.g., `ls meeting_summaries/sales_call_1/`)
2. Filter to dates >= last summarized date for that category
3. Read each `.md` file in those date directories

### Relevant Categories

| Category | Directory | Process? |
|----------|-----------|----------|
| Sales - Call 1 | `sales_call_1/` | Yes - primary |
| Onboarding - Call 2 | `onboarding_call_2/` | Yes - primary |
| Customer calls | `customer_calls/` | Yes - primary |
| VC Calls | `vc_calls/` | Yes (if has action items) |
| Team meetings | `team_meetings/` | Yes (if has action items) |
| Vendors | `vendors/` | Yes (if has action items) |

### Example: Finding New Summaries

If `last_summarized.md` shows:
```
| Category | Last Summarized |
|----------|-----------------|
| Sales - Call 1 | 2026-01-14 09:00 |
```

Then scan `meeting_summaries/sales_call_1/` for:
- Any date folder `>= 2026-01-14`
- Read all `.md` files in those folders

---

## Output File

**Path**: `/Users/edmund/MyAssistant/scheduled_action_items.md`

This is a persistent file that accumulates action items. The skill **appends** new items and should NOT overwrite existing content.

---

## Action Item Header Detection

Meeting summaries use various headers for action items. Scan for these patterns (case-insensitive):

| Header Pattern | Priority |
|---------------|----------|
| `## Action Items / Follow-ups` | 1 |
| `## Action Items/Follow-ups` | 1 |
| `## Action Items` | 2 |
| `## Next Steps/Action Items` | 3 |
| `## Next Steps` | 4 |
| `### Action Items` | 5 |
| `### Next Steps` | 5 |

**Extraction Rule**: Capture all numbered or bulleted items under these headers until the next `##` heading or end of file.

---

## Date Parsing Rules (CRITICAL)

### Reference Date
The **meeting date** from the summary metadata serves as the reference point for relative date calculations:
- Extract from `**Meeting Date**:` or `**Date**:` field
- Format: `YYYY-MM-DD`

### Relative Date Patterns

| Pattern | Calculation | Example (if meeting was 2026-01-14, Tuesday) |
|---------|-------------|----------------------------------------------|
| `today` | meeting_date | 2026-01-14 |
| `tonight` | meeting_date | 2026-01-14 |
| `tomorrow` | meeting_date + 1 day | 2026-01-15 |
| `this week` | Friday of meeting week | 2026-01-17 |
| `by end of week` / `by EOW` | Friday of meeting week | 2026-01-17 |
| `next week` | Monday of following week | 2026-01-20 |
| `next Tuesday` | Next occurrence of that day | 2026-01-21 |
| `next [Weekday]` | Next occurrence of that day | Calculate from meeting_date |
| `in X days` | meeting_date + X | Varies |
| `this Friday` | Friday of meeting week | 2026-01-17 |
| `asap` / `immediately` | meeting_date + 1 | 2026-01-15 |
| `H2 2026` / `second half` | 2026-07-01 | Flag as `(approx)` |
| `Q1/Q2/Q3/Q4 YYYY` | First day of quarter | Flag as `(approx)` |
| `summer/fall/spring YYYY` | Approximate start | Flag as `(approx)` |

### No Date Specified
If no date is mentioned in the action item:
- Default to **meeting_date + 3 business days**
- Flag as `(date inferred)`

### Date Priority Order
1. Explicit date in action text (`by Jan 20`, `Friday 5pm`)
2. Contextual date (`tomorrow`, `next week`)
3. Default calculation (meeting_date + 3 business days)

---

## Owner Attribution

### Detection Patterns
Action items often have owner prefixes:

| Pattern | Owner | Type |
|---------|-------|------|
| `**Superposition**:` | Edmund/Team | Internal |
| `**Superposition (Edmund)**:` | Edmund | Internal |
| `**Superposition (Li)**:` | Li | Internal |
| `**Edmund**:` | Edmund | Internal |
| `**[Company Name]**:` | External party | External |
| No prefix | Edmund (default) | Internal |

### Internal vs External Actions
- **Internal** (Superposition/Edmund/Li): Track in main sections by date
- **External** (customer actions): Track in "Awaiting External Action" section

---

## Validation Rules (CRITICAL)

### Required for Actionability
Every action item MUST have:
1. **Specificity**: Clear description of WHAT to do
2. **Contact Details**: Email address if action involves sending email
3. **Context**: Enough detail to execute without re-reading transcript

### Automatic Enhancement
When extracting, **ENHANCE** action items with:
- Contact email from `**Contact**:` field in meeting metadata
- Company name from `**Company**:` field
- Granola URL for reference

### Reject/Flag These Patterns
- `Follow up` (with no specifics) - FLAG for clarification
- `Schedule meeting` (with no attendees) - FLAG for clarification
- `Send email` (with no recipient or topic) - FLAG for clarification
- `Check in` (with no context) - FLAG for clarification

### Good vs Bad Examples

**VAGUE (Reject/Flag):**
```
- Follow up with Jason
- Send email about the role
- Schedule onboarding
- Check in next week
```

**ACTIONABLE (Accept):**
```
- Follow up email to Jason about sales cycle progress and whether they filled their role - send to jason@company.com
- Schedule 5pm meeting tomorrow for Ashby integration with Kevin + Sol at Vimes (kevin@vimes.co)
- Fix Poly's access issue and resend invite to poly@skillcraft.co
- Send testimonials and case studies to ken@baycompute.com before Friday demo
```

---

## Meeting Summary Locations

```
/Users/edmund/MyAssistant/meeting_summaries/
├── sales_call_1/{YYYY-MM-DD}/*.md
├── onboarding_call_2/{YYYY-MM-DD}/*.md
├── customer_calls/{YYYY-MM-DD}/*.md
├── vc_calls/{YYYY-MM-DD}/*.md
├── team_meetings/{YYYY-MM-DD}/*.md
└── vendors/{YYYY-MM-DD}/*.md
```

---

## Extraction Workflow

### Step 1: Identify Target Summaries
Either:
- Process specific meeting summary file (if provided)
- Scan all summaries since `last_extracted.md` timestamp
- Process all summaries in a date range

### Step 2: Extract Meeting Metadata
For each summary, extract:
```
company: from **Company**: field
contact: from **Contact**: field (name + email)
meeting_date: from **Date**: or **Meeting Date**: field
granola_url: from **Granola URL**: field
```

### Step 3: Find and Parse Action Items
1. Locate action items section using header patterns
2. Parse each item:
   - Detect owner prefix
   - Extract action text
   - Parse date (relative → absolute)
   - Enhance with contact details if missing
3. Validate actionability
4. Flag vague items

### Step 4: Merge Into Output File
1. Read existing `scheduled_action_items.md` (if exists)
2. Parse existing entries
3. Add new entries (avoid duplicates by checking source meeting + action text)
4. Re-sort all entries by action date
5. Write updated file with `Last updated` timestamp

---

## Output File Format

**File**: `/Users/edmund/MyAssistant/scheduled_action_items.md`

```markdown
# Scheduled Action Items

Last updated: 2026-01-15 10:30

---

## 2026-01-15 (Today)

### Skillcraft
- [ ] **Edmund**: Fix Poly's access issue and resend invite to poly@skillcraft.co
  - Source: [Skillcraft Customer Call 2026-01-13](https://granola.ai/note/abc123)

- [ ] **Edmund**: Manually curate shortlist - create "Extra Shortlist" column for top candidates
  - Source: [Skillcraft Customer Call 2026-01-13](https://granola.ai/note/abc123)

---

## 2026-01-16 (Thursday)

### Plastic Labs
- [ ] **Superposition**: Turn on agent for Plastic Labs - contact courtland@plasticlabs.ai
  - Source: [Plastic Labs Customer Call 2026-01-14](https://granola.ai/note/def456)

---

## 2026-01-17 (Friday)

### BayCompute
- [ ] **Edmund**: Demo at 12:00 PM Eastern with Vijay and Matt (Head of ML) - focus on RL role
  - Source: [BayCompute Sales Call 2026-01-14](https://granola.ai/note/ghi789)

- [ ] **Edmund**: Send testimonials/case studies to ken@baycompute.com before demo
  - Source: [BayCompute Sales Call 2026-01-14](https://granola.ai/note/ghi789)

---

## 2026-01-20 (Next Week)

### Plastic Labs
- [ ] **Superposition**: Get sales evals created with Aubrey (founding sales at Growth Central)
  - Source: [Plastic Labs Customer Call 2026-01-14](https://granola.ai/note/def456)

---

## Future / Approximate Dates

### Zenline (Q2 2026 - approx)
- [ ] **Edmund**: Reconnect when Europe expansion ready - arber@zenline.ch, gerrit@zenline.ch
  - Source: [Zenline Sales Call 2026-01-02](https://granola.ai/note/jkl012)

---

## Awaiting External Action

### Vimes
- [ ] **Vimes**: Will intro to Nate at Pair
  - Source: [Vimes Customer Call 2026-01-13](https://granola.ai/note/mno345)

### BayCompute
- [ ] **BayCompute (Ken)**: Prepare job description/notes for ML role before Friday demo
  - Source: [BayCompute Sales Call 2026-01-14](https://granola.ai/note/ghi789)

---

## Flagged for Clarification

*Items that need more detail before being actionable*

(none currently)
```

---

## State Tracking

**File**: `.claude/skills/extract-actions/last_extracted.md`

Tracks when action items were last extracted per meeting category.

### Format
```markdown
| Category | Last Extracted | Files Processed |
|----------|----------------|-----------------|
| sales_call_1 | 2026-01-15 10:30 | 5 |
| onboarding_call_2 | 2026-01-15 10:30 | 3 |
| customer_calls | 2026-01-15 10:30 | 4 |
```

### Usage
1. Read timestamp for target category
2. Only process summaries newer than timestamp
3. After processing, update timestamp and count

---

## Integration with Other Skills

### After fetch-granola-notes
Run extract-actions **Mode 1** to capture new action items from freshly summarized meetings.

### With daily-plan (Daily Planning)
Run extract-actions **Mode 2** to get today's action items and include them in the daily plan.

### With crm-update
Action items that involve CRM updates (e.g., "Update Hexagon status to Onboarding") can trigger crm-update skill.

---

## Retrieve Today's Items Workflow (Mode 2)

Used by **Daily Planning** to get action items scheduled for today and include them in the daily plan.

### Step 1: Read the Action Items File

Read `/Users/edmund/MyAssistant/scheduled_action_items.md`

### Step 2: Identify Today's Date Section

Get today's date (YYYY-MM-DD format) and find the matching section header:
- Look for `## YYYY-MM-DD` or `## YYYY-MM-DD (Today)` or `## YYYY-MM-DD (Day Name)`
- Example: `## 2026-01-15 (Today)` or `## 2026-01-15 (Wednesday)`

### Step 3: Extract Today's Action Items

Capture all content under today's date header until the next `---` or `##` section:
- Include company subheaders (`### Company Name`)
- Include all action items with checkboxes, owners, descriptions
- Include source links

**Return format for Daily Planning:**
```markdown
## Action Items from Meetings

### Skillcraft
- [ ] **Edmund**: Fix Poly's access issue and resend invite to poly@skillcraft.co
  - Source: [Skillcraft Customer Call 2026-01-13](https://granola.ai/note/abc123)

### BayCompute
- [ ] **Edmund**: Send testimonials/case studies to ken@baycompute.com before demo
  - Source: [BayCompute Sales Call 2026-01-14](https://granola.ai/note/ghi789)
```

### Step 4: Remove Today's Items from File

After successfully returning items for daily planning:

1. **Read** the full `scheduled_action_items.md` content
2. **Delete** the entire today's date section (from `## YYYY-MM-DD` to the next `---` or `##`)
3. **Update** the `Last updated:` timestamp
4. **Write** the modified content back to the file

**CRITICAL**: Only delete after items are successfully included in the daily plan. Do NOT delete if daily planning fails.

### Step 5: Verify Deletion

Confirm the items were removed:
- Today's date section should no longer exist in `scheduled_action_items.md`
- File should still have valid structure (other date sections intact)

### Example: Before and After

**Before** (`scheduled_action_items.md`):
```markdown
# Scheduled Action Items

Last updated: 2026-01-15 08:00

---

## 2026-01-15 (Today)

### Skillcraft
- [ ] **Edmund**: Fix Poly's access issue...

---

## 2026-01-16 (Thursday)

### Plastic Labs
- [ ] **Superposition**: Turn on agent...
```

**After** (items moved to daily plan, deleted from file):
```markdown
# Scheduled Action Items

Last updated: 2026-01-15 10:30

---

## 2026-01-16 (Thursday)

### Plastic Labs
- [ ] **Superposition**: Turn on agent...
```

### Edge Cases

| Scenario | Action |
|----------|--------|
| No items for today | Return empty, no deletion needed |
| File doesn't exist | Return empty, nothing to delete |
| Today's section is empty | Delete the empty section header |
| Items already marked complete `[x]` | Still include and delete (user completed early) |

---

## Maintenance

### Marking Items Complete
User manually checks off completed items: `- [x]`

### Weekly Cleanup
- Archive or delete completed items (`[x]`)
- Review "Future / Approximate Dates" for items becoming current
- Check "Awaiting External Action" for items to follow up on
- Move items with passed dates to an "Overdue" section if needed

### Duplicate Prevention
Before adding an action item, check if it already exists by matching:
- Source meeting (Granola URL)
- Action text (fuzzy match)
