from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Log

def get_logs(request):
    # Obtención de los parámetros de filtrado
    year = request.GET.get('year', None)
    month = request.GET.get('month', None)
    day = request.GET.get('day', None)
    event = request.GET.get('event', None)
    recipient = request.GET.get('recipient', None)
    sender_mask = request.GET.get('sender_mask', None)

    # Obtención de todos los logs ordenados por fecha
    logs_list = Log.objects.all().order_by('-date')

    # Filtrado por fecha
    if year:
        logs_list = logs_list.filter(date__year=2000 + int(year))
    if month:
        logs_list = logs_list.filter(date__month=int(month))
    if day:
        logs_list = logs_list.filter(date__day=int(day))
    
    # Filtrado por evento, destinatario y remitente
    if event:
        logs_list = logs_list.filter(event=event)
    if recipient:
        logs_list = logs_list.filter(recipient__icontains=recipient)
    if sender_mask:
        logs_list = logs_list.filter(sender_mask__icontains=sender_mask)

    # Paginación
    paginator = Paginator(logs_list, 50)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Estructura de la respuesta
    data = {
        'logs': list(page_obj.object_list.values('id', 'date', 'event', 'recipient', 'url', 'message')),
        'total_pages': paginator.num_pages
    }

    return JsonResponse(data, safe=False)

def get_events(request):
    events = Log.objects.values_list('event', flat=True).distinct()
    return JsonResponse({"events": list(events)}, safe=False)
