from django import forms
from .models import Comment ,Post,Category
from django.contrib.auth.models import User


    # print(item)

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

# post form 
class PostForm(forms.ModelForm):
    # category= forms.Select(choices =choice_list,attrs={'class':'form-control'})
    
    class Meta:
        model = Post
        choice = Category.objects.all().values_list('name','name')
        choice_list = []
        for item in choice:
            choice_list.append(item)
        fields =('title','slug','author','body','category','status','tags')
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'slug':forms.TextInput(attrs={'class':'form-control'}),
            'author':forms.TextInput(attrs={'class':'form-control','value':'','id':'elder','type':'hidden'}),
            # 'author': forms.Select(attrs={'class':'form-control'}),
            'body':forms.Textarea(attrs={'rows': 5, 'cols': 100}),
            'category':forms.Select(choices =choice_list,attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            'tags':forms.TextInput(attrs={'class':'form-control'})
            
        }




class SearchForm(forms.Form):
    query = forms.CharField()

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')




