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
        .then(data => {
            const cookieDuration = 1;
            const expirationDate = new Date();
            expirationDate.setDate(expirationDate.getDate() + cookieDuration);
            const cookieValue = `token=${encodeURIComponent(data['access_token'])}; expires=${expirationDate.toUTCString()}; path=/`;
            document.cookie = cookieValue;
        })
        .catch(err => console.log(err));
})

function save_token(access_token) {
    token = access_token;
}

function get_token() {
    return token;
}