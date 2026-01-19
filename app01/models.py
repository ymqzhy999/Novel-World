from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False, verbose_name="是否为管理员")
    role = models.CharField(max_length=10, default='user', choices=[('user', '普通用户'), ('admin', '管理员')])
    is_active = models.BooleanField(default=True, verbose_name='是否激活')

class Novel(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    cover_url = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Chapter(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

class RechargeRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    recharge_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default='pending', choices=[('pending', '待审核'), ('approved', '已通过'), ('rejected', '已拒绝')])

class PurchaseRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    purchase_time = models.DateTimeField(auto_now_add=True)

class Bookshelf(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    added_time = models.DateTimeField(auto_now_add=True)

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=200)
    search_time = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

class Announcement(models.Model):
    title = models.CharField(max_length=200, verbose_name='公告标题')
    content = models.TextField(verbose_name='公告内容')
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    is_published = models.BooleanField(default=True, verbose_name='是否发布')

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = '公告'
        ordering = ['-published_at']

    def __str__(self):
        return self.title
