"""
Author: VieiraTeam
Last update: 29/11/2018

Serializers for tcc app models.

Classes utilizadas para serializar objetos.
"""

from rest_framework import serializers
from .models import Category, Entertainment, EntertainmentCategory, Feedback, Measure, Notification, OfficeHour, Product, Question, SearchHistory, Store, User


class IntListField(serializers.ListField):
    """
    Classe utilizada para criar uma lista serializada de IntegerField.

    ...

    Extends
    ----------
    serializers.ListField
        Uma classe de campo que valida uma lista de objetos

    Attributes
    ----------
    child : serializers.IntegerField
        uma instância de campo que deve ser usada para validar os objetos na lista
    """
    child = serializers.IntegerField(min_value=0, max_value=25)


class CharListField(serializers.ListField):
    """
    Classe utilizada para criar uma lista serializada de CharField.

    ...

    Extends
    ----------
    serializers.ListField
        Uma classe de campo que valida uma lista de objetos

    Attributes
    ----------
    child : serializers.CharField
        uma instância de campo que deve ser usada para validar os objetos na lista
    """
    child = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    """
    Classe utilizada para serializar objetos do tipo Category.
    Método da requisição: GET (via App).

    ...

    Extends
    ----------
    serializers.ModelSerializer
        Fornece um atalho que permite criar automaticamente uma classe Serializer com campos que correspondem aos campos Model
    """
    class Meta:
        """
        Apenas os campos ('id', 'name') da classe Category poderão ser serializados.
        """
        model = Category
        fields = ('id', 'name')


class EntertainmentSerializer(serializers.ModelSerializer):
    """
    Classe utilizada para serializar objetos do tipo Entertainment.
    Método da requisição: GET (via App).

    ...

    Extends
    ----------
    serializers.ModelSerializer
        Fornece um atalho que permite criar automaticamente uma classe Serializer com campos que correspondem aos campos Model

    Attributes
    ----------
    category : serializers.CharField
        uma representação de texto para serializar um campo de relacionamento
    """
    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        """
        Todos os campos da classe Entertainment poderão ser serializados
        """
        model = Entertainment
        fields = '__all__'


class EntertainmentCategorySerializer(serializers.ModelSerializer):
    """
    Classe utilizada para serializar objetos do tipo EntertainmentCategory.
    Método da requisição: GET (via App).

    ...

    Extends
    ----------
    serializers.ModelSerializer
        Fornece um atalho que permite criar automaticamente uma classe Serializer com campos que correspondem aos campos Model
    """
    class Meta:
        """
        Todos os campos da classe EntertainmentCategory poderão ser serializados
        """
        model = EntertainmentCategory
        fields = '__all__'


class FeedbackPostSerializer(serializers.ModelSerializer):
    """
    Classe utilizada para serializar objetos do tipo Feedback.
    Método da requisição: POST (via App).

    ...

    Extends
    ----------
    serializers.ModelSerializer
        Fornece um atalho que permite criar automaticamente uma classe Serializer com campos que correspondem aos campos Model

    Attributes
    ----------
    answers : IntListField
        uma instância de objeto para criar uma lista de inteiros
    token : serializers.CharField
        uma representação de texto para serializar o token do usuário por questão segurança
    """
    answers = IntListField()
    token = serializers.CharField()

    class Meta:
        """
        Apenas os campos ('user.token', 'message', 'answers') da classe Feedback poderão ser serializados
        """
        model = Feedback
        fields = ('token', 'message', 'answers')


class MeasureSerializer(serializers.ModelSerializer):
    """
    Classe utilizada para serializar objetos do tipo Measure.
    Método da requisição: GET (via App).

    ...

    Extends
    ----------
    serializers.ModelSerializer
        Fornece um atalho que permite criar automaticamente uma classe Serializer com campos que correspondem aos campos Model
    """
    class Meta:
        """
        Apenas os campos ('id', 'name') da classe Measure poderão ser serializados
        """
        model = Measure
        fields = ('id', 'name')


class NotificationSerializer(serializers.ModelSerializer):
    """
    Classe utilizada para serializar objetos do tipo Notification.
    Método da requisição: GET (via App).

    ...

    Extends
    ----------
    serializers.ModelSerializer
        Fornece um atalho que permite criar automaticamente uma classe Serializer com campos que correspondem aos campos Model

    Attributes
    ----------
    type : serializers.CharField
        uma representação de texto para serializar o tipo da notificação
    """
    type = serializers.CharField(source='get_type_display')
    token = serializers.CharField(source='user.email', read_only=True)
    image = serializers.CharField(default='/static/images/icon_round.png')

    class Meta:
        """
        Apenas os campos ('id', 'title', 'body', 'type', 'id_object', 'user.token') da classe Notification poderão ser serializados
        """
        model = Notification
        fields = ('id', 'title', 'body', 'type', 'id_object', 'token', 'image')

    @staticmethod
    def get_type(obj):
        """
        Método estático que retorna o nome do tipo da notifcação.

        Parameters
        ----------
        obj : Notification
            Instância do objeto da classe Notification

        Returns
        -------
        str
            a string associada a chave do dia da semana
        """
        return obj.get_type_display()


