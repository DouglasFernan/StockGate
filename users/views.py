from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, ListView
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from . import forms
from . import models


# Create your views here.
# ceo = CustomUser.objects.create(email="douglasgenetic@gmail.com",
#                                 name="Douglas Fernandes", cpf="13359863402")
# ceo.set_password("Pass@2024")
# ceo.groups.add(Group.objects.get(name="CEO"))
# ceo.save()


def get_dashboard_url(user):
    group_dashboard_map = {
        'CEO': 'ceo_dashboard',
        'Gerente': 'gerente_dashboard',
        'Vendedor': 'vendedor_dashboard',
    }
    user_group = user.groups.first().name
    return group_dashboard_map[user_group]
    # for group, dashboard_url in group_dashboard_map.items():
    #     if user.groups.filter(name=group).exists():
    #         return dashboard_url
    # return ''


def login_view(request):
    if request.method == 'POST':
        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # print(user, username, password,)
        # breakpoint()
        if user is not None:
            login(request, user)
            return redirect(get_dashboard_url(user))
        else:
            return render(request, 'users/login.html', {'error': 'Invalid username or password'})
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect("login")


class UserRegistration(FormView):
    form_class = forms.CustomUserCreationForm
    template_name = "users/registration.html"

# ---------  CEO   ------------


@login_required
def ceo_dashboard(request):
    return render(request, 'users/ceo/dashboard.html')


class VendasListView(ListView):
    model = models.Vendas
    template_name = "users/ceo/historico_de_vendas.html"

    def get_queryset(self):
        order = self.request.GET.get(
            'order', '-created_at')
        queryset = models.Vendas.objects.all()

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(
                created_at__range=[start_date, end_date])

        return queryset.order_by(order)


class UsersListView(ListView):
    model = models.CustomUser
    template_name = 'users/ceo/customuser_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search)
            )
        return queryset


class CreateUserView(CreateView):
    model = models.CustomUser
    form_class = forms.CustomUserCreationForm
    template_name = 'users/ceo/create_user.html'
    success_url = reverse_lazy('gerenciar_usuarios')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get('password1'))
        user.save()

        vendedor_group, created = Group.objects.get_or_create(name="Vendedor")
        user.groups.add(vendedor_group)

        return super().form_valid(form)


class CreateProdutoView(CreateView):
    model = models.Produto
    form_class = forms.ProdutoForm
    template_name = 'users/ceo/create_produto.html'
    # Após a criação, redireciona para a lista de produtos
    success_url = reverse_lazy('gerenciar_produtos')


class CategoriaListView(ListView):
    model = models.Categoria
    template_name = 'users/ceo/categoria_list.html'


class FornecedorListView(ListView):
    model = models.Fornecedor
    template_name = 'users/ceo/fornecedor_list.html'


class ProdutoListView(ListView):
    model = models.Produto
    template_name = "users/ceo/produto_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search))
        return queryset


# ---------  Gerente   ------------


class GerenteVendasListView(ListView):
    model = models.Vendas
    template_name = "users/gerente/historico_de_vendas.html"

    def get_queryset(self):
        order = self.request.GET.get(
            'order', '-created_at')
        queryset = models.Vendas.objects.all()

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(
                created_at__range=[start_date, end_date])

        return queryset.order_by(order)


class CreateUserVendedorView(CreateView):
    model = models.CustomUser
    form_class = forms.VendedorCreationForm
    template_name = 'users/gerente/create_user_vendedor.html'
    success_url = reverse_lazy('gerente_gerenciar_usuarios')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()

        vendedor_group, created = Group.objects.get_or_create(name="Vendedor")
        user.groups.add(vendedor_group)

        return super().form_valid(form)


class GerenteUsersListView(ListView):
    model = models.CustomUser
    template_name = 'users/gerente/customuser_list.html'

    def get_queryset(self):
        return models.CustomUser.objects.filter(groups__name="Vendedor")


class GerenteCategoriaListView(ListView):
    model = models.Categoria
    template_name = 'users/gerente/categoria_list.html'


class GerenteFornecedorListView(ListView):
    model = models.Fornecedor
    template_name = 'users/gerente/fornecedor_list.html'


class GerenteProdutoListView(ListView):
    model = models.Produto
    template_name = "users/gerente/produto_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search))
        return queryset


class CreateProdutoGerenteView(CreateView):
    model = models.Produto
    form_class = forms.ProdutoForm
    template_name = 'users/gerente/create_produto.html'
    # Após a criação, redireciona para a lista de produtos
    success_url = reverse_lazy('gerente_gerenciar_produtos')


# ---------  Vendedor   ------------

class VendedorProdutoListView(ListView):
    model = models.Produto
    template_name = "users/vendedor/produto_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search))
        return queryset


class VendedorClienteListView(ListView):
    model = models.Cliente
    template_name = "users/vendedor/cliente_list.html"


class VendedorVendasListView(ListView):
    model = models.Vendas
    template_name = "users/vendedor/historico_de_vendas.html"

    def get_queryset(self):
        order = self.request.GET.get('order', '-created_at')
        queryset = models.Vendas.objects.filter(vendedor=self.request.user)

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(
                created_at__range=[start_date, end_date])

        return queryset.order_by(order)


@login_required
def vendedor_dashboard(request):
    return render(request, 'users/vendedor/registrar_vendas.html')


@login_required
def vendedor_registrar_vendas(request):
    return render(request, 'users/vendedor/registrar_vendas.html')
