let closeButton = document.querySelector('#close-button');
fetch('http://127.0.0.1:8000/user/me', {
    method: "GET",
    headers: {
        'Authorization': 'Bearer ' + document.cookie.split('=')[1]
    }
})
    .then(res => res.json())
    .then(data => {
        if (data['detail'] != null) {
            location.replace('http://127.0.0.1:5500/index.html');
        } else {
            console.log(data)
            let user = {
                'username': data['username'],
                'email': data['email'],
                'rol': data['rol'],
            }
            document.querySelector('#user-name').innerHTML = user.username;
            document.querySelector('#user-rol').innerHTML = user.rol;
            document.querySelector('#username').value = user.username;
            document.querySelector('#email').value = user.email;
        }
    })
    .catch(err => console.log(err));

closeButton.addEventListener('click', switchNav);

sideBar = closeButton.parentElement.parentElement;


function switchNav(){
    sideBar.classList.toggle('close-nav');
    let profile = sideBar.querySelector('.profile-container');
    let profileData = profile.querySelector('.profile-info').querySelector('div');
    profileData.classList.toggle('none');
    profile.querySelector('.profile-info').querySelector('img').classList.toggle('close-img');
    let buttonsSection = sideBar.querySelector('.buttons-container').getElementsByClassName('clickable');
    for (let item of buttonsSection){
        item.classList.toggle('center');
        item.querySelector('p').classList.toggle('none');
    }
    let sections = document.getElementsByTagName('section')
    let footer = document.querySelector('#footer');
    footer.classList.toggle('main-width');
    console.log(sections);
    for (let item of sections){
        item.classList.toggle('main-width');
    }

    
}

document.querySelector('.exit-button').addEventListener('click', (e) => {
    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    window.location.href = 'http://127.0.0.1:5500/index.html';
})