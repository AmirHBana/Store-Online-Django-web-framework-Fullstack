from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

messages = {
    'required':'.لطفاٌ اين فيلد را كامل نماييد',
    'invalid':'.لطفا يك ايميل معتبر وارد نماييد',
    'max_length':'.تعداد كارامتر ورودي كمتر از حد مجاز است'
}
class UserRegistrationForm(forms.Form):
    username = forms.CharField(label="نام کاربری",widget=forms.TextInput(attrs={'class':'form-control'}), error_messages=messages)
    email = forms.EmailField(label="ایمیل یا جیمیل",widget=forms.EmailInput(attrs={'class':'form-control'}), error_messages=messages)
    password1 = forms.CharField(label="رمزعبور", widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Your Password'}), error_messages=messages)
    password2 = forms.CharField(label='تایید رمزعبور', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Your Password'}), error_messages=messages)


    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user == True:
            raise ValidationError('This Email alreadey exists!')
        return email
    
    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user == True:
            raise ValidationError('This username alreadey exists!')
        return username
    
    def clean(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError('Passwords NOT match!')
        

class UserLoginForm(forms.Form):
    username = forms.CharField(label="نام کاربری",widget=forms.TextInput(attrs={'class':'form-control'}), error_messages=messages)
    password = forms.CharField(label="رمزعبور",widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Your Password'}), error_messages=messages)        