from django.db.models import Q
from django.contrib.auth.models import User

from Ani_blog.models import FriendRequest


def chat_sidebar_context(request):
    if not request.user.is_authenticated:
        return {
            'chat_friends': [],
            'active_chat_user': None,
        }

    chat_friends = User.objects.filter(
        Q(sent_friend_requests__receiver=request.user, sent_friend_requests__status='accepted') |
        Q(received_friend_requests__sender=request.user, received_friend_requests__status='accepted')
    ).distinct().order_by('username')

    active_chat_user = None
    chat_user_id = None

    if request.resolver_match:
        chat_user_id = request.resolver_match.kwargs.get('user_id')

    if not chat_user_id:
        chat_user_id = request.GET.get('chat_with')

    if chat_user_id:
        try:
            active_chat_user_id = int(chat_user_id)
            active_chat_user = chat_friends.filter(id=active_chat_user_id).first()
        except ValueError:
            active_chat_user = None

    return {
        'chat_friends': chat_friends,
        'active_chat_user': active_chat_user,
    }
