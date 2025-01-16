from django.db import models
from django.utils import timezone
from member.models import Member
from datetime import datetime

class BoardTable(models.Model):
  title = models.CharField(max_length=100, null=False ) # 게시판 제목
  content = models.CharField(max_length=300, null=False ) # 게시판 내용 
  save_date = models.DateField(default=timezone.now) #현재날짜 자동 추가
  file_name = models.CharField(max_length=100, blank=True ) # 이미지, 동영상 저장용
  user_id = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='board') # 작성자 id
  user_name = models.CharField(max_length=100) # 작성자 이름
  likes = models.ManyToManyField(Member, related_name='likes') # 좋아요
  hit = models.IntegerField(default=0) # 조회수

class ReplyTable(models.Model):
  user_id = models.CharField(max_length=100, null=False)  # 접속한 사용자(나) 아이디(username)
  title = models.CharField(max_length=100, null=False )   # 내가 댓글다는 글의 제목
  content = models.CharField(max_length=300, null=False ) # 댓글 내용
  save_date = models.DateTimeField(auto_now_add=True)      # 내가 댓글 쓴 시간
  write_group = models.ForeignKey(BoardTable,on_delete=models.CASCADE)  # 내가 댓글다는 글
  write_id = models.ForeignKey(Member, on_delete=models.CASCADE)        # 접속한 사용자(나) 아이디(id)

