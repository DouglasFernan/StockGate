from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, ListView
from django.db.models import Q
from django.urls import reverse_lazy, reverse
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Exibe o formulário de criação
        context["form"] = forms.CustomUserCreationForm()
        context["object_list"] = self.get_queryset()  # Lista de usuários
        context["modal_open"] = False  # Inicialmente o modal está fechado
        return context

    def post(self, request, *args, **kwargs):
        form = forms.CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redireciona após salvar
            return redirect(reverse('gerenciar_usuarios'))
        else:
            return render(request, 'users/ceo/customuser_list.html', {
                'form': form,
                'modal_open': True,  # Controla a abertura do modal
                'object_list': models.CustomUser.objects.all(),  # Lista de usuários
            })


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Exibe o formulário de criação
        context["form"] = forms.ProdutoForm()
        context["object_list"] = self.get_queryset()  # Lista de usuários
        context["modal_open"] = False  # Inicialmente o modal está fechado
        return context

    def post(self, request, *args, **kwargs):
        form = forms.ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redireciona após salvar
            return redirect(reverse('gerenciar_produtos'))
        else:
            return render(request, 'users/ceo/produto_list.html', {
                'form': form,
                'modal_open': True,  # Controla a abertura do modal
                'object_list': models.Produto.objects.all(),  # Lista de usuários
            })


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


class vendedor_dashboard(LoginRequiredMixin, ListView):
    model = models.Vendas
    template_name = 'users/vendedor/registrar_vendas.html'

    def get_queryset(self):
        order = self.request.GET.get('order', '-created_at')
        queryset = models.Vendas.objects.filter(vendedor=self.request.user)

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(
                created_at__range=[start_date, end_date])

        return queryset.order_by(order)


# def get_product(request, product_id):
#     try:
#         produto = models.Produto.objects.get(id=product_id)
#         data = {
#             'name': produto.name,
#             'price': produto.price,
#             'quantity': produto.quantity,
#             'fornecedor': produto.fornecedor.id,
#             'categoria': produto.categoria.id,
#             'description': produto.description,
#             'product_picture': produto.product_picture.url if produto.product_picture else None,
#         }
#         return JsonResponse(data)
#     except models.Produto.DoesNotExist:
#         return JsonResponse({'error': 'Produto não encontrado'}, status=404)


# def update_product(request):
#     if request.method == "POST":
#         product_id = request.POST.get('product_id')
#         product = get_object_or_404(models.Produto, id=product_id)
#         product.name = request.POST.get('name')
#         product.price = request.POST.get('price')
#         product.quantity = request.POST.get('quantity')
#         product.fornecedor_id = request.POST.get('fornecedor')
#         product.categoria_id = request.POST.get('categoria')
#         product.description = request.POST.get('description')

#         if request.FILES.get('product_picture'):
#             product.product_picture = request.FILES.get('product_picture')

#         product.save()
#         messages.success(request, "Produto atualizado com sucesso!")
#         # Substitua pelo nome correto da view de listagem, se diferente
#         return redirect('gerenciar_produtos')
#     return redirect('gerenciar_produtos')
