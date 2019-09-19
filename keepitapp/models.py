from django.db import models
from accounts.models import User
from pytz import timezone
from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta
import pytz

# Create your models here.

class Task(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    daily_or_weekly = models.CharField(max_length=20)
    last_checked_off = models.DateTimeField(default=None, null=True)
    current_streak = models.IntegerField(default=0)
    best_streak = models.IntegerField(default=0)
    total_count = models.IntegerField(default=0)

    def __str__(self):
        return self.description

    def checked_today(self):
        checked_off_time = self.last_checked_off
        if not checked_off_time:
            return False

        user = self.user_id
        tz = timezone(user.timezone)
        user_reset = self.next_reset_time()

        checked_off_time = self.last_checked_off.astimezone(tz)
        checked_off_time = checked_off_time.replace(tzinfo=None)

        if checked_off_time + timedelta(days=1) > user_reset:
            return True
        else:
            return False

    def next_reset_time(self):
        user = self.user_id
        tz = timezone(user.timezone)
        reset_time = user.reset_time

        user_time = datetime.now(tz)

        hour = user_time.hour
        if reset_time > hour:
            t = time(hour=reset_time)
            d = date(user_time.year, user_time.month, user_time.day)
            return datetime.combine(d, t)
        else:
            t = time(hour=reset_time)
            d = date(user_time.year, user_time.month, user_time.day)
            delta = timedelta(days=1)
            return datetime.combine(d, t) + delta

    def checked_yesterday(self):
        checked_off_time = self.last_checked_off
        if not checked_off_time:
            return True

        user = self.user_id
        tz = timezone(user.timezone)
        reset_time = user.reset_time

        last_reset = self.next_reset_time() + timedelta(days=-1)

        checked_off_time = self.last_checked_off.astimezone(tz)
        checked_off_time = checked_off_time.replace(tzinfo=None)

        if checked_off_time + timedelta(days=1) > last_reset:
            return True
        else:

            return False


# last time checked off = utc
# convert to local timezone = est
# get next occurrence of chosen time in their timezone -
#
# get current time in their timezone. if the hour of reset time is greater, stay same day
# otherwise go next day
#
# check if next occurrence - last checked gap is less than 24 hours




