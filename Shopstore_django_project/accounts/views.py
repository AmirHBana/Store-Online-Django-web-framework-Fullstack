from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from . forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from home.models import Product



class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'شما قبلا وارد حساب کاربری خود شده اید!', 'warning')
            return redirect('home:home')
        return super().dispatch(request,*args, **kwargs)


    def get(self, request):
        
        form = self.form_class()
        return render(request, self.template_name, {'form':form} )

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            messages.success(request, 'شما با موفقيت ثبت نام كرديد', 'success')
            return redirect('home:home')
        return render(request, self.template_name, {'form':form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request,'شما قبلا وارد حساب کاربری خود شده اید' , 'warning')
            return redirect('home:home')
        return super().dispatch(request,*args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username = cd['username'], password = cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'شما با موفقیت وارد شدید', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request, 'نام کاربری یا رمزعبور اشتباه است!', 'warning')
        return render(request, self.template_name, {'form':form})    
    

class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'شما از حساب کاربری خود خارج شدید', 'success')
        return redirect('home:home')
    

class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, username):
        user = get_object_or_404(User, username = username)
        products = user.products.all()
        return render(request, 'accounts/profile.html', {'user':user, 'products':products})    