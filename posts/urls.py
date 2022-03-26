from django.urls import path


app_name = "posts"

from posts.views import new_post, like_unlike_post, PostDeleteView, PostUpdateView, friend_post

urlpatterns = [
    path('new/', new_post, name='new-post'),
    path('friendpost', friend_post, name='friend-post'),
    #path("api/me/", GetProfileAPIView.as_view(), name="get_profile"),
    #path('', post_comment_create_and_list_view, name='main-post-view'),
    path('liked/', like_unlike_post, name='like-post-view'),
    path('<id>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<id>/update/', PostUpdateView.as_view(), name='post-update'),

]


#"{% static 'staticfiles/static/css/main.css' %}"