import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vunoh_project.settings')
django.setup()

from assistant.models import Task, TaskStep, TaskMessage, StatusHistory

data = []

for task in Task.objects.all():
    data.append({
        'task_code': task.task_code,
        'intent': task.intent,
        'original_request': task.original_request,
        'entities': task.entities,
        'risk_score': task.risk_score,
        'risk_label': task.risk_label,
        'status': task.status,
        'assigned_team': task.assigned_team,
        'created_at': str(task.created_at),
        'steps': [
            {'step_number': s.step_number, 'description': s.description}
            for s in task.steps.all()
        ],
        'messages': [
            {'channel': m.channel, 'content': m.content}
            for m in task.messages.all()
        ],
    })

with open('sample_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f'Exported {len(data)} tasks to sample_data.json')