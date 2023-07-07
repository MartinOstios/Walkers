let form = document.querySelector("#login-form");

form.addEventListener("submit", function (e) {
    e.preventDefault();
    const prePayload = new FormData(form);
    const payload = new URLSearchParams(prePayload);
    fetch('http://127.0.0.1:8000/login', {
        method: "POST",
        body: payload
    })
    .then(res => res.json())
    .then(data => console.log(data))
    .catch(err => alert(err));
})