from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class ResultSettings(SingletonModel):
    NextResult = models.IntegerField(default=20)
    UserPercent = models.IntegerField(default=10)
    BrokerPercent = models.IntegerField(default=10)

class Profile(models.Model):
    class ProfileType(models.IntegerChoices):
        ADMIN = 1
        MANAGER = 2
        BROKER = 3
        USER = 4
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    profile_type = models.IntegerField(choices=ProfileType.choices, default=4)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='created_by')

    def __str__(self):
        return self.user.username

class Transaction(models.Model):
    class TransactionType(models.IntegerChoices):
        FILLPOINTS = 1
        PLAYBET = 2
        WONPRIZE = 3
        WITHDRAWPOINT = 4
        COMMISION = 5
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='recevier')
    amount = models.IntegerField()
    transaction_type = models.IntegerField(choices=TransactionType.choices, default=1)
    date = models.DateTimeField(auto_now_add=True)
    selected_number = models.IntegerField(default=-1)

    def __str__(self):
        return "From : " + self.sender.user.get_username() + " To :  " + self.receiver.user.get_username() + " Amount : " + str(self.amount)

class BetEntry(models.Model):
    voter = models.ForeignKey(Profile, on_delete=models.CASCADE)
    selected_number = models.IntegerField()
    bet_amount = models.IntegerField()
    game_id = models.IntegerField(default=1)
    isArchive = models.BooleanField(default=False)

class BetWin(models.Model):
    winner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    entry = models.ForeignKey(BetEntry, on_delete=models.CASCADE, related_name='entry')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()