from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone

class CustomUserManager(BaseUserManager):

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(make_password(password))
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, username, password, **extra_fields)
    
    



class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now=True)
    username = models.CharField(unique=True, max_length=256)
    firstname = models.CharField(max_length=256, blank=True)
    lastname = models.CharField(max_length=256, blank=True)
    is_coordinator = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='images/', default='default_avatar.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.username
    
    def save(self, *args, **kwargs):
        # Hash the password if it's in plain text
        if self.pk is None:  # When the user is being created
            self.created_at = timezone.now()
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
PLATFORM_CHOICES = [
    ('Mobile', 'Mobile'),
    ('Web', 'Web'), 
    ('Desktop', 'Desktop'),
    ('CrossPlatform', 'CrossPlatform')
]


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        verbose_name ="Category"
        verbose_name_plural ="Categories"

    def __str__(self) -> str:
        return self.name

class ProjectSupervisor(models.Model):
    name = models.CharField(max_length=264)

    def __str__(self):
        return self.name

class Project(models.Model):
    coordinator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project_supervisor = models.ForeignKey(ProjectSupervisor, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now=True) 
    is_completed = models.BooleanField(default=False)
    proposal_deadline = models.DateTimeField(blank=True, null=True)
    documentation_deadline = models.DateTimeField(blank=True, null=True)
    implementation_deadline = models.DateTimeField(blank=True, null=True)
    report_deadline = models.DateTimeField(blank=True, null=True)
    progress = models.SmallIntegerField(default=0)
    report_file = models.FileField(upload_to='files/reports/', null=True, blank=True)
    documentation_file = models.FileField(upload_to='files/documentation/', null=True, blank=True)
    platform = models.TextField(choices=PLATFORM_CHOICES, null=True, blank=True, default=None)
    categories = models.ManyToManyField(Category, blank=True, related_name='projects')
    upgradable = models.BooleanField(default=False)
    comment = models.TextField(max_length=500, default="")
    
    def __str__(self) -> str:
        return self.title
    
class ProjectGroup(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='group', null=True, blank=True)
    name = models.TextField(max_length=264)
    faculty = models.CharField(max_length=256, blank=True)
    academic_year = models.IntegerField(default=datetime.now().year)
    
    def __str__(self) -> str:
        return self.name
    
class GroupMember(models.Model):
    project_group = models.ForeignKey(ProjectGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=264, blank=False, )
    regnumber = models.CharField(max_length=264, blank=False, unique=True)

    def __str__(self) -> str:
        return self.name

