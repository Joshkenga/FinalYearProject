const deadlinesForm = document.getElementById('deadlines_form');
const setDeadlinesBtn = document.getElementById('set_deadlines_btn');
const allDeadlines = deadlinesForm.querySelectorAll('input[type="date"]');


function deadlineSet(){
    let deadline_set = false;
    allDeadlines.forEach(item =>{
        const itemValue = item.value;
        if(itemValue){
            deadline_set = true;
        }
    });
    return deadline_set
}

function submitDeadlines(){
    if(deadlineSet()){
        deadlinesForm.submit();
    }else{
        alert('You need to set at least one deadline')
    }
};


setDeadlinesBtn.addEventListener('click', submitDeadlines);
