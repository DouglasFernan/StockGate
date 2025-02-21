document.addEventListener("DOMContentLoaded", () => {
    console.log("Ativando Select2 nos campos: #id_cliente, #id_produto e #id_vendedor");

    if (typeof jQuery !== "undefined") {
        // Ativar Select2 para Cliente
        $("#id_cliente").select2({
            placeholder: "Selecione um cliente...",
            allowClear: true,
            width: "100%",
            minimumResultsForSearch: 0
        });

        // Ativar Select2 para Produto
        $("#id_produto").select2({
            placeholder: "Selecione um produto...",
            allowClear: true,
            width: "100%",
            minimumResultsForSearch: 0
        });

        // Ativar Select2 para Vendedor
        $("#id_vendedor").select2({
            placeholder: "Selecione um vendedor...",
            allowClear: true,
            width: "100%",
            minimumResultsForSearch: 0
        });

        // Ajustar altura dos campos Select2
        $(".select2-selection").css({
            "height": "40px",
            "display": "flex",
            "align-items": "center"
        });

        // Ajustar alinhamento do texto dentro do Select2
        $(".select2-selection__rendered").css({
            "line-height": "40px",
            "padding-left": "10px"
        });

        // Centralizar seta do Select2
        $(".select2-selection__arrow").css({
            "height": "40px",
            "top": "50%",
            "transform": "translateY(-50%)"
        });

        // Aplicar valor padrão ao cliente, produto e vendedor (se houver)
        let clientePadrao = $("#id_cliente").data("valor-padrao");
        if (clientePadrao) {
            $("#id_cliente").val(clientePadrao).trigger("change");
        } else {
            $("#id_cliente").val("").trigger("change");
        }

        let produtoPadrao = $("#id_produto").data("valor-padrao");
        if (produtoPadrao) {
            $("#id_produto").val(produtoPadrao).trigger("change");
        } else {
            $("#id_produto").val("").trigger("change");
        }

        let vendedorPadrao = $("#id_vendedor").data("valor-padrao");
        if (vendedorPadrao) {
            $("#id_vendedor").val(vendedorPadrao).trigger("change");
        } else {
            $("#id_vendedor").val("").trigger("change");
        }

    } else {
        console.error("Erro: jQuery não carregado!");
    }

    // --- Máscara de CPF ---
    function applyCpfMask(cpfField) {
        cpfField.addEventListener("input", function (event) {
            let value = event.target.value.replace(/\D/g, "");
            if (value.length > 11) value = value.substring(0, 11);

            value = value.replace(/(\d{3})(\d)/, "$1.$2");
            value = value.replace(/(\d{3})(\d)/, "$1.$2");
            value = value.replace(/(\d{3})(\d{1,2})$/, "$1-$2");

            event.target.value = value;
        });
    }

    // --- Máscara de Telefone ---
    function applyPhoneMask(phoneField) {
        phoneField.addEventListener("input", function (event) {
            let value = event.target.value.replace(/\D/g, "");
            if (value.length > 11) value = value.substring(0, 11);

            value = value.replace(/^(\d{2})(\d)/, "($1) $2");
            value = value.replace(/(\d{5})(\d)/, "$1-$2");

            event.target.value = value;
        });
    }

    // Aplica as máscaras aos campos de CPF e telefone
    const cpfField = document.querySelector('input[name="cpf_cliente"]');
    if (cpfField) applyCpfMask(cpfField);

    const phoneField = document.querySelector('input[name="telefone_cliente"]');
    if (phoneField) applyPhoneMask(phoneField);
});
