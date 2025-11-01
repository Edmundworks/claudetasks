# Daily Routine Execution Summary - Example

This is what you'll see at the end of running `/daily-routine`:

```
╔════════════════════════════════════════════════════════════════╗
║           DAILY ROUTINE EXECUTION SUMMARY                      ║
║           2025-10-31 - Thursday                                ║
╚════════════════════════════════════════════════════════════════╝

📊 STATE TRACKING STATUS:
  • email_preprocessor: Last run 3 days ago (processed Oct 28-31)
  • sales_pipeline_tracker: Last run 3 days ago (processed Oct 28-31)
  • granola_meeting_summarizer: Last run 3 days ago (processed Oct 28-31)

📧 EMAIL PROCESSING (Date range: 2025-10-28 to 2025-10-31):
  • Work inbox: 247 emails processed, 198 archived, 49 remaining
  • Notion tasks created: 12 tasks from actionable emails
  • Newsletter insights: 23 items extracted
  • Files: email_summaries_2025_10_31.md, newsletter_digest_2025_10_31.md

📅 MEETINGS PROCESSED (Date range: 2025-10-28 to 2025-10-31):
  • Meetings found: 8 meetings across 3 days
  • Action items extracted: 15 items
  • Files: meetings_summary_2025-10-28_to_2025-10-31.md

💼 SALES PIPELINE (Date range: 2025-10-28 to 2025-10-31):
  • Sales calls tracked: 3 calls
  • New opportunities: 2 added to CRM (Acme Corp, CloudTech)
  • Progression detected: 1 moved to onboarding (Beta Systems)
  • CRM updates: 3 rows modified

✅ DAILY TASKS CREATED:
  • Direct tasks from Daily Todos: 8 tasks
  • Workflow-derived tasks: 5 tasks (3 chase-ups, 2 enrollment checks)
  • Email-based tasks: 12 tasks
  • Total tasks in today's sprint: 25 tasks
  • Verification: ✅ COMPLETE

📆 DAILY SCHEDULE:
  • Calendar events: 6 events from work calendar
  • Time blocks allocated: 12 blocks
  • Files: daily_schedule_2025-10-31.md

📝 STANDUP NOTES (Thursday):
  • Generated: YES
  • Files: standup_notes_2025-10-31.md

🎯 CURRENT SPRINT:
  • Sprint: Week 31
  • Sprint ID: 277c548c-c4ff-81bd-a4c4-df9f8665ce9c
  • Date range: September 23-30, 2025
  • Theme: Sprint Planning & Execution Optimization

⚠️  WARNINGS/ISSUES:
  • Calendar conflict detected: 2:00pm event overlaps with existing meeting
  • 1 ambiguous action item in CloudTech meeting needs clarification
  • Credit card bill due in 5 days (Chase •••1234)

🎉 ROUTINE COMPLETED: 00:03:42 elapsed

Next routine recommended: 2025-11-01
```

## Benefits of This Summary

1. **At-a-Glance Status**: See everything that happened in one view
2. **Multi-Day Awareness**: Clearly shows when catching up on missed days
3. **Task Accountability**: Exact count of tasks created and verified
4. **Warning Visibility**: Conflicts and issues surfaced immediately
5. **Performance Tracking**: See execution time for optimization
6. **File References**: Know exactly where to find detailed outputs

## When You See Large Date Ranges

If you skipped several days, the summary makes it obvious:

```
📊 STATE TRACKING STATUS:
  • email_preprocessor: Last run 7 days ago (processed Oct 24-31)

📧 EMAIL PROCESSING (Date range: 2025-10-24 to 2025-10-31):
  • Work inbox: 573 emails processed, 461 archived, 112 remaining
  ...
```

This tells you immediately that you're catching up on a week's worth of data.

## Error Scenario

If something fails partway through:

```
⚠️  WARNINGS/ISSUES:
  • Email preprocessor: Failed to archive 15 emails (network timeout)
  • State NOT updated for email_preprocessor (will retry next run)
  • Sales pipeline tracker: Skipped due to upstream failure
  • Daily tasks: Only 5/8 direct tasks created ❌ INCOMPLETE

⚠️  ROUTINE INCOMPLETE: Fix errors and re-run
```

The summary makes failures obvious and actionable.
