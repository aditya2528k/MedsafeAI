document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");

    if (form) {
        form.addEventListener("submit", function (e) {

            const name = document.querySelector("input[name='name']").value;
            const age = document.querySelector("input[name='age']").value;
            const symptoms = document.querySelectorAll("input[name='symptoms']:checked");

            if (name.trim() === "" || age.trim() === "") {
                alert("Please fill all fields");
                e.preventDefault();
                return;
            }

            if (symptoms.length === 0) {
                alert("Please select at least one symptom");
                e.preventDefault();
                return;
            }
        });
    }

});