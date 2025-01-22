document.addEventListener('DOMContentLoaded', () => {
    const modal = document.querySelector('.modal-sales'); // Seleciona o modal
    const openModalButtons = document.querySelectorAll('#open-modal'); // Seleciona todos os botões "Editar"
    const closeModalArea = document.querySelector('.modal-sales'); // Seleciona o modal inteiro para fechar clicando fora

    // Mostrar o modal ao clicar no botão "Editar"
    openModalButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault(); // Impede o comportamento padrão do botão
            modal.classList.add('show'); // Adiciona a classe para exibir o modal
        });
    });

    // Fechar o modal ao clicar fora do conteúdo do formulário
    closeModalArea.addEventListener('click', (event) => {
        if (event.target === closeModalArea) {
            modal.classList.remove('show'); // Remove a classe para esconder o modal
        }
    });
});
