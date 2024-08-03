import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.file_storage.serializers.file_serializer import FileSerializer

url = settings.METABASE_URL


def create_session():
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "username": settings.METABASE_USERNAME,
        "password": settings.METABASE_PASSWORD,
    }

    response = requests.post(f'{url}api/session/', headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


session_data = create_session()


def get_user_answer(session_token, form_id, user_id):
    headers = {
        "X-Metabase-Session": session_data.get("id"),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "query": '{"database":2,"type":"query","query":{"source-table":60,"joins":[{"source-table":35,"condition":["=",["field",446,null],["field",271,{"join-alias":"Fsm+Answersheet+-+Answersheet+Ptr"}]],"alias":"Fsm+Answersheet+-+Answersheet+Ptr"},{"fields":[["field",264,{"join-alias":"Fsm+Answer"}]],"source-table":106,"condition":["=",["field",271,{"join-alias":"Fsm+Answersheet+-+Answersheet+Ptr"}],["field",269,{"join-alias":"Fsm+Answer"}]],"alias":"Fsm+Answer"},{"fields":[["field",290,{"join-alias":"Fsm+Biganswer"}]],"source-table":46,"condition":["=",["field",263,{"join-alias":"Fsm+Answer"}],["field",288,{"join-alias":"Fsm+Biganswer"}]],"alias":"Fsm+Biganswer"},{"fields":[["field",451,{"join-alias":"Fsm+Smallanswer"}]],"source-table":96,"condition":["=",["field",263,{"join-alias":"Fsm+Answer"}],["field",449,{"join-alias":"Fsm+Smallanswer"}]],"alias":"Fsm+Smallanswer"},{"fields":[["field",142,{"join-alias":"Accounts+User+-+User"}],["field",156,{"join-alias":"Accounts+User+-+User"}],["field",151,{"join-alias":"Accounts+User+-+User"}]],"source-table":32,"condition":["=",["field",443,null],["field",151,{"join-alias":"Accounts+User+-+User"}]],"alias":"Accounts+User+-+User"}],"filter":["and",["=",["field",779,null],'+f'{form_id}'+'],["=",["field",443,null],"'+f'{user_id}'+'"]]},"middleware":{"js-int-to-string?":true,"add-default-userland-constraints?":true}}'
    }
    response = requests.post(
        f'{url}api/dataset/xlsx', headers=headers, data=data)

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
                ["=", ["field", 779, None], 1]
            ],
            "joins": [
                {
                    "fields": [
                        ["field", 142, {
                            "join-alias": "Accounts+User+-+User"}],
                        ["field", 156, {
                            "join-alias": "Accounts+User+-+User"}],
                        ["field", 158, {
                            "join-alias": "Accounts+User+-+User"}],
                        ["field", 144, {
                            "join-alias": "Accounts+User+-+User"}],
                        ["field", 159, {
                            "join-alias": "Accounts+User+-+User"}],
                        ["field", 151, {
                            "join-alias": "Accounts+User+-+User"}],
                        ["field", 146, {
                            "join-alias": "Accounts+User+-+User"}],
                        ["field", 147, {
                            "join-alias": "Accounts+User+-+User"}]
                    ],
                    "source-table": 32,
                    "condition": ["=", ["field", 443, None],
                                  ["field", 151, {"join-alias": "Accounts+User+-+User"}]],
                    "alias": "Accounts+User+-+User"
                }
            ]
        },
    }

    response = requests.post(f'{url}api/dataset/', headers=headers, json=data)
    if response.status_code == 202:
        return response.json()
    else:
        response.raise_for_status()


def export_excel(form_id):
    headers = {
        "X-Metabase-Session": session_data.get("id"),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "query": '{"database":2,"type":"query","query":{"source-table":60,"filter":["=",["field",779,null],' + f'{form_id}' + '],"joins":[{"fields":[["field",142,{"join-alias":"Accounts+User+-+User"}],["field",156,{"join-alias":"Accounts+User+-+User"}],["field",158,{"join-alias":"Accounts+User+-+User"}],["field",157,{"join-alias":"Accounts+User+-+User"}],["field",144,{"join-alias":"Accounts+User+-+User"}],["field",161,{"join-alias":"Accounts+User+-+User"}],["field",150,{"join-alias":"Accounts+User+-+User"}],["field",159,{"join-alias":"Accounts+User+-+User"}],["field",146,{"join-alias":"Accounts+User+-+User"}],["field",147,{"join-alias":"Accounts+User+-+User"}],["field",163,{"join-alias":"Accounts+User+-+User"}],["field",152,{"join-alias":"Accounts+User+-+User"}],["field",154,{"join-alias":"Accounts+User+-+User"}],["field",153,{"join-alias":"Accounts+User+-+User"}],["field",162,{"join-alias":"Accounts+User+-+User"}]],"source-table":32,"condition":["=",["field",443,null],["field",151,{"join-alias":"Accounts+User+-+User"}]],"alias":"Accounts+User+-+User"}],"fields":[["field",446,null],["field",444,null],["field",448,null],["field",447,null],["field",707,null]]},"middleware":{"js-int-to-string?":true,"add-default-userland-constraints?":true}}'
    }
    response = requests.post(
        f'{url}api/dataset/xlsx', headers=headers, data=data)

    if response.status_code == 200:
        in_memory_file = SimpleUploadedFile("test.xlsx", response.content)
        file = FileSerializer(data={"file": in_memory_file})
        file.is_valid(raise_exception=True)
        file.save()
        return file.data
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")


