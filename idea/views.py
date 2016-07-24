from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Idea, Comment, Vote
from .forms import IdeaForm, CommentForm
from hackerthon.decorators import user_wrote_this, get_resume
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from accounts.models import Resume

def index(request):
    social_accounts_kakao = SocialAccount.objects.filter(provider="kakao")
    kakaos = {}
    resume_list = Resume.objects.all()
    for resume in resume_list:
        for kakao in social_accounts_kakao:
            if int(resume.user.username[6:]) == kakao.extra_data['id']:
                kakaos[kakao.extra_data['id']] = resume.name + ',' + kakao.extra_data['properties']['profile_image'] + ',' + "resume" + ',' +resume.group + ',' + resume.position
    for kakao in social_accounts_kakao:
        if not kakao.extra_data['id'] in kakaos.keys():
            kakaos[kakao.extra_data['id']] = kakao.extra_data['name'] +','+ kakao.extra_data['properties']['profile_image'] + ',' +'kakao'
    return render(request, 'idea/index.html',{
        'kakaos':kakaos,
        })

def idea_list(request):
    idea_list = Idea.objects.all().annotate(vote_count = Count('vote')).order_by('-vote_count')
    return render(request, 'idea/idea_list.html', {'idea_list': idea_list})

def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return days, hours, minutes, seconds

def generate_elapsed_time(duration):
    day, hour, mins, sec = convert_timedelta(duration)
    if day >= 365:
        elapsed_time = str(day // 365) + ' year ago'
    elif day >= 30:
        elapsed_time = str(day // 30) + ' month ago'
    elif day >= 7:
        elapsed_time = str(day // 7) + ' week ago'
    elif day > 0:
        elapsed_time = str(day) + ' day ago'
    elif hour > 0:
        elapsed_time = str(hour) + ' hour ago'
    elif mins > 0:
        elapsed_time = str(mins) + ' minute ago'
    elif sec > 0:
        elapsed_time = str(sec) + ' seconds ago'
    else:
        elapsed_time = 'now'
    return elapsed_time


@login_required
@get_resume()
def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    request_post = request.POST.dict()
    if request.method == "POST" and request.is_ajax() and request_post['formtype'] == 'comment-add':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.idea = idea
            comment.author = request.user
            comment.save()
            local_now = timezone.localtime(timezone.now())
            comments = Comment.objects.filter(idea = idea)
            for comment in comments:
                comment.elapsed_time = generate_elapsed_time(local_now - comment.updated_at)
            context = {
                'idea' : idea,
                'comments' : comments,
            }
            return render(request, 'idea/idea_comment.html', context)
    elif request.method == "POST" and request.is_ajax() and request_post['formtype'] == 'comment-edit':
        # comment_edit(request, pk, str(request_post['comment']))
        comment = get_object_or_404(Comment, pk=request_post['comment'])
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            local_now = timezone.localtime(timezone.now())
            comments = Comment.objects.filter(idea = idea)
            for comment in comments:
                comment.elapsed_time = generate_elapsed_time(local_now - comment.updated_at)
            context = {
                'idea' : idea,
                'comments' : comments,
            }
            return render(request, 'idea/idea_comment.html', context)
    elif request.method == "POST":
        if Vote.objects.filter(vote_user = request.user).count()<4 and not Vote.objects.filter(vote_user=request.user, vote_idea=idea).exists():
            #메세지 넣기
            Vote.objects.create(vote_user=request.user, vote_idea = idea)
            return redirect('idea:idea_detail', pk=idea.pk)
        elif Vote.objects.filter(vote_user=request.user, vote_idea=idea).exists():
            Vote.objects.filter(vote_user=request.user, vote_idea=idea).delete()
            return redirect('idea:idea_detail', pk=idea.pk)
        else:
            #실패했다는 메세지 넣어야함
            return redirect('idea:idea_detail', pk=idea.pk)
    else:
        social_accounts = SocialAccount.objects.all()
        form = CommentForm()
        local_now = timezone.localtime(timezone.now())
        comments = Comment.objects.filter(idea = idea)
        vote = Vote.objects.filter(vote_user=request.user, vote_idea=idea).exists()
        for comment in comments:
            comment.elapsed_time = generate_elapsed_time(local_now - comment.updated_at)
        return render(request, 'idea/idea_detail.html', {
            'idea' : idea,
            'comments' : comments,
            'form' : form,
            'vote': vote,
            })


@login_required
@get_resume()
def idea_new(request):
    if request.method == "POST":
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.author = request.user
            idea.save()
            return redirect('idea:idea_detail', pk=idea.pk)
    else:
        form = IdeaForm()
    return render(request, 'idea/idea_form.html', {
        'form' : form,
        })


@login_required
@get_resume()
@user_wrote_this(Idea)
def idea_edit(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == "POST":
        form = IdeaForm(request.POST, request.FILES, instance=idea)

        if form.is_valid():
            idea = form.save()
            return redirect('idea:idea_detail', pk=idea.pk)
    else:
        form = IdeaForm(instance = idea)
    return render(request, 'idea/idea_form.html', {
        'form' : form,
        })


@login_required
@get_resume()
@user_wrote_this(Idea)
def idea_del(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    idea.delete()
    return redirect('idea:idea_list')


@login_required
@get_resume()
@user_wrote_this(Comment)
def comment_edit(request, idea_pk, pk):
    idea = get_object_or_404(Idea, pk=idea_pk)
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            local_now = timezone.localtime(timezone.now())
            comments = Comment.objects.filter(idea = idea)
            for comment in comments:
                comment.elapsed_time = generate_elapsed_time(local_now - comment.updated_at)
            context = {
                'idea' : idea,
                'comments' : comments,
            }
            return render(request, 'idea/idea_comment.html', context)
            # return redirect('idea:idea_detail', pk=idea_pk)
    # else:
    #     form = CommentForm(instance=comment)
    # return render(request, 'idea/comment_form.html', {
    #     'form' : form,
    #     })


@login_required
@get_resume()
@user_wrote_this(Comment)
def comment_del(request, idea_pk, pk):
    idea = get_object_or_404(Idea, pk=idea_pk)
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('idea:idea_detail', idea_pk)

"""
def users(request):
    social_accounts_facebook = SocialAccount.objects.filter(provider = "facebook")
    social_accounts_kakao = SocialAccount.objects.filter(provider="kakao")
    kakaos = {}
    facebooks = {}
    for kakao in social_accounts_kakao:
        kakaos[kakao.extra_data['id']] = kakao.extra_data['name'] +','+ kakao.extra_data['properties']['profile_image']
    for facebook in social_accounts_facebook:
        facebooks[facebook.extra_data['id']] = facebook.extra_data['name']

    return render(request, "idea/users.html", {'kakaos':kakaos,'facebooks': facebooks})
"""
def location(request):
    return render(request, "idea/location.html")
