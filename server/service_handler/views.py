from django.shortcuts import render
from django.http import HttpResponse
import service_handler.model_container.class_container as ct
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def api(request):
    print(request.body)
    r_json_data = json.loads(request.body.decode("UTF-8"))
    print("\n\nJSON received:\n",r_json_data)
    q_session = ct.question_session(id=r_json_data['id'])
    q_session.fetch_info(option=r_json_data['option'])
    a = q_session.getResponse()
    json_res = json.dumps(a)
    q_session.save_options()
    return HttpResponse(json_res)
    
@csrf_exempt
def first_api(request):
    print(request.body)
    r_json_data = json.loads(request.body.decode("UTF-8"))
    print("\n\nJSON received:\n",r_json_data)
    q_session = ct.question_session(email=r_json_data['email'])
    q_session.fetch_info()
    a = q_session.getResponse()
    json_res = json.dumps(a)
    q_session.save_email()
    return HttpResponse(json_res)
        