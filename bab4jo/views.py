from django.shortcuts import render
from member.models import Member


def index(req):
    if req.user.is_active:
        info = Member.objects.values("profile").get(id=req.user.id)
        return render(req,'main/index.html', info)
    else:
        return render(req, 'main/index.html')