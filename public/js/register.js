const form = document.querySelector("#form");
const textAlert = document.querySelector('#alert');

form.addEventListener('submit', function (e) {
    e.preventDefault();
    let payload = new FormData(form).values();
    payload = [...payload];
    let data = {
        'username': payload[0],
        'email': payload[1],
        'plain_password': payload[2]
    }
    data = JSON.stringify(data);
    console.log(data);
    let url = "http://127.0.0.1:8000/register"
    fetch(url, {
        method: 'POST',
        body: data,
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data['id'] != null){
            location.replace('http://127.0.0.1:5500/login.html');
        }else{
            textAlert.innerHTML = 'Error: ' + data['detail'];
        }
    })
    .catch(err => console.log(err))
})