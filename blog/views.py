from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm
from django.views.decorators.http import require_POST

# Create your views here.
def post_list(request):
    post_list = Post.published.all()

    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try : 
        posts = paginator.page(page_number) 
    except PageNotAnInteger : 
        posts = paginator.page(1)
    except EmptyPage:  #페이지 번호가 범위를 벗어난 경우 마지막 페이지 전달
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, 
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day) 
    # active 댓글 목록
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(request, 'blog/post/detail.html',
                   {'post':post, 'comments':comments, 'form':form})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'blog/post/comment.html', 
                  {'post':post, 'form':form, 'comment':comment})