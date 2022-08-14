"""
Author: VieiraTeam
Last update: 28/11/2018

Forms for tcc app.

Os usuários da aplicação somente terão permissões de leitura e escrita
sobre as classes que contém um modelo de formulário.
"""

from django import forms
from .models import Category, Entertainment, Measure, Notification, OfficeHour, Product, Store


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)


class EntertainmentForm(forms.ModelForm):
    class Meta:
        model = Entertainment
        fields = '__all__'


class MeasureForm(forms.ModelForm):
    class Meta:
        model = Measure
        fields = ('name',)


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ('title', 'body', 'priority')


class OfficeHourForm(forms.ModelForm):
    class Meta:
        model = OfficeHour
        fields = '__all__'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = '__all__'
