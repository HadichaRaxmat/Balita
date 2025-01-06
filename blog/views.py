from django.shortcuts import render, redirect
from blog.models import Post, Comment, Contact, Category
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.paginator import Paginator
from django.http import HttpResponseServerError
from django.db.models import Q
import requests

BOT_TOKEN = '7049827349:AAEGygN8m8c0wyMm8NjBHw5uSA2OSNtMGCg'
CHAT_ID = '7072790607'


def home_view(request):
    data = request.GET
    posts = Post.objects.filter(is_published=True).order_by('-view_count')[:3]
    categories = Category.objects.all()
    page_obj = Paginator(posts, 1)
    page = data.get('page', 1)
    d = {
        'posts': page_obj.get_page(page),
        'categories': categories,
        'comments': Comment.objects.all(),
        'home': 'active'
    }
    return render(request, 'index.html', context=d)


def category_view(request, id):
    data = request.GET
    posts = Post.objects.filter(category_id=id)
    categories = Category.objects.all()
    category_name = Category.objects.filter(id=id)
    page_obj = Paginator(posts, 1)
    page = data.get('page', 1)
    d = {
        'posts': page_obj.get_page(page),
        'categories': categories,
        'category_name': category_name[0]
    }
    return render(request, 'category.html', context=d)


def about_view(request):
    categories = Category.objects.all()
    return render(request, 'about.html', {'categories': categories})


def contact_view(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        data = request.POST
        obj = Contact.objects.create(name=data['name'], phone=data['phone'],
                                     email=data['email'], message=data['message'])
        obj.save()
        text = f"""
                project: BALITA \nid: {obj.id} \nname: {obj.name} \nemail: {obj.email} \nphone: {obj.phone} 
                \nmessage: {obj.message} \ntimestamp: {obj.created_at}
                """
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}'
        response = requests.get(url)
        print(response)
        return redirect('/contact')
    return render(request, 'contact.html', {'contact': 'active', 'categories': categories})


def blog_detail_view(request, id):
    if request.method == 'POST':
        data = request.POST
        comment = Comment.objects.create(post_id=id, name=data['name'], email=data['email'], message=data['message'])
        comment.save()
        return redirect(f'/blog/{id}/')
    post = Post.objects.get(id=id)
    post.view_count += 1
    post.save(update_fields=['view_count'])
    comments = Comment.objects.filter(post_id=id, is_published=True)
    categories = Category.objects.all()
    return render(request, 'blog-single.html', {'post': post, 'comments': comments,
                                                'categories': categories, 'blog': 'active'})


@receiver(post_save, sender=Comment)
def update_post_comments_count(sender, instance, **kwargs):
    post = instance.post
    post.comments_count = Comment.objects.filter(post=post).count()
    post.save(update_fields=['comments_count'])


@receiver(post_save, sender=Post)
def update_category_posts_count(sender, instance, **kwargs):
    category = instance.category
    category.posts_count = Post.objects.filter(category=category).count()
    category.save(update_fields=['posts_count'])


