document.addEventListener('DOMContentLoaded', function() {
    const uploadButton = document.getElementById('upload-button');
    const fileInput = document.getElementById('profile_picture');
    const overlay = document.getElementById('imageOverlay');
    const overlayImage = document.getElementById('overlayImage');
    const submitBtn = document.getElementById('submitBtn');
    const cancelBtn = document.getElementById('cancelBtn');

    // Click upload button → trigger hidden file input
    uploadButton.addEventListener('click', function() {
        fileInput.click();
    });
    fileInput.addEventListener('change', function(event) {
        if (event.target.files.length > 1) {
          alert('Please select only one image.');
          event.target.value = '';
          return;
        }
        const file = event.target.files[0];

        if (file) {
          const reader = new FileReader();
          reader.onload = function(e) {
              overlayImage.src = e.target.result;
              overlay.style.display = 'flex';
          };
          reader.readAsDataURL(file);
          console.log(file);
        } else {
          // TODO
        }

        submitBtn.addEventListener('click', function() {
            send_file(file);
            overlay.style.display = 'none';
        });

        cancelBtn.addEventListener('click', function() {
            overlay.style.display = 'none';
            fileInput.value = '';
        });
  });
});

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}


function send_file(file) {
    const formData = new FormData();
    formData.append('profile_picture', file)
    fetch('/users/change_pfp', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
        },
        body:formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'Image Uploaded Successfully'){
            const alert_success = document.getElementById('pfp-alert-success');
            alert_success.style.display = 'block';
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            const alert_failed = document.getElementById('pfp-alert-failed');
            alert_failed.style.display = 'block';
            alert_failed.innerText = data.message;
        }
    })
    .catch(error => {
        console.error('Profile Image error: ', error);
    });
}
