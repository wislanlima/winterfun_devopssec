from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.template.defaultfilters import slugify
import uuid
from winterfun.models import WinterModel
from django.urls import reverse
from django.db.models import Q
from django.core.cache import cache

from winterfun.redis_key_schema import key_schema

User = get_user_model()
ONE_HOUR = 60 * 60


def get_random_code():
    code = str(uuid.uuid4())[:8].replace("-", "").lower()
    return code


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}/{2}'.format(instance.user.pkid, 'avatar', filename)


class Gender(models.TextChoices):
    MALE = "Male", _("Male")
    FEMALE = "Female", _("Female")
    OTHER = "Other", _("Other")


class ProfileManager(models.Manager):
    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        query_set = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
        # print(query_set)
        # print("#########")

        accepted = set([])
        for rel in query_set:
            if rel.status == "accepted":
                accepted.add(rel.receiver)
                accepted.add(rel.sender)
        # print(accepted)
        # print("#########")

        available = [profile for profile in profiles if profile not in accepted]
        # print(available)
        # print("#########")
        return available

    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles


class Profile(WinterModel):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    about_me = models.TextField(
        verbose_name=_("About me"), default="say something about yourself"
    )
    avatar = models.ImageField(default="avatar.png", upload_to=user_directory_path)

    gender = models.CharField(
        verbose_name=_("Gender"),
        choices=Gender.choices,
        default=Gender.OTHER,
        max_length=20,
    )
    country = CountryField(
        verbose_name=_("Country"), default="BR", blank=False, null=False
    )
    city = models.CharField(
        verbose_name=_("City"),
        max_length=180,
        default="Dublin",
        blank=False,
        null=False,
    )
    slug = models.SlugField(unique=True, blank=True)
    friends = models.ManyToManyField(User, blank=True, related_name="friends")

    objects = ProfileManager()

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_absolute_url(self):
        # return reverse('update-profile', args=[str(self.user)])
        return reverse("profiles:profile-detail-view", kwargs={"slug": self.slug})

    @staticmethod
    def get_my_profile(user) -> str:
        """
        This query returns the user.request profile
        If the profile was loaded previously, it loads it from redis
        key: winterfun:user:username
        DONE!
        """
        #Check the standart key for my_profile
        key = key_schema().get_user_key(user)
        cached_result = cache.get(key)
        if not cached_result:
            # print("Not FROM CACHE")
            profile = Profile.objects.get(user=user)
            cache.set(key, profile, timeout=ONE_HOUR)
            return profile
        else:
            # print("FROM CACHE")
            return cached_result

    def get_all_authors_posts(self):
        return self.posts.all()

    def get_friends_no(self):
        return self.friends.all().count()

    def get_posts_no(self):
        return self.posts.all().count()

    def get_all_authors_posts(self):
        return self.posts.all()

    def get_likes_given_no(self):
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value == 'Like':
                total_liked += 1
        return total_liked

    def get_likes_recieved_no(self):
        posts = self.posts.all()
        total_liked = 0
        for item in posts:
            total_liked += item.liked.all().count()
        return total_liked

    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name

    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        if (
                self.first_name != self.__initial_first_name
                or self.last_name != self.__initial_last_name
                or self.slug == ""
        ):
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
                ex = Profile.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_random_code()))
                    ex = Profile.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)


STATUS_CHOICES = (("send", "send"), ("accepted", "accepted"))


class RelationshipManager(models.Manager):
    def invatations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status="send")
        return qs

    def invatations_accepted(self, sender):
        qs = Relationship.objects.filter(sender=sender, status="accepted")
        return qs


class Relationship(WinterModel):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="receiver")
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
