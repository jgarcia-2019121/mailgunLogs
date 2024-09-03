from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Log

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

    data = {
        'logs': list(page_obj.object_list.values('id', 'date', 'event', 'recipient', 'url', 'message')),
        'total_pages': paginator.num_pages
    }

    return JsonResponse(data, safe=False)

def get_events(request):
    events = Log.objects.values_list('event', flat=True).distinct()
    return JsonResponse({"events": list(events)}, safe=False)