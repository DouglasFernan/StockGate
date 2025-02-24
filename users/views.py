from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import FormView, ListView
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, UpdateView
from . import forms
from . import models
import re


def get_dashboard_url(user):
    group_dashboard_map = {
        'CEO': 'ceo_dashboard',
        'Gerente': 'gerente_dashboard',
        'Vendedor': 'registrar_vendas',
    }
    user_group = user.groups.first().name
    return group_dashboard_map[user_group]
    # for group, dashboard_url in group_dashboard_map.items():
    #     if user.groups.filter(name=group).exists():
    #         return dashboard_url
    # return ''


def login_view(request):
    email = ""
    email_error = None
    password_error = None

    if request.method == 'POST':
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        # Verifica se os campos estão vazios
        if not email and not password:
            email_error = "O e-mail é obrigatório."
            password_error = "A senha é obrigatória."
        elif not email:
            email_error = "O e-mail é obrigatório."
        elif not password:
            password_error = "A senha é obrigatória."
        else:
            # Verifica se o e-mail tem um formato válido
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                email_error = "E-mail inválido."
            else:
                try:
                    user = models.CustomUser.objects.get(
                        email=email)  # Verifica se o e-mail existe

                    # Se o e-mail existir, agora verificamos a senha
                    user = authenticate(
                        request, email=email, password=password)

                    if user is not None:
                        login(request, user)
                        return redirect(get_dashboard_url(user))
                    else:
                        password_error = "Senha incorreta."  # Apenas erro de senha

                except models.CustomUser.DoesNotExist:
                    email_error = "E-mail não cadastrado."

    return render(request, 'users/login.html', {
        'email_error': email_error,
        'password_error': password_error,
        'email': email
    })


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


class CeoDeletarUsuarioView(View):
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        CustomUser = get_user_model()
        usuario = get_object_or_404(CustomUser, id=user_id)

        if usuario.is_superuser:
            messages.error(
                request, "Erro: Não é permitido excluir superusuários.")
            return redirect("gerenciar_usuarios")

        usuario.delete()
        messages.success(request, "Usuário deletado com sucesso!")

        return redirect("gerenciar_usuarios")


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
        context["form"] = forms.CustomUserCreationForm()
        context["object_list"] = self.get_queryset()
        context["modal_open"] = False
        return context

    def post(self, request, *args, **kwargs):
        form = forms.CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(self.request, 'Usuário criado com sucesso!')
            return redirect(reverse('gerenciar_usuarios'))
        else:
            return render(request, 'users/ceo/customuser_list.html', {
                'form': form,
                'modal_open': True,
                'object_list': models.CustomUser.objects.all(),
            })


class UserUpdateView(UpdateView):
    model = models.CustomUser
    form_class = forms.CustomUserChangeForm
    template_name = "users/ceo/user_update.html"

    def get_success_url(self):
        messages.success(self.request, 'Usuário modificado com sucesso!')
        return reverse_lazy('gerenciar_usuarios')


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
        context["form"] = forms.ProdutoForm()
        context["object_list"] = self.get_queryset()
        context["modal_open"] = False
        return context

    def post(self, request, *args, **kwargs):
        form = forms.ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(self.request, 'Produto criado com sucesso!')
            return redirect(reverse('gerenciar_produtos'))
        else:
            return render(request, 'users/ceo/produto_list.html', {
                'form': form,
                'modal_open': True,
                'object_list': models.Produto.objects.all(),
            })


class ProdutoUpdateView(UpdateView):
    model = models.Produto
    form_class = forms.ProdutoChangeForm
    template_name = "users/ceo/update_produto.html"

    def get_success_url(self):
        messages.success(self.request, 'Produto modificado com sucesso!')
        return reverse_lazy('gerenciar_produtos')


class ProdutoDeleteView(View):
    def post(self, request, *args, **kwargs):
        product_id = kwargs.get("pk")
        product = get_object_or_404(models.Produto, id=product_id)

        try:
            product.delete()
            messages.success(self.request, "Produto deletado com sucesso!")
        except Exception as e:
            messages.error(self.request, f"Erro ao deletar produto: {str(e)}")

        return redirect("gerenciar_produtos")


class CategoriaListView(ListView):
    model = models.Categoria
    template_name = 'users/ceo/categoria_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = forms.CategoriaForm()
        context["object_list"] = self.get_queryset()
        context["modal_open"] = False
        return context

    def post(self, request, *args, **kwargs):
        form = forms.CategoriaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(self.request, 'Categoria criada com sucesso!')
            return redirect(reverse('gerenciar_categorias'))
        else:
            return render(request, 'users/ceo/categoria_list.html', {
                'form': form,
                'modal_open': True,
                'object_list': models.Categoria.objects.all(),
            })


class CeoCategoriaUpdateView(UpdateView):
    model = models.Categoria
    form_class = forms.CategoriaForm
    template_name = "users/ceo/update_categoria.html"

    def get_success_url(self):
        messages.success(self.request, 'Categoria modificada com sucesso!')
        return reverse_lazy('gerenciar_categorias')


