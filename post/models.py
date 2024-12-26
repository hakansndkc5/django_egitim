from django.db import models
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey('auth.User', verbose_name="Yazar", on_delete=models.CASCADE,default=1)
    title = models.CharField(max_length=120, verbose_name="Başlık")
    text = models.TextField(verbose_name="Metin")
    date = models.DateTimeField(verbose_name="Tarih", auto_now_add=True)
    image = models.ImageField(null=True, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post:detail', kwargs = {'id' : self.id})

class Comment(models.Model):
    post = models.ForeignKey('post.Post', related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="İsim")
    content = models.TextField(max_length=500,verbose_name="Yorum")

    created_date = models.DateTimeField(auto_now_add=True)