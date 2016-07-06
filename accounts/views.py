from django.shortcuts import render, redirect
from accounts.forms import SignupForm
from django.contrib.auth import get_user_model, authenticate, login as auth_login

def sign_up(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            authenticated_user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1'],)
            auth_login(request, authenticated_user)
            return redirect("index")
    else:
        form = SignupForm()
        return render(request, 'accounts/signup_form.html',{'form': form,})
