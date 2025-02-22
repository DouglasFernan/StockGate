document.addEventListener("DOMContentLoaded", () => {
    const modal = document.querySelector(".modal");
    const openModalButtons = document.querySelectorAll("#open-modal");
    const closeModalArea = document.querySelector(".modal");
    const errorMessages = document.querySelectorAll(".error");
    const form = document.getElementById("form");
    const cpfField = document.querySelector('input[name="cpf"]');
    const phoneField = document.querySelector('input[name="phone"]');
    const deleteButtons = document.querySelectorAll(".delete-cliente");

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

    // Aplica máscara ao telefone
    function applyPhoneMask(phoneField) {
        phoneField.addEventListener("input", function (event) {
            let value = event.target.value.replace(/\D/g, "");
            if (value.length > 11) {
                value = value.substring(0, 11);
            }

            if (value.length <= 10) {
                value = value.replace(/(\d{2})(\d)/, "($1) $2");
                value = value.replace(/(\d{4})(\d)/, "$1-$2");
            } else {
                value = value.replace(/(\d{2})(\d)/, "($1) $2");
                value = value.replace(/(\d{5})(\d)/, "$1-$2");
            }

            event.target.value = value;
        });
    }

    if (cpfField) applyCpfMask(cpfField);
    if (phoneField) applyPhoneMask(phoneField);

    function clearErrors() {
        errorMessages.forEach(error => {
            error.innerHTML = "";
        });
    }

    function clearFormFields() {
        form.reset();
    }

    // Abre o modal de criação de cliente
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

    // Lógica para deletar cliente via fetch()
    deleteButtons.forEach(button => {
        button.addEventListener("click", (event) => {
            event.preventDefault();
            const clienteId = button.dataset.clienteId;

            if (confirm("Tem certeza que deseja deletar este cliente?")) {
                fetch(`/clientes/deletar/${clienteId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCsrfToken(),
                        "Content-Type": "application/json",
                    },
                }).then(response => {
                    if (response.ok) {
                        alert("Cliente deletado com sucesso!");
                        location.reload();
                    } else {
                        alert("Erro ao deletar o cliente.");
                    }
                });
            }
        });
    });

    // Remove a formatação antes de enviar o formulário
    form.addEventListener("submit", function () {
        if (cpfField) {
            cpfField.value = cpfField.value.replace(/\D/g, "");
        }
        if (phoneField) {
            phoneField.value = phoneField.value.replace(/\D/g, "");
        }
    });

    function getCsrfToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }
});
