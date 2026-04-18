from django.contrib import admin
from .models import Task, TaskStep, TaskMessage, StatusHistory

# Registering the main Task model to manage customer requests and risk scores.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # list_display controls which columns are visible in the task list view.  
    list_display  = ['task_code', 'intent', 'status', 'risk_score', 'risk_label', 'assigned_team', 'created_at']
    # list_filter allows employees to quickly sort by intent (e.g., see all 'send_money' tasks). 
    list_filter   = ['intent', 'status', 'assigned_team']
    # search_fields allows searching for specific tasks using the unique VG code.
    search_fields = ['task_code', 'original_request']

# Registering TaskSteps to view the AI-generated fulfillment plan for each task.
@admin.register(TaskStep)
class TaskStepAdmin(admin.ModelAdmin):
    list_display = ['task', 'step_number', 'description']
# Registering TaskMessages to verify the three required communication formats.
@admin.register(TaskMessage)
class TaskMessageAdmin(admin.ModelAdmin):
    list_display = ['task', 'channel', 'created_at']
# Registering StatusHistory to provide a clear audit trail for the diaspora customers.
@admin.register(StatusHistory)
class StatusHistoryAdmin(admin.ModelAdmin):
    list_display = ['task', 'old_status', 'new_status', 'changed_at']