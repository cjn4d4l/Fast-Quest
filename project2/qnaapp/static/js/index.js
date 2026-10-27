console.log("Loaded")

const csrf_token = document.body.dataset.csrf;

const createBtn = document.getElementById("createBtn");
const container = document.getElementById("container");

document.getElementById("topic").addEventListener("input", () => {
    container.innerHTML = "";
})

async function create_question () {
    const topic = document.getElementById("topic").value;
    const count = document.getElementById('count').value;
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
            "topic": topic, "count": count
        })
    })

    const data = await response.json();
    if (data.status) {
        container.innerHTML = `<div id="success">
                                    <p>Successfully Generated Questions for ${topic}. Check Below</p>
                                </div>`;
        console.log(data)
        get_topics();
    } else {
        container.innerHTML = `
            <div id="warning">
                <p>${data.detail}</p>
            </div>
        `;
    }
    document.getElementById("topic").value = "";
    document.getElementById("count").value = 1;
    createBtn.textContent = "Create";
    createBtn.disabled = false;

}

async function get_topics() {
    const container = document.getElementById("topic-container");
    try {
        const response = await fetch("/get_recents/");
        if (response.status == 404) {
            console.log("Could not Get Topics")
            return;
        }
        const topics = await response.json();
        container.innerHTML = "";
        let n = 0;
        topics.forEach(topic => {
            container.innerHTML += `
                <div class="tcard">
                    <div>
                        <h4>Topic: ${topic.topic}</h4>
                        <p>${topic.count} Questions Generated</p>
                    </div>
                    <div>
                        <button onclick="window.location.href='/questions/${topic.topic_id}'">View Questions</button>
                    </div>
                </div>
            `;
            n++;
        });

        if (n < 1) {
            container.innerHTML = `
                <div id="topic-container">
                    <div id="emptycard">
                        <h5>No Topics Available</h5>
                    </div>
                </div>
            `;
        }
    } catch (e) {
        console.error(e);
        container.innerHTML = `
            <div id="topic-container">
                <div id="emptycard">
                    <h5>Something Went Wrong. Try Again Later</h5>
                </div>
            </div>
        `;
    }
}

document.addEventListener("DOMContentLoaded", get_topics);

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