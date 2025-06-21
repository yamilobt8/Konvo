document.addEventListener('DOMContentLoaded', function() {
    const generalInfoBtn  = document.getElementById('general-information-btn');
    const securityBtn  = document.getElementById('security-btn');

    generalInfoBtn .addEventListener('click', function(event) {
        event.preventDefault();
        generalInfoBtn.classList.add('tab-active');
        securityBtn.classList.remove('tab-active');
        main();
    })

    securityBtn .addEventListener('click', function(event) {
        event.preventDefault();
        generalInfoBtn.classList.remove('tab-active');
        securityBtn.classList.add('tab-active');
        main2();
    })
})


function main() {
    const securityDiv = document.getElementById('security-div');
    const generalInfos = document.getElementById('general-infos');

    if (generalInfos.classList.contains('d-none')) {
            generalInfos.classList.remove('d-none');
            securityDiv.classList.add('d-none');
    }
}

function main2() {
    const generalInfos = document.getElementById('general-infos');
    const securityDiv = document.getElementById('security-div');
    if (securityDiv.classList.contains('d-none')) {
            securityDiv.classList.remove('d-none');
            generalInfos.classList.add('d-none');
    }
}