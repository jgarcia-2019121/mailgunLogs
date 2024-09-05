from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Log
import json

def get_logs(request):
    year = request.GET.get('year', None)
    month = request.GET.get('month', None)
    day = request.GET.get('day', None)
    event = request.GET.get('event', None)
    recipient = request.GET.get('recipient', None)
    sender_mask = request.GET.get('sender_mask', None)
    
    logs_list = Log.objects.all().order_by('-date')

    if year:
        try:
            logs_list = logs_list.filter(date__year=2000 + int(year))
        except ValueError:
            return JsonResponse({'error': 'Invalid year format'}, status=400)
    
    if month:
        try:
            logs_list = logs_list.filter(date__month=int(month))
        except ValueError:
            return JsonResponse({'error': 'Invalid month format'}, status=400)
    
    if day:
        try:
            logs_list = logs_list.filter(date__day=int(day))
        except ValueError:
            return JsonResponse({'error': 'Invalid day format'}, status=400)
    
    if event:
        logs_list = logs_list.filter(event=event)
    
    if recipient:
        logs_list = logs_list.filter(recipient__icontains=recipient)
    
    if sender_mask:
        logs_list = logs_list.filter(sender_mask__icontains=sender_mask)

    paginator = Paginator(logs_list, 50)
    page_number = request.GET.get('page', 1)
    
    try:
        page_obj = paginator.get_page(page_number)
    except ValueError:
        return JsonResponse({'error': 'Invalid page number'}, status=400)

    logs_data = []
    for log in page_obj.object_list:
        subject = "N/A"
        sender = "N/A"
        message_data = log.message
        if isinstance(message_data, dict):
            headers = message_data.get('headers', '{}')
        else:
            headers = message_data

        try:
            headers_dict = json.loads(headers) 
            subject = headers_dict.get('subject', 'N/A')
            sender = headers_dict.get('from', 'N/A')
        except (json.JSONDecodeError, TypeError):
            print(f"Error parsing headers for Log ID: {log.id}")
        print(f"Log ID: {log.id}, Subject: {subject}, From: {sender}")

        logs_data.append({
            'id': log.id,
            'date': log.date,
            'event': log.event,
            'recipient': log.recipient,
            'url': log.url,
            'subject': subject,
            'from': sender,
        })

    data = {
        'logs': logs_data,
        'total_pages': paginator.num_pages
    }

    return JsonResponse(data, safe=False)

def get_events(request):
    events = Log.objects.values_list('event', flat=True).distinct()
    return JsonResponse({"events": list(events)}, safe=False)