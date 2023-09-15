from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

from django.db.models.signals import post_save # her kaytta otomatk olusmasi icin yani kullanici kydnda bnnda olsmasi icin
from django.dispatch import receiver #buda kayt tetklemesi


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=False, verbose_name='User', on_delete=models.CASCADE)
    bio = models.TextField(max_length=5000, blank=True, null=True)
    profile_photo = models.ImageField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    instagram = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'User Profiles'

    def get_screen_name(self):
        user = self.user
        if user.get_full_name():
            return user.get_full_name()
        return user.username

    def user_full_name(self):
        if self.user.get_full_name():
            return self.user.get_full_name()
        return None

    def get_user_profile_url(self):
        url = reverse('user-profile', kwargs={'username': self.user.username})
        return url

    def get_profile_photo(self):
        if self.profile_photo:
            return self.profile_photo.url
        return "/static/img/default.jpg"

    def __str__(self):
        return "%s Profile" % (self.get_screen_name())


@receiver(post_save, sender=User) #user olustugu anda bu modelde olsutursun
def create_profile(sender, created, instance, **kwargs):
    if not created:
        return
    Profile.objects.create(user=instance)
    instance.profile.save()


# AbstractUser
# from django.contrib.auth.models import AbstractUser
# class CustomUserModel(AbstractUser):
#     avatar = models.ImageField(upload_to='avatar/', blank=True, null=True)
#
#     class Meta:
#         db_table = 'user'
#         verbose_name = 'Kullanıcı'
#         verbose_name_plural = 'Kullanıcılar'
#
#     def __str__(self):
#         return self.username