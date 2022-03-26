import factory
from profiles.models import Profile
from django.db.models.signals import post_save
from faker import Factory as FakerFactory
from winterfun.base_settings import AUTH_USER_MODEL

faker = FakerFactory.create()


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory("tests.factories.UserFactory")
    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())
    about_me = factory.LazyAttribute(lambda x: faker.sentence(nb_words=5))
    avatar = factory.LazyAttribute(
        lambda x: faker.file_extension(category="image")
    )
    gender = factory.LazyAttribute(lambda x: f"other")
    country = factory.LazyAttribute(lambda x: faker.country_code())
    city = factory.LazyAttribute(lambda x: faker.city())

    #friends=factory.SubFactory("tests.factories.UserFactory")


    class Meta:
        model = Profile


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):

    username = factory.LazyAttribute(lambda x: faker.first_name())
    email = factory.LazyAttribute(lambda x: f"alpha@winterfun.com")
    password = factory.LazyAttribute(lambda x: faker.password())
    is_active = True
    is_staff = False

    class Meta:
        model = AUTH_USER_MODEL

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        if "is_superuser" in kwargs:
            return manager.create_superuser(*args, **kwargs)
        else:
            return manager.create_user(*args, **kwargs)
