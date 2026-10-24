console.log("Loaded")

const csrf_token = document.body.dataset.csrf;

const createBtn = document.getElementById("createBtn");
const container = document.getElementById("container");

document.getElementById("topic").addEventListener("input", () => {
    container.innerHTML = "";
})

async function create_question () {
    const topic = document.getElementById("topic").value;
    if (!topic) {
        container.innerHTML = `
            <div id="warning">
                <p>Please Enter a Topic to Generate</p>
            </div>
        `;
        return;
    }
    createBtn.disabled = true;
    createBtn.textContent = "Loading...";

    container.innerHTML = `<div id="sign">
                            <p>Generating Question for Topic: ${topic}...</p>
                        </div>`;

    const response = await fetch("/create_question/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token
        },
        body: JSON.stringify({
            "topic": topic
        })
    })

    const data = await response.json();
    if (data.status) {
        container.innerHTML = "";
        console.log(data)
        get_questions();
    } else {
        container.innerHTML = `
            <div id="warning">
                <p>${data.detail}</p>
            </div>
        `;
    }
    document.getElementById("topic").value = "";
    createBtn.textContent = "Create";
    createBtn.disabled = false;

}

async function get_questions() {
    const container = document.getElementById("question-container");
    try {
        const response = await fetch("/get_question/");
        const questions = await response.json();
        container.innerHTML = "";
        let n = 0;
        questions.forEach(question => {
            container.innerHTML += `
                <div class="qcard">
                    <h4>Topic: ${question.topic}</h4>
                    <p>${question.question}</p>
                    <p>- ${question.answer}</p>
                </div>
            `;
            n++;
        });

        if (n < 1) {
            container.innerHTML = `
                <div id="question-container">
                    <div id="emptycard">
                        <h5>No Questions Generated</h5>
                    </div>
                </div>
            `;
        }
    } catch (e) {
        console.error(e);
        container.innerHTML = `
            <div id="question-container">
                <div id="emptycard">
                    <h5>Something Went Wrong. Try Again Later</h5>
                </div>
            </div>
        `;
    }
}

document.addEventListener("DOMContentLoaded", get_questions);

document.getElementById("createBtn").addEventListener("click", create_question)
document.getElementById("topic").addEventListener("keydown", (e) => {
    if (e.key == "Enter") {
        create_question();
    }
})

document.getElementById("logout").addEventListener("click", () => {
    if (!confirm("Do you wish to Log out?")) {
        return;
    }
    fetch("/userlogout/").then(response => response.json()).then(data => {
        if (data.status) {
            window.location.href = "/userlogin/"
        } else {
            console.log("The System Refuses to Log out");
        }
    })
})