from django.urls import path
# from . import views 
from .views import Homeview, postDetailview, postAddview, postUpdateview, postDeleteview, categoryAddview, CategoryView, CategoryListView, LikeView, SearchView





urlpatterns = [
    # path('', views.home, name='home'),
    path('', Homeview.as_view(), name='Home'), 
    path('post/<int:pk>', postDetailview.as_view(), name="post_details"),
    path('add_post/', postAddview.as_view(), name='add_post'),
    path('add_category/', categoryAddview.as_view(), name='add_category'),
    path('post/edit/<int:pk>',postUpdateview.as_view(), name='update_post'),
    path('post/<int:pk>/remove',postDeleteview.as_view(), name='delete_post'),
    path('category/<str:cats>/',CategoryView, name='category' ),
    path('category-list/',CategoryListView, name='category-list' ),
    path('like/<int:pk>', LikeView, name='like_post'),
    path('search', SearchView, name='search'),
    # path('admin', )
    
]
