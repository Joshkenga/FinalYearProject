from datetime import datetime, date
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.urls import reverse
from .decorators import dynamic_login_required
from django.views.decorators.http import require_POST
from .models import Project, ProjectGroup, Category, GroupMember, ProjectSupervisor
import json
from django.utils import timezone
from django.db.models import Q
from django.utils.timezone import make_aware

UserModel = get_user_model()

# Create your views here.


def index(request):
    return redirect('core_app:dashboard', filter='all')

def signup(request):

    if request.method == "POST":
        username = str(request.POST['userName']).strip()
        email = str(request.POST['email']).strip()
        password = str(request.POST['password']).strip()
        try:
            user = UserModel.objects.create(email=email, username=username, password=make_password(password))
            messages.info(request, message="Your account has just been created, you can login now!")
            return redirect('core_app:login')
        except Exception as e:
            print(f'\n\nExcepion occurred in signup as : {e}\n\n')
            return render(request, 'error_page.html', {'error_code':'404', 'error_message':"Oops! Something went wrong!"})
    return render(request, 'core/signup.html')

def filter_by_specific_year(request,filter, year):
    year = int(year)
    # projects = Project.objects.all()
    project_groups = ProjectGroup.objects.filter(academic_year = year)
    all_categories = Category.objects.all()
    filter_used = 'all'
    if request.method == "POST":
        data = json.loads(request.body)
        projectsFilter = data.get('projectsFilter')
        return redirect('core_app:dashboard', filter=projectsFilter)
    if filter == "ongoing":
        # projects = projects.filter(is_completed=False)
        project_groups = project_groups.filter(project__is_completed = False)
        filter_used = 'ongoing'
        
    elif filter == "per_Year":
        # projects = projects.order_by('-group__academic_year')
        project_groups = project_groups.order_by('-academic_year')
        filter_used = 'per_year'
    all_years = []
    all_groups = ProjectGroup.objects.all()
    for group in all_groups:
        year = group.academic_year
        all_years.append(year)
    all_years = set(all_years)

    context = {'filter_used':filter_used, 'groups':project_groups, 'all_categories':all_categories, 'current_year':year, 'all_years':all_years}
    return render(request, 'core/dashboard.html', context)

def login_view(request):
    if request.method == "POST":
        email = str(request.POST['email']).strip()
        password = str(request.POST['password']).strip()
        try:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_coordinator:
                    login(request, user)
                    return redirect('core_app:dashboard', filter='all')
                else:
                    messages.add_message(request, level=messages.INFO, message="You're not yet allowed to access the system, check with the administrator!")
                    # messages.info(request, message="You're not yet allowed to access the system, check with the administrator!")
                    return redirect('core_app:login')
            else:
                print("Invalid creadentials!")
                messages.info(request, message="Invalid credentials!")
                return redirect('core_app:login')
            
        except Exception as e:
            print(f'\n\nExcepion occurred in signup as : {e}\n\n')
            messages.info(request, message="Oops! Something went wrong")
            return HttpResponse('OOps ! Somthing went wrong !')
    return render(request, 'core/login.html')

@dynamic_login_required()
def home(request, filter):


    print(f"\nlogged user : {request.user}\n")
    # projects = Project.objects.all()
    project_groups = ProjectGroup.objects.all()
    all_categories = Category.objects.all()
    filter_used = 'all'
    if request.method == "POST":
        data = json.loads(request.body)
        projectsFilter = data.get('projectsFilter')
        return redirect('core_app:dashboard', filter=projectsFilter)
    if filter == "ongoing":
        # projects = projects.filter(is_completed=False)
        project_groups = project_groups.filter(project__is_completed = False)
        filter_used = 'ongoing'

        
    elif filter == "per_Year":
        # projects = projects.order_by('-group__academic_year')
        project_groups = project_groups.order_by('-academic_year')
        filter_used = 'per_year'
    all_years = []
    all_groups = ProjectGroup.objects.all()
    for group in all_groups:
        year = group.academic_year
        all_years.append(year)
    all_years = set(all_years)
    context = {'filter_used':filter_used, 'groups':project_groups, 'all_categories':all_categories, "all_years":all_years}
    return render(request, 'core/dashboard.html', context)


@dynamic_login_required
def logout_view(request):
    logout(request)
    messages.info(request, message="Logout successful!")
    return redirect('core_app:login')


@dynamic_login_required
def set_deadlines(request, project_id):
    project = Project.objects.get(pk=project_id)
    context = {'project':project}

    if request.method == "POST":
        documentation_deadline = request.POST['documentation_deadline']
        proposal_deadline = request.POST['proposal_deadline']
        implementation_deadline = request.POST['implementation_deadline']
        report_deadline = request.POST['report_deadline']

        print(f"\nThe documentation deadline : {documentation_deadline}\n")

        if documentation_deadline:
       
            project.documentation_deadline = make_aware(datetime.strptime(documentation_deadline, "%Y-%m-%d"))
        if report_deadline:
            project.report_deadline = make_aware(datetime.strptime(report_deadline, "%Y-%m-%d"))
        if implementation_deadline:
            project.implementation_deadline = make_aware(datetime.strptime(implementation_deadline, "%Y-%m-%d"))
        if proposal_deadline:
            project.proposal_deadline = make_aware(datetime.strptime(proposal_deadline, "%Y-%m-%d"))
        project.save()
        return redirect('core_app:single_group', group_id=project.group.pk)
    return render(request, 'core/deadlines.html', context)

