from django import forms
from .models import  Comment

messages = {
    'required':'',

}
class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets ={
            'body': forms.Textarea(attrs={'class':'form-control'})
        }   

class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)        


class SearchForm(forms.Form):
    search = forms.CharField(error_messages=messages)        