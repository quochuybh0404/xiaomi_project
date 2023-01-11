from django import forms
from customer.models import Customer


class FormSignUp(forms.ModelForm):
    first_name = forms.CharField(max_length=200, label = "Họ", widget = forms.TextInput(attrs = {
        'class': 'form-control',
        'placeholder': 'Họ',
    }))
    last_name = forms.CharField(max_length=200, label = "Tên", widget = forms.TextInput(attrs = {
        'class': 'form-control',
        'placeholder': 'Tên',
    }))
    email = forms.EmailField(label = "Email", widget = forms.EmailInput(attrs = {
        'class': 'form-control',
        'placeholder': 'E-mail',
    }))
    tel = forms.CharField(max_length=15, label = "Điện thoại", widget = forms.TextInput(attrs = {
        'class': 'form-control',
        'placeholder': 'Điện thoại',
    }))
    password = forms.CharField(max_length=100, label = "Mật khẩu", widget = forms.PasswordInput(attrs = {
        'class': 'form-control',
        'placeholder': 'Mật khẩu',
    }))
    confirm_password = forms.CharField(max_length=100, label = "Xác nhận mật khẩu", widget = forms.PasswordInput(attrs = {
        'class': 'form-control',
        'placeholder': 'Xác nhận mật khẩu',
    }))
    address = forms.CharField(label = "Địa chỉ", widget = forms.Textarea(attrs = {
        'class': 'form-control',
        'placeholder': 'Địa chỉ',
        'rows': '3',
    }))
    province = forms.CharField(label = "Tỉnh/TP", widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    district = forms.CharField(label = "Quận/Huyện", widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    ward = forms.CharField(label = "Phường/Xã", widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    class Meta:
        model = Customer
        fields = '__all__'

