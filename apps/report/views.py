from django.shortcuts import render
# your_app/views.py
from django.http import HttpResponse
from django.core.serializers import serialize
from django.apps import apps
from rest_framework.response import Response
from rest_framework.decorators import api_view
from apps.file_storage.models import File
from django.core.files.uploadedfile import SimpleUploadedFile

from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import csv


def export(request):
    app_models = apps.get_models()
    serialized_data_list = []
    for model in app_models:
        queryset = model.objects.all()
        serialized_data = serialize('json', queryset)
        serialized_data_list.append(serialized_data)

    exported_data = "[" + ",".join(serialized_data_list) + "]"

    response = HttpResponse(exported_data, content_type='application/json')

    response['Content-Disposition'] = 'attachment; filename=exported_data.json'

    return response


def export_csv(request):
    app_models = apps.get_models()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=exported_data.csv'
    csv_writer = csv.writer(response)
    for model in app_models:
        fields = [field.name for field in model._meta.fields]
        csv_writer.writerow([f"{model.__name__}_{field}" for field in fields])

    for model in app_models:
        queryset = model.objects.all()
        for row in queryset.values():
            csv_writer.writerow([row[field] for field in row])

    return response







import requests



from apps.file_storage.serializers.file_serializer import FileSerializer
def create_session():
    url = "https://metabase.sepid.org/api/session"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "username": "sepid.platform@gmail.com",
        "password": "ThisIsSepidPassword4Metabase"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

session_data = create_session()

def get_user_answer(session_token,form_id , user_id):
    url = "https://metabase.sepid.org/api/dataset/xlsx"
    headers = {
        "X-Metabase-Session": session_data.get("id"),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "query":'{"database":2,"type":"query","query":{"source-table":60,"joins":[{"source-table":35,"condition":["=",["field",446,null],["field",271,{"join-alias":"Fsm+Answersheet+-+Answersheet+Ptr"}]],"alias":"Fsm+Answersheet+-+Answersheet+Ptr"},{"fields":[["field",264,{"join-alias":"Fsm+Answer"}]],"source-table":106,"condition":["=",["field",271,{"join-alias":"Fsm+Answersheet+-+Answersheet+Ptr"}],["field",269,{"join-alias":"Fsm+Answer"}]],"alias":"Fsm+Answer"},{"fields":[["field",290,{"join-alias":"Fsm+Biganswer"}]],"source-table":46,"condition":["=",["field",263,{"join-alias":"Fsm+Answer"}],["field",288,{"join-alias":"Fsm+Biganswer"}]],"alias":"Fsm+Biganswer"},{"fields":[["field",451,{"join-alias":"Fsm+Smallanswer"}]],"source-table":96,"condition":["=",["field",263,{"join-alias":"Fsm+Answer"}],["field",449,{"join-alias":"Fsm+Smallanswer"}]],"alias":"Fsm+Smallanswer"},{"fields":[["field",142,{"join-alias":"Accounts+User+-+User"}],["field",156,{"join-alias":"Accounts+User+-+User"}],["field",151,{"join-alias":"Accounts+User+-+User"}]],"source-table":32,"condition":["=",["field",443,null],["field",151,{"join-alias":"Accounts+User+-+User"}]],"alias":"Accounts+User+-+User"}],"filter":["and",["=",["field",779,null],'+f'{form_id}'+'],["=",["field",443,null],"'+f'{user_id}'+'"]]},"middleware":{"js-int-to-string?":true,"add-default-userland-constraints?":true}}'
    }
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        with open('output.xlsx', 'wb') as f:
            f.write(response.content)

        file = SimpleUploadedFile("test.xlsx", b"file_content")
        new_file = FileSerializer(data={"file": file})
        new_file.is_valid(raise_exception=True)
        new_file.save()
        print(new_file.data)
        print("File created successfully:")
        return new_file.data
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        print(response.text)


def get_current_user(session_token):
    url = "https://metabase.sepid.org/api/dataset/"
    headers = {
        "Content-Type": "application/json",
        "X-Metabase-Session": session_token
    }
    data = {
            "database": 2,
            "query": {
                "source-table": 60,
                "filter": [
                    "and",
                    ["=", ["field", 448, None], True],
                    ["=", ["field", 444, None], "Accepted"],
                    ["=", ["field", 779, None], 1]
                ],
                "joins": [
                    {
                        "fields": [
                            ["field", 142, {"join-alias": "Accounts+User+-+User"}],
                            ["field", 156, {"join-alias": "Accounts+User+-+User"}],
                            ["field", 158, {"join-alias": "Accounts+User+-+User"}],
                            ["field", 144, {"join-alias": "Accounts+User+-+User"}],
                            ["field", 159, {"join-alias": "Accounts+User+-+User"}],
                            ["field", 151, {"join-alias": "Accounts+User+-+User"}],
                            ["field", 146, {"join-alias": "Accounts+User+-+User"}],
                            ["field", 147, {"join-alias": "Accounts+User+-+User"}]
                        ],
                        "source-table": 32,
                        "condition": ["=", ["field", 443, None],
                                      ["field", 151, {"join-alias": "Accounts+User+-+User"}]],
                        "alias": "Accounts+User+-+User"
                    }
                ]
            },
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.status_code)
    if response.status_code == 202:
        return response.json()
    else:
        response.raise_for_status()


