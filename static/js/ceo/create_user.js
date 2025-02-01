document.addEventListener('DOMContentLoaded', () => {
    const modal = document.querySelector('.modal'); // Seleciona o modal
    const openModalButtons = document.querySelectorAll('#open-modal'); // Seleciona todos os botões "Novo Usuário"
    const closeModalArea = document.querySelector('.modal'); // Seleciona o modal inteiro para fechar clicando fora
    const errorMessages = document.querySelectorAll('.error'); // Seleciona todas as mensagens de erro
    const form = document.getElementById('form'); // Seleciona o formulário
    const userIdField = document.getElementById('user_id'); // Campo oculto do ID do usuário

    // Função para aplicar a máscara de CPF
    function applyCpfMask(cpfField) {
        cpfField.addEventListener('input', function (event) {
            let value = event.target.value.replace(/\D/g, ''); // Remove tudo que não é dígito
            if (value.length > 11) {
                value = value.substring(0, 11); // Limita a 11 caracteres
            }

            // Aplica a máscara
            value = value.replace(/(\d{3})(\d)/, '$1.$2'); // Adiciona o primeiro ponto
            value = value.replace(/(\d{3})(\d)/, '$1.$2'); // Adiciona o segundo ponto
            value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2'); // Adiciona o traço

            event.target.value = value; // Atualiza o valor do campo
        });
    }

    // Aplica a máscara ao campo de CPF
    const cpfField = document.querySelector('input[name="cpf"]'); // Seleciona o campo de CPF pelo nome
    if (cpfField) {
        applyCpfMask(cpfField);
    }

    // Função para limpar os erros do formulário
    function clearErrors() {
        errorMessages.forEach(error => {
            error.innerHTML = ''; // Remove o conteúdo das divs de erro
        });
    }

    // Função para limpar os campos do formulário
    function clearFormFields() {
        form.reset(); // Reseta todos os campos do formulário
    }

    // Mostrar o modal ao clicar no botão "Novo Usuário" ou "Editar Usuário"
    openModalButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault(); // Impede o comportamento padrão do botão
            clearErrors(); // Limpa os erros antes de exibir o modal
            clearFormFields(); // Limpa os campos do formulário
            modal.classList.add('show'); // Exibe o modal
        });
    });

    // Fechar o modal ao clicar fora do conteúdo do formulário
    closeModalArea.addEventListener('click', (event) => {
        if (event.target === closeModalArea) {
            modal.classList.remove('show'); // Remove a classe para esconder o modal
        }
    });
});

// quase desistindo de formulario kkk