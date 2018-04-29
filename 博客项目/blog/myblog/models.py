from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField('名称', max_length = 20)
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('名称', max_length = 20)
    def __str__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class Article(models.Model):
    title = models.CharField('标题',max_length = 150)
    body = models.TextField('正文')
    date = models.DateTimeField('发布时间')
    category = models.ForeignKey(Category, verbose_name='分类',on_delete=models.CASCADE)
    tags = models.ForeignKey(Tag, verbose_name = '标签',on_delete=models.CASCADE,null=True,blank=True) #null=True表示数据库中该字段可为空，blank=Ture表示admin中添加数据可以为空
    editer = models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)

    def __str__(self):
        return self.title


