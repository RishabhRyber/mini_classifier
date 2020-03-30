from django.shortcuts import render
from django.http import HttpResponse
import service_handler.model_container.class_container as ct

def api(request):
    q = ct.question_session(id=6)
    q.fetch_info()
    a = q.getResponse()
    text = "<h1>You are user no {}!</h1>".format(q.return_id())
    return HttpResponse(text)