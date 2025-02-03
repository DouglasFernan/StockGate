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
    description = models.TextField("description", blank=True)

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"

    def __str__(self):
        return f"Venda {self.pk} - {self.cliente}"

    def __str__(self):
        return self.name


class Categoria(models.Model):
    name = models.CharField("name", max_length=100)
    description = models.TextField("description", blank=True)

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
        Categoria, verbose_name=_("Categoria"), on_delete=models.DO_NOTHING
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
    name = models.CharField("name", max_length=150)
    email = models.EmailField("email", max_length=254, unique=True)
    phone = models.CharField("phone", max_length=20)
    cpf = models.CharField(
        "cpf",
        max_length=15,
        validators=[RegexValidator(
            regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', message="Invalid CPF format.")],
    )
    neighborhood = models.CharField("neighborhood", max_length=100)
    city = models.CharField("city", max_length=100)
    street = models.CharField("street", max_length=100)
    number = models.CharField("house number", max_length=10)
    cep = models.CharField(
        "cep",
        max_length=9,
        validators=[RegexValidator(
            regex=r'^\d{5}-\d{3}$', message="Invalid CEP format.")],
    )
    uf = models.CharField("uf", max_length=2, choices=STATES)
    created_at = models.DateTimeField("created at", auto_now_add=True)
    updated_at = models.DateTimeField("updated at", auto_now=True)

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
    vendedor = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("vendedor"), null=True, on_delete=models.SET_NULL
    )
    cliente = models.ForeignKey(
        Cliente, verbose_name=_("cliente"), null=True, blank=True, on_delete=models.SET_NULL
    )
    produto = models.ForeignKey(
        Produto, verbose_name=_("produto"), null=True, on_delete=models.SET_NULL
    )
    quantity = models.PositiveIntegerField("quantity")
    created_at = models.DateTimeField("created at", auto_now_add=True)
    updated_at = models.DateTimeField("updated at", auto_now=True)
    payment_method = models.CharField(
        "payment method", max_length=10, choices=PAYMENT_METHODS)
    total = models.DecimalField("total", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"
