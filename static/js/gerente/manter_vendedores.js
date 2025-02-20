document.addEventListener("DOMContentLoaded", () => {
    const modal = document.querySelector(".modal");
    const openModalButtons = document.querySelectorAll("#open-modal");
    const closeModalArea = document.querySelector(".modal");
    const errorMessages = document.querySelectorAll(".error");
    const form = document.getElementById("form");
    const cpfField = document.querySelector('input[name="cpf"]');
    const deleteButtons = document.querySelectorAll(".btn-delete");

    // Aplica máscara ao CPF
    function applyCpfMask(cpfField) {
        cpfField.addEventListener("input", function (event) {
            let value = event.target.value.replace(/\D/g, "");
            if (value.length > 11) {
                value = value.substring(0, 11);
            }

            value = value.replace(/(\d{3})(\d)/, "$1.$2");
            value = value.replace(/(\d{3})(\d)/, "$1.$2");
            value = value.replace(/(\d{3})(\d{1,2})$/, "$1-$2");

            event.target.value = value;
        });
    }

    if (cpfField) {
        applyCpfMask(cpfField);
    }

    function clearErrors() {
        errorMessages.forEach(error => {
            error.innerHTML = "";
        });
    }

    function clearFormFields() {
        form.reset();
    }

    // Abre o modal de criação
    openModalButtons.forEach(button => {
        button.addEventListener("click", (event) => {
            event.preventDefault();
            clearErrors();
            clearFormFields();
            modal.classList.add("show");
        });
    });

    // Fecha o modal ao clicar fora
    closeModalArea.addEventListener("click", (event) => {
        if (event.target === closeModalArea) {
            modal.classList.remove("show");
        }
    });

    // Lógica para deletar usuário via fetch()
    deleteButtons.forEach(button => {
        button.addEventListener("click", (event) => {
            event.preventDefault();
            const userId = button.dataset.userId;

            if (confirm("Tem certeza que deseja deletar este usuário?")) {
                fetch(`/delete_user/${userId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCsrfToken(),
                        "Content-Type": "application/json",
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
        return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }
});
