document.addEventListener('DOMContentLoaded', () => {
    const modal = document.querySelector('.modal'); 
    const openModalButtons = document.querySelectorAll('#open-modal');
    const closeModalArea = document.querySelector('.modal'); 

    openModalButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault(); 
            modal.classList.add('show'); 
        });
    });

    closeModalArea.addEventListener('click', (event) => {
        if (event.target === closeModalArea) {
            modal.classList.remove('show'); 
        }
    });
});
