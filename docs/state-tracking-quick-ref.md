# State Tracking Quick Reference

## Will It Work?

**YES**, with these key points:

### ✅ What Works

1. **State file tracks last run**: `.assistant_state.json` persists between sessions
2. **Agents query state**: Each agent runs bash command to get date range
3. **Gmail date filters**: Agents use `after:YYYY/MM/DD before:YYYY/MM/DD` in queries
4. **Granola MCP search**: Can search meetings by date range
5. **Automatic updates**: Agents update state after successful completion
6. **Safety caps**: Maximum 14-day lookback prevents token explosion

### How Agents Execute

**Example: Email Preprocessor after 3-day gap**

```
1. Agent starts
2. Runs: python -c "...get_date_range_since_last_run('email_preprocessor')..."
3. Gets output: "2025-10-28|2025-10-31"
4. Parses dates: start=2025-10-28, end=2025-10-31
5. Queries Gmail: query="after:2025/10/28 before:2025/10/31 -is:archived"
6. Processes all emails from those 3 days
7. Updates state: python -c "...update_last_run('email_preprocessor')..."
```

### Key Implementation Details

**Date Format Conversion**
- State file uses: `YYYY-MM-DD`
- Gmail queries need: `YYYY/MM/DD`
- Agent must convert: `2025-10-28` → `2025/10/28`

**State Update Timing**
- Only update state AFTER successful completion
- If processing fails partway, state remains at old date
- Next run will retry the same date range

**Multi-Day Processing**
- Agent processes all days in range
- Output organized by date
- Summary shows date range processed

## Testing Checklist

Before going live, verify:

- [ ] State file created/updated correctly
- [ ] Date range calculation works
- [ ] Gmail queries accept date format
- [ ] Granola search works with dates
- [ ] State updates only on success
- [ ] Multi-day gaps handled correctly
- [ ] Maximum lookback cap works
- [ ] Reset function clears state

## Common Issues & Solutions

**Issue**: Agent still only processes today
- **Fix**: Check if agent is actually running the bash command
- **Debug**: Look for "⚠️ No previous run found" message

**Issue**: Date format error in Gmail
- **Fix**: Ensure agent converts `YYYY-MM-DD` to `YYYY/MM/DD`
- **Check**: Gmail query string in agent output

**Issue**: State not updating
- **Fix**: Verify bash command runs after processing
- **Check**: Run `python scripts/assistant_state.py summary`

**Issue**: Too many emails/meetings
- **Fix**: State tracking caps at 14 days automatically
- **Manual**: Reset specific agent if needed

## Quick Commands

```bash
# Check all agent states
python scripts/assistant_state.py summary

# See date range for specific agent
python scripts/assistant_state.py range email_preprocessor

# Force reprocess by resetting
python scripts/assistant_state.py reset email_preprocessor

# Manually set last run date
python -c "from scripts.assistant_state import update_last_run; update_last_run('email_preprocessor', '2025-10-28')"
```

## Next Steps

1. **Test email preprocessor** with a known gap
2. **Verify Gmail queries** return correct date range
3. **Check state file** updates after run
4. **Test multi-day scenario** (skip 3 days, run on 4th)
5. **Verify output** shows all days processed
