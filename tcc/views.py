"""
Author: VieiraTeam
Last update: 29/11/2018

Views for tcc app.

Contém a lógica da aplicação.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import F
from django.utils import timezone
from datetime import date
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from collections import Counter
from threading import Thread
from .models import *
from .forms import *
from .serializers import *


@login_required
def category_new(request):
    title = "Cadastrar Categoria"
    message = ""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            _, created = Category.objects.get_or_create(name=form.cleaned_data['name'])
            if created:
                form = CategoryForm()
                message = "Cadastrado com sucesso"
            else:
                message = "Categoria existente"
    else:
        form = CategoryForm()
    return render(request, 'tcc/category_edit.html', {'title': title, 'form': form, 'message': message})


@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    title = "Editar Cadastro"
    message = ""
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            try:
                Category.objects.get(name=form.cleaned_data['name'])
                message = "Categoria existente"
            except Category.DoesNotExist:
                category = form.save()
                category.save()
                message = "Alterado com sucesso"
    else:
        form = CategoryForm(instance=category)
    return render(request, 'tcc/category_edit.html', {'title': title, 'form': form, 'message': message})


@login_required
def category_remove(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if category.relationships == 0:
        category.delete()
    return redirect('product_list')


@api_view(['GET'])
def category_get(request):
    if request.method == 'GET':
        categories = Category.objects.filter(relationships__gt=0).order_by('name')
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@login_required
def entertainment_new(request):
    title = 'Novo Entretenimento'
    if request.method == 'POST':
        form = EntertainmentForm(request.POST, request.FILES)
        if form.is_valid():
            entertainment = form.save()
            entertainment.save()
            Thread(target=notify_users(entertainment_notification, entertainment)).start()
            return redirect('entertainment_list')
    else:
        form = EntertainmentForm()
    return render(request, 'tcc/entertainment_edit.html', {'title': title, 'form': form})


@login_required
def entertainment_edit(request, pk):
    entertainment = get_object_or_404(Entertainment, pk=pk)
    title = 'Editar Entretenimento'
    if request.method == 'POST':
        form = EntertainmentForm(request.POST, request.FILES, instance=entertainment)
        if form.is_valid():
            entertainment = form.save()
            entertainment.save()
            return redirect('entertainment_list')
    else:
        form = EntertainmentForm(instance=entertainment)
    return render(request, 'tcc/entertainment_edit.html', {'title': title, 'form': form})


def entertainment_notification(entertainment, user):
    title = entertainment.category.name
    body = entertainment.name
    id_object = entertainment.id
    if entertainment.category.name == 'Receitas':
        loop = True
        for like in user.likes.all():
            for count, string in enumerate(like.name.lower().split(" ")):
                if string in entertainment.desc.lower() or string in entertainment.sub_desc.lower():
                    priority = like.intensity
                    notification = Notification(title=title, body=body, type="ENT", id_object=id_object, priority=priority, user=user)
                    notification.save()
                    loop = False
                    break
                if count == 2:
                    break
            if not loop:
                break
    else:
        notification = Notification(title=title, body=body, type="ENT", id_object=id_object, user=user)
        notification.save()


@login_required
def entertainment_remove(request, pk):
    entertainment = get_object_or_404(Entertainment, pk=pk)
    Notification.objects.filter(type="ENT", id_object=pk).delete()
    entertainment.delete()
    return redirect('entertainment_list')


@login_required
def entertainment_list(request):
    title = 'Entretenimentos'
    entertainments = Entertainment.objects.all().order_by(F('id').desc())
    return render(request, 'tcc/entertainment_list.html', {'title': title, 'entertainments': entertainments})


@api_view(['GET'])
def entertainment_get(request):
    if request.method == 'GET':
        entertainments = Entertainment.objects.all().order_by(F('id').desc())
        serializer = EntertainmentSerializer(entertainments, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def entertainment_get_by_id(request, pk):
    try:
        entertainment = Entertainment.objects.get(pk=pk)
    except Entertainment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = EntertainmentSerializer(entertainment)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def entertainment_category_get(request):
    if request.method == 'GET':
        categories = EntertainmentCategory.objects.all().order_by('name')
        serializer = EntertainmentCategorySerializer(categories, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@login_required
def feedback_remove(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    feedback.delete()
    return redirect('result_list')


@api_view(['GET', 'POST'])
def feedback_rest(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            feedback = Feedback.objects.all()
            questions = Question.objects.all()
            answer_list = {}
            for question in questions:
                answer_list[question.name] = {'Não':0,'Neutro':0,'Sim':0}
            for feed in feedback:
                for answer in feed.answers.all():
                    value = answer_list[answer.question.name][answer.answer]
                    answer_list[answer.question.name][answer.answer] = value + 1
            return JsonResponse(answer_list)

    if request.method == 'POST':
        serializer = FeedbackPostSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.data.get('token')
            message = serializer.data.get('message')
            answers_list = serializer.data.get('answers')
            try:
                user = User.objects.get(email=token)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            feedback = Feedback(user=user, message=message)
            feedback.save()
            questions = Question.objects.all()
            count = 0
            while count < len(answers_list) and count < len(questions):
                question = questions[count]
                if answers_list[count] == 0:
                    alternative = 'Não'
                elif answers_list[count] == 1:
                    alternative = 'Neutro'
                else:
                    alternative = 'Sim'
                answer, created = QuestionArray.objects.get_or_create(question=question, answer=alternative)
                feedback.answers.add(answer)
                count = count + 1
            if count >= len(answers_list) and count >= len(questions):
                Thread(target=feedback_notification(user)).start()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


def feedback_notification(user):
    title = "Olá, " + user.name.split(" ")[0]
    body = "Agradecemos seu feedback, estamos à disposição"
    priority = "100"
    notification = Notification(title=title, body=body, priority=priority, user=user)
    notification.save()


@login_required
def result_list(request):
    feedback = Feedback.objects.all()
    questions = Question.objects.all()
    searches = SearchHistory.objects.all()
    return render(request, 'tcc/result_list.html',
                  {'feedback': feedback, 'questions': questions, 'searches': searches})


@login_required
def measure_new(request):
    title = "Cadastrar Unidade de Medida"
    message = ""
    if request.method == 'POST':
        form = MeasureForm(request.POST)
        if form.is_valid():
            _, created = Measure.objects.get_or_create(name=form.cleaned_data['name'])
            if created:
                form = MeasureForm()
                message = "Cadastrado com sucesso"
            else:
                message = "Unidade de Medida existente"
    else:
        form = MeasureForm()
    return render(request, 'tcc/measure_edit.html', {'title': title, 'form': form, 'message': message})


@login_required
def measure_edit(request, pk):
    measure = get_object_or_404(Measure, pk=pk)
    title = "Editar Cadastro"
    message = ""
    if request.method == 'POST':
        form = MeasureForm(request.POST, instance=measure)
        if form.is_valid():
            try:
                Measure.objects.get(name=form.cleaned_data['name'])
                message = "Unidade de Medida existente"
            except Measure.DoesNotExist:
                measure = form.save()
                measure.save()
                message = "Alterado com sucesso"
    else:
        form = MeasureForm(instance=measure)
    return render(request, 'tcc/measure_edit.html', {'title': title, 'form': form, 'message': message})


@login_required
def measure_remove(request, pk):
    measure = get_object_or_404(Measure, pk=pk)
    if measure.relationships == 0:
        measure.delete()
    return redirect('product_list')


@api_view(['GET'])
def measure_get(request):
    if request.method == 'GET':
        measures = Measure.objects.filter(relationships__gt=0).order_by('name')
        serializer = MeasureSerializer(measures, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@login_required
def notification_new(request):
    title = "Criar Notificação Personalizada"
    message = ""
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            Thread(target=notify_users(custom_notification, form)).start()
            form = NotificationForm()
            message = "Notificações agendadas com sucesso"
    else:
        form = NotificationForm()
    return render(request, 'tcc/notification_new.html', {'form': form, 'title': title, 'message': message})


@api_view(['GET'])
def notification_get(request, slug, pk):
    try:
        user = User.objects.get(email=slug)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        Notification.objects.filter(user=user, id__lte=pk).delete()
        notifications = Notification.objects.filter(user=user).order_by(F('priority').desc())
        for notification in notifications:
            image = '/media/{}'
            if notification.type == 'PRO':
                notification.image = image.format(str(Product.objects.get(pk=notification.id_object).image))
            elif notification.type == 'ENT':
                notification.image = image.format(str(Entertainment.objects.get(pk=notification.id_object).image))
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


def custom_notification(form, user):
    title = form.cleaned_data['title']
    body = form.cleaned_data['body']
    priority = form.cleaned_data['priority']
    notification = Notification(title=title, body=body, priority=priority, user=user)
    notification.save()


def notify_users(function, object):
    users = User.objects.all()
    for user in users:
        function(object, user)


@login_required
def office_hour_new(request):
    title = 'Cadastrar Horário de Atendimento'
    message = ""
    if request.method == 'POST':
        form = OfficeHourForm(request.POST)
        if form.is_valid():
            office_hour = form.save()
            office_hour.save()
            form = OfficeHourForm()
            message = "Cadastrado com sucesso"
    else:
        form = OfficeHourForm()
    return render(request, 'tcc/office_hour_edit.html', {'title': title, 'form': form, 'message': message})


@login_required
def office_hour_edit(request, pk):
    office_hour = get_object_or_404(OfficeHour, pk=pk)
    title = 'Editar Horário de Atendimento'
    message = ""
    if request.method == 'POST':
        form = OfficeHourForm(request.POST, instance=office_hour)
        if form.is_valid():
            office_hour = form.save()
            office_hour.save()
            message = "Alterado com sucesso"
    else:
        form = OfficeHourForm(instance=office_hour)
    return render(request, 'tcc/office_hour_edit.html', {'title': title, 'form': form, 'message': message})


@login_required
def office_hour_remove(request, pk):
    office_hour = get_object_or_404(OfficeHour, pk=pk)
    office_hour.delete()
    return redirect('store_list')


@api_view(['GET'])
def office_hour_get_by_store(request, pk):
    try:
        store = Store.objects.get(pk=pk)
    except Store.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        office_hour = store.office_hour.all()
        serializer = OfficeHourSerializer(office_hour, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@login_required
def product_new(request):
    title = "Cadastrar Produto"
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            product.save()
            relationship = form.cleaned_data['category']
            relationship.add_relationship()
            relationship = form.cleaned_data['measure']
            relationship.add_relationship()
            if product.offer:
                Thread(target=notify_users(product_offer_notification, product)).start()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'tcc/product_edit.html', {'title': title, 'form': form})


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    title = "Editar Cadastro"
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product_old = Product.objects.get(pk=pk)
            if not product_old.offer and form.cleaned_data['offer']:
                Thread(target=notify_users(product_offer_notification, product)).start()
            elif product_old.value > form.cleaned_data['value']:
                Thread(target=product_value_notification(product)).start()
            if product_old.category != form.cleaned_data['category']:
                product_old.category.remove_relationship()
                form.cleaned_data['category'].add_relationship()
            if product_old.measure != form.cleaned_data['measure']:
                product_old.measure.remove_relationship()
                form.cleaned_data['measure'].add_relationship()
            product = form.save()
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'tcc/product_edit.html', {'title': title, 'form': form})


def product_offer_notification(product, user):
    title = 'Olá ' + user.name.split(" ")[0] + ', temos uma oferta especial para você'
    body = product.name + ' ' + product.measure.name + ' por apenas R$ ' + "{:,.2f}".format(product.value)
    id_object = product.id
    for like in user.likes.all():
        if product.category.name.lower() in like.name.lower() or product.name.lower().split(" ")[0] in like.name.lower().split(" ")[0]:
            priority = like.intensity
            notification = Notification(title=title, body=body, type="PRO", id_object=id_object, priority=priority, user=user)
            notification.save()
            break


def product_value_notification(product):
    users = User.objects.all()
    for user in users:
        for like in user.likes.all():
            if product.name.lower() in like.name.lower() or product.category.name.lower() in like.name.lower():
                title = 'Olá ' + user.name.split(" ")[0] + ', abaixamos o preço'
                body = product.name + ' ' + product.measure.name + ' por apenas R$ ' + "{:,.2f}".format(product.value)
                id_object = product.id
                priority = 2
                notification = Notification(title=title, body=body, type="PRO", id_object=id_object, priority=priority, user=user)
                notification.save()
                break


@login_required
def product_remove(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.category.remove_relationship()
    product.measure.remove_relationship()
    Notification.objects.filter(type="PRO", id_object=pk).delete()
    product.delete()
    return redirect('product_list')


@login_required
def product_list(request):
    products = Product.objects.filter(offer=True, validate__lt=timezone.localdate())
    for product in products:
        product.offer = False
        product.save()
    categories = Category.objects.all().order_by('name')
    measures = Measure.objects.all().order_by('name')
    products = Product.objects.all().order_by('name')
    return render(request, 'tcc/product_list.html',
                  {'categories': categories, 'products': products, 'measures': measures})


@api_view(['GET'])
def product_get(request):
    if request.method == 'GET':
        products = Product.objects.all().order_by('?')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def product_get_by_id(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def product_get_offer(request):
    if request.method == 'GET':
        products = Product.objects.filter(offer=True, validate__lt=timezone.localdate())
        for product in products:
            product.offer = False
            product.save()
        products = Product.objects.filter(offer=True).order_by('?')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def question_get(request):
    if request.method == 'GET':
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def search_history_rest(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            search_history = SearchHistory.objects.values_list('product_name', flat=True)
            counter = Counter(search_history)
            return JsonResponse(counter)

    if request.method == 'POST':
        serializer = SearchHistoryPostSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.data.get('token')
            searches = serializer.data.get('search')
            product_name = serializer.data.get('product_name')
            product_category = serializer.data.get('product_category')
            product_visualized = serializer.data.get('product_visualized')
            try:
                user = User.objects.get(email=token)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            search_history = SearchHistory(user=user, product_name=product_name, product_category=product_category, product_visualized=product_visualized)
            search_history.save()
            user_like_add(user, product_name)
            user_like_add(user, product_category)
            for search in searches:
                string, created = Search.objects.get_or_create(string=search)
                search_history.search.add(string)
                user_like_add(user, string)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@login_required
def store_new(request):
    title = 'Cadastrar Loja'
    office_hours = OfficeHour.objects.all()
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            store = form.save()
            store.save()
            return redirect('store_list')
    else:
        form = StoreForm()
    return render(request, 'tcc/store_edit.html', {'title': title, 'form': form, 'office_hours': office_hours})


@login_required
def store_edit(request, pk):
    store = get_object_or_404(Store, pk=pk)
    title = 'Editar Cadastro'
    office_hours = OfficeHour.objects.all()
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES, instance=store)
        if form.is_valid():
            store = form.save()
            store.save()
            return redirect('store_list')
    else:
        form = StoreForm(instance=store)
    return render(request, 'tcc/store_edit.html', {'title': title, 'form': form, 'office_hours': office_hours})


@login_required
def store_remove(request, pk):
    store = get_object_or_404(Store, pk=pk)
    store.delete()
    return redirect('store_list')


@login_required
def store_list(request):
    stores = Store.objects.all().order_by('city')
    office_hours = OfficeHour.objects.all().order_by('weekday')
    return render(request, 'tcc/store_list.html', {'stores': stores, 'office_hours': office_hours})


@api_view(['GET'])
def store_get(request):
    if request.method == 'GET':
        stores = Store.objects.all().order_by('city')
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_post(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            email = serializer.data.get('email')
            user, created = User.objects.get_or_create(name=name, email=email)
            if created:
                title = 'Bem vindo(a), ' + name
                notification = Notification(title=title, body='Cadastro realizado com sucesso', user=user)
                notification.save()
                http_status = status.HTTP_201_CREATED
            else:
                http_status = status.HTTP_200_OK
            return Response(serializer.data, status=http_status)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


def user_like_add(user, string):
    try:
        like = user.likes.get(name=string)
        like.intensity = like.intensity + 1
        like.save()
    except Like.DoesNotExist:
        like = Like(name=string)
        like.save()
        user.likes.add(like)


@login_required
def user_list(request):
    title = 'Usuários Cadastrados'
    users = User.objects.all().order_by('name')
    return render(request, 'tcc/user_list.html', {'title': title, 'users': users})
