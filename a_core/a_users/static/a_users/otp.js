document.addEventListener('DOMContentLoaded', function () {
    const otp_verification = document.querySelector('#verify_otp');
    const email_verification = document.querySelector('#verify_email');
    email_verification.addEventListener('click', function(event) {
        event.preventDefault();
        email_verification.classList.add('disabled');
        const email = document.getElementById('email_field').value;
        console.log('button clicked');
        console.log('hello', email);
        send_otp_mail(email);
    })
    otp_verification.addEventListener('click', function(event){
        event.preventDefault();
        const otp = document.getElementById('id_otp').value;
        console.log('otp verification button clicked');
        console.log('otp: ', otp);
        verify_otp(otp);
    })
})

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function send_otp_mail(email) {
    fetch('ajax/send-otp/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body:JSON.stringify({
            email: email
        })
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector('#verify_email').classList.remove('disabled');
        if (data.message === 'OTP sent Successfully'){
            const otp_verification = document.getElementById('verify_otp');
            if (otp_verification.classList.contains('disabled')){
                otp_verification.classList.remove('disabled');
                document.getElementById('email_message').innerText = '';
                document.getElementById('email_field').disabled = true;
                document.getElementById('verify_email').classList.add('disabled');
                document.getElementById('otp_message').innerText = data.message;
            }
        } else if (data.message === 'Email already registered'){
            const mail_message = document.getElementById('email_message');
            if (mail_message.classList.contains('text-success')){
                mail_message.classList.remove('text-success');
                mail_message.classList.add('text-danger');
                mail_message.innerText = data.message;
            }
        }
        console.log(data.message);
    });
}

function verify_otp(otp_code){
    fetch('ajax/verify-otp/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body:JSON.stringify({
            otp: otp_code
        })
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector('#verify_email').classList.remove('disabled');
        const otp_message = document.getElementById('otp_message')
        if (data.message === 'OTP verified'){
            otp_message.innerText = data.message;
            otp_message.classList.remove('text-danger');
            otp_message.classList.add('text-success');
            document.getElementById('id_otp').disabled = true;
            document.getElementById('verify_otp').classList.add('disabled');
        } else{
            otp_message.classList.remove('text-success');
            otp_message.classList.add('text-danger');
            otp_message.innerText = data.message;
        }
    })
}