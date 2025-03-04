from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser, Produto, Categoria, Fornecedor, Vendas, Cliente
from django.contrib.auth.models import Group, User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "name", "cpf", "groups", "profile_picture")

    def clean_groups(self):
        groups = self.cleaned_data.get("groups")
        if not groups:
            raise forms.ValidationError("Selecione um grupo.")
        return groups

    def save(self, commit=True):
        user = super().save(commit=False)
        if not user.profile_picture:
            user.profile_picture = 'profile_pictures/default.jpg'
        if commit:
            user.save()
            self.save_m2m()  # Salva os grupos
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email", "name", "cpf", "profile_picture", "groups")

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")
        user_id = self.instance.id  # Obtém o ID do cliente que está sendo editado

        if CustomUser.objects.filter(cpf=cpf).exclude(id=user_id).exists():
            raise forms.ValidationError(
                "Já existe um cliente com esse CPF cadastrado.")

        return cpf


class CustomVendedorChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email", "name", "cpf", "profile_picture")

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")
        user_id = self.instance.id  # Obtém o ID do cliente que está sendo editado

        if CustomUser.objects.filter(cpf=cpf).exclude(id=user_id).exists():
            raise forms.ValidationError(
                "Já existe um cliente com esse CPF cadastrado.")

        return cpf


class VendedorCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = CustomUser  # Alterei para CustomUser, caso seja esse o modelo correto
        fields = ["email", "name", "cpf", "profile_picture"]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("As senhas devem ser iguais.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")  # Use "password1" aqui
        if password:
            user.set_password(password)  # Define a senha corretamente
        if commit:
            user.save()
            vendedor_group, created = Group.objects.get_or_create(
                name="Vendedor")
            user.groups.add(vendedor_group)
        return user


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['name', 'price', 'quantity', 'description',
                  'product_picture', 'fornecedor', 'categoria']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona classes CSS para estilização (opcional)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class ProdutoChangeForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['name', 'price', 'quantity', 'description',
                  'product_picture', 'fornecedor', 'categoria']


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['name', 'description']


class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['name', 'company', 'email']


class VendasForm(forms.ModelForm):
    class Meta:
        model = Vendas
        fields = ['cliente', 'produto', 'quantity',
                  'payment_method', 'cpf_cliente', 'telefone_cliente']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'min': 1})
        self.fields['quantity'].required = True

    def clean_total(self):
        cleaned_data = self.cleaned_data
        quantity = cleaned_data.get("quantity")
        produto = cleaned_data.get("produto")
        if quantity and produto:
            total = produto.price * quantity
            return total
        return 0.0

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        produto = cleaned_data.get('produto')
        if produto and quantity is not None and produto.quantity is not None:
            if quantity > produto.quantity:
                self.add_error(
                    'quantity', f"A quantidade solicitada ({quantity}) é maior que a disponível em estoque ({produto.quantity}).")

        return cleaned_data


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["name", "email", "phone", "cpf", "neighborhood",
                  "city", "street", "number", "complemento", "uf"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")
        cliente_id = self.instance.id  # Obtém o ID do cliente que está sendo editado

        if Cliente.objects.filter(cpf=cpf).exclude(id=cliente_id).exists():
            raise forms.ValidationError(
                "Já existe um cliente com esse CPF cadastrado.")

        return cpf

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not phone.isdigit():
            raise forms.ValidationError(
                "O telefone deve conter apenas números.")
        return phone

    def clean_number(self):
        number = self.cleaned_data.get("number")
        if not number.isdigit():
            raise forms.ValidationError("O número deve conter apenas dígitos.")
        return number

    def clean_complemento(self):
        complemento = self.cleaned_data.get("complemento")
        if complemento and len(complemento) < 3:
            raise forms.ValidationError(
                "O complemento deve ter pelo menos 3 caracteres.")
        return complemento
