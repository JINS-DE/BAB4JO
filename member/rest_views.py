from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Member


@api_view(['get'])
def id_chk(req):
    bool = Member.objects.filter(username = req.GET.get("num")).exists()
    return Response( bool )


@api_view(['get'])
def get_data(req):
    users = Member.objects.get(id=req.GET.get("num"))
    users = users.__dict__
    del(users['_state'])
    return Response(users)

@api_view(['get'])
def main_header(req):
        info = Member.objects.values("profile").get(id=req.user.id) #딕셔너리 폼
        print("=======",info["profile"],"=======") # info = { profile : filename }
        return Response(info["profile"]) # info = { profile : filename }를 ajax로 전송