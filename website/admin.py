from django.contrib import admin

from website.models import Post, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'categories_name',
        'date_time',
    )

    readonly_fields = (
        'date_time',
        'reply_to',
    )

    fields = (
        'title',
        'author',
        'category',
        'date_time',
        'image',
        'content',
        'reply_to',
    )

    def save_related(self, request, form, formsets, change):
        super(PostAdmin, self).save_related(request, form, formsets, change)
        ca = form.instance.category.all()[0]
        i = 0
        cat = Category.objects.get(id=ca.id)
        while True:
            if cat.is_sub_category:
                cat = Category.objects.get(id=cat.parent.id)
                form.instance.category.add(cat)
            else:
                break
            i += 1

    @admin.display(description="دسته ها", empty_value='???')
    def categories_name(self, obj):
        list_names = ''
        for category in obj.category.all():
            list_names = list_names + ", " + str(category.name)
        return list_names


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'parent',
        'is_sub_category',
        'sub_lvl',
    )
    readonly_fields = (
        'is_sub_category',
        'sub_lvl',
    )
    fields = (
        'parent',
        'name',
        'is_sub_category',
        'sub_lvl',
    )

