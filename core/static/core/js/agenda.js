window.abrirModal = function(element) {
    const titulo = element.getAttribute("data-titulo");
    const descricao = element.getAttribute("data-descricao");

    document.getElementById("modal-titulo").innerText = titulo;
    document.getElementById("modal-descricao").innerText = descricao;

    const modal = document.getElementById("evento-modal");
    modal.classList.add("show");
    modal.classList.remove("hidden");
}

window.fecharModal = function() {
    const modal = document.getElementById("evento-modal");
    modal.classList.remove("show");
    modal.classList.add("hidden");
}

window.addEventListener("click", function(event) {
    const modal = document.getElementById("evento-modal");
    if (event.target === modal) {
        fecharModal();
    }
});

function confirmarExclusao() {
    return confirm("Tem certeza que deseja excluir este evento?");
}
