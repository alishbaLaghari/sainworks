from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('BD_login/', views.BD, name="BD"),
    path('add_BD/', views.add_BD, name="add_BD"),
    path('BD_details/', views.BD_details, name="BD_details"),
    path('delete_BD/<int:id>/', views.delete_BD, name="delete_BD"),
    path('update_BD/<int:id>/', views.update_BD, name="update_BD"),
    path('BD_dashboard/<str:username>/', views.BD_dashboard, name="BD_dashboard"),
    path('BD_chat/<str:username>/', views.save_BD_msg, name='save_BD_msg'),
    path('BD_profile/<str:username>/', views.update_BD_profile, name='update_BD_profile'),
    path('client/list/', views.client_list, name='client_list'),
    path('BD_submission/<str:username>/', views.submission, name='submission'),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
