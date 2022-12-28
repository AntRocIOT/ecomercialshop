# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe


PROVINCES = (
	('', 'Provincia...'),
    ('a coruña', 'A Coruña'),
    ('alava', 'Álava'),
    ('alicante', 'Alicante'),
    ('almeria', 'Almería'),
    ('asturias', 'Asturias'),
    ('avila', 'Ávila'),
    ('badajoz', 'Badajoz'),
    ('baleares', 'Baleares'),
    ('barcelona', 'Barcelona'),
    ('burgos', 'Burgos'),
    ('caceres', 'Cáceres'),
    ('cadiz', 'Cádiz'),
    ('cantabria', 'Cantabria'),
    ('castellon', 'Castellón'),
    ('ceuta', 'Ceuta'),
    ('ciudad real', 'Ciudad Real'),
    ('cordoba', 'Córdoba'),
    ('cuanca', 'Cuenca'),
    ('extranjero', 'Extranjero'),
    ('girona', 'Girona'),
    ('granada', 'Granada'),
    ('guadalajara', 'Guadalajara'),
    ('guipuzcoa', 'Guipúzcoa'),
    ('huelva', 'Huelva'),
    ('huesca', 'Huesca'),
    ('jaen', 'Jaén'),
    ('la rioja', 'La rioja'),
    ('las palmas', 'Las palmas'),
    ('leon', 'León'),
    ('lleida', 'Lleida'),
    ('lugo', 'Lugo'),
    ('madrid', 'Madrid'),
    ('malaga', 'Málaga'),
    ('melilla', 'Melilla'),
    ('murcia', 'Murcia'),
    ('navarra', 'Navarra'),
    ('ourense', 'Ourense'),
    ('palencia', 'Palencia'),
    ('pontevedra', 'Pontevedra'),
    ('salamanca', 'Salamanca'),
    ('santa cruz de tenerife', 'Santa cruz de tenerife'),
    ('segovia', 'Segovia'),
    ('sevilla', 'Sevilla'),
    ('soria', 'Soria'),
    ('tarragona', 'Tarragona'),
    ('teruel', 'Teruel'),
    ('toledo', 'Toledo'),
    ('valencia', 'Valencia'),
    ('valladolid', 'Valladolid'),
    ('viscaya', 'Vizcaya'),
    ('zamora', 'Zamora'),
    ('zaragoza', 'Zaragoza'),
)      
CATEGORY= (
	('vehicles', 'Vehicles'),
	('inmobles', 'Inmobles'),
	('mobles', 'Mobles'),
	('moda', 'Moda'),
	('nens', 'Nens'),
	('electronica', 'Electrónica'),
	('mascotes', 'Mascotes'),
	('treball i formacio', 'Treball i formació'),
	('esports', 'Esports'),
	('negocis i serveis', 'Negocis i serveis'),
	('altres', 'Altres'),

) 

class CartAddProductForm(forms.Form):
		update = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)
		
class Consultaform(forms.Form):
	    consulta = forms.CharField(label='consulta',required=False,max_length=100)
	    provincia = forms.ChoiceField(label='provincia',choices=PROVINCES,required=False)
	    
class Filtresform(forms.Form):
		preu = forms.IntegerField(required=False)
		finsa = forms.IntegerField(required=False)
		
class SignUpForm(forms.Form):
		name = forms.CharField(max_length=100)
		password = forms.CharField(max_length=100)
		
class LoginForm(forms.ModelForm):
		username = forms.CharField( widget=forms.TextInput(attrs={ 'id': 'input'}) )
		password = forms.CharField(widget=forms.PasswordInput(attrs={ 'id': 'input'}))
		class Meta:
			model = User
			fields = ['username']
			
class PaymentForm(forms.Form):
	adress = forms.CharField(label="Adreça",max_length=100)	
	city = forms.CharField(label="Ciutat/Població:",max_length=100)		
	def __init__(self,profile ,*args, **kwargs):
		super(PaymentForm, self).__init__(*args, **kwargs)
		self.fields['province'] = forms.CharField(label="Provincia:",initial=profile.province )
		self.fields['cp']= forms.CharField(label="Codi Postal:",initial=profile.postalnumber)

	
class ProfileForm(forms.Form):
	def __init__(self,profile ,*args, **kwargs):
		self.request = kwargs.pop('profile',None)
		super(ProfileForm, self).__init__(*args, **kwargs)
		self.fields['username'] = forms.CharField(required=False,initial=profile.username,widget=forms.TextInput(attrs={ 'id': 'input'}) )
		self.fields['email'] = forms.CharField(required=False,initial=profile.email,widget=forms.TextInput(attrs={ 'id': 'input'}) )
		self.fields['password']= forms.CharField(required=False,widget=forms.PasswordInput(attrs={ 'id': 'input'}))
		self.fields['password2'] = forms.CharField(required=False,label="Repeteix constrasenya",widget=forms.PasswordInput(attrs={ 'id': 'input'}))
		self.fields['province'] = forms.ChoiceField(required=False,widget=forms.Select(attrs={'id': 'input'}),initial=profile.province,choices=PROVINCES)
		self.fields['cp']= forms.CharField(required=False,initial=profile.postalnumber, widget=forms.TextInput(attrs={ 'id': 'input'}))
	class Meta:
		model = User
		fields =['username','email']
	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password2'] != cd['password']:
			raise ValidationError('Password dont match')
		return cd['password2']
	
class ProductForm(forms.Form):
	name = forms.CharField( widget=forms.TextInput(attrs={ 'id': 'input'}) )	
	description = forms.CharField( widget=forms.Textarea(attrs={ 'id': 'input'}) )
	price = forms.IntegerField(widget=forms.TextInput(attrs={ 'id': 'input'}) )
	image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))	
	category = forms.ChoiceField(choices=CATEGORY,widget=forms.Select(attrs={ 'id': 'input'}))
	
class ProductEditForm(forms.Form):
	def __init__(self,product ,*args, **kwargs):
		self.request = kwargs.pop('product',None)
		super(ProductEditForm, self).__init__(*args, **kwargs)
		self.fields['name'] = forms.CharField(required=False,initial=product.name, widget=forms.TextInput(attrs={ 'id': 'input'}) )	
		self.fields['description'] = forms.CharField(required=False,initial=product.description, widget=forms.Textarea(attrs={ 'id': 'input'}) )
		self.fields['price'] = forms.IntegerField(required=False,initial=product.price,widget=forms.TextInput(attrs={ 'id': 'input'}) )
		self.fields['image'] = forms.ImageField(required=False)	
		self.fields['is_buyed'] = forms.BooleanField(required=False,initial=product.is_buyed)
	category = forms.ChoiceField(required=False,choices=CATEGORY,widget=forms.Select(attrs={ 'id': 'input'}))	
	
class RegisterForm(forms.ModelForm):
	username = forms.CharField( widget=forms.TextInput(attrs={ 'id': 'input'}) )
	email = forms.CharField( widget=forms.TextInput(attrs={ 'id': 'input'}) )
	password = forms.CharField(widget=forms.PasswordInput(attrs={ 'id': 'input'}))
	password2 = forms.CharField(label="Repeteix constrasenya",widget=forms.PasswordInput(attrs={ 'id': 'input'}))
	province = forms.ChoiceField(choices=PROVINCES,widget=forms.Select(attrs={'id': 'input'}))
	cp = forms.CharField( widget=forms.TextInput(attrs={ 'id': 'input'}))
	class Meta:
		model = User
		fields =['username','email']
	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password2'] != cd['password']:
			raise ValidationError('Password dont match')
		return cd['password2']
