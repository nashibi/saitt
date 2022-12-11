import os

from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from django.db import models
from tinymce.models import HTMLField


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='parents')
    name = models.CharField(max_length=50, unique=True)
    is_sub_category = models.BooleanField(default=False, null=False, editable=False, verbose_name='آیا دسته زیر مجموعه است؟')
    sub_lvl = models.PositiveSmallIntegerField(default=0, null=False, editable=False, verbose_name='لول دسته')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'دسته'
        verbose_name_plural = 'دسته ها'

    def save(self, *args, **kwargs):
        if self.parent:
            self.is_sub_category = True
            self.sub_lvl = self.parent.sub_lvl + 1
        super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name='عنوان')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, verbose_name='نویسنده')
    category = models.ManyToManyField(Category, blank=False, verbose_name='دسته ها')
    image = models.ImageField(upload_to='post_images', default='empty.png', null=False, blank=True,
                              verbose_name='تصویر')
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='زمان انتشار')
    content = HTMLField(blank=True)
    reply_to = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True, verbose_name='ریپلای شد به')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'
        ordering = ['id']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.image:
            self.image = UploadedFile(
                file=open(os.path.join('media', 'empty.png'), 'rb')
            )
        super().save(*args, **kwargs)

