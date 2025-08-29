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

### 3. Daily Planning
- Use Agent: `daily-planning`
- Pulls calendar events from both calendars
- Runs task analyzers for work and personal tasks
- Integrates email insights
- Creates comprehensive daily schedule
- Output: `daily_schedule_YYYY-MM-DD.md`

### 4. Sprint Information Update
- Query current active sprint from Notion
- Check if CLAUDE.md sprint information is current
- If today is Tuesdat, execute standup notes using `sprint-planning-agent`
- Update CLAUDE.md if outdated with:
  - Sprint name and ID
  - Sprint date range
  - Sprint goal

### 5. Standup Notes Generation (Workdays Only)
- If today is Monday, Wednesday, Thursday, Friday, execute standup notes using `daily-standup-notes-agent`
- Uses daily schedule and previous day's completions as context
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
2. **Daily Planning** → Reads email summary, produces schedule file
3. **Sprint Update** → Checks/updates CLAUDE.md
4. **Standup Notes** → Reads schedule file, produces standup notes

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

## Example Execution

When you run this command, I will:

1. First, run **`email-preprocessor`** agent then **`daily-email-triage-agent`** agent to process your inbox and extract newsletter content
2. Then, run **`daily-planning-agent`** agent to generate your daily schedule incorporating urgent emails and tasks
3. Update sprint information by using **`sprint-planning-agent`** if it's Tuesday
4. Finally, run **`daily-standup-notes-agent`** if it's a Monday, Wednesday, Thursday and Friday