"""
Author: VieiraTeam
Last update: 28/11/2018

Admin registers for tcc app.

O usuário administrador terá todas as permissões CRUD sobre as classes.
"""

from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'relationships')
    search_fields = ('name',)
    ordering = ('name',)


class EntertainmentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


class EntertainmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
    ordering = ('name',)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'message')
    search_fields = ('message',)
    filter_horizontal = ('answers',)
    raw_id_fields = ('user',)


class LikeAdmin(admin.ModelAdmin):
    list_display = ('name', 'intensity')
    search_fields = ('name',)
    ordering = ('name',)


class MeasureAdmin(admin.ModelAdmin):
    list_display = ('name', 'relationships')
    search_fields = ('name',)
    ordering = ('name',)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'body', 'type', 'id_object', 'priority')
    list_filter = ('type',)
    search_fields = ('title', 'body')
    raw_id_fields = ('user',)


class OfficeHourAdmin(admin.ModelAdmin):
    list_display = ('weekday', 'hour_start', 'hour_final', 'date')
    list_filter = ('weekday', 'hour_start', 'hour_final')
    search_fields = ('weekday',)
    date_hierarchy = 'date'
    ordering = ('weekday', 'hour_start', 'hour_final')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'measure', 'category', 'value', 'offer', 'validate')
    list_filter = ('offer', 'category', 'measure')
    search_fields = ('name',)
    date_hierarchy = 'validate'
    ordering = ('name', 'category')
    filter_horizontal = ('store',)
    raw_id_fields = ('category',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


class QuestionArrayAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')
    list_filter = ('question',)
    search_fields = ('question',)
    ordering = ('question',)


class SearchAdmin(admin.ModelAdmin):
    list_display = ('string',)
    search_fields = ('string',)
    ordering = ('string',)


class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_name', 'product_category', 'product_visualized')
    list_filter = ('product_visualized', 'user', 'product_category')
    search_fields = ('product_name', 'product_category')
    filter_horizontal = ('search',)
    raw_id_fields = ('user',)


class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'neighborhood', 'city', 'phone', 'email')
    search_fields = ('name', 'address', 'neighborhood', 'city', 'phone', 'email')
    ordering = ('name', 'city')
    filter_horizontal = ('office_hour',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')
    filter_horizontal = ('likes',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Entertainment, EntertainmentAdmin)
admin.site.register(EntertainmentCategory, EntertainmentCategoryAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Measure, MeasureAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(OfficeHour, OfficeHourAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionArray, QuestionArrayAdmin)
admin.site.register(Search, SearchAdmin)
admin.site.register(SearchHistory, SearchHistoryAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(User, UserAdmin)
