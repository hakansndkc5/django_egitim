from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from post.models import Post
from .forms import PostForm, CommentForm
from django.contrib import messages
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_create(request):
    
    if (request.method == 'POST'):
        form = PostForm(request.POST, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.title)
            post.save()
            messages.success(request, 'Başarılı bir şekilde oluşturuldu!')
        return HttpResponseRedirect('/post/index')
    else:
        form = PostForm()
        
    context = {
        'form' : form
    }
    return render(request, 'form.html',context)

def post_index(request):
    post_list = Post.objects.all()

    paginator = Paginator(post_list, 5)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return render(request, "index.html", {'posts' : posts})

def post_detail(request, id):

    post = get_object_or_404(Post,id=id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return HttpResponseRedirect('/post/index')
    context = {
        'post' : post,
        'form' : form
    }
    
    return render (request, "detail.html", context)



def post_update(request, id ):
    post = get_object_or_404(Post,id=id)

    form = PostForm(request.POST or None,request.FILES or None, instance=post)

    if form.is_valid():
            post = form.save()
            return HttpResponseRedirect('/post/index')


    context = {
        'form' : form
    }

    return render (request, "form.html", context)

def post_delete(request, id):
    post = get_object_or_404(Post,id=id)
    post.delete()
    return redirect('post:index')