@dynamic_login_required
def single_group(request, group_id):
    try:
        group = ProjectGroup.objects.get(pk=group_id)
        group_members = GroupMember.objects.filter(project_group = group)
        project = None
        # project_categories = None
        if group.project is not None:
            project = group.project
            project_categories = project.categories.all()
        context = {'group':group, 'group_members':group_members,  'messages':messages.get_messages(request), 'project':project}
        return render(request, 'core/single_group.html', context)
    except Exception as e:
        print(f"Fatal error : {e}")
        return render(request, 'error_page.html', {'error_code':'404', 'error_message':"Oops! Something went wrong!"})

@dynamic_login_required
def create_group(request):
    if request.user.is_coordinator == False:
        return redirect('core_app:dashboard', filter="all")
    
    if request.method == "POST":
        group_members = []
        members_reg_nums = []
        request_dict = dict(request.POST)
        group_name = request.POST['group_name']
        group_faculty = request.POST['group_faculty']
        academic_year = request.POST['academic_year']
        for key in request_dict.keys():
            if 'projectmember' in str(key).lower():
                member = request.POST[str(key)]
                group_members.append(member)
            if 'member_reg_num' in str(key).lower():
                member_reg_num = request.POST[str(key)]
                members_reg_nums.append(member_reg_num)
        print(request_dict) 
        try:
            new_group = ProjectGroup.objects.create(name=group_name, faculty=group_faculty, academic_year=academic_year )
            new_group.save()
            for name, reg_num in zip(group_members, members_reg_nums):
                if GroupMember.objects.filter(regnumber=reg_num):
                    messages.warning(request, message=f"Student with Registration Number {reg_num} already exists, try again!")
                    return redirect('core_app:create_group')
                member = GroupMember.objects.create(name=name, regnumber=reg_num, project_group=new_group)
                member.save()
            return redirect('core_app:single_group', group_id=new_group.pk)
        except Exception as e:
            print(f"\n\nException in create group  : {e}\n\n")
            return render(request, 'error_page.html', {'error_code':'404', 'error_message':"Oops! Something went wrong!"})
    return render(request, 'core/create_group.html')

@dynamic_login_required
def delete_group(request, group_id):
    try:
        group = ProjectGroup.objects.get(pk=group_id)
        group.delete()
    except Exception as e:
        print(f"An exception occurred as : {e}")
        return render(request, 'error_page.html', {'error_code':'404', 'error_message':"Oops! Something went wrong!"})
    return redirect('core_app:dashboard', filter="all")
@dynamic_login_required
def create_project(request, group_id):
    project_group = ProjectGroup.objects.get(pk=group_id)
    all_supervisors = ProjectSupervisor.objects.all()
    categories = Category.objects.all()
    if not project_group:
        return render(request, 'error_page.html', {'error_code':'404', 'error_message':"Oops! We could not find this page!"})
    if request.user.is_coordinator == False:
        return redirect('core_app:dashboard', filter="all")
    
    if request.method == "POST":
        project_title = request.POST['projectSubject']
        project_platform = request.POST['projectPlatform']
        project_supervisor_id = request.POST['projectSupervisor']
        project_categories = request.POST.getlist('projectCategory')
        
        # print(f"\n\nThe project members : {project_members}\n\n")
        try:
            supervisor = None
            if project_supervisor_id:
                print("\n\n", project_supervisor_id)
                supervisor = ProjectSupervisor.objects.get(pk=project_supervisor_id)
                print("\n\n",supervisor.name)
            categories_list = [Category.objects.get(name=x) for x in project_categories]
            project = Project.objects.create(coordinator=request.user ,title=project_title, platform=project_platform, project_supervisor=supervisor)
            project.categories.set(categories_list)
            
                
            project.save()
            project_group.project = project
            project_group.save()
            return redirect('core_app:single_group', group_id=group_id)
        except Exception as e:
            print(f"\n\nException in create project  : {e}\n\n")
            return render(request, 'error_page.html', {'error_code':'404', 'error_message':"Oops! Something went wrong!"})
    context = {'project_group':project_group, 'categories':categories, 'supervisors':all_supervisors}
    return render(request, 'core/create_project.html', context)

