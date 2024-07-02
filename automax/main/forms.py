from django import forms

from .models import Listing
from users.widgets import CustomPictureImageFieldWidget

class ListingForm(forms.ModelForm):
    image = forms.ImageField(widget=CustomPictureImageFieldWidget)

    class Meta:
        model = Listing
        fields = ['brand', 'model', 'vin', 'mileage',
                  'color', 'description', 'engine', 'transmisson', 'image']