class OfficeHourSerializer(serializers.ModelSerializer):
    """
    Classe utilizada para serializar objetos do tipo OfficeHour.
    Método da requisição: GET (via App).

    ...

    Extends
    ----------
    serializers.ModelSerializer
        Fornece um atalho que permite criar automaticamente uma classe Serializer com campos que correspondem aos campos Model

    Attributes
    ----------
    weekday : serializers.CharField
        uma representação de texto para serializar o dia da semana
    """
    weekday = serializers.CharField(source='get_weekday_display')

    class Meta:
        """
        Todos os campos da classe OfficeHour poderão ser serializados
        """
        model = OfficeHour
        fields = '__all__'

    @staticmethod
    def get_weekday(obj):
        """
        Método estático que retorna o nome do dia da semana.

        Parameters
        ----------
        obj : OfficeHour
            Instância do objeto da classe OfficeHour

        Returns
        -------
        str
            a string associada a chave do dia da semana
        """
        return obj.get_weekday_display()


class ProductSerializer(serializers.ModelSerializer):
    """
    Classe utilizada para serializar objetos do tipo Product.
    Método da requisição: GET (via App).

    ...

    Extends
    ----------
    serializers.ModelSerializer
        Fornece um atalho que permite criar automaticamente uma classe Serializer com campos que correspondem aos campos Model

    Attributes
    ----------
    category_name : serializers.CharField
        uma representação de texto para serializar o nome da categoria relacionada
    measure_name : serializers.CharField
        uma representação de texto para serializar o nome da unidade de medida relacionada
    store_name : serializers.ReadOnlyField
        retorna uma lista dos nomes das lojas relacionadas sem modificação
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    measure_name = serializers.CharField(source='measure.name', read_only=True)
    store_name = serializers.ReadOnlyField()

    class Meta:
        """
        Apenas os campos ('id', 'name', 'image', 'value', 'offer', 'validate', 'category', 'measure', 'store') da classe Product poderão ser serializados
        """
        model = Product
        fields = ('id', 'name', 'image', 'value', 'offer', 'validate', 'category_name', 'measure_name', 'store_name')


class QuestionSerializer(serializers.ModelSerializer):
    """
    Classe utilizada para serializar objetos do tipo Question.
    Método da requisição: GET (via App).

    ...

    Extends
    ----------
    serializers.ModelSerializer
        Fornece um atalho que permite criar automaticamente uma classe Serializer com campos que correspondem aos campos Model
    """
    class Meta:
        """
        Todos os campos da classe Question poderão ser serializados
        """
        model = Question
        fields = '__all__'


class SearchHistoryPostSerializer(serializers.ModelSerializer):
    """
    Classe utilizada para serializar objetos do tipo SearchHistory.
    Método da requisição: POST (via App).

    ...

    Extends
    ----------
    serializers.ModelSerializer
        Fornece um atalho que permite criar automaticamente uma classe Serializer com campos que correspondem aos campos Model

    Attributes
    ----------
    search_history : serializers.ReadOnlyField
        retorna uma lista de string das pesquisas realizadas sem modificação
    token : serializers.CharField
        uma representação de texto para serializar o token do usuário por questão segurança
    """
    token = serializers.CharField()
    search = CharListField()

    class Meta:
        """
        Apenas os campos ('user.token', 'search', 'product_name', 'product_visualized') da classe SearchHistory poderão ser serializados
        """
        model = SearchHistory
        fields = ('token', 'search', 'product_name', 'product_category', 'product_visualized')


class StoreSerializer(serializers.ModelSerializer):
    """
    Classe utilizada para serializar objetos do tipo Store.
    Método da requisição: GET (via App).

    ...

    Extends
    ----------
    serializers.ModelSerializer
        Fornece um atalho que permite criar automaticamente uma classe Serializer com campos que correspondem aos campos Model
    """
    class Meta:
        """
        Apenas os campos ('id', 'name', 'address', 'neighborhood', 'city', 'phone', 'email', 'latitude', 'longitude', 'image') da classe Store poderão ser serializados
        """
        model = Store
        fields = ('id', 'name', 'address', 'neighborhood', 'city', 'phone', 'email', 'latitude', 'longitude', 'image')


class UserSerializer(serializers.ModelSerializer):
    """
    Classe utilizada para serializar objetos do tipo User.
    Método da requisição: POST (via App).

    ...

    Extends
    ----------
    serializers.ModelSerializer
        Fornece um atalho que permite criar automaticamente uma classe Serializer com campos que correspondem aos campos Model
    """

    class Meta:
        """
        Apenas os campos ('name', 'email') da classe User poderão ser serializados
        """
        model = User
        fields = ('name', 'email')
