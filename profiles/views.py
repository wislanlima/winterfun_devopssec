from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from django.views.generic import ListView, DetailView
from .renderers import ProfileJSONRenderer
from .models import Profile, Relationship
from .serializers import ProfileSerializer, UpdateProfileSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions, status, viewsets, parsers
from django.contrib.auth import get_user_model
from .exceptions import NotYourProfile, ProfileNotFound
from django.core.paginator import Paginator

from winterfun.redis_key_schema import key_schema
from django.core.cache import cache

from django.contrib.auth.decorators import login_required
from .forms import ProfileModelForm, EditProfileForm
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

User = get_user_model()
ONE_HOUR = 60 * 60

"""API REQUEST START HERE"""


class brasil_list_api_view(generics.ListAPIView):
    """
    This is an api call for a list of profiles from BR
    It use the serializer class rest_framework
    Link: api/brasilprofiles/
    Done!
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.filter(country="BR")
    serializer_class = ProfileSerializer


class GetProfileAPIView(APIView):
    """
    This is an api call for the current profile logged
    It use the serializer class rest_framework
    Link: api/me
    Use the cache if the value was already stored
    Done!
    """
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [ProfileJSONRenderer]

    def get(self, request):
        user = self.request.user
        profile = Profile.get_my_profile(user)
        serializer = ProfileSerializer(profile, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfileAPIView(APIView):
    """
    This is an api call for the current profile logged
    It use the serializer class rest_framework
    Link: api/update/<str:username>/
    Use the cache if the value was already stored and then delete to reflect the change
    Done!
    """
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [ProfileJSONRenderer]
    serializer_class = UpdateProfileSerializer

    def patch(self, request, username):
        key = key_schema().get_user_key(username)
        try:
            Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise ProfileNotFound

        user_name = request.user.username
        if user_name != username:
            raise NotYourProfile

        data = request.data
        serializer = UpdateProfileSerializer(
            instance=request.user.profile, data=data, partial=True
        )

        serializer.is_valid()
        serializer.save()
        cache.delete(key)
        return Response(serializer.data, status=status.HTTP_200_OK)


"""API end here"""

@login_required
def my_profile(request):
    """
    This function display the profile details of the user.
    If the user was loaded previously, it loads it from redis
    key: winterfun:user:username
    Done!
    """
    context = {}
    user = request.user
    profile = Profile.get_my_profile(user)
    context['profile'] = profile

    return render(request, "profiles/my_profile.html", context)


@login_required
def update_profile(request):
    """
    This function allow the users to update their profile
    If the user was loaded previously, it loads it from redis
    If the form is updated, update the profile and remove the old data from the cache
    key: winterfun:user:username
    Done
    """
    context = {}
    user = request.user
    profile = Profile.get_my_profile(user)
    key = key_schema().get_user_key(user)

    form = ProfileModelForm(
        request.POST or None, request.FILES or None, instance=profile
    )
    confirm = False

    if request.method == "POST":
        if form.is_valid():
            form.save()

            cache.delete(key)
            confirm = True
    context = {
        "profile": profile,
        "form": form,
        "confirm": confirm,
    }
    return render(request, "profiles/update_profile.html", context)


@login_required
def friend_list(request):
    """
    This function allow the users to find all friends from this profile
    If the profile's friends was loaded previously, it loads it from redis cache
    key: winterfun:profile:friends:username
    Done
    """
    context = {}
    user = request.user
    profile = Profile.get_my_profile(user)

    key = key_schema().my_friends_key(user)
    print(key)
    cached_result = cache.get(key)

    if not cached_result:
        print("Not FROM CACHE")
        friends = Relationship.objects.invatations_accepted(profile)
        cache.set(key, friends, timeout=ONE_HOUR)
    else:
        print("FROM CACHE")
        friends = cached_result
    context['friends'] = friends
    return render(request, "profiles/friend_list.html", context)


@login_required
def profile_available(request):
    """
    This function allow the users to check the list of users available to invite
    Done
    """
    user = request.user
    all_profile = Profile.objects.get_all_profiles_to_invite(user)
    context = {"all_profile": all_profile}
    return render(request, "profiles/profile_available.html", context)


@login_required
def be_friend(request):
    """
    Im using the get_my_profile from cache if exist and using this as a sender
    The user's friend, I need the pk in order to find the friend's profile
    key: winterfun:user:username
    Done
    """
    if request.method == "POST":
        profile_pk = request.POST.get("profile_pk")
        user = request.user
        myself = Profile.get_my_profile(user)
        new_friend = Profile.objects.get(pk=profile_pk)
        try:
            sender_request = Relationship.objects.create(
                sender=myself, receiver=new_friend, status="send"
            )
        except Exception as e:
            print(str(e))

        return redirect(request.META.get("HTTP_REFERER"))
    return redirect("profiles:my-profile")


@login_required
def un_friend(request):
    """
    Im using the get_my_profile from cache if exist and using this as a sender
    The user's friend, I need the pk in order to find the friend's profile
    key: winterfun:user:username
    Done
    """
    if request.method == "POST":
        profile_pk = request.POST.get("profile_pk")
        user = request.user
        myself = Profile.get_my_profile(user)
        receiver = Profile.objects.get(pk=profile_pk)

        sender_request = Relationship.objects.get(
            (Q(sender=myself) & Q(receiver=receiver))
            | (Q(sender=receiver) & Q(receiver=myself))
        )
        sender_request.delete()
        return redirect(request.META.get("HTTP_REFERER"))
    return redirect("profiles:my-profile")


@login_required
def request_received(request):
    """
    List of request send to my_profile where the status is send(Here the user can decide to accept is or reject
    key: winterfun:user:username
    Done
    """
    user = request.user
    myself_profile = Profile.get_my_profile(user)
    query_set = Relationship.objects.invatations_received(myself_profile)
    friendship_request = list(map(lambda x: x.sender, query_set))
    is_empty = False
    if len(friendship_request) == 0:
        is_empty = True

    context = {
        "friends": friendship_request,
        "is_empty": is_empty,
    }
    return render(request, "profiles/profile_received.html", context)


@login_required
def request_accept(request):
    """
    Change the status of the relationship table from send to accept
    Check if my user is saved in the cache
    key: winterfun:user:username
    Done
    """
    if request.method == "POST":
        user = request.user
        profile_pk = request.POST.get("profile_pk")
        sender = Profile.objects.get(pkid=profile_pk)
        myself_profile = Profile.get_my_profile(user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=myself_profile)
        if rel.status == "send":
            rel.status = "accepted"
            rel.save()
    return redirect("profiles:profiles-list")


@login_required
def request_refuse(request):
    """
    Delete the relationship from the user profile
    Check if my user is saved in the cache
    key: winterfun:user:username
    Done
    """
    if request.method == "POST":
        user = request.user
        profile_pk = request.POST.get("profile_pk")
        myself_profile = Profile.get_my_profile(user)
        sender = Profile.objects.get(pk=profile_pk)
        rel_model = get_object_or_404(Relationship, sender=sender, receiver=myself_profile)
        rel_model.delete()
    return redirect("profiles:request-received")


class ProfileListView(LoginRequiredMixin, ListView):
    """
    Generic List View of the profile
    Check if my user is saved in the cache
    key: winterfun:user:username
    Done
    """
    model = Profile
    template_name = "profiles/profile_list.html"
    paginate_by = 4
    ordering = '-created_at'


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """
    Generic Detail View of the profile - Using cache to find the profile
    Check if my user is saved in the cache
    key: winterfun:user:username
    Done
    """
    model = Profile
    template_name = "profiles/profile_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        request_user = self.request.user
        #user = User.objects.get(username=request_user)
        myself_profile = Profile.get_my_profile(request_user)
        rel_r = Relationship.objects.filter(sender=myself_profile)
        rel_s = Relationship.objects.filter(receiver=myself_profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender

        return context


# class ProfileUpdateView(
#     LoginRequiredMixin, UserPassesTestMixin, UpdateView
# ):  # LoginRequiredMixin deve ser o primeiro
#     model = Profile
#     fields = [
#         "first_name",
#         "last_name",
#         "about_me",
#         "avatar",
#         "gender",
#         "country",
#         "city",
#     ]
#
#     def get_object(self):
#         username = self.kwargs.get("username")
#         return get_object_or_404(Profile, user__username=username)
#
#     def test_func(self):
#         # film_details = self.get_object()
#         if (
#                 self.request.user.is_superuser
#         ):  # apenas super usuario pode alterar isso, tem que herdar de UserPassesTestMixin
#             return True
#         return False
