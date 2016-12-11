from django.db import models
from django.contrib.auth.models import User
from www import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.core.urlresolvers import reverse


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=True)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=255, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, default=12)
    text = models.CharField(max_length=100000, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField()
    picture = models.FileField(blank=False)
    class Meta:
        ordering = ['-date_created']


    def __str__(self):
        return self.title + ' - ' + self.author.first_name + ' ' + self.author.last_name + ' - ' + self.date_created.strftime("%d-%m-%y, %H:%M:%S")

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000, blank=False)
    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.blog.title + ' - ' + self.author.first_name + ' ' + self.author.last_name + ' - ' + self.date_created.strftime("%d-%m-%y, %H:%M:%S") + '| Comment: ' + self.text

class Profile(models.Model):

    sex_choice = (
        ('Male', 'Male'),
        ('Female', 'Female'),
                  )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(default=timezone.now, blank=True)
    picture = models.FileField(storage=FileSystemStorage(location=settings.MEDIA_ROOT), upload_to='default', default='default/default.png')
    sex = models.CharField(max_length=6, choices=sex_choice, blank=True)
    bio = models.CharField(max_length=5000, blank=True)
    show_email = models.BooleanField(blank=False, default=False)
    occupation = models.CharField(max_length=25, blank=True)

    def get_absolute_url(self):
        return reverse('home:user', kwargs={'usr_pk':self.pk})

    def __str__(self):
        return str(self.id) + ' ' + self.user.first_name + ' ' + self.user.last_name + ' ' + self.user.username + ' ' + self.date_of_birth.strftime("%d-%m-%y") + ' ' + self.sex

class Commercial(models.Model):
    name = models.CharField(max_length=255, blank=False)
    picture = models.FileField(blank=False)
    url = models.CharField(max_length=5000, blank=False)
    def __str__(self):
        return self.name + '    URL: ' + self.url


