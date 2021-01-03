from django.shortcuts import render, redirect
from django.http import HttpResponse
import pandas as pd

# Create your views here.
def calculate(request):
    print("calculate")
    file = request.FILES['fileInput']
    # file = request.FILES.get('fileInput')
    # print(file)
    df = pd.read_excel(file, sheet_name='Sheet1', header=0)
    print(df.head(5))
    return HttpResponse("calculate, calculate function")
