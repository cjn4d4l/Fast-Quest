console.log("loaded")

const csrf_token = document.body.dataset.csrf;

async function createUser() {
    const user = {
        username: document.getElementById("username").value,
        email: document.getElementById("gmail").value,
        password: document.getElementById("password").value,
        first_name: document.getElementById("first_name").value
    }
    document.getElementById("message").innerText = "Loading...";
    const response = await fetch("/create_user/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token
        },
        body: JSON.stringify(user)
    })

    const data = await response.json();
    if (data.status) {
        window.location.href = "/userlogin/";
    }
}

async function loginUser() {
    const user = {
        username: document.getElementById("username").value,
        password: document.getElementById("password").value
    }
    document.getElementById("message").innerText = "Loading...";
    const response = await fetch("/login_user/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token
        },
        body: JSON.stringify(user)
    })

    const data = await response.json();
    if (data.status) {
        window.location.href = "/";
    } else {
        document.getElementById("message").innerText = data.message;
    }
}

const create = document.getElementById("create")
const login = document.getElementById("login")

if (create) {
    create.addEventListener("click", createUser)
}

if (login) {
    login.addEventListener("click", loginUser)
}