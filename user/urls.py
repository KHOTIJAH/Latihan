from django.contrib.auth import views
from django.urls import path
from .views import signup

urlpatterns = [
	path('signup/', signup, name= 'signup'),
	path('login/', views.LoginView.as_view(template_name= 'user/login.html'), name= 'login'),
	path('logout/', views.LogoutView.as_view(), name= 'logout'),
	path('reset/', views.PasswordResetView.as_view(
		template_name= 'user/password_reset.html',
		email_template_name= 'user/password_reset_email.html',
		subject_template_name= 'user/password_reset_subject.txt'
	), name= 'password_reset'),
	path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), name='password_reset_confirm'),
	path('reset/done/', views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name= 'password_reset_done'),
	path('reset/complete/', views.PasswordResetDoneView.as_view(template_name='user/password_reset_complete.html'), name= 'password_reset_complete'),
	path('settings/password/', views.PasswordChangeView.as_view(template_name= 'user/password_change.html'), name= 'password_change'),
	path('settings/password/done', views.PasswordChangeDoneView.as_view(template_name= 'user/password_change_done.html'), name='password_change_done'),

]