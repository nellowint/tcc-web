"""
Author: VieiraTeam
Last update: 29/11/2018

Models for tcc app.

Para melhor entendimento, veja o diagrama de classes.
"""

from django.db import models
    

class Category(models.Model):
    """
    Classe utilizada para armazenar objetos do tipo Category.

    ...

    Extends
    ----------
    models.Model
        Contém os campos e comportamentos essenciais dos dados.

    Attributes
    ----------
    name : models.CharField, required
        Um campo de string, para o nome.
    relationships : models.PositiveIntegerField, optional, default 0
        Como um IntegerField, mas deve ser positivo (0 a 2147483647).
    """
    name = models.CharField(max_length=100, verbose_name="Categoria", help_text="Somente texto (máx. 100 caracteres)")
    relationships = models.PositiveIntegerField(default=0, verbose_name="Relacionamentos")

    def add_relationship(self):
        """
        Sum new relationship.
        """
        self.relationships = self.relationships + 1
        self.save()

    def remove_relationship(self):
        """
        Remove relationship.
        """
        self.relationships = self.relationships - 1
        self.save()

    def __str__(self):
        """
        Sobrescreve método toString.

        Returns
        -------
        str
            Valor do atributo name.
        """
        return self.name


class EntertainmentCategory(models.Model):
    """
    Classe utilizada para armazenar objetos do tipo EntertainmentCategory.

    ...

    Extends
    ----------
    models.Model
        Contém os campos e comportamentos essenciais dos dados.

    Attributes
    ----------
    name : models.CharField, required
        Um campo de string, para o nome (da categoria do entretenimento).
    """
    name = models.CharField(max_length=100, verbose_name="Categoria")

    def __str__(self):
        """
        Sobrescreve método toString.

        Returns
        -------
        str
            Valor do atributo name.
        """
        return self.name


class Entertainment(models.Model):
    """
    Classe utilizada para armazenar objetos do tipo Entertainment.

    ...

    Extends
    ----------
    models.Model
        Contém os campos e comportamentos essenciais dos dados.

    Attributes
    ----------
    name : models.CharField, required
        Um campo de string, para o nome.
    image : models.ImageField, required
        Herda todos os atributos e métodos do FileField, mas também valida se o objeto carregado é uma imagem válida.
    desc : models.TextField, required
        Um grande campo de texto para descrição.
    sub_desc : models.TextField, optional, default null
        Um grande campo de texto para sub descrição (somente para categoria "Receitas").
    category : models.ForeignKey, required
        Um relacionamento muitos-para-um com EntertainmentCategory
    """
    name = models.CharField(max_length=100, verbose_name="Nome", help_text="Somente texto (máx. 100 caracteres)")
    image = models.ImageField(verbose_name="Imagem")
    desc = models.TextField(verbose_name="Descrição")
    sub_desc = models.TextField(blank=True, null=True, verbose_name="Modo de preparo")
    category = models.ForeignKey(EntertainmentCategory, on_delete=models.CASCADE, verbose_name="Categoria")

    def __str__(self):
        """
        Sobrescreve método toString.

        Returns
        -------
        str
            Valor do atributo name.
        """
        return self.name


class Like(models.Model):
    """
    Classe utilizada para criar uma lista de CharField (relacionada à classe User).

    ...

    Extends
    ----------
    models.Model
        Contém os campos e comportamentos essenciais dos dados.

    Attributes
    ----------
    name : models.CharField, required
        Um campo de string, para strings de tamanho pequeno a grande.
    intensity : models.PositiveSmallIntegerField, optional, default 0
        Como um PositiveSmallIntegerField, mas apenas permite valores entre 0 e 32767.
    """
    name = models.CharField(max_length=100, verbose_name="Nome")
    intensity = models.PositiveSmallIntegerField(default=0, verbose_name="Intensidade")

    def __str__(self):
        """
        Sobrescreve método toString.

        Returns
        -------
        str
            Valor do atributo name.
        """
        return self.name


