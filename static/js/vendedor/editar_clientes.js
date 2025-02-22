document.addEventListener('DOMContentLoaded', () => {
    const modal = document.querySelector('.modal');
    const openModalButtons = document.querySelectorAll('#open-modal');
    const editButtons = document.querySelectorAll('.edit-cliente');
    const closeModalButton = document.querySelector('.close-modal');
    const errorMessages = document.querySelectorAll('.error');
    const form = document.getElementById('form');
    const deleteButtons = document.querySelectorAll('.delete-cliente');

    // Função para limpar mensagens de erro
    function clearErrors() {
        document.querySelectorAll('.error').forEach(error => {
            error.innerHTML = '';
        });
    }

    function clearFormFields() {
        form.reset();
    }

    // Obtém o CSRF Token
    function getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    // Abre o modal de criação de cliente
    openModalButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            clearErrors();
            clearFormFields();
            form.action = "/vendedor/gerenciar_clientes/";
            document.querySelector(".btn-new-user-2").textContent = "Criar Cliente";
            modal.classList.add('show');

            // Remove o evento de submit anterior para evitar conflitos
            form.onsubmit = async (e) => {
                e.preventDefault();
                const formData = new FormData(form);

                const response = await fetch("/vendedor/gerenciar_clientes/", {
                    method: "POST",
                    body: formData,
                    headers: { "X-CSRFToken": getCsrfToken() }
                });

                const data = await response.json();

                if (response.ok) {
                    alert(data.message);
                    modal.classList.remove('show');
                    atualizarListaClientes();
                } else {
                    mostrarErros(data.errors);
                }
            };
        });
    });

    // Abre o modal de edição de cliente
    editButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            clearErrors();
            const clienteId = button.dataset.clienteId;

            // Preenche o formulário com os dados do cliente
            form.name.value = button.dataset.nome || "";
            form.email.value = button.dataset.email || "";
            form.phone.value = button.dataset.phone || "";
            form.cpf.value = button.dataset.cpf || "";
            form.uf.value = button.dataset.uf || "";
            form.city.value = button.dataset.city || "";
            form.neighborhood.value = button.dataset.neighborhood || "";
            form.street.value = button.dataset.street || "";
            form.number.value = button.dataset.number || "";
            form.complemento.value = button.dataset.complemento || "";

            document.querySelector(".btn-new-user-2").textContent = "Salvar Alterações";

            modal.classList.add('show');

            // Remove o evento de submit anterior e adiciona um novo para edição
            form.onsubmit = async (e) => {
                e.preventDefault();

                const formData = new FormData(form);
                const response = await fetch(`/editar-cliente/${clienteId}/`, {
                    method: "POST",
                    body: formData,
                    headers: { "X-CSRFToken": getCsrfToken() }
                });

                const data = await response.json();

                if (response.ok) {
                    alert(data.message);
                    modal.classList.remove('show');
                    atualizarListaClientes();
                } else {
                    mostrarErros(data.errors);
                }
            };
        });
    });

    // Fecha o modal ao clicar no botão de fechar
    closeModalButton.addEventListener('click', () => {
        modal.classList.remove('show');
    });

    // Fecha o modal ao clicar fora dele
    modal.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.classList.remove('show');
        }
    });

    // Exclui um cliente via AJAX
    deleteButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const clienteId = button.dataset.clienteId;
            const confirmation = confirm("Tem certeza que deseja deletar este cliente?");

            if (confirmation) {
                fetch(`/clientes/deletar/${clienteId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCsrfToken(),
                        'Content-Type': 'application/json',
                    },
                }).then(response => {
                    if (response.ok) {
                        alert("Cliente deletado com sucesso!");
                        atualizarListaClientes();
                    } else {
                        alert("Erro ao deletar o cliente.");
                    }
                });
            }
        });
    });

    // Atualiza a lista de clientes após criação/edição/exclusão sem recarregar a página
    function atualizarListaClientes() {
        fetch("/vendedor/gerenciar_clientes/")
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const novaTabela = doc.querySelector(".tabela-clientes");
                document.querySelector(".tabela-clientes").innerHTML = novaTabela.innerHTML;
            });
    }

    // Exibe mensagens de erro no formulário
    function mostrarErros(errors) {
        for (const field in errors) {
            const errorElement = document.querySelector(`.error-${field}`);
            if (errorElement) {
                errorElement.innerHTML = errors[field].join("<br>");
            }
        }
    }
});
