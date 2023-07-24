let form = document.querySelector("#login-form");
let loginAlert = document.querySelector('#login-alert')
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
            if (data['access_token'] != null) {
                const cookieDuration = 1;
                const expirationDate = new Date();
                expirationDate.setDate(expirationDate.getDate() + cookieDuration);
                const cookieValue = `token=${encodeURIComponent(data['access_token'])}; expires=${expirationDate.toUTCString()}; path=/`;
                document.cookie = cookieValue;
                location.replace('http://127.0.0.1:5500/profile.html')
            }else{
                loginAlert.innerHTML = data['detail'];
            }
        })
        .catch(err => console.log(err));
})