from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    objects = CustomUserManager()
    first_name = None
    last_name = None
    username = None
    USERNAME_FIELD = "email"
    email = models.EmailField("email", unique=True)
    name = models.CharField("name", max_length=150)
    cpf = models.CharField("CPF", max_length=14, unique=True,
                           validators=[MinLengthValidator(14)])
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', null=True, blank=True, default='profile_pictures/default.jpg')
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.profile_picture:
            self.profile_picture = 'profile_pictures/default.jpg'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    def is_vendedor(self):
        return self.groups.filter(name="Vendedor").exists()


class Fornecedor(models.Model):
    name = models.CharField("name", max_length=100)
    company = models.CharField("company name", max_length=100)
    email = models.EmailField("email", max_length=254, unique=True)

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"

    def __str__(self):
        return f"Venda {self.pk} - {self.cliente}"

    def __str__(self):
        return self.name


class Categoria(models.Model):
    name = models.CharField("name", max_length=40)
    description = models.TextField("description", max_length=115)

    def __str__(self):
        return self.name


class Produto(models.Model):
    name = models.CharField("name", max_length=150)
    price = models.DecimalField("price", max_digits=10, decimal_places=2, validators=[
                                MinValueValidator(1), MaxValueValidator(100000)])
    quantity = models.PositiveIntegerField(
        "quantity", validators=[MinValueValidator(1), MaxValueValidator(100000)])
    description = models.TextField("description", blank=True)
    product_picture = models.ImageField(
        upload_to='product_pictures/', null=True, blank=True, default='product_pictures/default.jpg'
    )
    fornecedor = models.ForeignKey(
        Fornecedor, verbose_name=_("Fornecedor"), on_delete=models.DO_NOTHING
    )
    categoria = models.ForeignKey(
        Categoria, verbose_name=_("Categoria"), on_delete=models.SET_DEFAULT, default=4
    )

    def __str__(self):
        return self.name


class Cliente(models.Model):
    STATES = [
        ("AC", "Acre"),
        ("AL", "Alagoas"),
        ("AP", "Amapá"),
        ("AM", "Amazonas"),
        ("BA", "Bahia"),
        ("CE", "Ceará"),
        ("DF", "Distrito Federal"),
        ("ES", "Espírito Santo"),
        ("GO", "Goiás"),
        ("MA", "Maranhão"),
        ("MT", "Mato Grosso"),
        ("MS", "Mato Grosso do Sul"),
        ("MG", "Minas Gerais"),
        ("PA", "Pará"),
        ("PB", "Paraíba"),
        ("PR", "Paraná"),
        ("PE", "Pernambuco"),
        ("PI", "Piauí"),
        ("RJ", "Rio de Janeiro"),
        ("RN", "Rio Grande do Norte"),
        ("RS", "Rio Grande do Sul"),
        ("RO", "Rondônia"),
        ("RR", "Roraima"),
        ("SC", "Santa Catarina"),
        ("SP", "São Paulo"),
        ("SE", "Sergipe"),
        ("TO", "Tocantins"),
    ]

    name = models.CharField("Nome", max_length=150)
    email = models.EmailField("E-mail", max_length=254, unique=True)
    phone = models.CharField(
        "Telefone",
        max_length=20,
        validators=[RegexValidator(
            regex=r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$',
            message="Formato inválido de telefone. Ex: (11) 91234-5678"
        )]
    )
    cpf = models.CharField(
        "cpf",
        max_length=11,  # Apenas números
        validators=[RegexValidator(
            regex=r'^\d{11}$', message="CPF deve conter apenas números.")],
        unique=True,  # Evita duplicados
    )
    neighborhood = models.CharField("Bairro", max_length=100)
    city = models.CharField("Cidade", max_length=100)
    street = models.CharField("Rua", max_length=100)

    number = models.CharField(
        "Número",
        max_length=10,
        validators=[RegexValidator(
            regex=r'^\d+$',
            message="O número deve conter apenas dígitos."
        )]
    )
    complemento = models.CharField(
        "Complemento", max_length=100, blank=True, null=True)
    uf = models.CharField("UF", max_length=2, choices=STATES)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.name} ({self.cpf})"


class Vendas(models.Model):
    PAYMENT_METHODS = [
        ("card", "Cartão"),
        ("pix", "Pix"),
        ("cash", "Dinheiro"),
    ]
    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "vendedor"), null=True, on_delete=models.SET_NULL)
    cliente = models.ForeignKey("Cliente", verbose_name=_(
        "cliente"), null=True, blank=True, on_delete=models.SET_NULL)
    produto = models.ForeignKey("Produto", verbose_name=_(
        "produto"), null=True, on_delete=models.SET_NULL)
    cpf_cliente = models.CharField(
        "CPF do Cliente",
        max_length=14,
        validators=[
            RegexValidator(
                regex=r"^\d{3}\.\d{3}\.\d{3}-\d{2}$",
                message="O CPF deve estar no formato XXX.XXX.XXX-XX.",
            )
        ],
    )
    telefone_cliente = models.CharField(
        "Telefone do Cliente",
        max_length=15,
        validators=[
            RegexValidator(
                regex=r"^\(\d{2}\) \d{5}-\d{4}$",
                message="O telefone deve estar no formato (XX) XXXXX-XXXX.",
            )
        ],
    )
    quantity = models.PositiveIntegerField(
        "quantity", validators=[MinValueValidator(1), MaxValueValidator(1000)])
    total = models.DecimalField("total", max_digits=10, decimal_places=2, validators=[
                                MinValueValidator(0)], null=True,)
    payment_method = models.CharField(
        "payment method", max_length=10, choices=PAYMENT_METHODS)
    created_at = models.DateTimeField("created at", auto_now_add=True)
    updated_at = models.DateTimeField("updated at", auto_now=True)

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"

    def __str__(self):
        return f"Venda {self.pk} - {self.cliente}"
