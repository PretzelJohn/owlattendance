
function updateFeedback(e) {
    "use strict";

    var add = "";
    if(e.target.id === "ksu_id") {
        add = "(9-digit number)";
    } else if(e.target.id === "first_name" || e.target.id === "last_name") {
        add = "(Letters, dashes, apostrophes)";
    }
    e.target.nextElementSibling.innerHTML = e.target.validationMessage+"<br>"+add;
}

(function() {
    "use strict";

    var forms = document.querySelectorAll(".needs-validation");
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    var fields = document.querySelectorAll('.form-control');
    fields.forEach(function (field) {
        field.addEventListener('input', updateFeedback);
        field.addEventListener('invalid', updateFeedback);
    });
})();

