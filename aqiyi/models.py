from django.db import models

# Create your models here.

# 制作生成数据表
# 执行python manage.py makemigrations app名(可选)
# 在执行python manage.py migrate

class Movie(models.Model):
    title = models.CharField(max_length=32,default="Title")
    #Img = models.ImageField(max_length=32)
    content = models.TextField(null=True)
   # content1 = models.TextField(null=True)
    # 文章正文，使用的是TextField
    # 存储比较短的字符串可以使用 CharField，但对于文章的正文来说可能会是一大段文本，因此使用 TextField 来存储大段文本。


    def __str__(self):
        return self.title