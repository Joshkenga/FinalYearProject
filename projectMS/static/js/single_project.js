const allCheckBoxForms = document.querySelectorAll('li form');
const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]');
const projectId = document.getElementById('projectId').getAttribute('data-project-id');
const markAsCompletedBtn = document.getElementById('markAsCompleted')
const cancelPopupBtn = document.getElementById('cancel_popup_btn');
const continuePopupBtn = document.getElementById('continue_popup_btn');
const popupOverlay = document.getElementById('complete_project_overlay');
const projectComment = document.getElementById('project_comment');
const upgradableRadioBtns = document.querySelectorAll('input[name="upgradable"]');




let allCheckValues = {};
let completionLevel = 0;

allCheckBoxForms.forEach(checkBoxForm =>{
    const checkInput = checkBoxForm.querySelector('input[type="checkbox"]');
    const projectStep = parseInt(checkInput.getAttribute('data-step-no'));
    allCheckValues[projectStep] = checkInput.checked;
    if(checkInput.checked){
        completionLevel = projectStep
    };
    checkInput.addEventListener('click', async ()=>{
            allCheckValues[projectStep] = checkInput.checked;
            console.log(checkInput.checked);
            const request = new Request(`/complete-project-step/${projectId}`, {
                method:'POST',
                headers:{
                    'X-CSRFToken':csrfToken.value
                },
                body:JSON.stringify({'lastChecked':projectStep})
            });

            const response = await fetch(request);
            if(response.redirected){
                window.location.href = response.url
            }
            else{
                alert('Something went wrong !')
        }
    })
})


async function markAsCompleted(){
            
    const checkedRadio = [...upgradableRadioBtns].filter(radioBtn =>{
        return radioBtn.checked === true
    });
    const checkedValue = checkedRadio[0].value;
    const prjCommentContent = projectComment.value;
            const request = new Request(`/mark-as-completed/${projectId}`, {
                method:'POST',
                headers:{
                    'X-CSRFToken':csrfToken.value
                },
                body:JSON.stringify({'completionLevel':completionLevel, 'projectComment':prjCommentContent, 'upgradable':checkedValue})
            });

            const response = await fetch(request);
            if(response.redirected){
                window.location.href = response.url
            }
            else{
                alert('Something went wrong !')
        }
}

function showPopup(){
    popupOverlay.style.display = 'inline-block';
}

function dismissPopup(){
    popupOverlay.style.display = 'none'
}

popupOverlay.addEventListener('click', (e)=>{
    if(e.target.classList.contains('popup-container') || e.target.classList.contains('popup-overlay')){
        dismissPopup();
    }
})

markAsCompletedBtn.addEventListener('click', showPopup);
continuePopupBtn.addEventListener('click', markAsCompleted);