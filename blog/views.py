from django.shortcuts import render, redirect, reverse
from .models import BlogModel, BlogComment

from django.contrib.auth import get_user_model
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView, TemplateView
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

# Create your views here.

USER = get_user_model()

class BlogListView(ListView):
    model = BlogModel
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = BlogModel.objects.all()
        context['blog'] = blog
        return context


class BlogDetailView(DetailView):
    model = BlogModel
    template_name = 'blog/detail.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_id = self.kwargs['pk']
        blog = BlogModel.objects.get(id=blog_id)
        comments = BlogComment.objects.filter(blog=blog, parent=None)
        replies = BlogComment.objects.filter(blog=blog).exclude(parent=None)
        replyDict = {}
        for reply in replies:
            if reply.parent.id not in replyDict.keys():
                replyDict[reply.parent.id] = [reply]
            else:
                replyDict[reply.parent.id].append(reply)
        
        context['comments'] = comments
        context['blog'] = blog
        context['reply'] = replyDict
        return context


@login_required
def create_comment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            body = request.POST.get('body')
            blog_id = request.POST.get('blog_id')
            comment_id = request.POST.get('comment_id')

            blog = BlogModel.objects.get(id=blog_id)
            if comment_id == '':
                comment = BlogComment.objects.create(user=user, blog=blog, body=body, name=user.username)
                comment.save()
                messages.success(request, 'Your comment has been posted successfully')
            else:
                parent = BlogComment.objects.get(id=comment_id)
                comment = BlogComment.objects.create(user=user, blog=blog, body=body, name=user.username, parent=parent)
                comment.save()
                messages.success(request, 'Your reply has been posted successfully')

        return redirect(f'detail/{blog_id}')
    else:
        message.info(request, 'You must login to post comment')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   