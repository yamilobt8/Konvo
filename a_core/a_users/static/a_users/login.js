document.addEventListener('DOMContentLoaded', function () {
    const login_form = document.getElementById('login-form');
    login_form.addEventListener('submit', function (event) {
        event.preventDefault();
        const username = document.getElementById('is_username').value;
        const password = document.getElementById('id_password').value;
        verify_login(username, password);
    })
})

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function verify_login(username, password) {
    fetch('/users/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body:JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        const username_message = document.getElementById('username_message');
        if (data.message === 'Invalid username or password'){
            username_message.innerText = data.message;
        } else if (data.message === 'success'){
            window.location.href = '/';
            console.log('user logged in successfully');
        }
    })
    .catch(error => {
        console.error('Login error: ', error);
    });
}


