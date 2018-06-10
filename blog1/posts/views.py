from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import PostForm, UserForm, CommentForm
from .models import Post, Comment


def user_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/posts/')
    else:
        return render(request, "login.html")


def user_logout(request):
    logout(request)
    queryset = Post.objects.filter(draft=False).order_by("-timestamps")
    query = request.GET.get("q")
    if query:
        queryset = queryset.filter(title__icontains=query)
    context = {
    "object_list": queryset,
    "title": "Bez zalogowania"
    }
    return render(request, "logout.html", context)


def comment_create(request, pk=None):
    instance = get_object_or_404(Post, id=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = instance
        comment.save()
        messages.success(request, "Dododles komentarz")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "instance": instance,
        "form": form
    }
    return render(request, "comment_form.html", context)


def post_create(request):
    if not request.user.is_authenticated():
        raise Http404
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Pomyslnie dodales post")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Post nie zostal dodany")
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_detail(request, pk=None):
    instance = get_object_or_404(Post, id=pk)
    queryset = Comment.objects.all().order_by("comment_date")
    context = {
        "title": instance.title,
        "instance": instance,
        "object_list": queryset
    }
    return render(request, "post_detail.html", context)


def post_list(request):
    if request.user.is_authenticated():
        queryset = Post.objects.all().order_by("-timestamps")
        query = request.GET.get("q")
        if query:
            queryset = queryset.filter(title__icontains=query)
        context = {
        "object_list": queryset,
        "title": "Po zalogowaniu"
        }

    else:
        queryset = Post.objects.filter(draft=False).order_by("-timestamps")
        query = request.GET.get("q")
        if query:
            queryset = queryset.filter(title__icontains=query)
        context = {
        "object_list": queryset,
        "title": "Bez zalogowania"
        }
    return render(request, "post_list.html", context)


def post_update(request, pk=None):
    instance = get_object_or_404(Post, id=pk)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": instance.title,
        "instance": instance,
        "form": form
    }
    return render(request, "post_form.html", context)


def post_delete(request, pk=None):
    instance = get_object_or_404(Post, id=pk)
    instance.delete()
    messages.success(request, "Pomyslnie usunales post")
    return redirect("posts:list")


class UserFormView(View):
    form_class = UserForm
    template_name = 'register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request,self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('posts:list')
        return render(request, self.template_name, {'form': form})
