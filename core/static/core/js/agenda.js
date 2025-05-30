let cardAtual = null;

window.abrirModal = function(element) {
    cardAtual = element;
    const titulo = element.getAttribute("data-titulo");
    const descricao = element.getAttribute("data-descricao");
    const categoria = element.getAttribute("data-categoria") || "";

    document.getElementById("modal-titulo").innerText = titulo;
    document.getElementById("modal-descricao").innerText = descricao;

    const selectCategoria = document.getElementById("modal-categoria");
    if (selectCategoria) {
        selectCategoria.value = categoria;
    }

    const modal = document.getElementById("evento-modal");
    modal.classList.add("show");
    modal.classList.remove("hidden");
}

window.fecharModal = function() {
    const modal = document.getElementById("evento-modal");
    modal.classList.remove("show");
    modal.classList.add("hidden");
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

window.alterarCategoria = function(select) {
    const novaCategoriaId = select.value;
    if (!cardAtual) {
        alert('Erro: Nenhum card selecionado');
        return;
    }

    // Pega o id do evento pelo link dentro do card
    const linkEvento = cardAtual.querySelector("a[href*='evento/?id=']");
    if (!linkEvento) {
        alert('Erro: Link do evento não encontrado');
        return;
    }
    const url = new URL(linkEvento.href);
    const eventoId = url.searchParams.get('id');

    fetch("/atualizar_categoria/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie('csrftoken'),
        },
        body: JSON.stringify({
            evento_id: eventoId,
            categoria: novaCategoriaId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "sucesso") {
            // Atualiza a borda com a cor que veio do backend
            cardAtual.style.borderLeft = `6px solid ${data.cor}`;
            cardAtual.setAttribute('data-categoria', novaCategoriaId);
            fecharModal();
        } else {
            alert("Erro ao atualizar categoria: " + data.mensagem);
        }
    })
    .catch(error => {
        alert("Erro de rede: " + error);
    });
}

document.querySelectorAll('.sidebar-dropdown-toggle').forEach(button => {
    button.addEventListener('click', function() {
        const dropdown = this.parentElement; // pega o elemento pai .sidebar-dropdown
        dropdown.classList.toggle('open');   // adiciona ou remove a classe 'open'
    });
});
