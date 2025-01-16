from rest_framework.response import Response
from rest_framework.decorators import api_view
from board.models import BoardTable
from member.models import Member
from .models import ReplyTable
from .board_forms import ReplyForm
from django.utils import timezone
# blog_search
import requests
from bs4 import BeautifulSoup
# blog_list 정렬
from django.core import serializers
from django.http import JsonResponse
# list 정렬
import json

@api_view(["GET", "PUT"])
def like(req):
    user = Member.objects.get(username=req.user.username)
    dict_likes = {}
    #print("req.data.get(num) : " , req.data.get("num"))
    # 좋아요 하트 바꾸기
    if req.method == "PUT":
        print('req.data.get("num") : ', req.data.get("num"))
        board = BoardTable.objects.get(id=req.data.get("num"))
        if user in board.likes.all():
            board.likes.remove(user)
            heart = 1   # 빈하트
        else:
            board.likes.add(user)
            heart = 0   # 빨강하트
        board.save()
        dict_likes["likes"] = heart
    elif req.method == "GET":
        print('req.GET.get("num") : ', req.GET.get("num"))
        print('type(req.GET.get("num")) : ', type(req.GET.get("num")))
        board = BoardTable.objects.get(id=req.GET.get("num"))

    # 좋아요한 사용자 list 생성
    # list(board.likes.all())를 바로 넘기면 json error 발생함
    #print(board.likes.all())
    #print(list(board.likes.all()))
    likes_users = []
    likes_usersProfile = []
    list_likes = list(board.likes.all())
    for like in list_likes:
        #print("like : ", type(like))  # <class 'member.models.Member'>
        likes_users.append(str(like))
        profile = Member.objects.get(username=str(like)).profile
        if profile == "":
            likes_usersProfile.append("DONOTDELETE_DY/profile.jpg")
        else:
            likes_usersProfile.append(profile)
    dict_likes["profile"] = likes_usersProfile
    dict_likes["likes_users"] = likes_users
    print("likes_users : ", likes_users)
    print("profile : ", likes_usersProfile)

    # 좋아요한 사용자 수
    dict_likes["likes_cnt"] = board.likes.count()
    #print("board.likes.count() : ", board.likes.count())

    #print("===> dict_likes : ", dict_likes)
    return Response(dict_likes)

@api_view(['POST'])
def add_reply(request):
    form = ReplyForm(request.POST)
    #print("=======form : ", form)
    #print("=======form.is_valid() : ", form.is_valid())
    if form.is_valid():
        form.save()

    #print("request.POST['user_id'] : ", request.POST['user_id']) # ""->"non-user" / euna
    #print("request.POST['write_id'] : ", request.POST['write_id'])    # None / 18
    userID = request.POST['user_id']
    userProfile = Member.objects.get(id = request.POST['write_id']).profile
    userContent = request.POST['content']
    userdate = timezone.now()
    dict_newReply = {'user_id': userID, "content": userContent, 'profile': userProfile, 'userdate':userdate}
    #print("======dict_newReply : ", dict_newReply)
    return Response(dict_newReply)

@api_view(['GET'])
def reply_data(req, num):
    data = ReplyTable.objects.filter(write_group= num)
    data = ReplyTable.objects.filter(write_group=num).order_by('-save_date')
    #print("====", list(data.values()))    # querySet 안의 values 만 가져옴 (안에 시간있음)
    lsOfDict = list(data.values())
    #print('lsOfDict : ',lsOfDict) # 값 담아옴
    lsOfProfile = []
    for i in range(len(lsOfDict)):
        #print("lsOfDict[i] : ", lsOfDict[i])
        #print(lsOfDict[i]["save_date"]) #2023-01-13 19:00:1565:525
        profile = Member.objects.get(id=lsOfDict[i]["write_id_id"]).profile
        #print("===========profile : ", profile)
        lsOfProfile.append(profile)
    # 현재 시간 전송 (여기서 if문 작업해도 됨.)
    now = timezone.now()
    #print('year : ', now.year)
    #print('month : ', now.month)

    return Response({"replyData" : lsOfDict, "profile": lsOfProfile, "time": now})
    #return JsonResponse(list(data.values()),safe=False)     # safe=False : dict이 아니다

