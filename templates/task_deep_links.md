# Task Deep Links Reference

Use these deep links when creating tasks to make them immediately actionable:

## Prospecting & Sales
- **LinkedIn Connections**: https://www.linkedin.com/mynetwork/invite-connect/connections/
- **LinkedIn Messages**: https://www.linkedin.com/messaging/
- **LinkedIn Sales Navigator**: https://www.linkedin.com/sales/
- **Apollo Prospecting**: https://app.apollo.io/#/tasks?dateRange[max]=YYYY-MM-DD&sortByField=task_due_at&sortAscending=true
  - *Note: Replace YYYY-MM-DD with today's date (e.g., 2025-09-16)*
- **Valley Prospecting**: [Add Valley dashboard URL]

## Email & Communication
- **Work Email Inbox**: https://mail.google.com/mail/u/0/#inbox
- **Personal Email Inbox**: https://mail.google.com/mail/u/1/#inbox
- **Gmail Compose**: https://mail.google.com/mail/u/0/#compose
- **Calendly Scheduling**: [Add Calendly URL if used]

## Work Tools
- **Notion Workspace**: https://www.notion.so/super-ats/
- **Current Sprint**: https://www.notion.so/super-ats/Week-30-Scale-Prospecting-While-Maintaining-Quality-270c548cc4ff810aa5aad150e7bca812
- **Job Pipeline**: https://www.notion.so/super-ats/20ac548cc4ff80ee9628e09d72900f10?v=20ac548cc4ff8011a37b000c6e52b6c4
- **Work Tasks Database**: https://www.notion.so/super-ats/181c548cc4ff80ba8a01f3ed0b4a7fef

## Development & Admin
- **GitHub Repository**: https://github.com/Edmundworks/claudetasks
- **Claude Code IDE**: [Local IDE]
- **Terminal/Commands**: [Local terminal]

## Client Management
- **Job Pipeline Database**: https://www.notion.so/super-ats/20ac548cc4ff80ee9628e09d72900f10?v=20ac548cc4ff8011a37b000c6e52b6c4
- **Individual Company Pages**: Direct links to specific company Job Pipeline entries
  - *Example: Newton - https://www.notion.so/super-ats/Newton-26bc548cc4ff805db41be4124b7b4ecc*
  - *Example: Scanner.dev - [Get from Job Pipeline query results]*
- **Customer Dashboard**: [Add customer management tool URL]
- **Support Portal**: [Add support system URL]

## Financial
- **Mercury Banking**: [Add Mercury URL]
- **Expense Tracking**: [Add expense tool URL]
- **Invoice Management**: [Add invoicing tool URL]

## Task Creation Guidelines

When creating tasks, always include the most relevant deep link to make the task immediately actionable:

**Good Examples:**

*LinkedIn Connections Task:*
```
Task: "Send LinkedIn connections to 50 prospects"  
Description: "Use Apollo to find prospects and send connection requests via LinkedIn."
Links: 
- Apollo: https://app.apollo.io/#/tasks?dateRange[max]=2025-09-16&sortByField=task_due_at&sortAscending=true
- LinkedIn: https://www.linkedin.com/mynetwork/invite-connect/connections/
```

*Company Chase-up Task:*
```
Task: "Chase up Newton"
Description: "Follow up with Newton on onboarding progress"  
Links:
- Job Pipeline: https://www.notion.so/super-ats/Newton-26bc548cc4ff805db41be4124b7b4ecc
```

*Daily Schedule Format:*
```
- [ ] **[Chase up Newton](https://notion.so/task-id)** - Onboarding follow-up | [Newton Job](https://www.notion.so/super-ats/Newton-26bc548cc4ff805db41be4124b7b4ecc)
- [ ] **[Send LinkedIn connections](https://notion.so/task-id)** - 50 prospects via Apollo | [Apollo](https://app.apollo.io/#/tasks?dateRange[max]=2025-09-16&sortByField=task_due_at&sortAscending=true) | [LinkedIn](https://www.linkedin.com/mynetwork/invite-connect/connections/)
```

**Bad Example:**
```
Task: "Send LinkedIn connections to 50 prospects"
Description: "Send connection requests"
Links: None
```