class Measure(models.Model):
    """
    Classe utilizada para armazenar objetos do tipo Measure.

    ...

    Extends
    ----------
    models.Model
        Contém os campos e comportamentos essenciais dos dados.

    Attributes
    ----------
    name : models.CharField, required
        Um campo de string, para o nome.
    relationships : models.PositiveIntegerField, optional, default 0
        Como um IntegerField, mas deve ser positivo (0 a 2147483647).
    """
    name = models.CharField(max_length=100, verbose_name="Unidade de medida", help_text="Somente texto (máx. 100 caracteres)")
    relationships = models.PositiveIntegerField(default=0, verbose_name="Relacionamentos")

    def add_relationship(self):
        """
        Sum new relationship.
        """
        self.relationships = self.relationships + 1
        self.save()

    def remove_relationship(self):
        """
        Remove relationship.
        """
        self.relationships = self.relationships - 1
        self.save()

    def __str__(self):
        """
        Sobrescreve método toString.

        Returns
        -------
        str
            Valor do atributo name.
        """
        return self.name


class OfficeHour(models.Model):
    """
    Classe utilizada para armazenar objetos do tipo OfficeHour.

    ...

    Extends
    ----------
    models.Model
        Contém os campos e comportamentos essenciais dos dados.

    Attributes
    ----------
    WEEKDAY : tuple
        Uma tupla (constante) que armazena tuplas de alternativas
    date : models.DateField, optional, default null
        Data para espediente específico.
    hour_start : models.TimeField, required
        Hora de início do espediente.
    hour_final : models.TimeField, required
        Hora de fim do espediente.
    weekday : models.CharField, required
        Um campo de string, para o dia da semana.
    """
    WEEKDAY = (
        ('1', 'Domingo'),
        ('2', 'Segunda-feira'),
        ('3', 'Terça-feira'),
        ('4', 'Quarta-feira'),
        ('5', 'Quinta-feira'),
        ('6', 'Sexta-feira'),
        ('7', 'Sábado'),
    )
    date = models.DateField(blank=True, null=True, verbose_name="Data específica")
    hour_start = models.TimeField(verbose_name="Hora inicial")
    hour_final = models.TimeField(verbose_name="Hora final")
    weekday = models.CharField(max_length=1, choices=WEEKDAY, verbose_name="Dia da semana")

    def __str__(self):
        """
        Sobrescreve método toString.

        Returns
        -------
        str
            Valores de todos os atributos concatenados.
        """
        string = self.get_weekday_display()
        if self.date:
            string = string + ', ' + str(self.date.day) + '/' + str(self.date.month) + '/' + str(self.date.year)
        string = string + ': ' + str(self.hour_start) + ' às ' + str(self.hour_final)
        return string


class Question(models.Model):
    """
    Classe utilizada para armazenar objetos do tipo Question.

    ...

    Extends
    ----------
    models.Model
        Contém os campos e comportamentos essenciais dos dados.

    Attributes
    ----------
    name : models.CharField, required
        Um campo de string, para o nome.
    """
    name = models.CharField(max_length=100, verbose_name="Questão")

    def __str__(self):
        """
        Sobrescreve método toString.

        Returns
        -------
        str
            Valor do atributo name.
        """
        return self.name


