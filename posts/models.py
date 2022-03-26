from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile
from winterfun.models import WinterModel
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    user_pkid = instance.author_id
    post_id = instance.id
    print(instance.__dict__)
    return 'user_{0}/{1}/{2}/{3}'.format(user_pkid, 'post', post_id , filename)

class Post(WinterModel):
    content = models.TextField()
    image = models.ImageField(upload_to=user_directory_path, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
                              blank=False)
    liked = models.ManyToManyField(Profile, blank=True, related_name='likes')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return str(self.content[:20])

    def get_absolute_url(self):
        # return reverse('update-profile', args=[str(self.user)])
        return reverse("posts:new-post", kwargs={"id": self.id})

    def num_likes(self):
        return self.liked.all().count()

    def num_comments(self):
        return self.comment_set.all().count()

    class Meta:
        ordering = ('-created_at',)


class Comment(WinterModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)

    def __str__(self):
        return str(self.pk)


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(WinterModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)


    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"
