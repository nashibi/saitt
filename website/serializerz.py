from django.contrib.auth.models import User
from rest_framework import serializers

from website.models import Post, Category


class PostSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField

    class Meta:
        model = Post
        fields = (
            'title',
            'author',
            'category',
            'date_time',
            'image',
            'content',
        )

    def get_type(self, obj):
        return obj.get_type_display()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['author'] = str(User.objects.get(id=ret['author']).username)
        try:
            ret['category'] = str(Category.objects.get(id=ret['category']).category_name)
        except:
            pass
        ret['date_time'] = str(ret['date_time'])
        try:
            ret['image'] = ret['image']
        except:
            ret['image'] = 'no image'
        return ret