import requests
def export_excel(form_id):
    url = "https://metabase.sepid.org/api/dataset/xlsx"
    headers = {
        "X-Metabase-Session": session_data.get("id"),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    query='{"source-table":60,"filter":["and",["=",["field",448,null],true],["=",["field",444,null],"Accepted"],'+f'["=",["field",779,null],{form_id}]]'+',"joins":[{"fields":[["field",142,{"join-alias":"Accounts User - User"}],["field",156,{"join-alias":"Accounts User - User"}],["field",158,{"join-alias":"Accounts User - User"}],["field",144,{"join-alias":"Accounts User - User"}],["field",159,{"join-alias":"Accounts User - User"}],["field",151,{"join-alias":"Accounts User - User"}],["field",146,{"join-alias":"Accounts User - User"}],["field",147,{"join-alias":"Accounts User - User"}]],"source-table":32,"condition":["=",["field",443,null],["field",151,{"join-alias":"Accounts User - User"}]],"alias":"Accounts User - User"}]},"type":"query","middleware":{"js-int-to-string?":true,"add-default-userland-constraints?":true}}'
    data = {
        "query": '{"database":2,"query":'+ f'{query}'+',"type":"query","middleware":{"js-int-to-string?":true,"add-default-userland-constraints?":true}}'
    }
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        with open('test.xlsx', 'wb') as f:
            f.write(response.content)


        file = SimpleUploadedFile("test.xlsx", b"file_content")
        new_file = FileSerializer(data={"file":file})
        new_file.is_valid(raise_exception=True)
        new_file.save()
        print(new_file.data)
        print("File created successfully:")
        return new_file.data
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        print(response.text)




def get_all_user_answer(form_id):
    url = "https://metabase.sepid.org/api/dataset/xlsx"
    headers = {
        "X-Metabase-Session": session_data.get("id"),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "query":'{"query":{"source-table":60,"joins":[{"fields":"none","source-table":35,"condition":["=",["field",446,null],["field",271,{"join-alias":"Fsm+Answersheet+-+Answersheet+Ptr"}]],"alias":"Fsm+Answersheet+-+Answersheet+Ptr"},{"fields":"none","source-table":106,"condition":["=",["field",271,{"join-alias":"Fsm+Answersheet+-+Answersheet+Ptr"}],["field",269,{"join-alias":"Fsm+Answer"}]],"alias":"Fsm+Answer"},{"fields":"none","source-table":96,"condition":["=",["field",263,{"join-alias":"Fsm+Answer"}],["field",449,{"join-alias":"Fsm+Smallanswer"}]],"alias":"Fsm+Smallanswer"},{"fields":"none","source-table":46,"condition":["=",["field",263,{"join-alias":"Fsm+Answer"}],["field",288,{"join-alias":"Fsm+Biganswer"}]],"alias":"Fsm+Biganswer","strategy":"left-join"},{"fields":"none","source-table":27,"condition":["=",["field",263,{"join-alias":"Fsm+Answer"}],["field",368,{"join-alias":"Fsm+Multichoiceanswer"}]],"alias":"Fsm+Multichoiceanswer"},{"fields":"none","source-table":107,"condition":["=",["field",263,{"join-alias":"Fsm+Answer"}],["field",466,{"join-alias":"Fsm+Uploadfileanswer"}]],"alias":"Fsm+Uploadfileanswer"}],"filter":["=",["field",779,null],'+f'{form_id}'+'],"expressions":{"answer":["concat",["field",451,{"join-alias":"Fsm+Smallanswer"}],["field",290,{"join-alias":"Fsm+Biganswer"}],["field",466,{"join-alias":"Fsm+Uploadfileanswer"}]],"name":["concat",["field",142,{"source-field":443}],"+",["field",156,{"source-field":443}]]},"fields":[["field",446,null],["expression","answer",null],["expression","name"]]},"type":"query","database":2,"middleware":{"js-int-to-string?":true,"add-default-userland-constraints?":true}}'
    }
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        with open('test.xlsx', 'wb') as f:
            f.write(response.content)

        file = SimpleUploadedFile("test.xlsx", b"file_content")
        new_file = FileSerializer(data={"file": file})
        new_file.is_valid(raise_exception=True)
        new_file.save()
        print(new_file.data)
        print("File created successfully:")
        return new_file.data
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        print(response.text)


@api_view(["post"])
def get_user_excel(request):
    id = request.data.get('form_id')
    print(id)
    file_content =export_excel(form_id=id)
    print(file_content)
    return Response(file_content)



@api_view(["post"])
def get_answer_excel(request):
    id = request.data.get('form_id')
    file_content =get_all_user_answer(form_id=id)
    return Response(file_content)


