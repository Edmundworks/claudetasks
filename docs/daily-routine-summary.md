# Daily Routine Execution Summary

## What You'll See

When you run `/daily-routine`, you'll now get a comprehensive execution summary at the end showing:

- **State tracking status** - How many days were processed for each agent
- **Email processing** - Counts of processed/archived/remaining emails + tasks created
- **Meetings processed** - Meeting count and action items extracted
- **Sales pipeline updates** - Calls tracked, opportunities added, progressions detected
- **Daily tasks created** - Breakdown of direct/derived/email tasks with verification
- **Daily schedule** - Calendar events and time blocks
- **Standup notes** - Whether generated (workdays only)
- **Current sprint** - Sprint details and theme
- **Warnings/issues** - Any conflicts, errors, or items needing attention
- **Execution time** - How long the routine took

## Why This Helps

### 1. **Visibility Into Multi-Day Catchup**
If you skip 3 days, you'll immediately see:
```
📊 STATE TRACKING STATUS:
  • email_preprocessor: Last run 3 days ago (processed Oct 28-31)

📧 EMAIL PROCESSING (Date range: 2025-10-28 to 2025-10-31):
  • Work inbox: 247 emails processed, 198 archived, 49 remaining
```

### 2. **Task Accountability**
Know exactly what tasks were created:
```
✅ DAILY TASKS CREATED:
  • Direct tasks from Daily Todos: 8 tasks
  • Workflow-derived tasks: 5 tasks (3 chase-ups, 2 enrollment checks)
  • Email-based tasks: 12 tasks
  • Total tasks in today's sprint: 25 tasks
  • Verification: ✅ COMPLETE
```

### 3. **Issue Detection**
Spot problems immediately:
```
⚠️  WARNINGS/ISSUES:
  • Calendar conflict detected: 2:00pm event overlaps
  • 1 ambiguous action item needs clarification
  • Credit card bill due in 5 days
```

### 4. **Performance Tracking**
See how long the routine takes:
```
🎉 ROUTINE COMPLETED: 00:03:42 elapsed
```

## How It Works

The daily routine command now:

1. **Tracks metrics** as each agent runs
2. **Accumulates counts** (emails, tasks, meetings, etc.)
3. **Captures warnings** from each phase
4. **Generates formatted summary** at the end
5. **Displays summary** as final output

## Optional: Save Summary

The summary can optionally be saved to `execution_summary_YYYY-MM-DD.md` for future reference.

## Python Helper (Optional)

A helper script exists at `scripts/generate_execution_summary.py` that agents can use to format the summary consistently. However, agents can also generate the summary inline using the template in the daily routine command.

## What Changed

**Before**: Agents ran silently, you had to check multiple files to see what happened

**After**: One comprehensive summary shows everything that happened in your daily routine

## When Things Go Wrong

If a phase fails, the summary will show:

```
⚠️  WARNINGS/ISSUES:
  • Email preprocessor: Failed to archive 15 emails (network timeout)
  • State NOT updated for email_preprocessor (will retry next run)
  • Daily tasks: Only 5/8 direct tasks created ❌ INCOMPLETE

⚠️  ROUTINE INCOMPLETE: Fix errors and re-run
```

This makes it immediately obvious what failed and needs attention.