def get_all_user_answer(form_id):
    headers = {
        "X-Metabase-Session": session_data.get("id"),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "query": '{"database":2,"type":"query","query":{"source-table":60,"joins":[{"fields":"none","source-table":35,"condition":["=",["field",446,null],["field",271,{"join-alias":"Fsm+Answersheet+-+Answersheet+Ptr"}]],"alias":"Fsm+Answersheet+-+Answersheet+Ptr"},{"fields":"none","source-table":106,"condition":["=",["field",271,{"join-alias":"Fsm+Answersheet+-+Answersheet+Ptr"}],["field",269,{"join-alias":"Fsm+Answer"}]],"alias":"Fsm+Answer"},{"fields":"none","source-table":96,"condition":["=",["field",263,{"join-alias":"Fsm+Answer"}],["field",449,{"join-alias":"Fsm+Smallanswer"}]],"alias":"Fsm+Smallanswer"},{"fields":"none","source-table":117,"condition":["=",["field",450,{"join-alias":"Fsm+Smallanswer"}],["field",430,{"join-alias":"Fsm+Problem+-+Problem"}]],"alias":"Fsm+Problem+-+Problem"},{"fields":"none","source-table":46,"condition":["=",["field",263,{"join-alias":"Fsm+Answer"}],["field",288,{"join-alias":"Fsm+Biganswer"}]],"alias":"Fsm+Biganswer"},{"fields":"none","source-table":107,"condition":["=",["field",263,{"join-alias":"Fsm+Answer"}],["field",466,{"join-alias":"Fsm+Uploadfileanswer"}]],"alias":"Fsm+Uploadfileanswer"},{"fields":"none","source-table":9,"condition":["=",["field",263,{"join-alias":"Fsm+Answer"}],["field",371,{"join-alias":"Fsm+Multichoiceanswer+Choices"}]],"alias":"Fsm+Multichoiceanswer+Choices"},{"fields":"none","source-table":66,"condition":["=",["field",372,{"join-alias":"Fsm+Multichoiceanswer+Choices"}],["field",300,{"join-alias":"Fsm+Choice+-+Choice"}]],"alias":"Fsm+Choice+-+Choice"},{"fields":"none","source-table":32,"condition":["=",["field",443,null],["field",151,{"join-alias":"Accounts+User+-+User"}]],"alias":"Accounts+User+-+User"}],"expressions":{"ans":["concat",["field",451,{"join-alias":"Fsm+Smallanswer"}],["field",290,{"join-alias":"Fsm+Biganswer"}],["field",467,{"join-alias":"Fsm+Uploadfileanswer"}],["field",303,{"join-alias":"Fsm+Choice+-+Choice"}]],"نام+و+نام+خانوادگی":["concat",["field",142,{"join-alias":"Accounts+User+-+User"}],"+",["field",156,{"join-alias":"Accounts+User+-+User"}]],"phone":["field",144,{"join-alias":"Accounts+User+-+User"}]},"fields":[["field",446,null],["expression","ans"],["expression","نام+و+نام+خانوادگی"],["expression","phone"]],"filter":["=",["field",779,null],'+f'{form_id}' + ']},"middleware":{"js-int-to-string?":true,"add-default-userland-constraints?":true}}'
    }
    response = requests.post(
        f'{url}api/dataset/xlsx', headers=headers, data=data)

    if response.status_code == 200:
        in_memory_file = SimpleUploadedFile("test.xlsx", response.content)
        file = FileSerializer(data={"file": in_memory_file})
        file.is_valid(raise_exception=True)
        file.save()
        print("File created successfully:")
        return file.data
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")


@api_view(["post"])
def get_user_excel(request):
    id = request.data.get('form_id')
    file_content = export_excel(form_id=id)
    return Response(file_content)


@api_view(["post"])
def get_answer_excel(request):
    id = request.data.get('form_id')
    file_content = get_all_user_answer(form_id=id)
    return Response(file_content)
