# Job Pipeline CRM Schema

**Database ID**: `20ac548c-c4ff-80ee-9628-e09d72900f10`
**Database Name**: Job Pipeline CRM
**URL**: https://www.notion.so/20ac548cc4ff80ee9628e09d72900f10

## Core Fields

| Field | Type | Description |
|-------|------|-------------|
| **Name** | title | Company/opportunity name (required) |
| **Status** | status | Pipeline stage (see Status Options below) |
| **Owner** | people | Deal owner - Edmund's ID: `6ae517a8-2360-434b-9a29-1cbc6a427147` |
| **Source Type** | select | Category of lead source |
| **Source** | select | Specific source with person/org details |
| **Client** | relation | Links to Client database (`20bc548c-c4ff-80af-9020-d6e707d6eb5e`) |

## Status Options (Pipeline Stages)

**To-do Group:**
- `Lead` - Initial lead, not yet contacted
- `Sales Call` - Sales call scheduled or completed
- `RFP` - Request for proposal stage
- `Onboarding` - Onboarding call scheduled or in progress

**In Progress Group:**
- `paused` - Deal temporarily paused
- `Activating` - Customer activating on platform
- `In progress` - Active engagement

**Complete Group (Won):**
- `Filled by us` - Successfully filled the role (WIN)

**Complete Group (Lost/Closed):**
- `Good fit wrong time` - Good prospect, timing didn't work
- `Unresponsive (never activated)` - No response after activation
- `Not a fit` - Product/service not a match
- `Filled role` - They filled the role another way
- `closed lost` - General lost deal

## Source Type Options

| Value | Description |
|-------|-------------|
| `VC` | Venture Capital referral |
| `Customer` | Existing customer referral |
| `Referral` | General referral |
| `Inbound` | Inbound inquiry |
| `Outbound` | Outbound prospecting |
| `Event` | Event/conference lead |
| `Community` | Community/network lead |
| `Content` | Content marketing lead |
| `Ads` | Paid advertising |
| `Accelerator/Incubator` | Accelerator program |
| `Expansion` | Existing customer expansion |
| `Internal` | Internal/team referral |
| `Other` | Other sources |

## Source Field (Specific Sources)

Common patterns for Source select values:
- **VC referrals**: `VC - [First Name] - [Fund]` (e.g., `VC - Phill - Ardent`)
- **Customer referrals**: `Customer - [First Name] - [Company]` (e.g., `Customer - Vince - Plastic Labs`)
- **General referrals**: `Referral - [First Name] - [Company]`
- **Events**: `Event - [Event Name]` or `event - [event name]`
- **Platforms**: Just the name (e.g., `Betaworks`)

## Tracking Fields

| Field | Type | Description |
|-------|------|-------------|
| **# of roles** | number | Number of roles/positions |
| **Candidates sent** | number | Candidates submitted |
| **Interviews** | number | Interview count |
| **Fee** | number | Fee amount |
| **Comp Range** | rich_text | Compensation range |

## Date Fields

| Field | Type | Description |
|-------|------|-------------|
| **Created** | created_time | Auto-populated creation date |
| **Activated** | date | When customer activated |
| **Filled** | date | When role was filled |
| **Follow-Up Date** | date | Next follow-up date |

## Computed Fields

| Field | Type | Description |
|-------|------|-------------|
| **Days to fill** | formula | Days from Activated to Filled |
| **Weeks to fill** | formula | Days to fill / 7 |

## Other Fields

| Field | Type | Description |
|-------|------|-------------|
| **Customer Feedback** | rich_text | Feedback notes |
| **Metrics** | checkbox | Has metrics data |
| **Superposition Page** | url | Link to Superposition page |
| **Has a recruiter?** | select | Recruiter status |
| **Outreach method** | select | `Lemlist` or `In product` |

## Status Transition Rules

### Valid Progressions
```
Lead → Sales Call → RFP → Onboarding → Activating → In progress → Filled by us
                                    ↘ paused (can resume)
```

### Exit States (No Return)
- `Filled by us` - Won
- `closed lost` - Lost
- `Not a fit` - Disqualified
- `Filled role` - Lost to competition
- `Good fit wrong time` - Archived for future
- `Unresponsive (never activated)` - Churned

## Related Databases

- **Client Database**: `20bc548c-c4ff-80af-9020-d6e707d6eb5e`
  - Linked via `Client` relation field
  - Syncs back via `Job Pipeline` field on Client
