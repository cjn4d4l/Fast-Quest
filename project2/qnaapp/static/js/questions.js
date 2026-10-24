console.log("loaded")

const csrf_token = document.body.dataset.csrf;

async function get_questions() {
    const response = await fetch("/get_all_questions/");
    const questions = await response.json();
    const container = document.getElementById("question-container");
    container.innerHTML = "";
    let n = 0;
    questions.forEach(question => {
        container.innerHTML += `
            <div class="qcard">
                <h4>Topic: ${question.topic}</h4>
                <p>${question.question}</p>
                <p>- ${question.answer}</p>
                <button class="delete_question" onclick="delete_question(${question.question_id})">Delete</button>
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
}

async function delete_question(question_id) {
    if (!confirm('do you want to delete this question?')) {
        return null;
    }
    const response = await fetch(`/delete_question/${question_id}/`, {method: "DELETE", headers: {
        "X-CSRFToken": csrf_token
    }});
    if (response.status == 204) {
        get_questions();

        return null;
    } else {
        console.log("Delete Failed");
    }
}

document.addEventListener("DOMContentLoaded", get_questions)

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