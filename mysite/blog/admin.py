from django.contrib import admin
from .models import Post, Comment,export_csv,Category

admin.site.register(Category)




@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug','category', 'author','created','updated', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author','category')
    list_editable = ('slug','category', 'author', 'publish', 'status')
    search_fields = ('title', 'body','category')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    list_per_page = 5
    list_max_show_all = 8


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')




class MyModelAdmin(admin.ModelAdmin):
    
    actions = [export_csv]


