from django.core.cache import cache
from django.db import models

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.urls import reverse

from profiles.models import Profile
from winterfun.calendar_connection import get_calendar_service
from winterfun.models import WinterModel
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from winterfun.redis_key_schema import key_schema

from django.core.exceptions import ObjectDoesNotExist


User = get_user_model()
ONE_HOUR = 60 * 60


class EventManager(models.Manager):
    def get_all_events_to_invite(self, sender):
        events = Event.objects.all().exclude(user=sender)
        event = Event.objects.get(user=sender)
        query_set = Relationship.objects.filter(Q(sender=event) | Q(receiver=event))
        # print(query_set)
        # print("#########")

        accepted = set([])
        for rel in query_set:
            if rel.status == "yes":
                accepted.add(rel.receiver)
                accepted.add(rel.sender)
        # print(accepted)
        # print("#########")

        available = [profile for profile in events if profile not in accepted]
        # print(available)
        # print("#########")
        return available

    def get_all_events(self, me):
        events = Event.objects.all().exclude(user=me)
        return events


class Event(WinterModel):
    user = models.ForeignKey(User, related_name='user_events', on_delete=models.CASCADE)
    summary = models.CharField(max_length=254, blank=True, default='')
    description = models.TextField(blank=True, default='')
    start = models.DateTimeField(blank=False)
    end = models.DateTimeField(blank=False)
    accounts = models.ManyToManyField(
        User,
        verbose_name=_('accounts'),
        blank=True,
        help_text=_(
            'The accounts this event belongs to. A event will be sent to all accounts '
            'granted to each of their accounts.'
        ),
        related_name='event_set',
        related_query_name='account',
    )
    added_to_google_calendar = models.BooleanField(default=False)

    objects = EventManager()

    def __str__(self):
        return "{user}: {summary}: {pkid}: ".format(
            user=self.user.email,
            summary=self.summary,
            pkid=self.pkid,
        )

    def get_absolute_url(self):
        # return reverse('update-profile', args=[str(self.user)])
        return reverse("events:event-detail-view", kwargs={"id": self.id})

    class Meta:
        ordering = ('start', 'end', 'user')
        # unique_together = ('id',)
        # managed = True

    def clean(self):
        # Check oauth2 info of sender
        start_date = self.start
        end_date = self.end
        if end_date < start_date:
            raise ValidationError({'end': ['End date should be greater than start date.']})

    @staticmethod
    def get_my_events(user) -> str:
        """
        This query returns the events that the user created

        DONE!
        """
        events = Event.objects.filter(user=user)
        return events

    # def get_accounts(self):
    #     print(self.accounts)
    #     if self.accounts:
    #         return '%s' % " / ".join([account.username for account in self.accounts.all()])

    def get_user(self):
        """This method is used to find the used object based on the list of m2m"""

        user_list = []
        for user in self.accounts.all():
            user_id = user.id
            obj = User.objects.get(id=user_id)
            user_list.append(obj)
        # print(list)
        """return the list of Users object"""
        return user_list

    def get_status(self):
        list = []
        for user in self.accounts.all():
            user_pkid = user.pkid
            obj = Relationship.objects.get(event=self, receiver=user_pkid)
            list.append(obj)
        # print(list)
        """return the list of Relationship object"""
        return list


class CalendarEvent(WinterModel):
    calendar_event_id = models.CharField(max_length=1024, blank=False)
    event = models.ForeignKey(Event, related_name='calendar_event_events', on_delete=models.CASCADE)

    def __str__(self):
        return "{calendar_event_id}->{event}: ".format(
            calendar_event_id=self.calendar_event_id,
            event=self.event.pkid,
        )

    class Meta:
        ordering = ('created_at',)

    @staticmethod
    def set_google_calendar(event, calendar_id):
        """
        DONE!
        """
        try:
            CalendarEvent.objects.create(calendar_event_id=calendar_id, event=event)
            """If created, return TRUE"""
            return True
        except Exception as e:
            print(str(e))
            return False

    @staticmethod
    def delete_google_calendar(event):
        """
        DONE!
        """
        try:
            CalendarEvent.objects.filter(event=event).delete()
            """If created, return TRUE"""
            return True
        except Exception as e:
            print(str(e))
            return False

    @staticmethod
    def get_google_calendar(event):
        """
        Select the calendar event id from the database based on the current selected event
        """
        try:
            """It check if there is an event on the database"""
            qs = CalendarEvent.objects.get(event=event)
            result = qs.calendar_event_id
            """Return the google calendar id from the current event"""
            # print(result)
            return result

        except Exception as e:
            print(str(e))
            return None


class EventReceiver(WinterModel):
    event = models.ForeignKey(Event, related_name='event_receiver_events', on_delete=models.CASCADE)
    account = models.ForeignKey(User, related_name='event_receiver_accounts', on_delete=models.CASCADE)
    opened = models.BooleanField(default=False)
    clicked = models.BooleanField(default=False)

    def __str__(self):
        return "{user}->{receiver}: {event}".format(
            user=self.event.user.email,
            receiver=self.account.email,
            event=self.event.summary
        )


class RelationshipManager(models.Manager):
    def invatations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status="send")
        return qs

    def update_object_status(self, event, receiver, status):
        qs = Relationship.objects.filter(event=event, receiver=receiver).update(status=status)
        return qs

    @staticmethod
    def delete_event_relationship(event):
        try:
            Relationship.objects.filter(event=event).delete()
            """If created, return TRUE"""
            return True
        except Exception as e:
            print(str(e))
            return False

    @staticmethod
    def update_event_relationship(event, status='send'):
        """
        First I check all m2m users if it is not none
        then I check if the users is on the realtion with the current event, if yes, I add it to a list
        if the obj relation is not found, it generates an exception to create any user that was not found it before
        """
        obj_list = []
        try:
            m2m = event.accounts.all()
            if m2m is not None:
                for result in m2m:
                    try:
                        find_first = Relationship.objects.get(event=event, sender=event.user, receiver=result)
                        if find_first:
                            """Adding the relation to a list"""
                            obj_list.append(find_first.pkid)
                    except ObjectDoesNotExist:
                        qs = Relationship.objects.create(event=event, sender=event.user, receiver=result, status=status)
                        obj_list.append(qs.pkid)
            """The list is now used to remove any out of date relation excluding the objects on the list"""
            Relationship.objects.filter(event=event).exclude(pkid__in=obj_list).delete()
        except Exception as e:
            print(str(e))


STATUS_CHOICES = (("send", "send"), ("accepted", "accepted"), ("declined", "declined"), ("pending", "pending"))


class Relationship(WinterModel):
    event = models.ForeignKey(Event, related_name='event_receiver', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)

    objects = RelationshipManager()

    def __str__(self):
        return "{sender}: to {receiver} = {status}: to event pkid {pkid}".format(
            sender=self.sender,
            receiver=self.receiver,
            status=self.status,
            pkid=self.event.pkid
        )
