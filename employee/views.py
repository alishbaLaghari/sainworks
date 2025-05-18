from django.contrib import messages
from django.forms import ValidationError
from django.shortcuts import render,redirect
from .models import AddEmployee
from django.http import HttpResponse
from .models import AddEmployee
from .models import AddEmployee,EmployeeLogin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import EmployeeProfileUpdateForm
from manager.models import Project,TeamMemberTask
from manager.models import comment 




def employee(request):
    if request.method == 'POST':
        username = request.POST.get('login_employee_name')
        password = request.POST.get('login_employee_password')

        try:
            employee = AddEmployee.objects.get(add_employee_username=username)
            if employee.add_employee_password == password:
                employee_login, created = EmployeeLogin.objects.get_or_create(employee_login_username=username, employee_login_password=password)
                return redirect('update_employee_profile', username=username)
            else:
                return render(request, 'employee.signin.html', {'error': 'Password is incorrect'})
        except AddEmployee.DoesNotExist:
            return render(request, 'employee.signin.html', {'error': 'Username is incorrect'})
        except AddEmployee.MultipleObjectsReturned:
            messages.error(request, 'Multiple users found with the same username. Contact administrator.')
            return render(request, 'employee.signin.html')
    else:
        return render(request, 'employee.signin.html')

def update_employee_profile(request, username):
    employee_login = get_object_or_404(EmployeeLogin, employee_login_username=username)

    if request.method == 'POST':
        form = EmployeeProfileUpdateForm(request.POST, request.FILES, instance=employee_login)
        if form.is_valid():
            if 'new_profile_picture' in request.FILES:
                employee_login.profile_picture = form.cleaned_data['new_profile_picture']
            form.save()
            return HttpResponse("Profile updated successfully")
    else:
        form = EmployeeProfileUpdateForm(instance=employee_login)

    return render(request, 'update_employee_profile.html', {'form': form, 'username': username})


def employee_details(request):
    employees = AddEmployee.objects.all()
    context = {
        'employees': employees,
    }
    return render(request, 'employee_details.html', context)
    


def p_dashboard(request,username):
    return render(request,'p-dashboard.html',{'username':username})


def add_employee(request):
    if request.method == 'POST':
        email = request.POST.get('add_employee_email')
        username = request.POST.get('add_employee_username')
        password = request.POST.get('add_employee_password')
        
        employee = AddEmployee(add_employee_email=email, add_employee_username=username, add_employee_password=password)
        employee.save()
        return redirect('/employee/employee_details')  # Redirect to the same page or any other page as needed

    return render(request, 'add_employee.html')



def delete_employee(request, id):
    employee = get_object_or_404(AddEmployee, pk=id)
    employee.delete()
    return redirect('employee_details')


def update_employee(request, id):
    # Retrieve the employee object corresponding to the provided ID
    employee = get_object_or_404(AddEmployee, pk=id)

    if request.method == 'POST':
        # Logic for updating employee details goes here
        # Retrieve updated details from the form and update the employee object

        # For demonstration purposes, let's assume we retrieve the updated details from the form
        updated_email = request.POST.get('update_employee_email')
        updated_username = request.POST.get('update_employee_username')
        updated_password = request.POST.get('update_employee_password')

        # Update the employee object with the new details
        employee.add_employee_email = updated_email
        employee.add_employee_username = updated_username
        employee.add_employee_password = updated_password

        # Save the updated employee object
        employee.save()

        # Redirect to a success page or wherever appropriate
        # For now, let's redirect to the employee details page
        return redirect('/employee/employee_details')

    # If the request method is GET, render the update_employee.html template with the employee details
    return render(request, 'update_employee.html', {'employee': employee})

def project_list(request,username):
    projects = Project.objects.all()
    tasks = TeamMemberTask.objects.all()
    return render(request, 'p-team.html', {'projects': projects, 'tasks': tasks,'username': username})

def add_comment(request, project_id):
    if request.method == 'POST':
        project = Project.objects.get(id=project_id)
        comment_text = request.POST.get('comment')
        if comment_text:
            comment.objects.create(project=project, comment=comment_text)
        return redirect('comments')
    else:
        return HttpResponse(status=405)  # 