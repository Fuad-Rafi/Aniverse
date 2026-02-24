from django.db import models

from django.contrib.auth.models import User

from django.urls import reverse

from datetime import datetime, date

from ckeditor.fields import RichTextField



class Category(models.Model):
    name = models.CharField(max_length=255)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(args, kwargs)
    #     self.id = None

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        #return reverse('post_details', args=(str(self.id))
        return reverse("Home")

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/")
    fb_url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.user)

class Post(models.Model):
    title=models.CharField(max_length=255)
    header_image= models.ImageField(null=True, blank=True, upload_to="images/profile")
    title_tag=models.CharField(max_length=255)
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    #body=models.TextField() 
    body=RichTextField(blank=True, null=True) 
    post_date=models.DateField(auto_now_add=True)
    category=models.CharField(max_length=255, default='uncategorized')
    likes = models.ManyToManyField(User, related_name='blog_posts')
    snippet=models.CharField(max_length=255)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title + ' | ' + str(self.author) 
    
    def get_absolute_url(self):
        return reverse('post_details', args=(self.id,))
        # return reverse("Home")


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'{self.author} on {self.post}'


class FriendRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    sender = models.ForeignKey(User, related_name='sent_friend_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_friend_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_on = models.DateTimeField(auto_now_add=True)
    responded_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('sender', 'receiver')
        ordering = ['-created_on']

    def __str__(self):
        return f'{self.sender} -> {self.receiver} ({self.status})'


class DirectMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_direct_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_direct_messages', on_delete=models.CASCADE)
    body = models.TextField(max_length=1000)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'{self.sender} to {self.receiver}'