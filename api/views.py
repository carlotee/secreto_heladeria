from django.http import JsonResponse

def health(request):
    return JsonResponse({"status": "ok"})

def info_api(request):
    data = {
        "proyecto": "Secreto Heladeria API",
        "version": "1.0",
        "autor": "Carlos"
    }
    return JsonResponse(data)