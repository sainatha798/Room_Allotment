from django import forms

class RoomEntry(forms.Form):
    mail_id = forms.EmailField(required=True,widget=forms.EmailInput)