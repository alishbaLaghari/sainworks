
# Create your views here.
from django.contrib import messages
from django.forms import ValidationError
from django.shortcuts import render,redirect
from .models import AddBD
from django.http import HttpResponse
from .models import AddBD
from .models import AddBD,BDLogin
from myapp.models import ClientLogin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import BDProfileUpdateForm
import pyrebase
import os
import logging
from IPython.display import Image,display
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import BDLogin
import mimetypes

# Initialize Firebase configuration
config = {
    "apiKey": "AIzaSyAq4vehCBQNKeTfBIhfZrebQ40HUCTMl9k",
    "authDomain": "fir-3f7df.firebaseapp.com",
    "projectId": "fir-3f7df",
    "storageBucket": "fir-3f7df.appspot.com",
    "messagingSenderId": "538585929662",
    "appId": "1:538585929662:web:44525d079b83783f6dcbef",
    "databaseURL": "https://fir-3f7df-default-rtdb.firebaseio.com",
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()
storage = firebase.storage()

import logging
logger = logging.getLogger(__name__)

def save_BD_msg(request, username):
    # Fetch BDLogin object based on username
    BD_login = get_object_or_404(BDLogin, BD_login_username=username)
    username_fb = username  # Use the Django username as Firebase username

    if request.method == 'POST':
        BD_msg = request.POST.get('BD_msg')
        BD_file = request.FILES.get('BD_file')

        if BD_msg:
            # Save message to Firebase database
            data = {"message": BD_msg, "username_fb": username_fb}
            database.child('messages').push(data)

        if BD_file:
            try:
                # Ensure the 'uploads' directory exists
                upload_dir = 'uploads'
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)

                # Save file to local storage temporarily
                file_name = BD_file.name
                file_path = os.path.join(upload_dir, file_name)
                with open(file_path, 'wb+') as destination:
                    for chunk in BD_file.chunks():
                        destination.write(chunk)

                # Upload file to Firebase storage
                storage.child(f"files/{file_name}").put(file_path)

                # Get the file URL from Firebase Storage
                file_url = storage.child(f"files/{file_name}").get_url(None)

                # Determine the file type
                file_type, _ = mimetypes.guess_type(file_name)
                is_image = file_type and file_type.startswith('image')

                # Save file info to Firebase database
                data = {
                    "file": {
                        'url': file_url,
                        'is_image': is_image,
                        'name': file_name
                    },
                    "username_fb": username_fb
                }
                database.child('messages').push(data)

                # Clean up the temporary file saved locally
                if os.path.exists(file_path):
                    os.remove(file_path)

                logger.info(f"File {file_name} uploaded successfully")
            except Exception as e:
                logger.error(f"Error uploading file: {e}")
                return JsonResponse({'status': 'error', 'message': f"Error uploading file: {e}"}, status=500)

        return JsonResponse({'status': 'success', 'message': 'Message and file uploaded successfully.'})

    # Handle GET requests or non-AJAX POST requests
    all_messages = database.child('messages').get().val()
    messages_list = [{'key': key, 'data': val} for key, val in all_messages.items()] if all_messages else []

    return render(request, 'bd.chat.html', {'messages_list': messages_list, 'username': username, 'username_fb': username_fb})

def submission(request, username):
    return render(request,'bd-submission.html',{'username': username})




def client_list(request):
    clients = ClientLogin.objects.all()
    return render(request, 'bd.chat.html', {'clients': clients})

def BD(request):
    if request.method == 'POST':
        username = request.POST.get('login_BD_name')
        password = request.POST.get('login_BD_password')

        try:
            employee = AddBD.objects.get(add_BD_username=username)
            if employee.add_BD_password == password:
                BD_login, created = BDLogin.objects.get_or_create(BD_login_username=username, BD_login_password=password)
                return redirect('update_BD_profile', username=username)
            else:
                return render(request, 'BD.signin.html', {'error': 'Password is incorrect'})
        except AddBD.DoesNotExist:
            return render(request, 'BD.signin.html', {'error': 'Username is incorrect'})
        except AddBD.MultipleObjectsReturned:
            messages.error(request, 'Multiple users found with the same username. Contact administrator.')
            return render(request, 'BD.signin.html')
    else:
        return render(request, 'BD.signin.html')

def update_BD_profile(request, username):
    BD_login = get_object_or_404(BDLogin, BD_login_username=username)

    if request.method == 'POST':
        form = BDProfileUpdateForm(request.POST, request.FILES, instance=BD_login)
        if form.is_valid():
            if 'new_profile_picture' in request.FILES:
                BD_login.profile_picture = form.cleaned_data['new_profile_picture']
            form.save()
            return HttpResponse("Profile updated successfully")
    else:
        form = BDProfileUpdateForm(instance=BD_login)

    return render(request, 'update_BD_profile.html', {'form': form, 'username': username})


def BD_details(request):
    BDs = AddBD.objects.all()  # Replace 'BD' with the actual model name
    context = {'BDs': BDs}
    return render(request, 'BD_details.html', context)

def BD_dashboard(request, username):
    BD_login = get_object_or_404(BDLogin, BD_login_username=username)
    return render(request, 'bd-dashboard.html', {'username': username})


def add_BD(request):
    if request.method == 'POST':
        email = request.POST.get('add_BD_email')
        username = request.POST.get('add_BD_username')
        password = request.POST.get('add_BD_password')
        
        BD = AddBD(add_BD_email=email, add_BD_username=username, add_BD_password=password)
        BD.save()
        return redirect('/BD/BD_details')  # Redirect to the same page or any other page as needed

    return render(request, 'add_BD.html')




def delete_BD(request, id):
    BD = get_object_or_404(AddBD, pk=id)
    BD.delete()
    return redirect('BD_details')


def update_BD(request, id):
    # Retrieve the employee object corresponding to the provided ID
    BD= get_object_or_404(AddBD, pk=id)

    if request.method == 'POST':
        # Logic for updating employee details goes here
        # Retrieve updated details from the form and update the employee object

        # For demonstration purposes, let's assume we retrieve the updated details from the form
        updated_email = request.POST.get('update_BD_email')
        updated_username = request.POST.get('update_BD_username')
        updated_password = request.POST.get('update_BD_password')

        # Update the employee object with the new details
        BD.add_BD_email = updated_email
        BD.add_BD_username = updated_username
        BD.add_BD_password = updated_password
        

        # Save the updated employee object
        BD.save()

        # Redirect to a success page or wherever appropriate
        # For now, let's redirect to the employee details page
        return redirect('/BD/BD_details')

    # If the request method is GET, render the update_employee.html template with the employee details
    return render(request, 'update_BD.html', {'BD': BD})





