from django.urls import path

from blog import views


app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>', views.PostDetailView.as_view(), name='post_detail'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/update/<int:pk>', views.PostUpdateView.as_view(), name='post_update'),
    path('post/delete/<int:pk>', views.PostDeleteView.as_view(), name='post_delete'),
    path('comment-like/<int:comment_id>', views.CommentLikeView.as_view(), name='comment_like'),
    path('comment-like/admin/<int:comment_id>', views.CommentLikeAdminView.as_view(), name='comment_admin'),
]
