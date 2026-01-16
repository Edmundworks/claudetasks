#!/usr/bin/env python3
"""
Generate execution summary for daily routine

This is a helper script that can be used to generate formatted execution summaries.
The daily routine command can use this or generate inline.
"""

from datetime import datetime
from typing import Dict, Any, Optional


def generate_summary(metrics: Dict[str, Any]) -> str:
    """
    Generate a formatted execution summary from collected metrics.

    Args:
        metrics: Dictionary containing all execution metrics

    Returns:
        Formatted summary string
    """
    date_str = metrics.get('date', datetime.now().strftime('%Y-%m-%d'))
    day_of_week = metrics.get('day_of_week', datetime.now().strftime('%A'))

    summary = f"""╔════════════════════════════════════════════════════════════════╗
║           DAILY ROUTINE EXECUTION SUMMARY                      ║
║           {date_str} - {day_of_week:<43}║
╚════════════════════════════════════════════════════════════════╝

"""

    # State Tracking Status
    state_status = metrics.get('state_status', {})
    if state_status:
        summary += "📊 STATE TRACKING STATUS:\n"
        for agent, status in state_status.items():
            days_ago = status.get('days_ago', 0)
            date_range = status.get('date_range', 'today')
            summary += f"  • {agent}: Last run {days_ago} day(s) ago (processed {date_range})\n"
        summary += "\n"

    # Email Processing
    email = metrics.get('email', {})
    if email:
        date_range = email.get('date_range', 'today')
        summary += f"📧 EMAIL PROCESSING (Date range: {date_range}):\n"
        work = email.get('work', {})
        summary += f"  • Work inbox: {work.get('processed', 0)} emails processed, "
        summary += f"{work.get('archived', 0)} archived, {work.get('remaining', 0)} remaining\n"
        summary += f"  • Notion tasks created: {email.get('tasks_created', 0)} tasks from actionable emails\n"
        summary += f"  • Newsletter insights: {email.get('newsletter_insights', 0)} items extracted\n"
        summary += f"  • Files: {email.get('files', 'email_summaries_*.md, newsletter_digest_*.md')}\n\n"

    # Meetings
    meetings = metrics.get('meetings', {})
    if meetings:
        date_range = meetings.get('date_range', 'today')
        summary += f"📅 MEETINGS PROCESSED (Date range: {date_range}):\n"
        summary += f"  • Meetings found: {meetings.get('count', 0)} meetings across {meetings.get('days', 1)} days\n"
        summary += f"  • Action items extracted: {meetings.get('action_items', 0)} items\n"
        summary += f"  • Files: {meetings.get('files', 'meetings_summary_*.md')}\n\n"

    # Sales Pipeline
    sales = metrics.get('sales_pipeline', {})
    if sales:
        date_range = sales.get('date_range', 'today')
        summary += f"💼 SALES PIPELINE (Date range: {date_range}):\n"
        summary += f"  • Sales calls tracked: {sales.get('calls', 0)} calls\n"
        summary += f"  • New opportunities: {sales.get('new_opps', 0)} added to CRM"
        if sales.get('new_opp_names'):
            summary += f" ({', '.join(sales['new_opp_names'])})"
        summary += "\n"
        summary += f"  • Progression detected: {sales.get('progressions', 0)} moved to onboarding"
        if sales.get('progression_names'):
            summary += f" ({', '.join(sales['progression_names'])})"
        summary += "\n"
        summary += f"  • CRM updates: {sales.get('crm_updates', 0)} rows modified\n\n"

    # Daily Tasks
    tasks = metrics.get('tasks', {})
    if tasks:
        summary += "✅ DAILY TASKS CREATED:\n"
        summary += f"  • Direct tasks from Daily Todos: {tasks.get('direct', 0)} tasks\n"
        summary += f"  • Workflow-derived tasks: {tasks.get('derived', 0)} tasks"
        if tasks.get('derived_breakdown'):
            summary += f" ({tasks['derived_breakdown']})"
        summary += "\n"
        summary += f"  • Email-based tasks: {tasks.get('email', 0)} tasks\n"
        summary += f"  • Total tasks in today's sprint: {tasks.get('total', 0)} tasks\n"
        verification = tasks.get('verification', 'UNKNOWN')
        emoji = "✅" if verification == "COMPLETE" else "❌"
        summary += f"  • Verification: {emoji} {verification}\n\n"

    # Daily Plan
    schedule = metrics.get('schedule', {})
    if schedule:
        summary += "📆 DAILY PLAN:\n"
        summary += f"  • Calendar events: {schedule.get('events', 0)} events from work calendar\n"
        summary += f"  • High priority items: {schedule.get('blocks', 0)} items\n"
        summary += f"  • Files: {schedule.get('files', 'daily_plan_*.md')}\n\n"

    # Standup Notes
    standup = metrics.get('standup', {})
    if standup.get('applicable', False):
        summary += f"📝 STANDUP NOTES ({day_of_week}):\n"
        generated = "YES" if standup.get('generated', False) else "NO"
        summary += f"  • Generated: {generated}\n"
        if generated == "YES":
            summary += f"  • Files: {standup.get('files', 'standup_notes_*.md')}\n"
        summary += "\n"

    # Current Sprint
    sprint = metrics.get('sprint', {})
    if sprint:
        summary += "🎯 CURRENT SPRINT:\n"
        summary += f"  • Sprint: {sprint.get('name', 'Unknown')}\n"
        summary += f"  • Sprint ID: {sprint.get('id', 'Unknown')}\n"
        summary += f"  • Date range: {sprint.get('date_range', 'Unknown')}\n"
        summary += f"  • Theme: {sprint.get('theme', 'Unknown')}\n\n"

    # Warnings/Issues
    warnings = metrics.get('warnings', [])
    summary += "⚠️  WARNINGS/ISSUES:\n"
    if warnings:
        for warning in warnings:
            summary += f"  • {warning}\n"
    else:
        summary += "  • None\n"
    summary += "\n"

    # Completion
    elapsed = metrics.get('elapsed_time', '00:00:00')
    complete = metrics.get('complete', True)

    if complete:
        summary += f"🎉 ROUTINE COMPLETED: {elapsed} elapsed\n"
    else:
        summary += f"⚠️  ROUTINE INCOMPLETE: {elapsed} elapsed - Fix errors and re-run\n"

    next_date = metrics.get('next_date', 'tomorrow')
    summary += f"\nNext routine recommended: {next_date}\n"

    return summary


