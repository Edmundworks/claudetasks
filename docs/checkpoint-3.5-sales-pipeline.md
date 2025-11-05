# Checkpoint 3.5: Sales Pipeline Tracking

## What Changed

Added **Sales Pipeline Tracking** as a new mandatory checkpoint in the daily routine (Checkpoint 3.5).

## Why This Was Needed

Codex's feedback revealed that `sales-pipeline-tracker` agent was **not being run** during daily routine execution. The agent exists but wasn't included in the mandatory checkpoint list, so it got skipped.

## The Problem

- Sales pipeline tracker agent exists and works fine
- But it wasn't part of the daily routine checklist
- So when running `/daily-routine`, it never executed
- Result: Granola sales calls weren't being tracked in the CRM

## The Solution

Added **Checkpoint 3.5: Sales Pipeline Tracking** between Email Processing (Checkpoint 3) and Daily Tasks Creation (Checkpoint 4).

### Checkpoint Details

**Placement**: After Email Processing, before Daily Tasks

**Actions**:
1. Launch `sales-pipeline-tracker` agent (Task tool)
2. Agent processes Granola calls from state-tracked date range
3. Agent searches for onboarding meetings in calendar
4. Agent updates Job Pipeline CRM in Notion (Database: `20ac548cc4ff80ee9628e09d72900f10`)
5. Capture: calls tracked, new opportunities, progressions, CRM updates

**Verification**:
```
✅ CHECKPOINT 3.5 COMPLETE
- Date range processed: [start] to [end]
- Sales calls tracked: [X] calls
- New opportunities: [X] added to CRM
- Progression detected: [X] moved to onboarding
- CRM updates: [X] rows modified
```

**Stop Gate**: ⛔ Do not proceed until sales pipeline tracking completes.

## Updated Checkpoint Flow

**Old flow** (7 checkpoints):
1. Environment Setup
2. Sprint Detection
3. Email Processing
4. Daily Tasks ← Checkpoint 4 was here
5. Daily Planning
6. Sprint Update
7. Standup Notes

**New flow** (9 checkpoints):
1. Environment Setup
2. Sprint Detection
3. Email Processing
3.5. **Sales Pipeline Tracking** ← NEW MANDATORY CHECKPOINT
4. Daily Tasks
5. Meetings Processing ← Also added (optional)
6. Daily Planning
7. Sprint Update
8. Standup Notes
9. Execution Summary

## Why Between Email and Daily Tasks

**Placement rationale**:
1. **After Email Processing**: Email triage may mention sales calls/meetings, good context
2. **Before Daily Tasks**: Sales pipeline updates should inform daily task priorities
3. **Independent**: Doesn't depend on daily tasks being created
4. **State-tracked**: Uses same state tracking as email preprocessor

## Checkpoint 5: Meetings Processing

Also added **Checkpoint 5: Meetings Processing** (optional) to handle Granola meeting summaries. This was referenced in state tracking and execution summary but wasn't a formal checkpoint.

**Difference from Sales Pipeline**:
- **Sales Pipeline (3.5)**: Tracks sales calls → CRM updates (MANDATORY)
- **Meetings Processing (5)**: Extracts action items from ALL meetings (OPTIONAL)

## CRM Database

The sales pipeline tracker updates this Notion database:
- **Database ID**: `20ac548cc4ff80ee9628e09d72900f10`
- **Database Name**: Job Pipeline CRM
- **URL**: https://www.notion.so/super-ats/20ac548cc4ff80ee9628e09d72900f10

**Columns**:
- Name (company name)
- Status ("Sales Call" or "Onboarding")
- Owner (Edmund's user ID)
- Source (can be blank for automated entries)

## Mandatory Status

Checkpoint 3.5 is **MANDATORY** with a stop gate:
- Cannot be skipped
- Must complete before proceeding to Checkpoint 4
- Failure stops the entire routine
- Must report verification metrics

Updated success criteria:
```
✅ All mandatory checkpoints completed (1, 2, 3, 3.5, 4, 6)
✅ Checkpoint 3.5 completed: Sales pipeline tracked
```

## State Tracking

Sales pipeline tracker uses the same state tracking system:
- Tracks last run in `.assistant_state.json`
- Processes date range since last run
- Updates state after successful completion
- Falls back to 7 days if never run

## What This Fixes

**Before**: Sales calls from Granola weren't being tracked in CRM because agent never ran

**After**: Every daily routine run will:
1. Check for Granola sales calls
2. Match them to onboarding meetings in calendar
3. Update CRM with new opportunities and progressions
4. Report exactly what was tracked

## Execution Example

```
---

EXECUTING CHECKPOINT 3.5: Sales Pipeline Tracking

Actions:
1. Launching sales-pipeline-tracker agent...
2. Processing Granola calls from Oct 28-31...
3. Searching calendar for onboarding meetings...
4. Updating Job Pipeline CRM...

✅ CHECKPOINT 3.5 COMPLETE
- Date range processed: 2025-10-28 to 2025-10-31
- Sales calls tracked: 3 calls
- New opportunities: 2 added to CRM (Acme Corp, CloudTech)
- Progression detected: 1 moved to onboarding (Beta Systems)
- CRM updates: 3 rows modified

⛔ STOP GATE PASSED - Proceeding to Checkpoint 4

---
```

## Next Run

When you next run `/daily-routine`, the sales pipeline tracker will:
1. Be automatically executed at Checkpoint 3.5
2. Process all sales calls since last run
3. Update the CRM
4. Report results in execution summary

**No more missing sales call tracking!** 🎯
