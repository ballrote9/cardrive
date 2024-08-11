
// JavaScript to toggle the dropdown menu
document.addEventListener('DOMContentLoaded', function () {
    const dropdown = document.querySelector('.dropdown');
    const dropdownContent = document.querySelector('.dropdown-content');

    dropdown.addEventListener('click', function () {
        dropdownContent.classList.toggle('show');
    });

    window.addEventListener('click', function (event) {
        if (!dropdown.contains(event.target)) {
            dropdownContent.classList.remove('show');
        }
    });
});