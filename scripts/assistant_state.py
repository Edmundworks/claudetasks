#!/usr/bin/env python3
"""
Assistant State Management

Tracks the last run date for each agent to enable retroactive processing
when the assistant is not run daily.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Tuple

# State file location (in project root)
STATE_FILE = Path(__file__).parent.parent / ".assistant_state.json"

# Maximum days to look back if no state exists (prevent token explosion)
DEFAULT_LOOKBACK_DAYS = 7
MAX_LOOKBACK_DAYS = 14


def _load_state() -> dict:
    """Load the state file, creating it if it doesn't exist."""
    if not STATE_FILE.exists():
        return {}

    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # If file is corrupted, start fresh
        return {}


def _save_state(state: dict) -> None:
    """Save the state file."""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def get_last_run(agent_name: str) -> Optional[str]:
    """
    Get the last successful run date for an agent.

    Args:
        agent_name: Name of the agent (e.g., 'email_preprocessor')

    Returns:
        ISO date string (YYYY-MM-DD) or None if never run
    """
    state = _load_state()
    agent_state = state.get(agent_name, {})
    return agent_state.get('last_successful_run')


def update_last_run(agent_name: str, run_date: Optional[str] = None, success: bool = True) -> None:
    """
    Update the last run date for an agent.

    Args:
        agent_name: Name of the agent
        run_date: ISO date string (YYYY-MM-DD), defaults to today
        success: Whether the run was successful
    """
    if run_date is None:
        run_date = datetime.now().strftime('%Y-%m-%d')

    state = _load_state()

    if agent_name not in state:
        state[agent_name] = {}

    state[agent_name]['last_run'] = run_date

    if success:
        state[agent_name]['last_successful_run'] = run_date

    _save_state(state)


def get_date_range_since_last_run(
    agent_name: str,
    default_lookback_days: int = DEFAULT_LOOKBACK_DAYS,
    max_lookback_days: int = MAX_LOOKBACK_DAYS
) -> Tuple[str, str]:
    """
    Get the date range to process based on last successful run.

    Args:
        agent_name: Name of the agent
        default_lookback_days: Days to look back if no state exists
        max_lookback_days: Maximum days to look back (cap for safety)

    Returns:
        Tuple of (start_date, end_date) as ISO date strings (YYYY-MM-DD)
    """
    today = datetime.now().date()
    last_run = get_last_run(agent_name)

    if last_run is None:
        # Never run before - use default lookback
        start_date = today - timedelta(days=default_lookback_days)
        print(f"⚠️  No previous run found for {agent_name}, looking back {default_lookback_days} days")
    else:
        # Calculate days since last run
        last_run_date = datetime.strptime(last_run, '%Y-%m-%d').date()
        days_since = (today - last_run_date).days

        if days_since > max_lookback_days:
            print(f"⚠️  Gap of {days_since} days detected for {agent_name}, limiting to {max_lookback_days} days")
            start_date = today - timedelta(days=max_lookback_days)
        elif days_since <= 0:
            # Already run today or in future (clock skew?), just process today
            start_date = today
        else:
            # Normal case - start from day after last run
            start_date = last_run_date + timedelta(days=1)

    return start_date.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')


def get_days_since_last_run(agent_name: str) -> Optional[int]:
    """
    Get the number of days since the agent was last successfully run.

    Args:
        agent_name: Name of the agent

    Returns:
        Number of days, or None if never run
    """
    last_run = get_last_run(agent_name)
    if last_run is None:
        return None

    last_run_date = datetime.strptime(last_run, '%Y-%m-%d').date()
    today = datetime.now().date()
    return (today - last_run_date).days


def reset_agent_state(agent_name: str) -> None:
    """
    Reset the state for a specific agent.

    Args:
        agent_name: Name of the agent to reset
    """
    state = _load_state()
    if agent_name in state:
        del state[agent_name]
        _save_state(state)
        print(f"✓ Reset state for {agent_name}")
    else:
        print(f"ℹ️  No state found for {agent_name}")


def get_all_agent_states() -> dict:
    """Get the full state of all agents."""
    return _load_state()


def print_state_summary() -> None:
    """Print a human-readable summary of all agent states."""
    state = _load_state()

    if not state:
        print("No agent state tracked yet.")
        return

    print("Agent State Summary")
    print("=" * 60)

    today = datetime.now().date()

    for agent_name, agent_state in sorted(state.items()):
        last_run = agent_state.get('last_run', 'Never')
        last_success = agent_state.get('last_successful_run', 'Never')

        if last_success != 'Never':
            last_success_date = datetime.strptime(last_success, '%Y-%m-%d').date()
            days_ago = (today - last_success_date).days
            days_str = f"{days_ago} day(s) ago"
        else:
            days_str = ""

        print(f"\n{agent_name}:")
        print(f"  Last run:        {last_run}")
        print(f"  Last successful: {last_success} {days_str}")


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'summary':
            print_state_summary()
        elif command == 'reset' and len(sys.argv) > 2:
            agent_name = sys.argv[2]
            reset_agent_state(agent_name)
        elif command == 'range' and len(sys.argv) > 2:
            agent_name = sys.argv[2]
            start, end = get_date_range_since_last_run(agent_name)
            print(f"Date range for {agent_name}: {start} to {end}")
        else:
            print("Usage:")
            print("  python assistant_state.py summary              # Show all agent states")
            print("  python assistant_state.py reset <agent_name>   # Reset an agent's state")
            print("  python assistant_state.py range <agent_name>   # Show date range to process")
    else:
        print_state_summary()
