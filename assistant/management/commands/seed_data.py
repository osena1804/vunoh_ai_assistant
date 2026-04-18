from django.core.management.base import BaseCommand
from assistant.models import Task, TaskStep, TaskMessage, StatusHistory

class Command(BaseCommand):
    help = 'Seed the database with 5 sample tasks'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        tasks_data = [
            {
                'original_request': 'I need to send KES 15,000 to my mother in Kisumu urgently',
                'intent': 'send_money',
                'entities': {'amount': 15000, 'currency': 'KES', 'recipient': 'mother', 'location': 'Kisumu', 'urgency': 'high'},
                'risk_score': 60,
                'risk_label': 'high',
                'assigned_team': 'finance',
                'status': 'in_progress',
                'steps': [
                    'Verify customer identity and payment method',
                    'Confirm recipient details and M-Pesa number',
                    'Initiate KES 15,000 transfer',
                    'Send confirmation and transaction ID to customer',
                ],
                'messages': {
                    'whatsapp': 'Hi! We have received your urgent request to send KES 15,000 to your mother in Kisumu.\nYour task code is {task_code}.\nWe are on it!',
                    'email': 'Subject: Urgent Money Transfer Request\n\nDear Customer,\nWe acknowledge your request to transfer KES 15,000 to Kisumu.\nTask Code: {task_code}\nOur finance team will process this shortly.',
                    'sms': 'Vunoh: Transfer KES 15,000 to Kisumu in progress. Code: {task_code}',
                },
            },
            {
                'original_request': 'Please verify my land title deed for the plot in Karen',
                'intent': 'verify_document',
                'entities': {'document_type': 'land title deed', 'location': 'Karen', 'urgency': 'medium'},
                'risk_score': 55,
                'risk_label': 'medium',
                'assigned_team': 'legal',
                'status': 'pending',
                'steps': [
                    'Receive and log the land title document',
                    'Assign to legal team for review',
                    'Verify authenticity with land registry authorities',
                    'Prepare verification report',
                    'Send results to customer',
                ],
                'messages': {
                    'whatsapp': 'Hello! We have received your land title verification request for Karen.\nTask code: {task_code}\nOur legal team will handle this carefully.',
                    'email': 'Subject: Document Verification Request\n\nDear Customer,\nWe have received your request to verify a land title deed in Karen.\nTask Code: {task_code}\nOur legal team will be in touch shortly.',
                    'sms': 'Vunoh: Land title verification started. Code: {task_code}',
                },
            },
            {
                'original_request': 'Can someone clean my apartment in Westlands on Friday',
                'intent': 'hire_service',
                'entities': {'service_type': 'cleaning', 'location': 'Westlands', 'date': 'Friday', 'urgency': 'low'},
                'risk_score': 15,
                'risk_label': 'low',
                'assigned_team': 'operations',
                'status': 'completed',
                'steps': [
                    'Match customer with available cleaners in Westlands',
                    'Confirm Friday schedule with service provider',
                    'Send cleaner details to customer',
                    'Complete service and get sign-off',
                ],
                'messages': {
                    'whatsapp': 'Great! We are finding a cleaner for your Westlands apartment on Friday.\nTask code: {task_code}\nWe will confirm the details soon!',
                    'email': 'Subject: Cleaning Service Request\n\nDear Customer,\nWe have received your request for apartment cleaning in Westlands on Friday.\nTask Code: {task_code}',
                    'sms': 'Vunoh: Cleaner booking for Westlands Friday confirmed. Code: {task_code}',
                },
            },
            {
                'original_request': 'I need a lawyer to help with a property dispute in Nakuru',
                'intent': 'hire_service',
                'entities': {'service_type': 'lawyer', 'location': 'Nakuru', 'urgency': 'high'},
                'risk_score': 40,
                'risk_label': 'medium',
                'assigned_team': 'legal',
                'status': 'pending',
                'steps': [
                    'Identify qualified property lawyers in Nakuru',
                    'Brief lawyer on the dispute details',
                    'Schedule consultation with customer',
                    'Provide legal representation and updates',
                ],
                'messages': {
                    'whatsapp': 'We have received your request for a property lawyer in Nakuru.\nTask code: {task_code}\nOur legal team is on it!',
                    'email': 'Subject: Legal Service Request - Property Dispute\n\nDear Customer,\nWe acknowledge your request for legal assistance in Nakuru.\nTask Code: {task_code}',
                    'sms': 'Vunoh: Lawyer search for Nakuru property dispute started. Code: {task_code}',
                },
            },
            {
                'original_request': 'Please arrange airport pickup for my father arriving at JKIA on Saturday at 3pm',
                'intent': 'airport_transfer',
                'entities': {'recipient': 'father', 'location': 'JKIA', 'date': 'Saturday 3pm', 'urgency': 'medium'},
                'risk_score': 20,
                'risk_label': 'low',
                'assigned_team': 'logistics',
                'status': 'in_progress',
                'steps': [
                    'Confirm flight details and arrival time',
                    'Assign driver for JKIA pickup on Saturday',
                    'Share driver details with customer and recipient',
                    'Complete pickup and confirm safe arrival',
                ],
                'messages': {
                    'whatsapp': 'Airport pickup arranged for your father at JKIA on Saturday at 3pm!\nTask code: {task_code}\nWe will keep you updated!',
                    'email': 'Subject: Airport Transfer Request - JKIA\n\nDear Customer,\nWe have arranged an airport pickup for your father at JKIA on Saturday.\nTask Code: {task_code}',
                    'sms': 'Vunoh: JKIA pickup Saturday 3pm confirmed. Code: {task_code}',
                },
            },
        ]

        for task_data in tasks_data:
            task = Task.objects.create(
                original_request=task_data['original_request'],
                intent=task_data['intent'],
                entities=task_data['entities'],
                risk_score=task_data['risk_score'],
                risk_label=task_data['risk_label'],
                assigned_team=task_data['assigned_team'],
                status=task_data['status'],
            )

            for i, step in enumerate(task_data['steps'], start=1):
                TaskStep.objects.create(task=task, step_number=i, description=step)

            for channel, content in task_data['messages'].items():
                TaskMessage.objects.create(
                    task=task,
                    channel=channel,
                    content=content.replace('{task_code}', task.task_code)
                )

            StatusHistory.objects.create(
                task=task,
                old_status='',
                new_status=task_data['status'],
                note='Seeded sample task'
            )

            self.stdout.write(f'  Created task {task.task_code} — {task.intent}')

        self.stdout.write(self.style.SUCCESS('Done! 5 sample tasks created.'))