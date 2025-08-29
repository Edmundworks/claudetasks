#!/usr/bin/env python3
"""
Post-hook to remind about syncing local files with Google Calendar and Notion
"""
import json
import sys
import os

try:
    # Load input from stdin
    input_data = json.load(sys.stdin)
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    
    # Get just the filename
    filename = os.path.basename(file_path)
    
    # Check if this is a file we need to sync
    sync_patterns = [
        "daily_schedule",
        "email_summaries", 
        "sprint",
        "tasks",
        "week"
    ]
    
    needs_sync = any(pattern in filename.lower() for pattern in sync_patterns)
    
    if needs_sync:
        reminder = f"""
⚠️  SYNC REMINDER: You just edited {filename}

Please remember to:
1. ✅ Check Google Calendar for any new events to add to the schedule
2. ✅ Update Notion tasks if any were marked complete in the file
3. ✅ Create Google Calendar events for any new scheduled items
4. ✅ Sync any task status changes back to Notion database
5. ✅ Check if any completed tasks need to be archived in Notion

This is critical to keep all systems in sync!
"""
        print(reminder, file=sys.stderr)
        # Exit code 2 will show this to Claude to process
        sys.exit(2)
    
except Exception as e:
    # Silent fail for non-schedule files
    pass

sys.exit(0)