document.addEventListener('DOMContentLoaded', function() {
    const password_form = document.getElementById('password-form');
    password_form.addEventListener('submit', function(event) {
        event.preventDefault();
        const old_password = document.getElementById('old_password').value;
        const new_password = document.getElementById('new_password').value;
        const confirm_password = document.getElementById('confirm_password').value;
        const confirm_password_error = document.getElementById('confirm_password_message');
        const new_password_error = document.getElementById('new_password_message');
        if(new_password !== confirm_password || !isStrongPassword(new_password)) {
            confirm_password_error.innerText = '';
            new_password_error.innerText = '';
            if(new_password !== confirm_password) {
                confirm_password_error.innerText = 'Passwords do not match';
                console.log('Passwords do not match');
                console.log(`${new_password} != ${confirm_password}`);
            } else if(!isStrongPassword(new_password)){
                new_password_error.innerText = 'Passwords is weak';
            }
        } else {
            confirm_password_error.innerText = '';
            new_password_error.innerText = '';
            change_password(old_password, new_password);
        }
    })
})

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function isStrongPassword(password) {
  const strongPasswordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@./!#$%^&*()_+=\-])[A-Za-z\d@./!#$%^&*()_+=\-]{8,}$/;
  return strongPasswordRegex.test(password);
}

function change_password(old_password, new_password) {
    fetch('/users/security', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body:JSON.stringify({
            old_password: old_password,
            new_password: new_password
        })
    })
    .then(response => response.json())
    .then(data => {
        const old_password_error = document.getElementById('old_password_message');
        if (data.message === 'Incorrect old password'){
            old_password_error.innerText = data.message;
        } else if (data.message === 'Password changed successfully'){
            console.log(data.message);
        }
    })
    .catch(error => {
        console.error('Password Change error: ', error);
    });
}