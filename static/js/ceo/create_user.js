document.addEventListener('DOMContentLoaded', () => {
    const modal = document.querySelector('.modal'); 
    const openModalButtons = document.querySelectorAll('#open-modal');
    const closeModalArea = document.querySelector('.modal');
    const errorMessages = document.querySelectorAll('.error'); 
    const form = document.getElementById('form'); 
    const userIdField = document.getElementById('user_id'); 
    const deleteButtons = document.querySelectorAll('.delete-user'); 

    // Função para aplicar a máscara de CPF
    function applyCpfMask(cpfField) {
        cpfField.addEventListener('input', function (event) {
            let value = event.target.value.replace(/\D/g, ''); 
            if (value.length > 11) {
                value = value.substring(0, 11);
            }

            // Aplica a máscara
            value = value.replace(/(\d{3})(\d)/, '$1.$2'); // Adiciona o primeiro ponto
            value = value.replace(/(\d{3})(\d)/, '$1.$2'); // Adiciona o segundo ponto
            value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2'); // Adiciona o traço

            event.target.value = value; 
        });
    }

    // Aplica a máscara ao campo de CPF
    const cpfField = document.querySelector('input[name="cpf"]'); 
    if (cpfField) {
        applyCpfMask(cpfField);
    }

    function clearErrors() {
        errorMessages.forEach(error => {
            error.innerHTML = ''; 
        });
    }

    function clearFormFields() {
        form.reset(); 
    }

    // Abre o modal de criação
    openModalButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault(); 
            clearErrors(); 
            clearFormFields(); 
            modal.classList.add('show'); 
        });
    });

    closeModalArea.addEventListener('click', (event) => {
        if (event.target === closeModalArea) {
            modal.classList.remove('show'); // Remove a classe para esconder o modal
        }
    });

    // add lógica de exclusão
    deleteButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault(); 
            const userId = button.dataset.userId; // pega o ID 
            const confirmation = confirm("Tem certeza que deseja deletar este usuário?"); 

            if (confirmation) {
                //  requisição para deletar o usuário
                fetch(`/delete_user/${userId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCsrfToken(), // Obtém o token CSRF dinamicamente
                        'Content-Type': 'application/json',
                    },
                }).then(response => {
                    if (response.ok) {
                        alert("Usuário deletado com sucesso!");
                        location.reload(); 
                    } else {
                        alert("Erro ao deletar o usuário.");
                    }
                });
            }
        });
    });

    // Função para obter o token CSRF
    function getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
});
