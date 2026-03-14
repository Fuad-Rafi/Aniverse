from django import forms

from .models import Post, Category, Comment


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.choices = Category.objects.values_list('name', 'name')

    class Meta:
        model=Post
        fields=('title', 'title_tag', 'author', 'category' , 'body', 'snippet', 'header_image')

        widgets={
            'title':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tell a interesting story'}),
            'title_tag':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apply a meaningful tag'}), 
            'author':forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id':'number', 'type':'hidden'}),## hidden
            # 'author':forms.Select(attrs={'class': 'form-control', }),
            'category': forms.Select(attrs={'class': 'form-control', }),
            'body':forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Open your heart out!'}), 
            'snippet':forms.Textarea(attrs={'class': 'form-control'}),

        }

class EditForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=('title', 'title_tag', 'body','snippet')

        widgets={
            'title':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name a Interesting Title!'}), 
            'title_tag':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apply a meaningful tag'}), 
            'body':forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Open your heart out!'}),
            'snippet':forms.Textarea(attrs={'class': 'form-control'}),  

        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your comment...', 'rows': 3}),
        }