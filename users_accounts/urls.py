from django.urls import path

from users_accounts import views


app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('activate/<str:token>/<int:user_id>', views.ActivateAccountView.as_view(), name='activate'),
    path('reactivation_sent/', views.ReactivationSentView.as_view(), name='reactivation_sent'),
]