from django.shortcuts import render,get_object_or_404, HttpResponse

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post, Category, Profile

from .form import PostForm, EditForm

from django.urls import reverse_lazy, reverse

from django.http import HttpResponseRedirect

from django.contrib import messages

from django.db.models import Value as V

from django.db.models.functions import Concat
#just regular functional view enough for that

def LikeView(request, pk): # Pk is the primary key of the post itself, request contains persons userid if they are logged in
    
    post = get_object_or_404(Post, id=request.POST.get('post_id')) # present in post.details button of like, Post = DB table
    liked = False
    if post.likes.filter(id=request.user.id).exists(): #request.user.id is the id of the user if they have click the like button or not if they have clicked the like button then the request.user.id will have the id of the user and the condition will be satisfied.
        
        post.likes.remove(request.user) # Removing request as they have already clicked like button now clicking twice
        liked = False
    else:
        post.likes.add(request.user) # Saving the likes to a table after finding and assigning to the post variable
        liked = True
    
    
    return HttpResponseRedirect(reverse("post_details", args=[str(pk)])) # Here we are also paasing exact id, in args,  we want to know exactly what blog post or post.detail we are returning/reversing too

class Homeview(ListView):
    model=Post
    template_name='home.html'
    ordering=['-post_date']
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(Homeview, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context



def CategoryListView(request):
    cat_menu_list = Category.objects.all()
    return render(request, 'category_list.html', {'cat_menu_list': cat_menu_list})



def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats.replace('-', ' '))
    return render(request, 'categories.html', {'cats': cats.title().replace('-', ' '), 'category_posts':category_posts})



def SearchView(request):
    query=request.GET['searching']
    # post=Post.objects.order_by("-post_date")
    
    if len(query)<1:
        return render(request, 'search.html', {'error': True})

    if len(query)>50: #for acheiving protection against large query sets 
        allPosts= Post.objects.none()    
    else:    
        allPostsTitle= Post.objects.filter(title__icontains=query) 
        allPostsContents= Post.objects.filter(body__icontains=query)
        allPostsAuthor= Post.objects.filter(author__username__icontains=query)
        fname=Post.objects.filter(author__first_name__icontains=query)   
        lname=Post.objects.filter(author__last_name__icontains=query)    
        allPostsCategory= Post.objects.filter(category__icontains=query)
        allPostsSnippet= Post.objects.filter(snippet__icontains=query)
        allPosts= allPostsTitle.union(allPostsContents, allPostsCategory, allPostsSnippet, allPostsAuthor, fname, lname)


    # if allPosts.count()==0:
    #     messages.warning(request, 'Please fill the form correctly')  

    return render(request, 'search.html', {'allPosts': allPosts, 'query': query, }) 




class postDetailview(DetailView):
    model=Post
    template_name='post.details.html'

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(postDetailview, self).get_context_data(*args, **kwargs)

        stuff= get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        liked = False

        if stuff.likes.filter(id=self.request.user.id).exists(): #Similar to LikeView method
            liked = True


        context["cat_menu"] = cat_menu
        context["total_likes"] = total_likes  # Basically the variables inside are passed through context
        context["liked"] = liked              # Now we can use this liked variable on our actual html page
        return context    

class postAddview(CreateView):
    model=Post
    form_class=PostForm
    template_name='post_add.html'
    # fields=('__all__')
    # fields=('Title', 'Body')
class categoryAddview(CreateView):
    model= Category
    #form_class=PostForm
    template_name='category_add.html'
    fields='__all__'
    # fields=('Title', 'Body')

class postUpdateview(UpdateView):
    model=Post
    form_class=EditForm
    template_name='update_post.html'

class postDeleteview(DeleteView):
    model=Post
    template_name='delete_post.html'
    success_url=reverse_lazy('Home')
   