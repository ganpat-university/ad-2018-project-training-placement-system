from django.contrib import admin
from .models import Student,Company,Post,Document

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Student)
admin.site.register(Company)
admin.site.register(Document)
admin.site.register(Post, PostAdmin)