from django.shortcuts import render, get_object_or_404, redirect

from django.views import generic

from django.views.generic import DetailView

from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm

from django.contrib.auth.views import PasswordChangeView

from django.urls import reverse_lazy
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import SignUpForm, EditProfileForm

from Ani_blog.models import Profile, Post, FriendRequest, DirectMessage

# Create your views here.

class CreateProfilePageView(generic.CreateView):
    model = Profile
    template_name = 'registration/create_user_profile.html'
    fields = '__all__'
    success_url=reverse_lazy('Home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EditProfilePageView(generic.UpdateView):
    model = Profile
    template_name = 'registration/edit_profile_page.html'
    fields = ['bio', 'profile_pic']
    success_url=reverse_lazy('Home')

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404 (Profile, id=self.kwargs['pk'])
        context["page_user"] = page_user
        context["user_posts"] = Post.objects.filter(author=page_user.user).order_by('-post_date', '-id')

        is_friend = False
        pending_sent = None
        pending_received = None

        if self.request.user.is_authenticated and self.request.user != page_user.user:
            is_friend = FriendRequest.objects.filter(
                Q(sender=self.request.user, receiver=page_user.user, status='accepted') |
                Q(sender=page_user.user, receiver=self.request.user, status='accepted')
            ).exists()

            pending_sent = FriendRequest.objects.filter(
                sender=self.request.user,
                receiver=page_user.user,
                status='pending'
            ).first()

            pending_received = FriendRequest.objects.filter(
                sender=page_user.user,
                receiver=self.request.user,
                status='pending'
            ).first()

        context["is_friend"] = is_friend
        context["pending_sent"] = pending_sent
        context["pending_received"] = pending_received
        return context


def my_profile_redirect(request):
    if not request.user.is_authenticated:
        return redirect('login')

    profile = Profile.objects.filter(user=request.user).first()
    if profile:
        return redirect('show_profile_page', pk=profile.id)

    return redirect('create_profile_page')


@login_required
def send_friend_request(request, user_id):
    if request.method != 'POST':
        return redirect('Home')

    target_user = get_object_or_404(User, id=user_id)

    if target_user == request.user:
        messages.warning(request, "You can't send a friend request to yourself.")
        return redirect('my_profile')

    already_friends = FriendRequest.objects.filter(
        Q(sender=request.user, receiver=target_user, status='accepted') |
        Q(sender=target_user, receiver=request.user, status='accepted')
    ).exists()

    if already_friends:
        messages.info(request, 'You are already friends.')
        return redirect_back_to_profile(target_user)

    existing_outgoing = FriendRequest.objects.filter(sender=request.user, receiver=target_user).first()
    if existing_outgoing:
        if existing_outgoing.status == 'pending':
            messages.info(request, 'Friend request already sent.')
            return redirect_back_to_profile(target_user)

        existing_outgoing.status = 'pending'
        existing_outgoing.responded_on = None
        existing_outgoing.save(update_fields=['status', 'responded_on'])
        messages.success(request, 'Friend request sent.')
        return redirect_back_to_profile(target_user)

    existing_incoming = FriendRequest.objects.filter(sender=target_user, receiver=request.user).first()
    if existing_incoming and existing_incoming.status == 'pending':
        messages.info(request, 'This user already sent you a request. You can accept it.')
        return redirect('friend_requests')

    FriendRequest.objects.create(sender=request.user, receiver=target_user, status='pending')
    messages.success(request, 'Friend request sent.')
    return redirect_back_to_profile(target_user)


@login_required
def accept_friend_request(request, request_id):
    if request.method != 'POST':
        return redirect('friend_requests')

    friend_request = get_object_or_404(
        FriendRequest,
        id=request_id,
        receiver=request.user,
        status='pending'
    )

    friend_request.status = 'accepted'
    friend_request.responded_on = timezone.now()
    friend_request.save(update_fields=['status', 'responded_on'])

    messages.success(request, f'You are now friends with {friend_request.sender.username}.')
    return redirect('friend_requests')


@login_required
def friend_requests_view(request):
    incoming_requests = FriendRequest.objects.filter(
        receiver=request.user,
        status='pending'
    ).select_related('sender')

    sent_requests = FriendRequest.objects.filter(
        sender=request.user,
        status='pending'
    ).select_related('receiver')

    friends = User.objects.filter(
        Q(sent_friend_requests__receiver=request.user, sent_friend_requests__status='accepted') |
        Q(received_friend_requests__sender=request.user, received_friend_requests__status='accepted')
    ).distinct().order_by('username')

    return render(
        request,
        'registration/friend_requests.html',
        {
            'incoming_requests': incoming_requests,
            'sent_requests': sent_requests,
            'friends': friends,
        }
    )


def redirect_back_to_profile(user):
    target_profile = Profile.objects.filter(user=user).first()
    if target_profile:
        return redirect('show_profile_page', pk=target_profile.id)
    return redirect('Home')


@login_required
def send_direct_message(request, user_id):
    if request.method != 'POST':
        return redirect('Home')

    receiver = get_object_or_404(User, id=user_id)
    next_url = request.POST.get('next', reverse('Home'))

    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = reverse('Home')

    if receiver == request.user:
        return redirect(next_url)

    are_friends = FriendRequest.objects.filter(
        Q(sender=request.user, receiver=receiver, status='accepted') |
        Q(sender=receiver, receiver=request.user, status='accepted')
    ).exists()

    if not are_friends:
        messages.warning(request, 'You can only chat with friends.')
        return redirect(next_url)

    message_body = request.POST.get('message', '').strip()
    if message_body:
        DirectMessage.objects.create(
            sender=request.user,
            receiver=receiver,
            body=message_body,
        )

    return redirect(next_url)


@login_required
def chat_conversation_view(request, user_id):
    friend = get_object_or_404(User, id=user_id)

    are_friends = FriendRequest.objects.filter(
        Q(sender=request.user, receiver=friend, status='accepted') |
        Q(sender=friend, receiver=request.user, status='accepted')
    ).exists()

    if not are_friends:
        messages.warning(request, 'You can only chat with friends.')
        return redirect('friend_requests')

    chat_messages = DirectMessage.objects.filter(
        Q(sender=request.user, receiver=friend) |
        Q(sender=friend, receiver=request.user)
    ).select_related('sender').order_by('created_on')

    return render(
        request,
        'registration/chat_conversation.html',
        {
            'chat_friend': friend,
            'chat_messages': chat_messages,
        }
    )
    

class PasswordsChangeView(PasswordChangeView):
    form_class= PasswordChangeForm
    success_url=reverse_lazy('home')




class UserRegistrationView(generic.CreateView):
    form_class= SignUpForm
    template_name='registration/register.html'
    success_url=reverse_lazy('login')
class UserEditView(generic.UpdateView):
    form_class= EditProfileForm
    template_name='registration/edit_profile.html'
    success_url=reverse_lazy('Home')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)

        # Save profile picture if provided
        profile_pic = form.cleaned_data.get('profile_pic')
        if profile_pic:
            profile = Profile.objects.filter(user=self.request.user).first()
            if profile:
                profile.profile_pic = profile_pic
                profile.save()

        return response