class QuestionArray(models.Model):
    """
    Classe utilizada para armazenar objetos do tipo QuestionArray.

    ...

    Extends
    ----------
    models.Model
        Contém os campos e comportamentos essenciais dos dados.

    Attributes
    ----------
    question : models.ForeignKey, required
        Um relacionamento muitos-para-um com Question
    ALTERNATIVES : tuple
        Uma tupla (constante) que armazena tuplas de alternativas
    answer : models.CharField, required
        Um campo de string, para a resposta.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Questão")
    ALTERNATIVES = (
        ('Não', 0),
        ('Neutro', 1),
        ('Sim', 2)
    )
    answer = models.CharField(max_length=6, choices=ALTERNATIVES, verbose_name="Resposta")

    def __str__(self):
        """
        Sobrescreve método toString.

        Returns
        -------
        str
            Valor do atributo answer.
        """
        return self.answer


class Search(models.Model):
    """
    Classe utilizada para criar uma lista de CharField (relacionada à classe SearchHistory).

    ...

    Extends
    ----------
    models.Model
        Contém os campos e comportamentos essenciais dos dados.

    Attributes
    ----------
    string : models.CharField, required
        Um campo de string, para strings de tamanho pequeno a grande.
    """
    string = models.CharField(max_length=100)

    def __str__(self):
        """
        Sobrescreve método toString.

        Returns
        -------
        str
            Valor do atributo string.
        """
        return self.string


class Store(models.Model):
    """
    Classe utilizada para armazenar objetos do tipo Store.

    ...

    Extends
    ----------
    models.Model
        Contém os campos e comportamentos essenciais dos dados.

    Attributes
    ----------
    name : models.CharField, required
        Um campo de string, para o nome.
    address : models.CharField, required
        Um campo de string, para o endereço.
    neighborhood : models.CharField, required
        Um campo de string, para o bairro.
    city : models.CharField, required
        Um campo de string, para a cidade.
    phone : models.CharField, required
        Um campo de string, para o telefone.
    email : models.EmailField, optional, default null
        Um campo de string que valida e-mails, para o e-mail.
    latitude : models.CharField, required
        Um campo de string, para a latitude
    longitude : models.CharField, required
        Um campo de string, para a longitude.
    image : models.ImageField, required
        Herda todos os atributos e métodos do FileField, mas também valida se o objeto carregado é uma imagem válida.
    office_hour : models.ManyToManyField, required
        Um relacionamento muitos-para-um com OfficeHour.
    """
    name = models.CharField(max_length=100, verbose_name="Nome", help_text="Somente texto (máx. 100 caracteres)")
    address = models.CharField(max_length=100, verbose_name="Endereço", help_text="Somente texto (máx. 100 caracteres)")
    neighborhood = models.CharField(max_length=100, verbose_name="Bairro", help_text="Somente texto (máx. 100 caracteres)")
    city = models.CharField(max_length=100, verbose_name="Cidade", help_text="Somente texto (máx. 100 caracteres)")
    phone = models.CharField(max_length=20, verbose_name="Telefone", help_text="Inserir no formato (DDD)____-____ (máx. 20 caracteres)")
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name="E-mail", help_text="Opcional (máx. 100 caracteres)")
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    image = models.ImageField(verbose_name="Imagem")
    office_hour = models.ManyToManyField(OfficeHour, verbose_name="Horário de atendimento")

    def __str__(self):
        """
        Sobrescreve método toString.

        Returns
        -------
        str
            Valor do atributo name.
        """
        return self.name


class Product(models.Model):
    """
    Classe utilizada para armazenar objetos do tipo Product.

    ...

    Extends
    ----------
    models.Model
        Contém os campos e comportamentos essenciais dos dados.

    Attributes
    ----------
    name : models.CharField, required
        Um campo de string, para o nome.
    image : models.ImageField, required
        Herda todos os atributos e métodos do FileField, mas também valida se o objeto carregado é uma imagem válida.
    value : models.FloatField, required
        Um número de ponto flutuante para o valor.
    offer : models.BooleanField, optional, default False
        Um campo verdadeiro / falso para em oferta.
    validate : models.DateField, optional, default null
        Data de validade do valor do produto
    category : models.ForeignKey, required
        Um relacionamento muitos-para-um com Category
    measure : models.ForeignKey, required
        Um relacionamento muitos-para-um com Measure
    store : models.ManyToManyField, required
        Um relacionamento muitos-para-um com Store.
    """
    name = models.CharField(max_length=100, verbose_name="Nome", help_text="Somente texto (máx. 100 caracteres)")
    image = models.ImageField(verbose_name="Imagem")
    value = models.FloatField(verbose_name="Valor", help_text="Para inserir centavos utilize '.' ou ','")
    offer = models.BooleanField(default=False, verbose_name="Em oferta")
    validate = models.DateField(blank=True, null=True, verbose_name="Validade do preço")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Categoria")
    measure = models.ForeignKey(Measure, on_delete=models.CASCADE, verbose_name="Unidade de medida")
    store = models.ManyToManyField(Store, verbose_name="Lojas")

    def __str__(self):
        """
        Sobrescreve método toString.

        Returns
        -------
        str
            Valor do atributo name concatenado com o valor do atributo measure.name.
        """
        return self.name + ' ' + self.measure.name

    @property
    def store_name(self):
        """
        Objeto especial

        Returns
        -------
        list
            lista de string do atributo 'name' dos objetos do tipo Store relacionados
        """
        return self.store.values_list('name', flat=True)


class User(models.Model):
    """
    Classe utilizada para armazenar objetos do tipo User.

    ...

    Extends
    ----------
    models.Model
        Contém os campos e comportamentos essenciais dos dados.

    Attributes
    ----------
    name : models.CharField, required
        Um campo de string, para o nome.
    email : models.EmailField, required
        Um campo de string que valida e-mails, para o e-mail.
    likes : models.ManyToManyField
        Um relacionamento muitos-para-um com Like.
    """
    name = models.CharField(max_length=100, verbose_name="Usuário")
    email = models.EmailField(verbose_name="E-mail")
    likes = models.ManyToManyField(Like, verbose_name="Gostos")

    def __str__(self):
        """
        Sobrescreve método toString.

        Returns
        -------
        str
            Valor do atributo name.
        """
        return self.name


class Feedback(models.Model):
    """
    Classe utilizada para armazenar objetos do tipo Feedback.

    ...

    Extends
    ----------
    models.Model
        Contém os campos e comportamentos essenciais dos dados.

    Attributes
    ----------
    user : models.ForeignKey, required
        Um relacionamento muitos-para-um com User.
    message : models.TextField, optional, default null
        Um grande campo de texto para mensagem.
    answers : models.ManyToManyField, required
        Um relacionamento muitos-para-um com QuestionArray.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    message = models.TextField(blank=True, null=True, verbose_name="Mensagem")
    answers = models.ManyToManyField(QuestionArray, verbose_name="Respostas")

    def __str__(self):
        """
        Sobrescreve método toString.

        Returns
        -------
        str
            Valor do atributo message (se não nulo).
        """
        if self.message:
            return self.message
        else:
            return '(Feedback sem mensagem)'
        


