const navbarUser = document.querySelector('#navbar-user');

navbarUser.addEventListener('click', cambiarVentana);

function cambiarVentana(){
    console.log(document.cookie);
    if (document.cookie.includes('token')){
        window.location.href = 'http://127.0.0.1:5500/login.html';
    }else{
        window.location.href = 'http://127.0.0.1:5500/login.html';
    }
}