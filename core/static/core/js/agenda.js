let cardAtual = null;

const coresCategoria = {
    'aniversario': '#f39c12',
    'festa': '#e74c3c',
    'reuniao': '#3498db',
    'pessoal': '#9b59b6',
    'trabalho': '#2ecc71',
};

function alterarCategoria(select) {
    const novaCategoria = select.value;
    const eventoId = window.cardAtual.querySelector("a[href*='evento/?id=']").href.split("id=")[1];

    fetch("/atualizar_categoria/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie('csrftoken'),
        },
        body: JSON.stringify({
            evento_id: eventoId,
            categoria: novaCategoria
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "sucesso") {
            // Atualiza a cor do card na tela
            window.cardAtual.style.borderLeft = `6px solid ${data.cor}`;
        } else {
            alert("Erro ao atualizar categoria: " + data.mensagem);
        }
    })
    .catch(error => {
        alert("Erro de rede: " + error);
    });
}

// Função auxiliar para pegar o CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
window.abrirModal = function(element) {
    cardAtual = element;
    const titulo = element.getAttribute("data-titulo");
    const descricao = element.getAttribute("data-descricao");
    const categoria = element.getAttribute("data-categoria") || "";

    document.getElementById("modal-titulo").innerText = titulo;
    document.getElementById("modal-descricao").innerText = descricao;
    
    // Setar categoria no select
    const selectCategoria = document.getElementById("modal-categoria");
    if(selectCategoria) {
        selectCategoria.value = categoria;
    }

    // Salvar referência para depois alterar o card
    window.cardAtual = element;
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

window.alterarCategoria = function(select) {
    const categoria = select.value;
    const card = window.cardAtual;

    const cores = {
        'aniversario': '#f39c12',
        'festa': '#e74c3c',
        'reuniao': '#3498db',
        'pessoal': '#9b59b6',
        'trabalho': '#2ecc71',
    };

    if(card){
        card.style.backgroundColor = cores[categoria] || '';
        // Atualizar data-categoria para manter estado
        card.setAttribute('data-categoria', categoria);

        // Aqui você pode adicionar código AJAX para salvar a alteração no backend, se desejar
    }
}