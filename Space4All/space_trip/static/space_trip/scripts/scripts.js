function show() {
    document.getElementById('userimage').style.display = "block";
}

function hide() {
    document.getElementById('userimage').style.display = "none";
}

function showUserInfo() {
    document.getElementById('userInfo').style.display = "block";
}

function hideUserInfo() {
    document.getElementById('userInfo').style.display = "none";
}

function listaQuestoes() {
    var x = document.getElementById("questoes");
    if (x.style.display === "none") {
        document.getElementById('botaoQuestoes').innerHTML= 'Esconder lista de Questões';
        x.style.display = "block";
    } else {
        document.getElementById('botaoQuestoes').innerHTML= 'Mostrar lista de Questões';
        x.style.display = "none";
    }
}