class Notification(models.Model):
    """
    Classe utilizada para armazenar objetos do tipo Notification.

    ...

    Extends
    ----------
    models.Model
        Contém os campos e comportamentos essenciais dos dados.

    Attributes
    ----------
    TYPE : tuple
        Uma tupla (constante) que armazena tuplas de alternativas
    title : models.CharField, required
        Um campo de string, para o título.
    body : models.CharField, required
        Um campo de string, para o corpo da mensagem.
    type : models.CharField, optional, default CUS
        Um campo de string, para o tipo de notificação.
    id_object : models.PositiveIntegerField, optional, default 0
        Como um IntegerField, mas deve ser positivo (0 a 2147483647).
    priority : models.PositiveIntegerField, optional, default 0
        Como um IntegerField, mas deve ser positivo (0 a 2147483647).
    user : models.ForeignKey, required
        Um relacionamento muitos-para-um com User.
    """
    TYPE = (
        ('CUS', 'custom'),
        ('ENT', 'entertainment'),
        ('PRO', 'product'),
        ('STO', 'store'),
    )
    title = models.CharField(max_length=100, verbose_name="Título", help_text="Somente texto (máx. 100 caracteres)")
    body = models.CharField(max_length=100, verbose_name="Mensagem")
    type = models.CharField(max_length=3, default="CUS", choices=TYPE, verbose_name="Tipo")
    id_object = models.PositiveIntegerField(default=0, verbose_name="Id objeto")
    priority = models.PositiveIntegerField(default=0, verbose_name="Prioridade", help_text="Insira um número inteiro. A notificação com maior prioridade será a exibida no aplicativo. Padrão: 0")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")

    def __str__(self):
        """
        Sobrescreve método toString.

        Returns
        -------
        str
            Valor do atributo title.
        """
        return self.title


class SearchHistory(models.Model):
    """
    Classe utilizada para armazenar objetos do tipo SearchHistory.

    ...

    Extends
    ----------
    models.Model
        Contém os campos e comportamentos essenciais dos dados.

    Attributes
    ----------
    user : models.ForeignKey, required
        Um relacionamento muitos-para-um com User.
    search : models.ManyToManyField, required
        Um relacionamento muitos-para-um com Search.
    product_name : models.CharField, required
        Um campo de string, para o nome do produto.
    product_category : models.CharField, required
        Um campo de string, para o nome da categoria do produto
    product_visualized : models.BooleanField, optional, default False
        Um campo verdadeiro / falso para produto visualizado.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    search = models.ManyToManyField(Search, verbose_name="Pesquisas")
    product_name = models.CharField(max_length=100, verbose_name="Produto")
    product_category = models.CharField(max_length=100, verbose_name="Categoria do produto")
    product_visualized = models.BooleanField(default=False, verbose_name="Produto pesquisado")

    def __str__(self):
        """
        Sobrescreve método toString.

        Returns
        -------
        str
            Valor do atributo product_name.
        """
        return self.product_name

    @property
    def search_history(self):
        """
        Objeto especial

        Returns
        -------
        list
            lista de string do atributo 'string' dos objetos do tipo Search relacionados
        """
        return self.search.values_list('string', flat=True)
