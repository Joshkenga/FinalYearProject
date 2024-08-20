

const signupForm = document.getElementById('signup_form');
const emailEl = document.getElementById('email');
const usernameEl = document.getElementById('userName');
const passwordEl = document.getElementById('password');
const confPasswordEl = document.getElementById('confirmPassword');

const signupBtn = document.getElementById('signupBtn');

const email = emailEl.value;
const username = usernameEl.value;
const password = passwordEl.value;
const confPassword = confPasswordEl.value;




function checkForm(){
    console.log('Elements : ', password, username, email, confPassword);
    if(passwordEl.value.trim() && passwordEl.value.trim() === confPasswordEl.value.trim() && emailEl.value.trim() && usernameEl.value.trim()){
        return true
    }else{
        alert(`Invalid inputs, check again please!`);
        return false
    };
    
    
}


function sendForm(){
    if(checkForm()){
        signupForm.submit()
    }else{
        console.log('Something went wrong!!')
    }
}

window.addEventListener('DOMContentLoaded', ()=>{
    signupBtn.addEventListener('click', e=>{
        e.preventDefault();
        sendForm();
    })
})