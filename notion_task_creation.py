import requests
import os

# Notion API credentials
NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
DATABASE_ID = '181c548c-c4ff-80ba-8a01-f3ed0b4a7fef'
HEADERS = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

tasks = [
    {
        'Name': 'Call with Chaimaa Zirdane (ContactOut)',
        'Tags': ['Sell'],
        'Due Date': '2025-09-23T10:30:00-04:00',
        'Status': 'Not started'
    },
    {
        'Name': 'Call with Shahar Ben-Hador (Radiant Security)',
        'Tags': ['Sell'],
        'Due Date': '2025-09-23T14:30:00-04:00',
        'Status': 'Not started'
    },
    {
        'Name': 'Call with Sarah Allali (The Lobby)',
        'Tags': ['Sell'],
        'Due Date': '2025-09-24T10:00:00-04:00',
        'Status': 'Not started'
    },
    {
        'Name': 'Superposition Onboarding with Jeremy Philip Galen',
        'Tags': ['Serve'],
        'Due Date': '2025-09-24T15:30:00-04:00',
        'Status': 'Not started'
    },
    {
        'Name': 'Call with Julia Cole (Manta Cares)',
        'Tags': ['Sell'],
        'Due Date': '2025-09-24T16:45:00-04:00',
        'Status': 'Not started'
    }
]

def create_notion_task(task):
    data = {
        'parent': {'database_id': DATABASE_ID},
        'properties': {
            'Name': {'title': [{'text': {'content': task['Name']}}]},
            'Tags': {'multi_select': [{'name': tag} for tag in task['Tags']]},
            'Due Date': {'date': {'start': task['Due Date']}},
            'Status': {'status': {'name': task['Status']}},
            'Person': {'people': [{'id': '6ae517a8-2360-434b-9a29-1cbc6a427147'}]},
            'Sprint': {'relation': [{'id': '270c548c-c4ff-810a-a5aa-d150e7bca812'}]}
        }
    }
    response = requests.post('https://api.notion.com/v1/pages', headers=HEADERS, json=data)
    print(response.json())

for task in tasks:
    create_notion_task(task)
