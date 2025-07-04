document.addEventListener('DOMContentLoaded', function(event) {
    event.preventDefault();
    const toggleLink = document.getElementById('toggleArrow');
    const icon = toggleLink.querySelector('i');
    const collapseEl = document.getElementById('collapseForm1');

    collapseEl.addEventListener('show.bs.collapse', () => {
        icon.classList.remove('bi-chevron-right');
        icon.classList.add('bi-chevron-down');
    });

    collapseEl.addEventListener('hide.bs.collapse', () => {
        icon.classList.remove('bi-chevron-down');
        icon.classList.add('bi-chevron-right');
    });
})