from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Comment
from accounts.models import User, Student


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'image']

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # self.fields["image"].required = False
        # self.fields["text"].required = False
        self.fields["image"].widget.attrs.update({"id": "image_field"})
        self.fields["text"].widget.attrs.update({"id": "description_field"})

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        image = cleaned_data.get("image")
        print(text, image, '//////////////////////')

        if text == '' and image is None:
            raise ValidationError("D")

#
# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['comment', 'post']
#
#     def __init__(self, *args, **kwargs) -> None:
#         super().__init__(*args, **kwargs)
#         self.fields["comment"].required = False
#         self.fields["post"].required = False
#
#         self.fields["comment"].widget.attrs.update({"id": "comment_field"})
#         self.fields["post"].widget.attrs.update({"value": "{{ po }}"})


class ProfileUpdateForm1(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']


class ProfileUpdateForm2(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['location', 'birth_date', 'admission_num', 'batch_num']


class ProfileBgForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['background_img']
