from django.shortcuts import render

from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login


from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.conf import settings
print(settings.AUTHENTICATION_BACKENDS)



class FormLogin(forms.Form):
    username = forms.CharField(label="E-mail")
    password = forms.CharField(widget=forms.PasswordInput)

class ViewLoginManual(TemplateView):
    def get(self, request, *args, **kwargs):
        form = FormLogin()
        return render(self.request, "accounts/login.html", {"form" : form})

    def post(self, *args, **kwargs):
        form = FormLogin(self.request.POST)
        if form.is_valid():
            user = authenticate(email = form.cleaned_data["username"],
                                password =form.cleaned_data["password"])
            if user is not None:
                if user.is_active:
                    login(self.request, user)
                    return HttpResponseRedirect(reverse("accounts:main"))
                else:
                    return render(self.request, "accounts/login.html", {
                        'error_message' : 'invalid credential',
                        "form" : form
                    })
            return render(self.request, "accounts/login.html")




def register(request):
    form = RegisterForm(request.POST or None)  # post olduysa giricek olmadysa yni get olduysa hic girmicek
    if form.is_valid():  # clean fonk cagrlir
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        newUser = User(username=username, email = email)
        newUser.set_password(password)
        newUser.save()

        login(request, newUser)  # automatic login after register
        messages.info(request, "Successful Registration")  # ADD SUCCESS FOR GREEN IF ANY PROBLEM OCCURS
        return redirect("index:indexpage")  # name olani klnncak
    context = {
        "form": form
    }
    return render(request, "user/register.html", context)

"""
def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username=username, password=password)  # db ye bak varmi ykmu
        print(user)

        if user is None:
            #print(user)
            messages.info(request, "Username or password is invalid")
            return render(request, "user/login.html", context)

        messages.success(request, "Successfully login")
        login(request, user)
        return redirect("index:indexpage")
    return render(request, "user/login.html", context)
"""

@login_required(login_url = "user:login")
def logoutUser(request):
    logout(request)
    messages.success(request, "Succesfull Logout")
    return redirect("accounts:logout")