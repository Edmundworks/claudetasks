# Daily Routine Checkpoint System

## What Changed

The `/daily-routine` command has been completely restructured from a loose specification to a **mandatory execution protocol** with enforced checkpoints and stop gates.

## The Problem We Solved

**Before**: The daily routine was just instructions that could be partially executed or have steps skipped (like what happened with daily-tasks-agent).

**After**: A checkpoint system that makes it **impossible to skip steps** and **stops execution on failure**.

## How It Works

### 7 Mandatory Checkpoints

Each checkpoint has:
1. **Actions**: What must be done
2. **Verification format**: How to report completion
3. **Stop gate**: Prevents proceeding until verified

```
Checkpoint → Execute → Verify → Stop Gate → Next Checkpoint
```

### The Checkpoints

1. ✅ **Environment Setup & State Check** (⛔ Stop Gate)
2. ✅ **Current Sprint Detection** (⛔ Stop Gate)
3. ✅ **Email Processing** (⛔ Stop Gate)
4. ✅ **Daily Tasks Creation** (⛔ CRITICAL Stop Gate - CANNOT BE SKIPPED)
5. ✅ **Daily Planning** (⛔ Stop Gate)
6. ✅ **Sprint Information Update** (Conditional)
7. ✅ **Standup Notes** (Conditional)
8. ✅ **Final Execution Summary**

### Stop Gates

Stop gates prevent proceeding without verification:

```
✅ CHECKPOINT 4 COMPLETE
- Direct tasks created: 8 tasks
- Verification status: ✅ COMPLETE
⛔ STOP GATE PASSED - Proceeding to Checkpoint 5
```

If verification fails:

```
❌ CHECKPOINT 4 FAILED
- Verification status: ❌ INCOMPLETE
⛔ CRITICAL STOP GATE FAILED
Action: STOPPING EXECUTION - Manual intervention required
```

## Checkpoint 4: The Critical One

**Why it's special**:
- This is where daily-tasks-agent runs
- This is where tasks from Current Daily Todos are created
- This is the step that was being skipped

**Protection added**:
- ⚠️ **CRITICAL - DO NOT SKIP** warning
- **THIS STEP CANNOT BE SKIPPED UNDER ANY CIRCUMSTANCES**
- Explicit verification of task creation
- STOP gate that halts if tasks not created
- Must report exact counts of direct and derived tasks

## Benefits

### 1. No More Skipped Steps
Every step must execute and verify before proceeding.

### 2. Immediate Failure Detection
Stop gates catch failures immediately, not at the end.

### 3. Clear Audit Trail
Each checkpoint reports completion with specific metrics.

### 4. Works with Any AI
Both Claude and Codex can follow this protocol - it's explicit and unambiguous.

### 5. Forced Accountability
The executing AI must explicitly report each checkpoint completion.

## Execution Flow

```
Start Daily Routine
     ↓
Checkpoint 1: Environment Setup
     ↓ (verify + stop gate)
Checkpoint 2: Sprint Detection
     ↓ (verify + stop gate)
Checkpoint 3: Email Processing
     ↓ (verify + stop gate)
Checkpoint 4: Daily Tasks ← CRITICAL - CANNOT SKIP
     ↓ (verify + CRITICAL stop gate)
Checkpoint 5: Daily Planning
     ↓ (verify + stop gate)
Checkpoint 6: Sprint Update (if Tuesday)
     ↓ (verify)
Checkpoint 7: Standup Notes (if workday)
     ↓ (verify)
Final: Execution Summary
     ↓
Complete
```

## Example Execution

When you run `/daily-routine` now, you'll see:

```
EXECUTING CHECKPOINT 1: Environment Setup & State Check

Running: python scripts/assistant_state.py summary
...

✅ CHECKPOINT 1 COMPLETE
- Date: 2025-10-31
- Workday: YES
- State status: All agents current

⛔ STOP GATE PASSED - Proceeding to Checkpoint 2

---

EXECUTING CHECKPOINT 2: Current Sprint Detection
...
```

This continues through all 7 checkpoints with explicit verification at each stage.

## What This Prevents

### The Codex Issue
Codex manually ran email/schedule/standup but **skipped daily-tasks** step.

**With checkpoints**: This is now impossible because:
1. Checkpoint 4 is mandatory
2. Has explicit warning "CANNOT BE SKIPPED"
3. Has critical stop gate
4. Must report verification before proceeding

### Silent Failures
Before, if a step failed, execution continued and you only found out at the end.

**With checkpoints**: Execution stops immediately at failure with clear error message.

### Ambiguous Success
Before, you didn't know exactly what ran and what didn't.

**With checkpoints**: Every step reports completion status explicitly.

## For Both Claude and Codex

This system works regardless of which AI runs it because:

1. **Explicit instructions**: No ambiguity about what to do
2. **Mandatory verification**: Can't proceed without reporting
3. **Clear format**: Verification format is provided
4. **Stop gates**: Physical barriers to skipping steps
5. **No interpretation needed**: Just follow the checklist

## Migration Notes

The old "Process Flow" section has been replaced with "MANDATORY EXECUTION CHECKLIST". The workflow is the same, but enforcement is now built-in.

All existing agents still work the same way - they're just called through the checkpoint system now.

## Next Steps

1. Test the checkpoint system on next daily routine run
2. Verify that Claude/Codex follows checkpoints in order
3. Confirm that stop gates actually stop execution on failure
4. Ensure Checkpoint 4 always runs and creates tasks

The checkpoint system makes the daily routine **bulletproof** against execution failures and skipped steps.
