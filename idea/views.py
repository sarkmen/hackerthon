from django.shortcuts import render, redirect, get_object_or_404

from .models import Idea, Comment
from .forms import IdeaForm, CommentForm

def index(request):
    idea_list = Idea.objects.all()
    return render(request, 'idea/index.html', {
        'idea_list' : idea_list,
        })


def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    return render(request, 'idea/idea_detail.html', {
        'idea' : idea,
        })


def idea_new(request):
    if request.method == "POST":
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.author = request.user
            idea.save()
            return redirect(idea_detail, pk=idea.pk)
    else:
        form = IdeaForm()
    return render(request, 'idea/idea_form.html', {
        'form' : form,
        })


def idea_edit(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == "POST":
        form = IdeaForm(request.POST, request.FILES, instance=idea)
        if form.is_valid():
            idea = form.save()
            return redirect(idea_detail, pk=idea.pk)
    else:
        form = IdeaForm()
    return render(request, 'idea/idea_form.html', {
        'form' : form,
        })


def idea_del(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    idea.delete()
    return redirect('index')


def comment_detail(request, idea_pk, pk):
    idea = get_object_or_404(Idea, pk=idea_pk)
    comment = get_object_or_404(Comment, pk=pk)
    return render(request, 'idea/comment_detail.html', {
        'idea' : idea,
        'comment' : comment,
        })


def comment_new(request, idea_pk):
    idea = get_object_or_404(Idea, pk=idea_pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.idea = idea
            comment.author = request.user
            comment.save()
            return redirect(idea_detail, pk=idea_pk)
    else:
        form = CommentForm()
    return render(request, 'idea/comment_form.html', {
        'form' : form,
        })


def comment_edit(request, idea_pk, pk):
    idea = get_object_or_404(Idea, pk=idea_pk)
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            return redirect(idea_detail, pk=idea_pk)
    else:
        form = CommentForm()
    return render(request, 'idea/comment_form.html', {
        'form' : form,
        })


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