@api_view(['GET', 'POST'])
def edit_reply(request):
    if request.method == 'GET':
        targetID = request.GET.get("targetID")
        #print("targetID : ", targetID)
        targetData = ReplyTable.objects.get(id = targetID)
        #print("targetData : ", targetData)
        targetData.delete()
    elif request.method == 'POST':
        targetID = request.POST.get("targetID")
        newContent = request.POST.get("newContent")
        targetData = ReplyTable.objects.get(id = targetID)
        targetData.content = newContent
        targetData.save()
    return Response()


@api_view(['GET'])
def blog_search(request):
    #print("blog request.Get : ", request.GET.get("title"))
    res = requests.get(f"https://search.naver.com/search.naver?where=view&sm=tab_jum&query={request.GET.get('title')}")
    soup = BeautifulSoup(res.text, "html.parser")
    total = soup.select(".total_wrap") #블로그 한블럭 전체
    blog=[]
    for one in total:
        title = one.select_one(".total_area > a").text  #블로그 제목
        href = one.select_one(".total_area > a").get("href")   #블로그 href
        img = one.select_one("a > .thumb_fix > img")
        if img != None: #None으로 있는지 체크하고, 있으면 get("src")하기
            img = img.get("src")
        else:
            continue
        blog.append([title, href, img])
    return Response(blog)

