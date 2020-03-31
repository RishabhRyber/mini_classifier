from django.shortcuts import render
from django.http import HttpResponse
import service_handler.model_container.class_container as ct
import json
def api(request):
    q_session = ct.question_session()
    q_session.fetch_info()
    a = q_session.getResponse()
    json_res = json.dumps(a)
    # text = "<h1>You are user no id: {} \n symptomName: {} \nsymptomDetail:{}</h1>".format(a['id'],a['symptom_name'],a['symptom_details'])

    return HttpResponse(json_res    )
    