from django.shortcuts import render, redirect
from django.http import HttpResponse
import pandas as pd
from datetime import datetime
from .models import *
from django.conf import settings

# Create your views here.
def calculate(request):
    print("calculate")
    file = request.FILES['fileInput']
    # print("file1")
    # print(type(file))
    # print(file)
    # print(type(file.name))
    # print(file.name)

    origin_file_name = file.name
    user_name = request.session['user_name']
    now_HMS = datetime.today().strftime('%H%M%S')
    file_upload_name = now_HMS+'_'+user_name+'_'+origin_file_name
    file.name = file_upload_name
    # print("file upload")
    # print(file_upload_name)
    # print("previous db insert")
    # print(file)
    # document = Document(user_upload_file = file)
    document = Document.objects.create(user_upload_file=file)
    # print("previous db insert")
    # print(file)
    # print("document")
    # print(document)
    # print(document.__dict__)
    # print(document.user_upload_file.__dict__)
    loaction = document.user_upload_file.name
    # print("loaction")
    # print(loaction)
    document.save()
    # print("document2")
    # print(document)

    # print("after db insert")
    # print(file)
    # print("file2")
    # print(type(file))
    # print(file.name)
    # print(file)
    # print(settings.MEDIA_ROOT)
    # record = Document.objects.last()
    # path = record.user_upload_file
    # print("path")
    # print(type(path))
    # print(path.__dict__)
    # print(type(path.name))
    # path = settings.MEDIA_ROOT+"/"+path.name
    path = settings.MEDIA_ROOT+"/"+loaction
    # media\user_upload_files\210107\122651_jin_data.xlsx

    df = pd.read_excel(path, sheet_name='Sheet1', header=0)

    # df = pd.read_excel(origin_file_name, sheet_name='Sheet1', header=0)
    print(df.head(5))
    total_row_num = len(df.index)
    grade_dic= {
        # "1" : [84,17],
        # "2" : [],
    }
    for i in range(total_row_num):
        data = df.loc[i]
        # data = {
        #   "grade" : 1
        #   "name" : Belle Hunter
        # }
        if not data['grade'] in grade_dic.keys():
            grade_dic[data['grade']] = [data['value']]
        else:
            grade_dic[data['grade']].append(data['value'])
        grade_calculate_dic = {}

    for key in grade_dic.keys():
        grade_calculate_dic[key] = {
            # "min" : ,
            # "max" : ,
            # "avg" :
        }
        grade_calculate_dic[key]['min'] = min(grade_dic[key])
        grade_calculate_dic[key]['max'] = max(grade_dic[key])
        grade_calculate_dic[key]['avg'] = float( sum(grade_dic[key]) / len(grade_dic[key]) )
        grade_list = list(grade_calculate_dic.keys())
        grade_list.sort()

    # for key in grade_list:
    #     print("# grade : ", key)
    #     print("min : ", grade_calculate_dic[key]['min'], end="")
    #     print("/ max :", grade_calculate_dic[key]['max'], end="")
    #     print("/ avg : ", grade_calculate_dic[key]['avg'], end="\n\n")

    email_domain_dic = {}
    for i in range(total_row_num):
        data = df.loc[i]
        email_domain = (data["email"].split("@"))[1]
        if not email_domain in email_domain_dic.keys():
            email_domain_dic[email_domain] = 1
        else:
            email_domain_dic[email_domain] += 1
    # print("## EMAIL 도메인별 사용 인원")
    # print(key)
    # for key in email_domain_dic.keys():
    #     print("#", key, ":", email_domain_dic[key],"명")

    grade_calculate_dic_to_session = {}

    for key in grade_list:
        grade_calculate_dic_to_session[int(key)] = {}
        grade_calculate_dic_to_session[int(key)]['max'] = float(grade_calculate_dic[key]['max'])
        grade_calculate_dic_to_session[int(key)]['avg'] = float(grade_calculate_dic[key]['avg'])
        grade_calculate_dic_to_session[int(key)]['min'] = float(grade_calculate_dic[key]['min'])
        request.session['grade_calculate_dic'] = grade_calculate_dic_to_session
        request.session['email_domain_dic'] = email_domain_dic
    return redirect("/result")



    # return HttpResponse("calculate, calculate function")