@api_view(['GET'])
def map_load(request):
    res = requests.get(f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query={request.GET.get('title')}")
    soup = BeautifulSoup(res.text, "html.parser")
    # 이름 가져오기
    name = soup.select_one(".Fc1rA")
    if name != None:
        name = name.text
    elif soup.select_one(".place_bluelink") != None:
        name = soup.select_one(".place_bluelink").text
    else:
        name = ""   # 검색결과 없을 때
    #print("name : ", name)
    # 주소 가져오기
    addr = soup.select_one(".LDgIH")
    if addr != None:
        addr = addr.text
    else:
        addr = ""
    #print("addr : ", addr)
    tel = soup.select_one(".xlx7Q")
    if tel != None:
        tel = tel.text
    else:
        tel = ""
    #print("tel :", tel)
    util = soup.select_one(".zPfVt")
    if util != None:
        util = util.text
    else:
        util = ""
    #print("util :", util)
    # 전송할 dict 생성
    map_data = {'name': name, 'addr': addr, 'tel': tel,'util': util}
    return Response(map_data)

@api_view(['GET'])
def hit_top3(request):
    data = BoardTable.objects.all()
    top3_likes = [0]  # top3_likes 조회수 추출 위한 list
    top3 = {}    # 조회수 top3인 게시글 아이디(순위순)

    # 모든 조회수 출력
    #for d in data:
    #    print("id :", d.id, " / hit :", d.hit)

    # top3 조회수 선별
    for d in data:
        if d.hit >= top3_likes[-1]:   # 최솟값보다 크면 추가
            top3_likes.append(d.hit)
            top3_likes.sort(reverse=True)
            if len(top3_likes) > 3:   # 상위 3개
                top3_likes.pop()
    #print("=====top3_likes : ", top3_likes) # 조회수 top3 선별 완료

    # 선별된 조회수의 게시글 정보 저장
    for rank in range(3):
        for d in data:
            if d.hit == top3_likes[rank]:
                if top3_likes[rank] == top3_likes[rank-1]:  # 공동순위이면
                    top3[rank+1] = {"id": d.id, "title": d.title, "username": d.user_name, "hit": d.hit, "likes": d.likes.count(), "filename": d.file_name, "profile": d.user_id.profile, "overlap": rank}
                    break   # 처음 값 저장
                else:
                    top3[rank+1] = {"id": d.id, "title": d.title, "username": d.user_name, "hit": d.hit, "likes": d.likes.count(), "filename": d.file_name, "profile": d.user_id.profile}    # 다음 값 저장
    #print("=====top3 : ", top3)

    return Response(top3)

@api_view(["GET"])
def likes_top3(request):
    data = BoardTable.objects.all()
    top3_likes = [0]  # top3_likes 좋아요수 추출 위한 list
    top3 = {}    # 조회수 top3인 게시글 아이디(순위순)
    # 모든 좋아요 출력
    #for d in data:
        #print("id :", d.id, " / likes.count :", d.likes.count())
    
    # top3 조회수 선별
    for d in data:
        if d.likes.count() >= top3_likes[-1]:   # 최솟값보다 크면 추가
            top3_likes.append(d.likes.count())
            top3_likes.sort(reverse=True)
            if len(top3_likes) > 3:   # 상위 3개
                top3_likes.pop()
    #print("=====top3_likes : ", top3_likes) # 조회수 top3 선별 완료

    # 선별된 조회수의 게시글 정보 저장
    for rank in range(3):
        for d in data:
            if d.likes.count() == top3_likes[rank]:
                if top3_likes[rank] == top3_likes[rank-1]:  # 공동순위이면
                    top3[rank+1] = {"id": d.id, "title": d.title, "username": d.user_name, "likes": d.likes.count(), "hit": d.hit, "filename": d.file_name, "profile": d.user_id.profile, "overlap": rank}
                    break   # 처음 값 저장
                else:
                    top3[rank+1] = {"id": d.id, "title": d.title, "username": d.user_name, "likes": d.likes.count(), "hit": d.hit, "filename": d.file_name, "profile": d.user_id.profile}    # 다음 값 저장
    #print("=====top3 : ", top3)

    return Response(top3)

@api_view(['GET'])
def list_array(request):
    likes_orderby={}
    criterion = request.GET.get("criterion")
    b_QuerySet=BoardTable.objects.all()       # QuerySet , type : <class 'django.db.models.query.QuerySet'>
    if criterion == "id":   # 업데이트순 정렬
        b_QuerySet = b_QuerySet.order_by("-id")
    elif criterion == 'hit':    # 조회순 정렬
        b_QuerySet = b_QuerySet.order_by("-hit")      # <QuerySet [<BoardTable: BoardTable object (7)>, <BoardTable: BoardTable object (6)>, <BoardTable: BoardTable object (8)>, <BoardTable: BoardTable object (9)>, <BoardTable: BoardTable object (10)>, <BoardTable: BoardTable object (15)>, <BoardTable: BoardTable object (13)>, <BoardTable: BoardTable object (12)>, <BoardTable: BoardTable object (11)>]>
    elif criterion == 'likes':  # 좋아요 갯수 순 정렬
        # b_QuerySet = b_QuerySet.order_by("-likes")
        for i in b_QuerySet:
            # print("==>",len(i.likes))
            likes_orderby[i]=len(i.likes.all()) #likes_orderby에 딕셔너리 추가
        likes_orderby = sorted(likes_orderby.items(), key=lambda x:x[1], reverse=True) #likes_orderby안에 value값으로 내림차순정렬
        # print(likes_orderby)
        b_QuerySet=[]
        for i in likes_orderby:
            b_QuerySet.append(i[0])
        print("+=======================",b_QuerySet)

    #print("======b_QuerySet : ", b_QuerySet)
    #print("======type(b_QuerySet) : ", type(b_QuerySet))  # <class 'django.db.models.query.QuerySet'>
    
    # json error : list를 새로 만들어서 list에 차례차례 정리해서 dict value 값으로 전송해야 할듯...
    # ==> 모든 data를 전송해야하므로 너무 노가다, 새로운 방법 googling해봄
    # json error 잡기 위해, queryset을 json형태로 변형 (참고 url : https://hayeon1549.tistory.com/30 )
    # 1. from django.core import serializers
    # 2. b_QuerySet = serializers.serialize('json', b_QuerySet)

    # 넘길 값이 하나일때
    #b_QuerySet_json = serializers.serialize('json', b_QuerySet)     # list of dict형태의 str
    # 넘길 값이 여러개일때
    b_QuerySet_json = json.loads(serializers.serialize('json', b_QuerySet))     # list of dict형태의 str
    

    #print("=====b_QuerySet_json : ", b_QuerySet_json)   # [{"model": "board.boardtable", "pk": 7, "fields": {"title": "미들웨이", "content": "동네에서 유 명빵집이라 하여 방문해봤어요\r\n첫방문이니 일단 베스트메뉴 위주로 초이스 했어요\r\n나쁘지 않네요\r\n두번 가고 싶진 않아 요\r\n리뷰 수정", "save_date": "2023-01-11", "file_name": "01124-미들웨이.png", "user_id": 17, "user_name": "admin", "hit": 551, "likes": [17, 18]}}, {"model": "board.boardtable", "pk": 6, "fields": {"title": "ccc", "content": "rr\r\nr\r\nr\r\nr", "save_date": "2023-01-11", "file_name": "192814-125446-do.png", "user_id": 16, "user_name": "fff", "hit": 325, "likes": [16, 17, 18]}}, {"model": "board.boardtable", "pk": 8, "fields": {"title": "피자헛", "content": "맛있네요 피자  치즈  추가\r\n엔터\r\n엔터\r\n엔터\r\n수정", "save_date": "2023-01-12", "file_name": "1154-피자.png", "user_id": 17, "user_name": "admin", "hit": 114, "likes": [17]}}, {"model": "board.boardtable", "pk": 9, "fields": {"title": "브런치빈", "content": "음 브런치 맛있네요\r\n냐미\r\n냠\r\n냠", "save_date": "2023-01-12", "file_name": "17315-브런치.png", "user_id": 17, "user_name": "admin", "hit": 31, "likes": [17]}}, {"model": "board.boardtable", "pk": 10, "fields": {"title": "대성식당", "content": "낙곱새 맛집 대성식당!!!!\r\n종로 3가 세운상가에 있는데, 엄청 유명한 곳입니다~", "save_date": "2023-01-12", "file_name": "22032-대성식당.jfif", "user_id": 18, "user_name": "euna", "hit": 11, "likes": []}}, {"model": "board.boardtable", "pk": 15, "fields": {"title": "이경문순대곱창", "content": "이경문순대곱창이경문순대곱창\r\n이경문순대곱창", "save_date": "2023-01-14", "file_name": "01320-대성식당.jfif", "user_id": 18, "user_name": "euna", "hit": 11, "likes": []}}, {"model": "board.boardtable", "pk": 13, "fields": {"title": "오얏꽃", "content": "익선동 이쁜 카페~", "save_date": "2023-01-14", "file_name": "1685-BEAVER.PNG", "user_id": 18, "user_name": "euna", "hit": 10, "likes": []}}, {"model": "board.boardtable", "pk": 12, "fields": {"title": "스타벅스", "content": "스벅스벅", "save_date": "2023-01-14", "file_name": "16538-1706ca85cc54ad9f8118da5e2c845b8c.gif", "user_id": 18, "user_name": "euna", "hit": 5, "likes": []}}, {"model": "board.boardtable", "pk": 11, "fields": {"title": "빠리가옥", "content": "빠리가옥빠리가옥\r\n빠리가옥\r\n빠리가옥 빠리가옥", "save_date": "2023-01-12", "file_name": "05927-빠리가옥.jpeg", "user_id": 18, "user_name": "euna", "hit": 2, "likes": []}}]
    # [
    #   {"model": "board.boardtable",
    #       "pk": 게시글 번호,
    #       "fields": {"title": "제목",
    #                  "content": "내용",
    #                  "save_date": "YYYY-mm-dd",
    #                  "file_name": "파일이름.확장자",
    #                  "user_id": 게시글작성자아이디번호,
    #                  "user_name": "게시글작성자닉네임",
    #                  "hit": 조회수,
    #                  "likes": [좋아요한 사용자 list]}
    #    }, ~~ 위 구조의 dict의 list 
    # ]

    # [{"model": "board.boardtable", "pk": 7, "fields": {"title": "미들웨이", "content": "[내용]", "save_date": "2023-01-11", "file_name": "01124-미들웨이.png", "user_id": 17, "user_name": "admin", "hit": 551, "likes": [17, 18]}},
    #  {"model": "board.boardtable", "pk": 6, "fields": {"title": "ccc", "content": "[내용]", "save_date": "2023-01-11", "file_name": "192814-125446-do.png", "user_id": 16, "user_name": "fff", "hit": 325, "likes": [16, 17, 18]}}, 
    #   ...
    # ]

    #print("=====type(b_QuerySet_json) : ", type(b_QuerySet_json))   # <class 'str'>

    #for d in b_QuerySet:
    #    print("======d : ", d)  # BoardTable object (7)
    #    print("======d.id : ", d.id)
    #    print("======d.user_id : ", d.user_id)
    #    print("======d.title : ", d.title)
    #    print("======type(d) : ", type(d))  # <class 'board.models.BoardTable'>

    return JsonResponse({"reload_all": False, "data": b_QuerySet_json})




