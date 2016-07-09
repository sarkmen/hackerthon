from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Idea, Comment
from .forms import IdeaForm, CommentForm
from hackerthon.decorators import user_wrote_this
def index(request):
    return render(request, 'idea/index.html', {
        })

def idea_list(request):
    idea_list = Idea.objects.all()
    return render(request, 'idea/idea_list.html', {'idea_list': idea_list})

@login_required
def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.idea = idea
            comment.author = request.user
            comment.save()
            return redirect("idea:idea_detail", pk = idea.pk)
    else:
        form = CommentForm()
        comments = Comment.objects.filter(idea = idea)
        return render(request, 'idea/idea_detail.html', {
            'idea' : idea,
            'comments' : comments,
            'form' : form,
            })

@login_required
@user_wrote_this(Idea)
def idea_new(request):
    if request.method == "POST":
        form = IdeaForm(request.POST, request.FILES)
        print(form.is_valid())
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
@user_wrote_this(Idea)
def idea_del(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    idea.delete()
    return redirect('idea:idea_list')

@login_required
@user_wrote_this(Comment)
def comment_edit(request, idea_pk, pk):
    idea = get_object_or_404(Idea, pk=idea_pk)
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            return redirect('idea:idea_detail', pk=idea_pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'idea/comment_form.html', {
        'form' : form,
        })

@login_required
@user_wrote_this(Comment)
def comment_del(request, idea_pk, pk):
    idea = get_object_or_404(Idea, pk=idea_pk)
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('idea:idea_detail', idea_pk)


def recommend(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    idea.recommend += 1
    request.user.recommend -= 1
    return redirect('index')


def recommend_del(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    idea.recommend -= 1
    request.user.recommend += 1
    return redirect('index')


def post(request):
    return render(request, "idea/post.html")

def location(request):
    return render(request, "idea/location.html")