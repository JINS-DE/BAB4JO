from django import forms
from .models import BoardTable

class BoardForm(forms.ModelForm) :
    class Meta :
        model = BoardTable
        fields = ('user_id', 'title', 'content', 'user_name', 'file_name')

from .models import ReplyTable
class ReplyForm(forms.ModelForm) :
    class Meta :
        model = ReplyTable
        fields = ('user_id', 'title', 'content', 'write_group', 'write_id')         