from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Fornecedor, Categoria, Produto, Cliente, Vendas

# list_display: Define os campos que serão exibidos na lista de objetos.
# search_fields: Adiciona uma barra de pesquisa para buscar pelos campos especificados.
# list_filter: Adiciona filtros laterais com base em determinados campos.
# readonly_fields: Define campos como somente leitura no admin (útil para timestamps como created_at e updated_at).
# @admin.register: Registra o modelo no admin, associando-o à classe personalizada.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "name", "cpf", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password", "name", "cpf", "profile_picture")}),
        ("Permissions", {"fields": ("is_staff",
         "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "name", "cpf", "profile_picture", "is_staff", "is_active", "groups"),
            },
        ),
    )
    search_fields = ("email", "name", "cpf")
    ordering = ("email",)


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "email", "description")
    search_fields = ("name", "company", "email")
    list_filter = ("company",)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "quantity", "fornecedor", "categoria")
    search_fields = ("name", "fornecedor__name", "categoria__name")
    list_filter = ("categoria", "fornecedor")


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "cpf", "city", "uf")
    search_fields = ("name", "email", "cpf", "city")
    list_filter = ("uf",)
    readonly_fields = ("created_at", "updated_at")


User = get_user_model()

# Formulário personalizado para filtrar os vendedores


class VendasForm(forms.ModelForm):
    class Meta:
        model = Vendas
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra apenas os usuários do grupo "vendedores"
        self.fields["vendedor"].queryset = User.objects.filter(
            groups__name="Vendedor")


# Admin personalizado para Vendas
@admin.register(Vendas)
class VendasAdmin(admin.ModelAdmin):
    form = VendasForm
    list_display = ("vendedor", "cliente", "produto", "quantity",
                    "payment_method", "total", "created_at")
    search_fields = ("cliente__name", "produto__name", "vendedor__email")
    list_filter = ("payment_method", "created_at")
    readonly_fields = ("created_at", "updated_at")


admin.site.register(CustomUser, CustomUserAdmin)