@require_POST
@dynamic_login_required
def complete_project_step(request, pk):
    if request.method == "POST":
        project = Project.objects.get(pk=pk)
        data = json.loads(request.body)
        lastChecked = data.get('lastChecked')

        if(1 <= lastChecked < project.progress) :
            messages.add_message(request, messages.INFO, message="Cannot change this step before the next!")
            print('Step 1')
        elif (lastChecked > project.progress+1):
            messages.add_message(request, messages.INFO, message="Cannot change this step before the previous!")
            print('Step 2')
        else:
            print('Step 3')
            
            project.progress = lastChecked - 1 if lastChecked == project.progress else lastChecked
            project.save()
        return redirect('core_app:single_group', group_id=project.group.pk)

@require_POST
@dynamic_login_required
def mark_as_completed(request, pk):
    project = Project.objects.get(pk=pk)
    if request.method == "POST":
        data = json.loads(request.body)
        completion_level = int(data.get('completionLevel'))
        comment = data.get('projectComment')
        upgradable = int(data.get('upgradable'))
        
        if completion_level == 4: 
            if project.report_file and project.documentation_file: 
                project.is_completed = True
                project.comment = comment
                project.upgradable = upgradable
                project.save()
            else:
                messages.info(request, message="No file was submitted for this project, we can't mark it as completed")
        return redirect('core_app:single_group', group_id=project.group.pk)



@dynamic_login_required
def get_notifications(request, user_id):
    user_id = int(user_id)
    if int(request.user.pk) != int(user_id):
        return redirect('core_app:login')
    today = date.today()
    notif_list = []
    projects = Project.objects.filter(is_completed=False)
    print(f"\nThe projects : {projects}\n")
    for project in projects:
        try:
            notif_obj = {'deadlines_list':[], 'project_name':project.title,
                        'project_link':reverse('core_app:single_group', kwargs={'group_id':project.group.pk})}
            # print('\n\n project link ', notif_obj['project_link'], '\n\n')
            try:
                if project.proposal_deadline.date() >= today:
                    notif_obj['deadlines_list'].append({'Proposal deadline':
                    project.proposal_deadline.date().strftime("%d/%m/%Y")})
            except:
                pass
            try:
                if project.documentation_deadline.date() >= today:
                    notif_obj['deadlines_list'].append({'Documentation deadline':
                    project.documentation_deadline.date().strftime("%d/%m/%Y")})
            except:
                pass
            try:
                if project.implementation_deadline.date() >= today:
                    notif_obj['deadlines_list'].append({'Implementation deadline':
                    project.implementation_deadline.date().strftime("%d/%m/%Y")})
            except:
                pass
            try:
                if project.report_deadline.date() >= today:
                    notif_obj['deadlines_list'].append({'Report deadline':
                    project.report_deadline.date().strftime("%d/%m/%Y")})
            except:
                pass
            if len(notif_obj['deadlines_list']) > 0:
                notif_list.append(notif_obj)
        except Exception as e:
            print(f"Exception occurred as : {e}")
        
    print(f"\nThe notifications list : {notif_list}\n")
    return JsonResponse({'notifications': notif_list}, status=200)



def related_projects(request, category_key, filter):
    project_groups = ProjectGroup.objects.all()
    project_groups_by_category = project_groups
    if category_key != "all":
        project_groups_by_category = project_groups.filter(project__categories__name__icontains=category_key)
    all_categories = Category.objects.all()
    filter_used = 'all'
    if request.method == "POST":
        data = json.loads(request.body)
        projectsFilter = data.get('projectsFilter')
        projectsCategory = data.get('projectsCategory')
        return redirect('core_app:related_projects',category_key=projectsCategory, filter=projectsFilter)
    
    if filter == "ongoing":
        # projects = projects.filter(is_completed=False)
        project_groups_by_category = project_groups_by_category.filter(project__is_completed = False)
        filter_used = 'ongoing'
        
    elif filter == "per_Year":
        # projects = projects.order_by('-group__academic_year')
        project_groups_by_category = project_groups_by_category.order_by('-academic_year')
        filter_used = 'per_year'
    all_years = []
    all_groups = ProjectGroup.objects.all()
    for group in all_groups:
        year = group.academic_year
        all_years.append(year)
    all_years = set(all_years)
    print("Years :", all_years)
    context = {'filter_used':filter_used, 'groups':project_groups_by_category, 'all_categories':all_categories, "all_years":all_years}
    return render(request, 'core/related_projects.html', context)

@require_POST
@dynamic_login_required
def submit_project_files(request, project_id):
    if request.method == "POST":
        project = get_object_or_404(Project, pk=project_id)
        
        # Ensure that 'project_documentation' and 'project_report' are in request.FILES
        project_documentation_file = request.FILES.get('project_documentation')
        project_report_file = request.FILES.get('project_report')

        try:
            if project_documentation_file:
                project.documentation_file = project_documentation_file
            if project_report_file:
                project.report_file = project_report_file
            project.save()
            return redirect('core_app:single_group', group_id=project.group.pk)
        except Exception as e:
            # Handle the error appropriately
            print(f"Error uploading files: {e}")
            return(HttpResponse('<h3> Something went wrong !</h3>'))




