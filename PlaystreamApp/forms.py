from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Movie, Series, Season, Episode ,UserProfile,MovieReview



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password')

    def clean_username(self):
        # Get the cleaned username from the form
        username = self.cleaned_data.get('username')

        # Check if a user with the same username already exists
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')

        return username

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match')
        return cd['password2']




class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'email')



class ContentCreatorRegistrationForm(forms.ModelForm):
    #the only check we have to do is to compare passwords
    #Creating a Charfield object by passing values into the constructor
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    password2 =  forms.CharField(label="Confirm Password",widget=forms.PasswordInput)

    class Meta:
        #in ,eta class, we specify which model the form is far and the fields
        model = User
        fields = ('username' , 'first_name' ,'email' , 'password')

    #naming convention is clean < field_name
    def clean_password2(self):
        #clean the data in the context
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password not Matching')

        return cd['password2']


class CustomLoginForm(AuthenticationForm):
    # Add additional fields or customize existing ones if needed
    # For example, if you want to add a "Remember me" checkbox:
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'genre', 'post_image', 'youtube_link', 'description']

class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = ['title', 'genre', 'description', 'poster_image', 'youtube_link']

class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ['season_number']

class EpisodeForm(forms.ModelForm):
    class Meta:
        model = Episode
        fields = ['episode_number', 'title', 'description', 'youtube_link']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_photo', 'date_of_birth']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'email']


class MovieReviewForm(forms.ModelForm):
    class Meta:
        model = MovieReview
        fields = ['rating', 'review_text']
        widgets = {
            'review_text': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super(MovieReviewForm, self).__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({'class': 'form-control'})
        self.fields['review_text'].widget.attrs.update({'class': 'form-control'})