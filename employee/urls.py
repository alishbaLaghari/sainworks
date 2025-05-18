from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from employee import views

urlpatterns = [
    path('employee_login/', views.employee, name="employee"),
    path('add_employee/', views.add_employee, name="add_employee"),
    path('employee_details/', views.employee_details, name="employee_details"),
    path('delete_employee/<int:id>/', views.delete_employee, name="delete_employee"),
    path('update_employee/<int:id>/', views.update_employee, name="update_employee"),
    path('p_dashboard/<str:username>/', views.p_dashboard, name="p_dashboard"),
    path('employee_profile/<str:username>/', views.update_employee_profile, name='update_employee_profile'),
    path('projects/<str:username>/', views.project_list, name='project_list'),
    path('comments/<str:username>/', views.add_comment, name='comments'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
