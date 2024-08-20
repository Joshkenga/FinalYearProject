const ongoingFilterBtn  = document.getElementById('ongoing-filter');
const allFilterBtn  = document.getElementById('all-filter');
const yearFilterBtn  = document.getElementById('year-filter');
const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]');
const searchBarField = document.getElementById('search_bar_field');
const tableBody = document.getElementById('table_body');
const allRecords = tableBody.querySelectorAll('tr');
const userIdEl = document.getElementById('userId');
const userId =  parseInt(userIdEl.getAttribute('data-user-id'));
const notificationsContainer = document.getElementById('notifications-container');
const activeFilter = document.querySelector('.tab.btn.active').getAttribute("data-filter");
const relatedTags = document.querySelectorAll('.related_tag');

async function sortProjects(category, filterType){
    console.log(`The chosen category is : ${category}`);
    const request  = new Request(`/related-projects/${category}/${filterType}`, {
        method:'POST',
        headers:{
            'X-CSRFToken':csrfToken.value
        },
        body:JSON.stringify({'projectsFilter':filterType, 'projectsCategory':category})
    })
    const response = await fetch(request);
    if(response.redirected){
        window.location.href = response.url
    }
    else{
        alert('Something went wrong !')
    }
}

function filter(keyword){
    tableBody.innerHTML = '';
    allRecords.forEach(record =>{
        const title = record.querySelector('.prj_title').textContent.toLowerCase();
        if(title.includes(keyword)){
            console.log(title);
            tableBody.appendChild(record);
        }
    })
}


// Function to fetch notifications from the backend
async function fetchNotifications() {
    try {
        const response = await fetch(`/notifications/${userId}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        return data.notifications;  // Assuming API returns notifications in JSON format
    } catch (error) {
        console.error('Error fetching notifications:', error);
        return [];
    }
}

// Function to display notifications
async function displayNotifications() {
    const notifications = await fetchNotifications();
    if (notifications.length) {
        for (const notification of notifications) {
            const deadlines = notification.deadlines_list;
            const project_name = notification.project_name;
            const project_link = notification.project_link;
            await showToast(deadlines, project_name, project_link);
        }
    }
}

// Function to show a toast with a delay
async function showToast(deadlines_list, project_name, project_link) {
    return new Promise(resolve => {
        // Create toast element
        console.log(project_link)
        const toast = document.createElement('a');
        toast.className = 'toast'; toast.setAttribute('href', project_link);
        const toastContentEl = document.createElement('div');
        toastContentEl.className = "toast-top-content";
        
        deadlines_list.forEach(item => {
            for (const key in item) {
                toastContentEl.innerHTML += `
                    <p><span>${key}</span> <span class="bold">${item[key]}</span></p>`;
            }
        });

        toastContentEl.innerHTML += `
            <p class="bold main-content">Project: ${project_name.length > 10 ? project_name.slice(0, 10).concat('...') : project_name}</p>`;
        
        toast.appendChild(toastContentEl);
        notificationsContainer.appendChild(toast);

        // Automatically remove toast after a few seconds
        setTimeout(function() {
            notificationsContainer.removeChild(toast);
            setTimeout(function(){
                resolve();  // Resolve the promise after the toast is removed
            }, 2000)
        }, 6000); 
    });
}



yearFilterBtn.addEventListener('click', ()=>{
    sortProjects('all', 'per_Year');
});
allFilterBtn.addEventListener('click', ()=>{
    sortProjects('all','all');
});
ongoingFilterBtn.addEventListener('click', ()=>{
    sortProjects('all','ongoing');
});

relatedTags.forEach(tag =>{
    const chosenCategory = tag.getAttribute("data-tag-category");
    tag.addEventListener('click', ()=>{
        sortProjects(chosenCategory, activeFilter);
    })
})

searchBarField.addEventListener('keyup', ()=>{
    filter(searchBarField.value.toLowerCase());
});


window.addEventListener('DOMContentLoaded', ()=>{
    allRecords.forEach(item =>{
        const item_link = item.getAttribute('data-url');
        item.addEventListener('click', ()=>{
            window.location.href = item_link
        })
    })
    
})
