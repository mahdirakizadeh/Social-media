from django.shortcuts import render, redirect
from django.views import View
from .models import Post, Comment, Vote
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostCreateUpdateForms
from django.utils.text import slugify
from django.shortcuts import get_object_or_404


class Homeview(View):
    def get(self, request):
        post = Post.objects.all()
        return render(request, 'home/index.html', {'post': post})

    def post(self, request):
        pass


class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        is_like = False
        post = get_object_or_404(Post, pk=post_id, slug=post_slug)
        comments = post.post_comments.filter(is_replay=False)
        like = Vote.objects.filter(post=post, user=request.user)
        if like.exists():
            like.delete()
            messages.success(request, "you unlike this post", 'success')
        return render(request, 'home/detail.html', {'post': post, 'comments': comments, 'like': like})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, "you deleted successfully", 'success')
        else:
            messages.error(request, "you can't delete this post", 'danger')
        return redirect('home:home')


class PostUpdateView(View):
    form_class = PostCreateUpdateForms

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, "you can't change this post", 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, post_id):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'home/update.html', {'form': form})

    def post(self, request, post_id):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            update_post = form.save(commit=False)
            cd = form.cleaned_data
            update_post.slug = slugify(cd['body'][:20])
            update_post.save()
            messages.success(request, "updated your successfully", 'success')
            return redirect('home:post_detail', post.id, post.slug)


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForms

    def get(self, request):
        form = self.form_class()
        return render(request, 'home/create.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_post = form.save(commit=False)
            new_post.slug = slugify(cd['body'][:30])
            new_post.title = new_post.slug.replace("-", " ")
            new_post.user = request.user
            new_post.save()
            messages.success(request, "you created a post", 'success')
            return redirect('home:post_detail', new_post.id, new_post.slug)


class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        like = Vote.objects.filter(post=post, user=request.user)
        if like.exists():
            messages.error(request, "you like this post before", 'danger')
        else:
            Vote.objects.create(post=post, user=request.user)
            messages.success(request, "you like this post", 'success')
        return redirect('home:post_detail', post.id, post.slug)


class PostUnlikeView (LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        like = Vote.objects.filter(post=post, user=request.user)

        return redirect('home:post_detail', post.id, post.slug)

