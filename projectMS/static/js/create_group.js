
const addMemberBtn = document.getElementById('add_member_btn');
const academicYearInputEl = document.getElementById('academic-year');
const staticFilesPath = document.getElementById('staticFilesPath').getAttribute("data-path");


const thisYear = new Date().getFullYear();
academicYearInputEl.setAttribute('min', `${thisYear - 1}`)



function addMember() {
        const projectMembersParentEl = document.getElementById('project-members');
        const allMembers = projectMembersParentEl.querySelectorAll('.member-element');
        const lastMember = allMembers[allMembers.length -1];
        const lastMemberNumber = parseInt(lastMember.getAttribute('data-member-number'));
        if(lastMemberNumber < 5){
            // projectMembersParentEl.innerHTML += `
            // <div class="member-element" data-member-number="${lastMemberNumber+1}">
            //     <input type="text" name="projectMember${lastMemberNumber+1}"  placeholder="Member Name" required>
            //     <input type="text" name="member_reg_num${lastMemberNumber+1}"  placeholder="Reg num" required>
            //     <span class="remove-member">
            //         <img src="{% static 'images/icons/cross-check-icon.png' %}"  alt="">
            //     </span>
            // </div> 
            // `;
            const newMemberEl = document.createElement('div'); newMemberEl.className = "member-element";
                newMemberEl.setAttribute("data-member-number", `${lastMemberNumber+1}`);
            newMemberEl.innerHTML += `
            <input type="text" name="projectMember${lastMemberNumber+1}"  placeholder="Member Name" required>
            <input type="text" name="member_reg_num${lastMemberNumber+1}"  placeholder="Reg num" required>
            `;
            const removeMemberBtn = document.createElement('span'); removeMemberBtn.className = "remove-member";
            removeMemberBtn.innerHTML += `
            <img src="${staticFilesPath}/icons/cross-check-icon.png"  alt="">
            `;
            removeMemberBtn.addEventListener('click', ()=>{
                    newMemberEl.remove()
                });
            newMemberEl.append(removeMemberBtn);
            projectMembersParentEl.appendChild(newMemberEl);
            }
            else{
                alert("Cannot have more than 5 members!");
            } 
    }
addMemberBtn.addEventListener('click', addMember);
