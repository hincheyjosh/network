from django import http
from django.contrib.auth import authenticate, login, logout
import json
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *

@login_required
def follow_user(request, id):
    user = request.user
    user_to_follow = User.objects.get(id=id)
    user.following.add(user_to_follow)
    user.save()
    return redirect(reverse('profile', kwargs={'username': user_to_follow.username}))

@login_required
def unfollow_user(request, id):
    user = request.user
    user_to_unfollow = User.objects.get(id=id)
    user.following.remove(user_to_unfollow)
    user.save()
    return redirect(reverse('profile', kwargs={'username': user_to_unfollow.username}))

@login_required
def following(request):
    user = request.user
    following = user.following.all()
    posts = Post.objects.filter(user__in=following).order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        'page_obj': page_obj
    })

@login_required
def profile(request, username):
    user = request.user
    profile_owner = User.objects.get(username=username)
    follow_list = user.following.all()
    posts = Post.objects.filter(user=profile_owner).order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    following = None

    if profile_owner in follow_list:
        following = True

    return render(request, 'network/profile.html', {
        'profile_owner': profile_owner,
        'following': following,
        'page_obj': page_obj
    })

@csrf_exempt
@login_required
def edit(request, id):
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)

    try:
        post = Post.objects.get(id=id)    
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    data = json.loads(request.body)
    if data.get("body") is not None:
        post.body = data["body"]
    post.save()
    return JsonResponse({
        "success": "Post updated."
    }, status=204)
    
@csrf_exempt
@login_required
def like(request, id):
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)

    try:
        post = Post.objects.get(id=id)    
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    user = request.user

    data = json.loads(request.body)
    if data.get("like") == 'yes':
        post.likes.add(user)
    else:
        post.likes.remove(user)

    post.save()

    data = [{'likes': int(post.total_likes())}]

    return JsonResponse(data, safe=False)





@login_required
def create(request):
    if request.method == "POST":
        body = request.POST["body"]
        user = request.user
        post = Post(user=user, body=body)
        post.save()
        return redirect(reverse('index'))
    
    form = CreatePost()
    return render(request, "network/create.html", {
        'form':  form
    })


def index(request):
    posts = Post.objects.order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        'page_obj': page_obj
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
