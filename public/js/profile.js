console.log(document.cookie)
let title = document.querySelector('.title');
let id = document.querySelector('.id');
let email = document.querySelector('.email');
fetch('http://127.0.0.1:8000/users/me', {
    method: "GET",
    headers: {
        'Authorization': 'Bearer ' + document.cookie.split('=')[1]
    }
})
    .then(res => res.json())
    .then(data => {
        if (data['detail'] != null) {
            location.replace('http://127.0.0.1:5500/index.html')
        } else {
            title.innerHTML = '¡Bienvenido!' + data['username'];
            id.innerHTML = 'ID:' + data['id'];
            email.innerHTML = 'Correo: ' + data['email'];
        }
    })
    .catch(err => console.log(err));