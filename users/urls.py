from django.views.generic import FormView
from django.urls import path
from . import views
from . import forms
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('registration/', views.UserRegistration.as_view(), name='registration' ),
    # -------- CEO ------------
    path('ceo/dashboard/', views.ceo_dashboard, name='ceo_dashboard'),
    path('ceo/historico_de_vendas/', views.VendasListView.as_view(), name="historico_de_vendas"),
    path('ceo/gerenciar_usuarios/', views.UsersListView.as_view(), name="gerenciar_usuarios"),
    path("delete_user/<int:pk>/", views.CeoDeletarUsuarioView.as_view(), name="deletar_usuario"),
    path('ceo/gerenciar_produtos/', views.ProdutoListView.as_view(), name="gerenciar_produtos"),
    path('delete_produto/<int:pk>/', views.ProdutoDeleteView.as_view(), name='deletar_produto'),
    path('ceo/gerenciar_categorias/', views.CategoriaListView.as_view(), name="gerenciar_categorias"),
    path('delete_categoria/<int:pk>/', views.CategoriaDeleteView.as_view(), name='deletar_categoria'),
    path('ceo/fornecedores/', views.FornecedorListView.as_view(), name="fornecedores"),
    path('delete_fornecedor/<int:pk>/', views.FornecedorDeleteView.as_view(), name='deletar_fornecedor'),
    # -------- Gerente ------------
    path('gerente/historico_de_vendas/', views.GerenteVendasListView.as_view(), name="gerente_dashboard"),
    path('gerente/gerenciar_vendedores/', views.GerenteVendedorListView.as_view(), name="gerente_gerenciar_usuarios"),
    path("delete_user/<int:pk>/", views.GerenteDeletarVendedorView.as_view(), name="deletar_vendedor"),
    path('gerente/gerenciar_produtos/', views.GerenteProdutoListView.as_view(), name="gerente_gerenciar_produtos"),
    path('gerente/gerenciar_categorias/', views.GerenteCategoriaListView.as_view(), name="gerente_gerenciar_categorias"),
    path('delete_categoria/<int:pk>/', views.GerenteCategoriaDeleteView.as_view(), name='gerente_deletar_categoria'),
    path('gerente/fornecedores/', views.GerenteFornecedorListView.as_view(), name="gerente_fornecedores"),
    path('delete_fornecedor/<int:pk>/', views.GerenteFornecedorDeleteView.as_view(), name='gerente_deletar_fornecedor'),
    # -------- Vendedor ------------
    path('vendedor/registrar_vendas/', views.RegistrarVendasListView.as_view(), name="registrar_vendas"),
    path('vendedor/gerenciar_produtos/', views.VendedorProdutoListView.as_view(), name="vendedor_consultar_produtos"),
    path('vendedor/gerenciar_clientes/', views.VendedorClienteListView.as_view(), name="vendedor_clientes"),
    path("clientes/deletar/<int:pk>/", views.VendedorClienteDeleteView.as_view(), name="vendedor_cliente_deletar"),
    path('vendedor/minhas_vendas/', views.VendedorVendasListView.as_view(), name="vendedor_minhas_vendas"),
    
    # path('get-product/<int:product_id>/', views.get_product, name='get_product'),
    # path('update-product/', views.update_product, name='update_product'),

    


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
