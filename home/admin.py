from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Blog, Comment, Profile, Category,Commercial

# Register your models here.
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )

admin.site.unregister(User)
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Commercial)
admin.site.register(Profile)
