from django import forms

from blog.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'status', 'image_url')
        labels = {
            'title': 'Post title',
            'body': 'Post content',
            'status': 'Post status',
            'image_url': 'Url to image post'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control border border-4 rounded-pill',
                                            'placeholder': 'Enter the title'}),
            'body': forms.Textarea(attrs={'class': 'form-control border border-4',
                                          'placeholder': 'Enter the post content'}),
            'status': forms.Select(attrs={'class': 'form-control border border-4 rounded-pill'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control border border-4 rounded-pill',
                                               'placeholder': 'Enter the image post URL'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

        labels = {'body': 'Add a note'}
        widgets = {
            'body': forms.TextInput(attrs={'max_length': 255,
                                           'class': 'form-control border border-4',
                                           'placeholder': 'Type your comment here...'})}






