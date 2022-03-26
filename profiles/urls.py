from django.urls import path

from .views import (
    brasil_list_api_view,
    GetProfileAPIView,
    UpdateProfileAPIView,
    update_profile,
    request_received,
    request_accept,
    request_refuse,
    be_friend,
    un_friend,
    profile_available,
    ProfileDetailView,
    ProfileListView,
    friend_list, my_profile,
)

app_name = "profiles"


urlpatterns = [

    path("api/me/", GetProfileAPIView.as_view(), name="get_profile"),
    path(
        "api/update/<str:username>/",
        UpdateProfileAPIView.as_view(),
        name="update-profile",
    ),
    path("api/brasilprofiles/", brasil_list_api_view.as_view(), name="BR-profile"),
    path("me/", my_profile, name="my-profile"),
    path("update/", update_profile, name="update-profile"),

    # path("agents/all/", AgentListAPIView.as_view(), name="all-agents"),
    # path("top-agents/all/", TopAgentsListAPIView.as_view(), name="top-agents"),
    path("list/", ProfileListView.as_view(), name="profiles-list"),
    path("details/<slug>/", ProfileDetailView.as_view(), name="profile-detail-view"),
    path("befriend/", be_friend, name="be-friend"),
    path("unfriend/", un_friend, name="un-friend"),
    path("available/", profile_available, name="profile-available"),
    path("received/", request_received, name="request-received"),
    path("accept/", request_accept, name="request-accept"),
    path("refuse/", request_refuse, name="request-refuse"),
    path("friendship/", friend_list, name="friend-list"),
    #path("<str:username>/", ProfileUpdateView.as_view(), name="update-profile"),
    # it doesnt need another template, it uses the create template

]
