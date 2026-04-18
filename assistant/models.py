from django.db import models
import uuid

# This function generates a unique task code for diaspora users to easily track their requests.
def generate_task_code():
    return 'VG-' + str(uuid.uuid4()).upper()[:8]

#This the main TaskTable:stores the request,AI-extracted intent and risk scores.
class Task(models.Model):
    INTENT_CHOICES = [
        ('send_money', 'Send Money'),
        ('hire_service', 'Hire Service'),
        ('verify_document', 'Verify Document'),
        ('airport_transfer', 'Airport Transfer'),
        ('check_status', 'Check Status'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    TEAM_CHOICES = [
        ('finance', 'Finance'),
        ('operations', 'Operations'),
        ('legal', 'Legal'),
        ('logistics', 'Logistics'),
    ]

    task_code        = models.CharField(max_length=20, unique=True, default=generate_task_code)
    original_request = models.TextField()
    intent           = models.CharField(max_length=50, choices=INTENT_CHOICES)
    entities         = models.JSONField(default=dict)
    risk_score       = models.IntegerField(default=0)
    risk_label       = models.CharField(max_length=20, default='low')
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_team    = models.CharField(max_length=50, choices=TEAM_CHOICES, default='operations')
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.task_code} — {self.intent}"

    class Meta:
        ordering = ['-created_at']

#The TaskStep table: allows us to break down complex requests into manageable steps for better tracking and execution.
class TaskStep(models.Model):
    task        = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='steps')
    step_number = models.IntegerField()
    description = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['step_number']

    def __str__(self):
        return f"{self.task.task_code} — Step {self.step_number}"

#The TaskMessage table: stores all communications related to a task, categorized by channel for easy reference.
class TaskMessage(models.Model):
    CHANNEL_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('sms', 'SMS'),
    ]

    task      = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='messages')
    channel   = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    content   = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.task_code} — {self.channel}"

#The StatusHistory table: Provides an audit trail by tracking every status change of a task.
class StatusHistory(models.Model):
    task       = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='history')
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_at = models.DateTimeField(auto_now_add=True)
    note       = models.TextField(blank=True)

    class Meta:
        ordering = ['-changed_at']

    def __str__(self):
        return f"{self.task.task_code}: {self.old_status} → {self.new_status}"