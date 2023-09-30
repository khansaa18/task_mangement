from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .forms import LoginForm, CustomUserCreationForm, TaskForm, SearchForm
from .models import CustomUser, TaskModel


def index(request):
    if 'userid' not in request.session:
        return redirect('login')

    if (request.session['username'] == "admin"):
        total_assigned_task = len(TaskModel.objects.filter(assigned_to_id=None))
        total_completed_tasks = len(
            TaskModel.objects.filter(Q(assigned_to_id=None) & Q(is_completed=True)))
        total_in_progress_task = len(TaskModel.objects.filter(
            Q(assigned_to_id=None) & Q(is_in_progress=True) & Q(is_completed=False)))
        total_in_active_task = len(TaskModel.objects.filter(
            Q(assigned_to_id=None) & Q(is_in_progress=False) & Q(is_completed=False)))
    else:
        total_assigned_task = len(TaskModel.objects.filter(assigned_to_id= request.session['userid']))
        total_completed_tasks = len(TaskModel.objects.filter(Q(assigned_to_id=request.session['userid']) & Q(is_completed=True)))
        total_in_progress_task = len(TaskModel.objects.filter(Q(assigned_to_id=request.session['userid']) & Q(is_in_progress=True) & Q(is_completed=False)))
        total_in_active_task = len(TaskModel.objects.filter(Q(assigned_to_id=request.session['userid']) & Q(is_in_progress=False) & Q(is_completed=False)))

    context = {
        'totalassignedtask':total_assigned_task,
        'totalcompletedtasks': total_completed_tasks,
        'totalinprogresstask': total_in_progress_task,
        'totalinactivetask' : total_in_active_task
    }
    return render(request, 'dashboard/dashboard.html',context=context)


def login_view(request):
    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            username = loginform.cleaned_data['email']
            password = loginform.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['username'] = user.username
                request.session['userid'] = user.id
                return redirect('/home')  # Replace 'homepage' with your homepage URL name
            else:
                error_message = "Invalid username or password"
    else:
        loginform = LoginForm()
        error_message = ""

    return render(request, 'login/login.html', {'loginform': LoginForm, 'error_message': error_message})


def logout_view(request):
    print('Logout')
    if 'username' in request.session:
        del request.session['username']
    logout(request)
    return redirect('login')


def register_user(request):
    edit_user_id = request.GET.get('editUserId')
    delete_user_id = request.GET.get('deleteUserId')
    user_instance = None

    if delete_user_id:
        user_instance = get_object_or_404(CustomUser, id=delete_user_id)
        user_instance.delete()
        return redirect('/user')

    if edit_user_id:
        user_instance = get_object_or_404(CustomUser, id=edit_user_id)

    if request.method == 'POST':
        user_instance.set_password('password')
        form = CustomUserCreationForm(request.POST, instance=user_instance)
        if form.is_valid():
            user = form.save()
            form = CustomUserCreationForm()
            return redirect('/user')
    else:
        form = CustomUserCreationForm(instance=user_instance)

    users = CustomUser.objects.all()
    return render(request, 'user/user.html', {'form': form, 'list': users})


def delete_user(request, id):
    user_instance = get_object_or_404(CustomUser, id=id)
    user_instance.delete()
    return redirect('/user')


def add_task(request):
    if 'userid' not in request.session:
        return redirect('login')

    assignees = []
    if(request.session['username'] == "admin"):
        admin_user = User.objects.filter(username=request.session['username']).first()
        print(admin_user)
        assignees.append((admin_user.username, admin_user.username))
        users = CustomUser.objects.all()
    else:
        logged_in_user = CustomUser.objects.filter(id=request.session['userid']).first()
        assignees.append((logged_in_user.username, logged_in_user.first_name + ' ' + logged_in_user.last_name))
        users = CustomUser.objects.filter(manager_id=request.session['userid'])

    for user in users:
        assigneeChoice = (user.username, user.first_name + ' ' + user.last_name)
        assignees.append(assigneeChoice)

    priority = []
    prioritychoice1 = ('High', 'High')
    prioritychoice2 = ('Medium', 'Medium')
    prioritychoice3 = ('Low', 'Low')
    priority.append(prioritychoice1)
    priority.append(prioritychoice2)
    priority.append(prioritychoice3)
    if request.method == "POST":
        form = TaskForm(request.POST)
        form.fields['assigned_to'].choices = assignees
        form.fields['priority'].choices = priority

        print(request.POST.get('due_date'))

        user_instance = CustomUser.objects.filter(username=request.POST.get('assigned_to')).first()
        task = TaskModel(
            title=request.POST.get('title'),
            due_date=request.POST.get('due_date'),
            priority=request.POST.get('priority'),
            assigned_to=user_instance
        )
        print(task.due_date)
        task.save()
        return redirect('/addtask')

    else:
        form = TaskForm()
        form.fields['assigned_to'].choices = assignees
        form.fields['priority'].choices = priority

    return render(request, 'task/addtask.html', {'form': form})


