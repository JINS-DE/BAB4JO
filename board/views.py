from django.shortcuts import render,redirect
from .models import BoardTable
from .models import ReplyTable
from .board_forms import BoardForm
from datetime import datetime
from django.http import HttpResponse
from django.core.paginator import Paginator
import os
import mimetypes
from django.utils import timezone

path = "./static/image/"

searched=[]
def b_search(req):
    cnt_li=[] #게시판들의 제목과 검색이 일치하는 글자 수 리스트
    index_li=[] #cnt_li의 최대값index 번호 리스트
    data_li=[] # 최대값의 데이터가 있는 쿼리들을 리스트에 포함
    if req.method == "POST":
        # search=req.POST.get("search")
        if len(searched)==0:    
            pass
        else:
            del searched[0]
        search_text=req.POST.get("search")
        searched.append(search_text)

    # print("====================",searched,"====================")
    data = BoardTable.objects.order_by("-id")
    for i in range(len(data)):
        cnt=0
        for j in searched[0]:
            if j in data[i].title:
                cnt+=1
        cnt_li.append(cnt)
    cnt=0
    for i in cnt_li:
        if max(cnt_li)==i:
            index_li.append(cnt)
        cnt+=1
    # print("cnt_li=>",cnt_li) 
    # print("index_li=>",index_li) 
    for i in index_li:
        data_li.append(data[i])
    # print("data_li====>",data_li)
    
    if len(cnt_li)==len(index_li):
        msg = "검색결과 없습니다."
        url = "/"
        return HttpResponse( getMessage(url, msg) )

    start = req.GET.get("start",1)
    p = Paginator(data_li, 4)
    context= {"data":p.page(start),"search":searched[0]}
    return render(req,'board/search_list.html', context)

def list(req):
    reply=[] # key값 boardTable 값 : vlaue 값 key에 해당하는 댓글의 개수
    start = req.GET.get("start",1)
    data=BoardTable.objects.order_by("-id") # 업데이트순 정렬
    for i in data:
        reply.append({i:len(ReplyTable.objects.filter(write_group= i.id))})
    p = Paginator(reply, 4)
    context= {"data":p.page(start)}
    return render(req,'board/list.html', context)

    
def getFileName(fileName):
    date = datetime.now()
    return f"{date.hour}{date.minute}{date.second}-{fileName}"

def write(req):
    if req.user.is_active:
        if req.method == "POST":
            file = req.FILES.get("file")
            fileName = ""
            if file != None:
                fileName = getFileName( str(file) )
                #print("fileName : ",fileName)
                
                upFile = open(path+fileName,"wb")
                for chunk in file.chunks():
                    upFile.write(chunk)
                upFile.close()
            else:
                fileName = "nan"
            
            copyPost = req.POST.copy()
            copyPost['file_name'] = fileName
            copyPost['user_id'] = req.user.id

            form = BoardForm( copyPost )
            if form.is_valid():
                form.save()

            b=BoardTable.objects.order_by('-id')            
            return redirect("b_detail",b[0].id)

        return render(req,'board/write.html')
    else:
        msg = "로그인 후 글쓰기 가능합니다"
        url = "/member/login"
        return HttpResponse( getMessage(url, msg) )

def getMessage(url, msg):
    msg = "<script>alert('"+msg+"');"
    msg += "location.href='"+url+"';</script>"
    return msg

def fileDelete(num) :
    b_list = BoardTable.objects.filter(user_id = num)
    # 유저가 게시글을 작성하면 id가 모두 같다.
    # id가 같으면 게시글을 모두 가져와야 한다
    # 가져온 게시글의 파일명이 'nan이 아니면 파일 이미지도 지워야 한다
    if len(b_list) !=0:
        for i in b_list:
            if i.file_name !='nan' :
                os.remove(path+i.file_name)


def detail(req, num):
    # print("====",ReplyTable.objects.filter(write_group= num),"====")
    reply_cnt = len(ReplyTable.objects.filter(write_group= num))
    print("======================궁ㄱ매",ReplyTable.objects.filter(write_group= num))
    val = BoardTable.objects.get(id=num)
    val.hit += 1
    val.save()
    context= {"list": val,"reply_cnt":reply_cnt}
    return render(req, 'board/detail.html', context)

def download(request, file_name):
  filePath = path+file_name
  if os.path.exists(filePath):
    readFile = open(filePath , 'rb')
    mime_type, encoding = mimetypes.guess_type(filePath)
    #print( mime_type )
    #print( encoding )
    response = HttpResponse(readFile.read(), 
                                content_type=mime_type)
    response['Content-Disposition']='attachment;filename='+file_name
    return response

def delete(req, num) :
    model = BoardTable.objects.get(id = num) 
    fileDelete(num)
    model.delete()
    return redirect('b_list')

def modify(req, num):
    if req.method == 'POST':
        model = BoardTable.objects.get(id = num)
        file = req.FILES.get("file")
        if file != None:
            fileName = getFileName( str(file) )
            fileSave(file, fileName)
            if model.file_name != 'nan':
                os.remove(path + model.file_name )
        else:
            fileName = model.file_name
        copyPost = req.POST.copy()
        copyPost['file_name'] = fileName
        copyPost['user_id'] = req.user.id
        form = BoardForm( copyPost, instance = model)
        if form.is_valid():
            form.save()
        return redirect("b_detail", num)
    return render(req, 'board/modify.html',
                {"list":BoardTable.objects.get(id=num)})
                
def fileSave(file, fileName):
    upFile = open(path+fileName, "wb")
    for chunk in file.chunks():
        upFile.write(chunk)
    upFile.close()
