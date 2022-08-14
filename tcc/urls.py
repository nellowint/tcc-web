"""
Author: VieiraTeam
Last update: 28/11/2018

Urls for tcc app.

Urls utilizadas pelo módulo Web e pelo módulo App.
"""

from django.conf.urls import url
from . import views


urlpatterns = [
    # Feedback, Question, SearchHistory
    url(r'^$', views.result_list, name="result_list"),
    # Category
    url(r'^category/new/$', views.category_new, name="category_new"),
    url(r'^category/(?P<pk>\d+)/edit/$', views.category_edit, name="category_edit"),
    url(r'^category/(?P<pk>\d+)/remove/$', views.category_remove, name="category_remove"),
    url(r'^get/category/$', views.category_get, name="category_get"),
    # Entertainment
    url(r'^entertainment/new/$', views.entertainment_new, name="entertainment_new"),
    url(r'^entertainment/(?P<pk>\d+)/edit/$', views.entertainment_edit, name="entertainment_edit"),
    url(r'^entertainment/(?P<pk>\d+)/remove/$', views.entertainment_remove, name="entertainment_remove"),
    url(r'^entertainment/$', views.entertainment_list, name="entertainment_list"),
    url(r'^get/entertainment/$', views.entertainment_get, name="entertainment_get"),
    url(r'^get/entertainment/(?P<pk>\d+)/$', views.entertainment_get_by_id, name="entertainment_get_by_id"),
    # EntertainmentCategory
    url(r'^get/entertainment/category/$', views.entertainment_category_get, name="entertainment_category_get"),
    # Feedback
    url(r'^feedback/(?P<pk>\d+)/remove/$', views.feedback_remove, name="feedback_remove"),
    url(r'^get/feedback/$', views.feedback_rest, name="feedback_get"),
    url(r'^post/feedback/$', views.feedback_rest, name="feedback_post"),
    # Measure
    url(r'^measure/new/$', views.measure_new, name="measure_new"),
    url(r'^measure/(?P<pk>\d+)/edit/$', views.measure_edit, name="measure_edit"),
    url(r'^measure/(?P<pk>\d+)/remove/$', views.measure_remove, name="measure_remove"),
    url(r'^get/measure/$', views.measure_get, name="measure_get"),
    # Notification
    url(r'^notification/new/$', views.notification_new, name="notification_new"),
    url(r'^get/notification/(?P<slug>[-\w.@]+)/(?P<pk>\d+)/$', views.notification_get, name="notification_get"),
    # OfficeHour
    url(r'^office_hour/new/$', views.office_hour_new, name="office_hour_new"),
    url(r'^office_hour/(?P<pk>\d+)/edit/$', views.office_hour_edit, name="office_hour_edit"),
    url(r'^office_hour/(?P<pk>\d+)/remove/$', views.office_hour_remove, name="office_hour_remove"),
    url(r'^get/office_hour/store/(?P<pk>\d+)/$', views.office_hour_get_by_store, name="office_hour_get_by_store"),
    # Product
    url(r'^product/new/$', views.product_new, name="product_new"),
    url(r'^product/(?P<pk>\d+)/edit/$', views.product_edit, name="product_edit"),
    url(r'^product/(?P<pk>\d+)/remove/$', views.product_remove, name="product_remove"),
    url(r'^product/$', views.product_list, name="product_list"),
    url(r'^get/product/$', views.product_get, name="product_get"),
    url(r'^get/product/offer/$', views.product_get_offer, name="product_get_offer"),
    url(r'^get/product/(?P<pk>\d+)/$', views.product_get_by_id, name="product_get_by_id"),
    # Question
    url(r'^get/question/$', views.question_get, name="question_get"),
    # SearchHistory
    url(r'^get/history/search/$', views.search_history_rest, name="search_history_get"),
    url(r'^post/history/search/$', views.search_history_rest, name="search_history_post"),
    # Store
    url(r'^store/new/$', views.store_new, name="store_new"),
    url(r'^store/(?P<pk>\d+)/edit/$', views.store_edit, name="store_edit"),
    url(r'^store/(?P<pk>\d+)/remove/$', views.store_remove, name="store_remove"),
    url(r'^store/$', views.store_list, name="store_list"),
    url(r'^get/store/$', views.store_get, name="store_get"),
    # User
    url(r'^post/user/$', views.user_post, name="user_post"),
    url(r'^user/$', views.user_list, name="user_list"),
]
