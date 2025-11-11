const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});

const formLoginBtn = document.querySelector('.sign-in form button');

formLoginBtn.addEventListener('click', (e) => {
    e.preventDefault(); 
    window.location.href = 'home.html'; 
});
