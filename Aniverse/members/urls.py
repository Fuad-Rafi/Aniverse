from django.urls import path

from .views import UserRegistrationView, UserEditView, PasswordsChangeView , ShowProfilePageView ,EditProfilePageView , CreateProfilePageView, my_profile_redirect, send_friend_request, accept_friend_request, friend_requests_view, send_direct_message, chat_conversation_view

from django.contrib.auth import views as auth_views



urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name="register"),
    path('edit_profile/', UserEditView.as_view(), name="edit_profile"),
    path('my_profile/', my_profile_redirect, name='my_profile'),
    path('friend-requests/', friend_requests_view, name='friend_requests'),
    path('friend-request/send/<int:user_id>/', send_friend_request, name='send_friend_request'),
    path('friend-request/accept/<int:request_id>/', accept_friend_request, name='accept_friend_request'),
    path('chat/<int:user_id>/', chat_conversation_view, name='chat_conversation'),
    path('chat/send/<int:user_id>/', send_direct_message, name='send_direct_message'),
    path('members/password/', PasswordsChangeView.as_view(template_name="registration/change-password.html")),
    # path('password/', auth_views.PasswordChangeView.as_view()),
    path("<int:pk>/profile", ShowProfilePageView.as_view(), name='show_profile_page'),
    path("<int:pk>/edit_profile_page", EditProfilePageView.as_view(), name='edit_profile_page'),
    path("create_profile_page", CreateProfilePageView.as_view(), name='create_profile_page'),
      
    
]
