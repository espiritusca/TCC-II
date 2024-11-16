function showContent(content) {
    // Esconde todas as content-box
    const contentBoxes = document.querySelectorAll('.content-box');
    contentBoxes.forEach(box => box.classList.remove('active'));

    // Mostra o conteúdo clicado
    const target = document.getElementById(content);
    target.classList.add('active');
}

function goBack(previousContent) {
    showContent(previousContent); 
}

const API_URL = "http://localhost:8080/api/pacientes";

// Função para buscar todos os pacientes
async function fetchPacientes() {
    try {
        /*const response = await fetch(API_URL);*/
        const response =
        await fetch('http://localhost:8080/api/pacientes', {
            method:'GET', 
            headers:{'Content-Type':'application/json'}
          })
        console.log(response)

        if (!response.ok) throw new Error(`Erro ao buscar pacientes: ${response}`);
        const pacientes = await response.json();
        console.log(pacientes)

        const pacientesDiv = document.getElementById("wPL");
        pacientes.forEach(function(p) {
            pacientesDiv.innerHTML+=`<div class="waitingPatient">
                        <div class="nameID">
                            <span>#${p.id} -</span>
                            <span>${p.nome}</span>
                        </div>
                        <div class="agePhoneAvailability">
                            <span>${p.idade} anos</span>
                            <span>
                                <img src="img/phone-svgrepo-com.svg" alt="Telefone">
                                ${p.contato}
                            </span>
                            <span>
                                <input type="checkbox" disabled checked>Manhã
                                <input type="checkbox" disabled checked>Tarde
                            </span>
                        </div>
                        <div class="whatsObsEdit">
                            <button>
                                <img src="img/whatsapp-whats-app-svgrepo-com.svg" alt="Enviar Mensagem">
                                Enviar Mensagem
                            </button>
                            <button>
                                <img src="img/info-square-svgrepo-com.svg" alt="Observações">
                                Observações
                            </button>
                            <button>
                                <img src="img/edit-svgrepo-com.svg" alt="Editar">
                                Editar
                            </button>
                        </div>
                    </div>`
        })
       
    } catch (error) {
        console.error(error);
    }
}

async function createPaciente(nome, idade, contato) {
    try {
        const response = await fetch(API_URL, {
            method: "POST", // Método POST
            headers: {
                "Content-Type": "application/json", // Tipo de conteúdo
            },
            body: JSON.stringify({ nome, idade, contato }), // Envia os dados como JSON
        });

        if (!response.ok) throw new Error(`Erro ao criar paciente: ${response.statusText}`);

        const paciente = await response.json();
        console.log("Paciente criado:", paciente);
        alert("Paciente cadastrado com sucesso!");
    } catch (error) {
        console.error(error);
        alert("Erro ao cadastrar paciente.");
    }
}

// Função para lidar com o envio do formulário
document.getElementById("waitingListRegister").addEventListener("submit", function(event) {
    event.preventDefault(); // Evita o envio do formulário padrão

    // Pegando os valores dos campos do formulário
    const nome = document.getElementById("nome").value;
    const idade = document.getElementById("idade").value;
    const contato = document.getElementById("contato").value;

    // Enviando os dados para a API
    createPaciente(nome, idade, contato).then()
    fetchPacientes().then()
});

fetchPacientes().then()