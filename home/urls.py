from django.urls import path
from . import views


app_name = 'home'
urlpatterns = [
    path('', views.Homeview.as_view(), name='home'),
    path('post/detail/<int:post_id>/<slug:post_slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/delete/<int:post_id>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/update/<int:post_id>/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('like/<int:post_id>/', views.PostLikeView.as_view(), name='post_like'),
    path('unlike/<int:post_id>/', views.PostUnlikeView.as_view(), name='post_unlike'),

]
