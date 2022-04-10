import os
import shutil
import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import DeleteView, UpdateView
from posts.models import Post, Comment, Like
from .forms import PostModelForm, CommentModelForm
from django.contrib.auth.decorators import login_required

from django.urls import reverse, reverse_lazy
from profiles.models import Profile, Relationship

logger = logging.getLogger(__name__)


@login_required
def new_post(request):
    """
    This function allows  to create a new post with the form.py
    This function has two forms(Post and comments), it depends ons the submit button to trigger them
    key: winterfun:user:username => Get the profile username from redis, if it is cached
    Done!
    """
    user = request.user
    """Check the profile from cache"""
    profile = Profile.get_my_profile(user)
    # print(profile)
    """Shows all post created"""
    qs = Post.objects.filter(author=profile)

    # initials
    p_form = PostModelForm()
    c_form = CommentModelForm()
    post_added = False

    """Post form if trigger"""
    if 'submit_p_form' in request.POST:
        # print(request.POST)
        p_form = PostModelForm(request.POST, request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form = PostModelForm()
            post_added = True
    """Comments form if trigger"""
    if 'submit_c_form' in request.POST:
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelForm()

    context = {
        'qs': qs,
        'profile': profile,
        'p_form': p_form,
        'c_form': c_form,
        'post_added': post_added,
    }

    return render(request, 'posts/new_post.html', context)


@login_required
def friend_post(request):
    """
    This function shows post that are related to users with the status accepted
    key: winterfun:user:username => Get the profile username from redis, if it is cached
    Done!
    """
    user = request.user
    profile = Profile.get_my_profile(user)
    """Find users that have accepted"""
    query_set = Relationship.objects.invatations_accepted(profile)
    # print(query_set)


    # for x in query_set:
    #     print(x.receiver)
    #     post = Post.objects.filter(author=x.receiver)
    #     qs.append(post)
    #     post = None

    qs = Post.objects.all().exclude(author=profile)

    print(qs)
    # initials
    p_form = PostModelForm()
    c_form = CommentModelForm()
    post_added = False

    """Post form if trigger"""
    if 'submit_p_form' in request.POST:
        print('submit p form')
        p_form = PostModelForm(request.POST, request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form = PostModelForm()
            post_added = True
    """Comments form if trigger"""
    if 'submit_c_form' in request.POST:
        print('submit c form')
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelForm()

    context = {
        'qs': qs,
        'profile': profile,
        'p_form': p_form,
        'c_form': c_form,
        'post_added': post_added,
    }

    return render(request, 'posts/friend_post.html', context)


@login_required
def like_unlike_post(request):
    """
    This function send a response to the database to update the field LIke and Unlike
    key: winterfun:user:username => Get the profile username from redis, if it is cached
    Done!
    """
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(pkid=post_id)
        """Check profile in redis"""
        profile = Profile.get_my_profile(user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'

        else:
            like.value = 'Like'

        post_obj.save()
        like.save()

    return redirect('posts:new-post')


from django.conf import settings


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """
    This class delete the post

    Return messages warning if it is not the owner of the post

    Done!
    """
    model = Post
    slug_url_kwarg = 'id'
    slug_field = 'id'
    template_name = 'posts/post_delete.html'
    success_url = reverse_lazy('posts:new-post')

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            path, filename = os.path.split(instance.image.path)
            shutil.rmtree(path)
            logger.info(f"{path} ====>  This post folder was removed.")
        except Exception as e:
            print(str(e))
        return super(PostDeleteView, self).delete(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        id = self.kwargs.get('id')
        obj = Post.objects.get(id=id)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'You need to be the author of the post in order to delete it')
        return obj


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """
    This class update the post details
    Return messages warning if it is not the owner of the post

    Done!
    """
    form_class = PostModelForm
    model = Post

    template_name = 'posts/post_update.html'
    success_url = reverse_lazy('posts:new-post')

    def get_object(self, *args, **kwargs):
        id = self.kwargs.get('id')
        obj = Post.objects.get(id=id)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'You need to be the author of the post in order to delete it')
        return obj

    def form_valid(self, form):
        user = self.request.user
        """Check profile in redis"""
        profile = Profile.get_my_profile(user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, "You need to be the author of the post in order to update it")
            return super().form_invalid(form)
