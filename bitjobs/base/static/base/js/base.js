$(document).ready(function() {
    var navLinks = document.querySelector('.navNarrow');
    var narrowLinks = document.querySelector('.narrowLinks');



    function toggle() {
        narrowLinks.classList.toggle('hidden');
    };

     navLinks.addEventListener('click', toggle);
});