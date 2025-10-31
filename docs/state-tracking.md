# Assistant State Tracking System

## Overview

The assistant now tracks when agents were last run to enable retroactive processing when multiple days are skipped. This prevents the brittleness of assuming the assistant runs every single day.

## How It Works

### State File

A `.assistant_state.json` file in the project root tracks the last successful run date for each agent:

```json
{
  "email_preprocessor": {
    "last_run": "2025-10-31",
    "last_successful_run": "2025-10-31"
  },
  "sales_pipeline_tracker": {
    "last_run": "2025-10-30",
    "last_successful_run": "2025-10-30"
  },
  "granola_meeting_summarizer": {
    "last_run": "2025-10-31",
    "last_successful_run": "2025-10-31"
  }
}
```

**Note**: This file is gitignored and specific to each machine running the assistant.

### State Management Script

`scripts/assistant_state.py` provides utilities for:

1. **Getting last run date**: `get_last_run(agent_name)`
2. **Updating last run**: `update_last_run(agent_name, date, success=True)`
3. **Calculating date range**: `get_date_range_since_last_run(agent_name)`
4. **Checking days since**: `get_days_since_last_run(agent_name)`
5. **Resetting state**: `reset_agent_state(agent_name)`

### Safety Features

- **Default lookback**: If never run, looks back 7 days (configurable)
- **Maximum lookback**: Caps at 14 days to prevent token explosion
- **Warnings**: Alerts when large gaps are detected

## Updated Agents

The following agents now use state tracking:

### 1. Email Preprocessor (`email_preprocessor`)
- Processes emails from last run date to today
- Archives routine emails across multiple days if skipped
- Updates state after successful completion

### 2. Sales Pipeline Tracker (`sales_pipeline_tracker`)
- Analyzes sales calls from last run date to today
- Updates CRM for all missed days
- Detects onboarding progressions retroactively

### 3. Granola Meeting Summarizer (`granola_meeting_summarizer`)
- Processes meetings from last run date to today
- Extracts action items from all missed meetings
- Organizes output by date when processing multiple days

### 4. Daily Email Triage (`daily-email-triage`)
- Works with email preprocessor results
- State tracking handled by email preprocessor
- No direct state management needed

## Usage

### Command Line

```bash
# Check state of all agents
python scripts/assistant_state.py summary

# Check date range for specific agent
python scripts/assistant_state.py range email_preprocessor

# Reset an agent's state (force reprocessing)
python scripts/assistant_state.py reset email_preprocessor
```

### Within Agents

Agents automatically:
1. Check state at startup to determine date range
2. Process all days in range
3. Update state on successful completion

### Example: 3-Day Gap

If you skip Monday-Wednesday and run on Thursday:

```
Last run: Sunday (2025-10-28)
Current date: Thursday (2025-10-31)
Date range: Monday 2025-10-29 to Thursday 2025-10-31 (3 days)
```

All three agents will process:
- Monday's data
- Tuesday's data
- Wednesday's data
- Thursday's data

## Integration with Daily Routine

The `/daily-routine` command now:
1. Checks assistant state at startup
2. Shows which agents need processing
3. Runs each agent with state-aware date ranges
4. Updates state after successful completion

## Manual Override

If you need to force reprocessing:

```bash
# Reset specific agent
python scripts/assistant_state.py reset email_preprocessor

# Or delete entire state file to reset all
rm .assistant_state.json
```

## Error Handling

- **Corrupted state file**: Automatically starts fresh
- **Failed runs**: `last_run` updated but `last_successful_run` stays at previous date
- **Clock skew**: If "last run" is in future, processes today only

## Best Practices

1. **Let agents update state**: Don't manually edit `.assistant_state.json`
2. **Check state regularly**: Run `python scripts/assistant_state.py summary` to see gaps
3. **Reset when needed**: Use reset function if data seems stale
4. **Monitor gaps**: Large gaps (>14 days) are capped for safety

## Agents NOT Using State Tracking

These agents/workflows don't need state tracking:
- **Daily planning**: Always works with current day
- **Standup notes**: Only relevant for current day
- **Sprint planning**: Event-driven, not date-based
- **Task creation**: On-demand, not historical

## Future Enhancements

Potential improvements:
- Add state tracking to more agents
- Track processing duration/performance
- Add state sync across devices (via Notion)
- Implement smart gap detection (skip weekends automatically)
- Add state validation/health checks
