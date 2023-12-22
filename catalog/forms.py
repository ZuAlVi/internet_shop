from django import forms

from catalog.models import Product, Version


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('user',)

    def clean_product_name(self):
        cleaned_data = self.cleaned_data.get('product_name')
        censored = ['казино',
                    'криптовалюта',
                    'крипта',
                    'биржа',
                    'дешево',
                    'бесплатно',
                    'обман',
                    'полиция',
                    'радар'
                    ]

        for word in censored:
            if word in cleaned_data:
                raise forms.ValidationError('Не допустимое слово!')

        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')
        censored = ['казино',
                    'криптовалюта',
                    'крипта',
                    'биржа',
                    'дешево',
                    'бесплатно',
                    'обман',
                    'полиция',
                    'радар'
                    ]

        for word in censored:
            if word in cleaned_data:
                raise forms.ValidationError(f'Не допустимое слово - {word}!')

        return cleaned_data


class VersionForm(forms.ModelForm):

    class Meta:
        model = Version
        fields = '__all__'
