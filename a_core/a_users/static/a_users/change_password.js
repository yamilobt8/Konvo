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
            toggleButtonLoading(false);
            if(new_password !== confirm_password) {
                confirm_password_error.innerText = 'Passwords do not match';
                console.log('Passwords do not match');
                console.log(`${new_password} != ${confirm_password}`);
            } else if(!isStrongPassword(new_password)){
                toggleButtonLoading();
                new_password_error.innerText = 'Weak password: must include upper, lower, number, special char, and be 8+ chars';
            }
        } else {
            confirm_password_error.innerText = '';
            new_password_error.innerText = '';
            toggleButtonLoading(true);
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

function toggleButtonLoading(isLoading) {
    const btn = document.getElementById('update_btn');
    if (!btn) return;  // safety check

    if (isLoading) {
        btn.disabled = true;
        btn.innerHTML = 'Updating...';
    } else {
        btn.disabled = false;
        btn.innerHTML = 'Update';
    }
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
        toggleButtonLoading(false);
        const old_password_error = document.getElementById('old_password_message');
        if (data.message === 'Incorrect old password'){
            old_password_error.innerText = data.message;
        } else if (data.message === 'Password changed successfully'){
            console.log(data.message);
            const alert_success = document.getElementById('alert-success');
            if (alert_success.classList.contains('d-none')) {
                const collapseElement = document.getElementById('collapseForm2');
                // create an instance of the collapse form
                const bsCollapse = new bootstrap.Collapse(collapseElement, {
                toggle: false
                });
                bsCollapse.toggle();
                alert_success.classList.remove('d-none');
            }
        }
    })
    .catch(error => {
        console.error('Password Change error: ', error);
    });
}