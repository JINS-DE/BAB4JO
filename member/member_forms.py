from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from .models import Member

class UserModifyForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username','password','email',
        'last_name','first_name','ph_num',
        'birth','MBTI','addr1','addr2','addr3','profile')

class UserCreateForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ('username','password1','password2','email',
        'last_name','first_name','ph_num',
        'birth','MBTI','addr1','addr2','addr3','profile')