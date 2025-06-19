document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('registering_form');
    form.addEventListener('submit', function (event){
        event.preventDefault();

        const otp_message = document.getElementById('otp_message').textContent;
        const username = document.getElementById('is_username').value.trim();
        const email_message = document.getElementById('email_message');
        const registerBtn = document.getElementById('registering_button');
        const username_message = document.getElementById('username_message');
        const password = document.getElementById('id_password').value;
        const confirmed_password = document.getElementById('id_confirm_password').value;
        const password_message = document.getElementById('password_message');
        const email = document.getElementById('email_field').value;

        registerBtn.disabled = true;
        registerBtn.innerText = 'Registering...';

        if (otp_message !== 'OTP verified') {
             if (email_message.classList.contains('text-success')){
                email_message.classList.remove('text-success');
                email_message.classList.add('text-danger');
                email_message.innerText = 'This field is required';
            } else{
                email_message.classList.add('text-success');
            }
            resetButton(registerBtn);
             return;
        } else if(username === ''){
            username_message.innerText = 'This field is required';
            resetButton(registerBtn);
            return;
        } else if (password !== confirmed_password) {
            password_message.innerText = 'Passwords Must match';
            resetButton(registerBtn);
            return;
        } else {
            if (isStrongPassword(password)) {
                console.log("password is strong");
                console.log("username: ", username, "email: ", email, "password: ", password);
                register_user(username, email, password, registerBtn);

            } else {
                password_message.innerText = 'Weak password: must include upper, lower, number, special char, and be 8+ chars';
                resetButton(registerBtn);
                return;
            }
        }
    })
})

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function resetButton(button) {
    button.disabled = false;
    button.innerText = 'Register';
}



function isStrongPassword(password) {
  const strongPasswordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@./!#$%^&*()_+=\-])[A-Za-z\d@./!#$%^&*()_+=\-]{8,}$/;
  return strongPasswordRegex.test(password);
}

function register_user(username, email, password, registerBtn){
    fetch('/users/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body:JSON.stringify({
            username: username,
            email: email,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        const username_message = document.getElementById('username_message')
        if (data.message === 'Username already registered'){
            username_message.innerText = data.message;
        } else if (data.message === 'User registered successfully'){
            window.location.href = '/';
        } else {
            console.log(data.message);
        }

    })
    .catch(error => {
        console.error('Error:', error);
    })
    .finally(() => {
        resetButton(registerBtn);
    });
}