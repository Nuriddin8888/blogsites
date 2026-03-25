from django.shortcuts import render, redirect, get_object_or_404    
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.decorators import login_required

from .forms import PersonRegister, UpdateProfile, BlogCreate, CommentForm

import requests
from django.contrib import messages
from .models import Blog, Person, Comment

from django.conf import settings
# Create your views here.


def register_view(request):

    if request.method == "POST":
        form = PersonRegister(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

    else:
        form = PersonRegister()

    return render(request, "register.html", {"form": form})




def login_view(request):

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")

    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})



def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def update_profile(request):
    if request.method == "POST":
        form = UpdateProfile(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('home')
    
    else:
        form = UpdateProfile(instance=request.user)

    return render(request, 'update_profile.html', {'form': form})




# views.py
def home_page(request):
    blogs = Blog.objects.all().order_by('-created_at')

    carousel_blogs = blogs[:3]   # eng yangi 3 ta
    other_blogs = blogs[3:]      # qolganlari

    context = {
        'carousel_blogs': carousel_blogs,
        'other_blogs': other_blogs,
    }

    return render(request, 'index.html', context)


@login_required
def create_blog_view(request):
    if request.method == "POST":
        form = BlogCreate(request.POST, request.FILES)

        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            form.save()
            return redirect('home')
        
    else:
        form = BlogCreate()

    return render(request, 'create_blog.html', {"form": form})


def about_page(request, id):
    person = get_object_or_404(Person, id=id)
    return render(request, 'about.html', {"person": person})


def blog_page(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'blog.html', {'blogs': blogs})

BOT_TOKEN = "8531087320:AAEfU_Qv52LV5LNXBjDMn7KR9v6LiARQ6vk"
CHAT_ID = 1921911753

def contact_page(request):
    if request.method == "POST":
        name = request.POST.get("name")
        telegram = request.POST.get("telegram")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        text = f"""
📩 Yangi xabar keldi!

👤 Ism: {name}
📱 Telegram: {telegram}
📌 Mavzu: {subject}
✉️ Xabar: {message}
        """

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        data = {
            "chat_id": CHAT_ID,
            "text": text
        }

        response = requests.post(url, data=data)

        if response.status_code == 200:
            messages.success(request, "Xabaringiz muvaffaqiyatli yuborildi!")
        else:
            messages.error(request, "Xabar yuborishda xatolik bo‘ldi!")

        return redirect("contact")

    return render(request, "contact.html")


def single_page(request, id):
    blog = get_object_or_404(Blog, id=id)

    comments = Comment.objects.filter(blog=blog, parent__isnull=True).order_by("-created_at")

    form = CommentForm()

    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)

            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.blog = blog

                parent_id = request.POST.get("parent_id")
                if parent_id:
                    parent_comment = Comment.objects.get(id=parent_id)
                    comment.parent = parent_comment

                comment.save()
                return redirect("single", id=blog.id)

    context = {
        "blog": blog,
        "comments": comments,
        "form": form,
    }
    return render(request, "single.html", context)