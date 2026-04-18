from .models import Task, TaskStep, TaskMessage, StatusHistory

def assign_team(intent):
    team_map = {
        'send_money': 'finance',
        'verify_document': 'legal',
        'hire_service': 'operations',
        'airport_transfer': 'logistics',
        'check_status': 'operations',
    }
    return team_map.get(intent, 'operations')

def create_full_task(user_message, ai_data, risk_score, risk_label):
    intent = ai_data.get('intent', 'hire_service')
    entities = ai_data.get('entities', {})
    steps = ai_data.get('steps', [])
    messages = ai_data.get('messages', {})
    assigned_team = assign_team(intent)

    # Create the task
    task = Task.objects.create(
        original_request=user_message,
        intent=intent,
        entities=entities,
        risk_score=risk_score,
        risk_label=risk_label,
        assigned_team=assigned_team,
        status='pending',
    )

    # Save steps
    for i, step_text in enumerate(steps, start=1):
        TaskStep.objects.create(
            task=task,
            step_number=i,
            description=step_text,
        )

    # Save the 3 messages — replace {task_code} placeholder
    for channel in ['whatsapp', 'email', 'sms']:
        content = messages.get(channel, '')
        content = content.replace('{task_code}', task.task_code)
        TaskMessage.objects.create(
            task=task,
            channel=channel,
            content=content,
        )

    # Log initial status
    StatusHistory.objects.create(
        task=task,
        old_status='',
        new_status='pending',
        note='Task created',
    )

    return task