from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from blog.models import Post, Comment, CommentLike
from blog.forms import PostForm, CommentForm


class PostListView(ListView):
    model = Post
    template_name = 'blog/post/list.html'
    queryset = Post.published.all()
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        period = self.request.GET.get('period')
        author = self.request.GET.get('author')

        if period == 'day':
            today = timezone.localtime().date()
            queryset = queryset.filter(publish__date=today)
        elif period == 'week':
            start_date = timezone.localtime().date() - timedelta(days=7)
            queryset = queryset.filter(publish__gte=start_date)
        elif period == 'month':
            start_date = timezone.localtime().date() - timedelta(days=30)
            queryset = queryset.filter(publish__gte=start_date)

        if author:
            author = get_object_or_404(User, username=author)
            queryset = queryset.filter(author=author)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = Paginator(self.object_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        query_params = self.request.GET.copy()
        url_without_params = self.request.path

        if page_obj.has_previous():
            query_params['page'] = page_obj.previous_page_number()
            prev_page_url = f'{url_without_params}?{query_params.urlencode()}'
            context['prev_page_url'] = prev_page_url
        if page_obj.has_next():
            query_params['page'] = page_obj.next_page_number()
            next_page_url = f'{url_without_params}?{query_params.urlencode()}'
            context['next_page_url'] = next_page_url

        context['posts'] = page_obj
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post/detail.html'
    queryset = Post.published.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'post': self.object})
        return context

    def get_object(self, queryset=None):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        slug = self.kwargs.get('slug')

        queryset = queryset or self.queryset
        post = get_object_or_404(queryset,
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day,
                                 slug=slug)
        return post

    @method_decorator(login_required, name='dispatch')
    def post(self, request, *args, **kwargs):
        post_comment = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.save()
            return HttpResponseRedirect(f'{post_comment.get_absolute_url()}')
        return self.render_to_response({'post': post_comment, 'form': form})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post/new.html'
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post/edit.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Post, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        return context

    def form_valid(self, form):
        form.instance.author = self.object.author
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.publish.year,
                                                 self.object.publish.month,
                                                 self.object.publish.day,
                                                 self.object.slug])


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        if not self.request.user.is_superuser or self.object.author != self.request.user:
            raise PermissionDenied("You don't have permission to delete this post")
        messages.success(self.request, f'Post deleted {self.object.title}')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        return context


class CommentLikeView(LoginRequiredMixin, View):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        comment_like, created = CommentLike.objects.get_or_create(comment=comment, user=request.user)
        if not created:
            comment_like.delete()
        return HttpResponseRedirect(f'{comment.post.get_absolute_url()}')


class CommentLikeAdminView(LoginRequiredMixin, View):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)

        if not request.user.is_superuser:
            raise PermissionDenied("You don't have permission to admin comments")

        comment.active = False if comment.active else True
        comment.save()
        return HttpResponseRedirect(f'{comment.post.get_absolute_url()}')