class CategoriaDeleteView(View):
    def post(self, request, *args, **kwargs):
        categoria_id = kwargs.get("pk")
        categoria = get_object_or_404(models.Categoria, id=categoria_id)

        try:
            categoria.delete()
            messages.success(self.request, "Categoria deletada com sucesso!")
        except Exception as e:
            messages.error(
                self.request, f"Erro ao deletar categoria: {str(e)}")

        return redirect("gerenciar_categorias")


class FornecedorListView(ListView):
    model = models.Fornecedor
    template_name = 'users/ceo/fornecedor_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = forms.FornecedorForm()
        context["object_list"] = self.get_queryset()
        context["modal_open"] = False
        return context

    def post(self, request, *args, **kwargs):
        form = forms.FornecedorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(self.request, 'Fornecedor criado com sucesso!')
            return redirect(reverse('fornecedores'))
        else:
            return render(request, 'users/ceo/fornecedor_list.html', {
                'form': form,
                'modal_open': True,  # Controla a abertura do modal
                'object_list': models.Fornecedor.objects.all(),  # Lista de usuários
            })


class FornecedorUpdateView(UpdateView):
    model = models.Fornecedor
    form_class = forms.FornecedorForm
    template_name = "users/ceo/update_fornecedor.html"

    def get_success_url(self):
        messages.success(self.request, 'Fornecedor modificado com sucesso!')
        return reverse_lazy('fornecedores')


class FornecedorDeleteView(View):
    def post(self, request, *args, **kwargs):
        fornecedor_id = kwargs.get("pk")
        fornecedor = get_object_or_404(models.Fornecedor, id=fornecedor_id)

        try:
            fornecedor.delete()
            messages.success(request, "Fornecedor deletado com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao deletar fornecedor: {str(e)}")

        return redirect("fornecedores")


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


class GerenteVendedorListView(ListView):
    model = models.CustomUser
    template_name = 'users/gerente/customuser_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        vendedor_group = Group.objects.get(name="Vendedor")
        queryset = queryset.filter(groups=vendedor_group)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = forms.VendedorCreationForm()
        context["object_list"] = self.get_queryset()
        context["modal_open"] = False
        return context

    def post(self, request, *args, **kwargs):
        form = forms.VendedorCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(self.request, 'Vendedor criado com sucesso!')
            return redirect(reverse('gerente_gerenciar_usuarios'))
        else:
            return render(request, 'users/gerente/customuser_list.html', {
                'form': form,
                'modal_open': True,
                'object_list': self.get_queryset(),
            })


class GerenteUserUpdateView(UpdateView):
    model = models.CustomUser
    form_class = forms.CustomVendedorChangeForm
    template_name = "users/gerente/user_update.html"

    def get_success_url(self):
        messages.success(self.request, 'Vendedor modificado com sucesso!')
        return reverse_lazy('gerente_gerenciar_usuarios')


class GerenteDeletarVendedorView(View):
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        CustomUser = get_user_model()
        vendedor = get_object_or_404(CustomUser, id=user_id)

        vendedor_group = Group.objects.get(name="Vendedor")
        if vendedor_group in vendedor.groups.all():
            vendedor.delete()
            messages.success(request, "Vendedor deletado com sucesso!")
        else:
            messages.error(
                request, "Erro: O usuário não pertence ao grupo Vendedor.")

        return redirect("gerente_gerenciar_usuarios")


class GerenteCategoriaListView(ListView):
    model = models.Categoria
    template_name = 'users/gerente/categoria_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = forms.CategoriaForm()
        context["object_list"] = self.get_queryset()
        context["modal_open"] = False
        return context

    def post(self, request, *args, **kwargs):
        form = forms.CategoriaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(self.request, 'Categoria criada com sucesso!')
            return redirect(reverse('gerente_gerenciar_categorias'))
        else:
            return render(request, 'users/gerente/categoria_list.html', {
                'form': form,
                'modal_open': True,
                'object_list': models.Categoria.objects.all(),
            })


class GerenteCategoriaUpdateView(UpdateView):
    model = models.Categoria
    form_class = forms.CategoriaForm
    template_name = "users/gerente/update_categoria.html"

    def get_success_url(self):
        messages.success(self.request, 'Categoria modificada com sucesso!')
        return reverse_lazy('gerente_gerenciar_categorias')


class GerenteCategoriaDeleteView(View):
    def post(self, request, *args, **kwargs):
        categoria_id = kwargs.get("pk")
        categoria = get_object_or_404(models.Categoria, id=categoria_id)

        try:
            categoria.delete()
            messages.success(request, "Categoria deletada com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao deletar categoria: {str(e)}")

        return redirect("gerente_gerenciar_categorias")


