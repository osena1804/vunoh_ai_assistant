from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .ai_service import process_request
from .risk_engine import calculate_risk
from .task_service import create_full_task
from .models import Task, TaskStep, TaskMessage, StatusHistory

def index(request):
    return render(request, 'assistant/index.html')

@csrf_exempt
def process_message(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        body = json.loads(request.body)
        user_message = body.get('message', '').strip()
        if not user_message:
            return JsonResponse({'error': 'Message is empty'}, status=400)
        ai_data = process_request(user_message)
        risk_score, risk_label, risk_reasons = calculate_risk(
            ai_data.get('intent', ''),
            ai_data.get('entities', {})
        )
        task = create_full_task(user_message, ai_data, risk_score, risk_label)
        steps = list(task.steps.values_list('description', flat=True))
        messages = {m.channel: m.content for m in task.messages.all()}
        return JsonResponse({
            'task_code': task.task_code,
            'intent': task.intent,
            'entities': task.entities,
            'risk_score': task.risk_score,
            'risk_label': task.risk_label,
            'assigned_team': task.assigned_team,
            'steps': steps,
            'messages': messages,
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON from AI. Try again.'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def dashboard(request):
    tasks = Task.objects.all()
    return render(request, 'assistant/dashboard.html', {
        'tasks': tasks,
        'total_tasks': tasks.count(),
        'pending_count': tasks.filter(status='pending').count(),
        'inprogress_count': tasks.filter(status='in_progress').count(),
        'completed_count': tasks.filter(status='completed').count(),
    })

@csrf_exempt
def update_status(request, task_code):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        body = json.loads(request.body)
        new_status = body.get('status')
        task = Task.objects.get(task_code=task_code)
        old_status = task.status
        task.status = new_status
        task.save()
        StatusHistory.objects.create(
            task=task,
            old_status=old_status,
            new_status=new_status,
            note='Status updated via dashboard'
        )
        return JsonResponse({'success': True, 'status': new_status})
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)