def my_task(request):
    if 'userid' not in request.session:
        return redirect('login')

    page_number = 1
    if request.GET.get('page'):
        page_number = request.GET.get('page')

    if (request.session['username'] == "admin"):
        tasks = TaskModel.objects.filter(Q(assigned_to_id=None) & Q(is_completed=False)).order_by('due_date')
    else:
        tasks = TaskModel.objects.filter(Q(assigned_to_id=request.session['userid']) & Q(is_completed=False)).order_by('due_date')

    paginator = Paginator(tasks, 10)
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    if (int(page_number) - 1) > 0 and (int(page_number) - 1) % 5 == 0:
        pagerange = range(int(page_number), int(page_number) + 5)
    else:
        if paginator.num_pages > 5:
            pagerange = range(1, 5)
        else:
            pagerange = range(1, paginator.num_pages + 1)

    page_obj = paginator.get_page(page_number)

    return render(request, 'task/mytasks.html',
                  {'pagerange': pagerange, 'page_obj': page_obj, 'totalitems': len(tasks)})


def delete_task(request, taskid):
    pagenumber = request.GET.get('page')

    task_instance = get_object_or_404(TaskModel, id=taskid)
    task_instance.delete()

    return redirect(f'/mytasks?page={pagenumber}')


def mark_complete(request, taskid):
    pagenumber = request.GET.get('page')

    task_instance = get_object_or_404(TaskModel, id=taskid)
    task_instance.is_completed = True
    task_instance.save()

    return redirect(f'/mytasks?page={pagenumber}')


def start_task(request, taskid):
    pagenumber = request.GET.get('page')

    task_instance = get_object_or_404(TaskModel, id=taskid)
    task_instance.is_in_progress = True
    task_instance.save()

    return redirect(f'/mytasks?page={pagenumber}')


def user_task(request):
    if 'userid' not in request.session:
        return redirect('login')

    selected_user = request.GET.get('user')
    searchForm = SearchForm(initial={'user': selected_user})

    print(selected_user)
    page_number = 1
    if request.GET.get('page'):
        page_number = request.GET.get('page')
    if selected_user is None:
        tasks = []
    else:
        tasks = TaskModel.objects.filter(assigned_to_id=selected_user).order_by('-due_date')

    paginator = Paginator(tasks, 10)
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    if (int(page_number) - 1) > 0 and (int(page_number) - 1) % 5 == 0:
        pagerange = range(int(page_number), int(page_number) + 5)
    else:
        if paginator.num_pages > 5:
            pagerange = range(1, 5)
        else:
            pagerange = range(1, paginator.num_pages + 1)

    page_obj = paginator.get_page(page_number)

    user_choices = []
    if (request.session['username'] == "admin"):
        filetered_users = CustomUser.objects.all()
    else:
        logged_in_user = CustomUser.objects.filter(id=request.session['userid']).first()
        user_choices.append((logged_in_user.id, logged_in_user.first_name + ' ' + logged_in_user.last_name))
        filetered_users = CustomUser.objects.filter(manager_id=request.session['userid'])

    for user in filetered_users:
        choice = (user.id, user.first_name + ' ' + user.last_name)
        user_choices.append(choice)

    searchForm.fields['user'].choices = user_choices

    return render(request, 'task/usertasks.html',
                  {'pagerange': pagerange, 'page_obj': page_obj, 'totalitems': len(tasks), 'searchForm': searchForm})
