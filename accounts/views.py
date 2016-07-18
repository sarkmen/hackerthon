from django.shortcuts import render, redirect
from accounts.forms import SignupForm, ResumeForm
from django.contrib.auth import get_user_model, authenticate, login as auth_login
"""
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
"""

def resume(request):
    if request.method == "POST":
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect('idea:idea_list')
    else:
        form = ResumeForm()
    return render(request, 'accounts/resume_form.html', {'form':form,})