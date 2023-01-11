from django import forms
from cart.models import OrderConfirm


class FormOrder(forms.ModelForm):
    first_name = forms.CharField(max_length=200, label = "Họ", widget = forms.TextInput(attrs = {
        'class': 'form-control',
        'placeholder': 'Họ',
    }))
    last_name = forms.CharField(max_length=200, label = "Tên", widget = forms.TextInput(attrs = {
        'class': 'form-control',
        'placeholder': 'Tên',
    }))

    address = forms.CharField(label = "Địa chỉ", widget = forms.Textarea(attrs = {
        'class': 'form-control',
        'placeholder': 'Địa chỉ',
        'rows': '1',
    }))
    email = forms.EmailField(label = "Email", widget = forms.EmailInput(attrs = {
        'class': 'form-control',
        'placeholder': 'E-mail',
    }))
    tel = forms.CharField(max_length=15, label = "Điện thoại", widget = forms.TextInput(attrs = {
        'class': 'form-control',
        'placeholder': 'Điện thoại',
    }))

    class Meta:
        model = OrderConfirm
        fields = '__all__'