class GerenteFornecedorListView(ListView):
    model = models.Fornecedor
    template_name = 'users/gerente/fornecedor_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = forms.FornecedorForm()
        context["object_list"] = self.get_queryset()
        context["modal_open"] = False
        return context

    def post(self, request, *args, **kwargs):
        form = forms.FornecedorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(self.request, 'Fornecedor criado com sucesso!')
            return redirect(reverse('gerente_fornecedores'))
        else:
            return render(request, 'users/gerente/fornecedor_list.html', {
                'form': form,
                'modal_open': True,  # Controla a abertura do modal
                'object_list': models.Fornecedor.objects.all(),  # Lista de usuários
            })


class GerenteFornecedorUpdateView(UpdateView):
    model = models.Fornecedor
    form_class = forms.FornecedorForm
    template_name = "users/gerente/update_fornecedor.html"

    def get_success_url(self):
        messages.success(self.request, 'Fornecedor modificado com sucesso!')
        return reverse_lazy('gerente_fornecedores')


class GerenteFornecedorDeleteView(View):
    def post(self, request, *args, **kwargs):
        fornecedor_id = kwargs.get("pk")
        fornecedor = get_object_or_404(models.Fornecedor, id=fornecedor_id)

        try:
            fornecedor.delete()
            messages.success(request, "Fornecedor deletado com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao deletar fornecedor: {str(e)}")

        return redirect("gerente_fornecedores")


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = forms.ProdutoForm()
        context["object_list"] = self.get_queryset()
        context["modal_open"] = False
        return context

    def post(self, request, *args, **kwargs):
        form = forms.ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(self.request, 'Produto criado com sucesso!')
            return redirect(reverse('gerente_gerenciar_produtos'))
        else:
            return render(request, 'users/gerente/produto_list.html', {
                'form': form,
                'modal_open': True,
                'object_list': models.Produto.objects.all(),
            })


class GerenteProdutoUpdateView(UpdateView):
    model = models.Produto
    form_class = forms.ProdutoForm
    template_name = "users/gerente/update_produto.html"

    def get_success_url(self):
        messages.success(self.request, 'Produto modificado com sucesso!')
        return reverse_lazy('gerente_gerenciar_produtos')

# ---------  Vendedor   ------------


class RegistrarVendasListView(View):
    template_name = 'users/vendedor/registrar_vendas.html'

    def get(self, request, *args, **kwargs):
        form = forms.VendasForm()
        vendas_do_vendedor = models.Vendas.objects.filter(
            vendedor=request.user).order_by('-id')
        context = {'form': form, 'vendas_do_vendedor': vendas_do_vendedor}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = forms.VendasForm(request.POST, request.FILES)

        if form.is_valid():
            venda = form.save(commit=False)
            produto = venda.produto
            quantidade = venda.quantity

            if produto and quantidade:
                venda.total = produto.price * quantidade
                if produto.quantity >= quantidade:
                    produto.quantity -= quantidade
                    produto.save()
                else:
                    form.add_error(
                        'quantity', 'Estoque insuficiente para essa venda.')
                    vendas_do_vendedor = models.Vendas.objects.filter(
                        vendedor=request.user).order_by('-id')
                    return render(request, self.template_name, {'form': form, 'vendas_do_vendedor': vendas_do_vendedor})
            else:
                venda.total = 0

            venda.vendedor = request.user
            venda.save()
            messages.success(self.request, 'Venda registrada com sucesso!')
            return redirect('registrar_vendas')

        else:
            vendas_do_vendedor = models.Vendas.objects.filter(
                vendedor=request.user
            ).order_by('-id')

            return render(request, self.template_name, {
                'form': form,
                'vendas_do_vendedor': vendas_do_vendedor
            })


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

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(email__icontains=search)
            )

        # Adicionar última compra de cada cliente
        for cliente in queryset:
            cliente.ultima_compra = models.Vendas.objects.filter(
                cliente=cliente).order_by('-created_at').first()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = forms.ClienteForm()
        context["object_list"] = self.get_queryset()
        context["modal_open"] = False
        return context

    def post(self, request, *args, **kwargs):
        form = forms.ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(self.request, 'Cliente criado com sucesso!')
            return redirect(reverse('vendedor_clientes'))
        else:
            return render(request, 'users/vendedor/cliente_list.html', {
                'form': form,
                'modal_open': True,
                'object_list': self.get_queryset(),
            })


class ClienteUpdateView(UpdateView):
    model = models.Cliente
    form_class = forms.ClienteForm
    template_name = "users/vendedor/cliente_update.html"

    def get_success_url(self):
        messages.success(self.request, 'Cliente modificado com sucesso!')
        return reverse_lazy('vendedor_clientes')


class VendedorClienteDeleteView(View):
    def post(self, request, *args, **kwargs):
        cliente_id = kwargs.get("pk")
        cliente = get_object_or_404(models.Cliente, id=cliente_id)

        try:
            cliente.delete()
            messages.success(request, "Cliente deletado com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao deletar cliente: {str(e)}")

        return redirect("vendedor_clientes")


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
