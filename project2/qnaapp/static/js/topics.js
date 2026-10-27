console.log("loaded")

const csrf_token = document.body.dataset.csrf;

async function get_topics() {
    const response = await fetch("/get_topics/");
    const topics = await response.json();
    const container = document.getElementById("topic-container");
    container.innerHTML = "";
    let n = 0;
    topics.forEach(topic => {
        container.innerHTML += `
            <div class="tcard">
                <div>
                    <strong>Topic: ${topic.topic}</strong>
                    <p>${topic.count} Questions Generated</p>
                </div>
                <div>
                    <button onclick="window.location.href='/questions/${topic.topic_id}/'">View Questions</button>
                    <button class="delete_question" onclick="delete_topic(${topic.topic_id})">Delete</button>
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
}

async function delete_topic(topic_id) {
    if (!confirm('do you want to delete this Topic?')) {
        return null;
    }
    const response = await fetch(`/delete_topic/${topic_id}/`, {method: "DELETE", headers: {
        "X-CSRFToken": csrf_token
    }});
    if (response.status == 204) {
        get_topics();

        return null;
    } else {
        console.log("Delete Failed");
    }
}

document.addEventListener("DOMContentLoaded", get_topics)

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