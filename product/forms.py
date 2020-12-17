from django import forms
from .models import Product, Tag


class ProductCreateForm(forms.ModelForm):
    more_images = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={
        "class": "form-control",
        "multiple": True
    }))

    tags = forms.ModelMultipleChoiceField(queryset= Tag.objects.all(), required=False)

    class Meta:
        model = Product
        fields = ['category', 'title', 'price', 'description', 'image', 'video', 'discount_price',
                    'season_choice', 'is_namuna_falful']

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the product title here..."
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Price of the product..."
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Description of the product...",
                "rows": 5,
                'style': 'resize:none'
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "video": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "discount_price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Discount price of the product..."
            }),
            "season_choice": forms.Select(attrs={
                "class": "form-control"
            }),
        }
