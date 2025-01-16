from django.shortcuts import render, redirect
from .models import Member
from django.contrib import auth
from .member_forms import UserModifyForm, UserCreateForm
import mimetypes
import os
from django.http import HttpResponse
from datetime import datetime

path = "./static/image/"

def register(req):
  if req.method == 'POST':
    file = req.FILES.get("file")
    MBTI=req.POST.get("MBTI").upper()
    fileName=""
    if file != None:
      fileName = getFileName(str(file))
      upFile = open(path+fileName,'wb')
      for chunk in file.chunks():
        upFile.write(chunk)
      upFile.close()
    else:
      fileName = "nan"
    print(fileName)
    copyPost = req.POST.copy()
    copyPost['MBTI']=MBTI
    copyPost['profile'] = fileName
    print(copyPost['profile'],copyPost['username'])
    form = UserCreateForm(copyPost)
    print("=========",form.is_valid())
    for i in form:
      print(str(i))
    if form.is_valid():
        print(">>>>>>>>>>>>>>>성공<<<<<<<<<<<")
        form.save()
    else:
        a = form.errors.as_data()
        print(a)
    return redirect('m_login')
  else:
    return render(req,'member/register.html')


def membership(req):
  users = Member.objects.all()
  return render(req,'member/membership.html', {"users":users})

def info(req, id):
  info = Member.objects.get(id = id)
  return render(req,'member/info.html', {"info":info})

def delete(req, id):
  info = Member.objects.get(id = id)
  info.delete()
  # info = Member.objects.all()
  # info.delete()
  return redirect("m_logout")

def getFileName(fileName):
    date = datetime.now()
    return f"{date.hour}{date.minute}{date.second}-{fileName}"

def m_download(req, profile):
    if profile == "nan":
        filePath = path+"DONOTDELETE_DY/"+profile+".jpeg"  
        if os.path.exists(filePath):
            readFile = open(filePath , 'rb')
            mime_type, encoding = mimetypes.guess_type(filePath)
            response = HttpResponse(readFile.read(), content_type=mime_type)
            response['Content-Disposition']='attachment;filename='+profile  
            return response
    else: 
        filePath = path+profile
        if os.path.exists(filePath):
            readFile = open(filePath , 'rb')
            mime_type, encoding = mimetypes.guess_type(filePath)
            response = HttpResponse(readFile.read(), content_type=mime_type)
            response['Content-Disposition']='attachment;filename='+profile  
            return response

def fileSave(file, fileName):
    upFile = open(path+fileName, "wb")
    for chunk in file.chunks():
        upFile.write(chunk)
    upFile.close()

def modify(req,id):
    if req.method == 'POST':
        model = Member.objects.get(id = id)
        file = req.FILES.get("file")
        if file != None:
            fileName = getFileName( str(file) )
            fileSave(file, fileName)
            if model.profile != '':
              os.remove(path + model.profile )
        else:
            fileName = model.profile
        copyPost = req.POST.copy()
        copyPost['profile'] = fileName
        form = UserModifyForm( copyPost, instance = model)
        if form.is_valid():
          data = form.save(commit=False)
          if model.password != req.POST.get('password'):
            data.set_password(req.POST.get('password'))
            auth.login(req, model)
          data.save()
        return redirect("m_info", model.id)
    return render(req, 'member/modify.html',{"info":Member.objects.get(id=id)})
        


