document.getElementById('login-btn').addEventListener('click', function(event){
    event.preventDefault();
    var userLogin = document.getElementById('input-login').value;
    var userPassword = document.getElementById('input-pass').value;

    var loginData = {
        username: userLogin,
        userpass: userPassword
    };

    fetch('/login',{
        method: 'POST',
        headers:{
            'Content-Type' : 'application/json'
        },
        body: JSON.stringify(loginData)
    })
    .then(response =>{
        if(response.ok){
            if (response.status == 200){
                alert('Teacher, Login is authorized');
                window.location.href = '/teacher.html';
            }
            else if (response.status == 201){
                alert('Student, Login is authorized');
                window.location.href = '/student.html';
            }
            else{
                return response.text()
            }
        }
    })
    .then(errorMsg =>{
        if(errorMsg){
            alert('Who are you? Go away! Erorr:'+ errorMsg)
        }
    })
    .catch(error => console.log('Ошибка', error));
});