def save_summary(summary: str, date: Optional[str] = None) -> str:
    """Save summary to file and return filepath."""
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    filepath = f"execution_summary_{date.replace('-', '_')}.md"

    with open(filepath, 'w') as f:
        f.write("# Daily Routine Execution Summary\n\n")
        f.write(summary)

    return filepath


if __name__ == '__main__':
    # Example usage
    example_metrics = {
        'date': '2025-10-31',
        'day_of_week': 'Thursday',
        'state_status': {
            'email_preprocessor': {'days_ago': 3, 'date_range': 'Oct 28-31'},
            'sales_pipeline_tracker': {'days_ago': 3, 'date_range': 'Oct 28-31'},
        },
        'email': {
            'date_range': '2025-10-28 to 2025-10-31',
            'work': {'processed': 247, 'archived': 198, 'remaining': 49},
            'tasks_created': 12,
            'newsletter_insights': 23,
        },
        'meetings': {
            'date_range': '2025-10-28 to 2025-10-31',
            'count': 8,
            'days': 3,
            'action_items': 15,
        },
        'sales_pipeline': {
            'date_range': '2025-10-28 to 2025-10-31',
            'calls': 3,
            'new_opps': 2,
            'new_opp_names': ['Acme Corp', 'CloudTech'],
            'progressions': 1,
            'progression_names': ['Beta Systems'],
            'crm_updates': 3,
        },
        'tasks': {
            'direct': 8,
            'derived': 5,
            'derived_breakdown': '3 chase-ups, 2 enrollment checks',
            'email': 12,
            'total': 25,
            'verification': 'COMPLETE',
        },
        'schedule': {
            'events': 6,
            'blocks': 12,
        },
        'standup': {
            'applicable': True,
            'generated': True,
        },
        'sprint': {
            'name': 'Week 31',
            'id': '277c548c-c4ff-81bd-a4c4-df9f8665ce9c',
            'date_range': 'September 23-30, 2025',
            'theme': 'Sprint Planning & Execution Optimization',
        },
        'warnings': [
            'Calendar conflict detected: 2:00pm event overlaps with existing meeting',
            '1 ambiguous action item in CloudTech meeting needs clarification',
        ],
        'elapsed_time': '00:03:42',
        'complete': True,
        'next_date': '2025-11-01',
    }

    print(generate_summary(example_metrics))
