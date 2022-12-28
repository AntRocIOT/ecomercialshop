# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received,invalid_ipn_received

def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    print ipn_obj.address_name
    print ipn_obj.address_country
    print ipn_obj.receiver_email
    print ipn_obj.residence_country
    print ipn_obj.payment_status
    for e in kwargs:
		print e
    user = kwargs.get('instance',None)
    #if ipn_obj.payment_status == ST_PP_COMPLETED:
	#u = UserProfile.objects.get(id=user.id)
    print user
  

valid_ipn_received.connect(show_me_the_money) 
# Create your models here.
def get_image_path(instance, filename):
    return os.path.join('fotos', str(instance.id), filename)
    
class Product(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=500)
	price = models.DecimalField(max_digits = 8,decimal_places = 2)
	#avatar = models.ImageField(upload_to=get_image_path, null=True)
	data = models.DateTimeField(auto_now_add=True)
	is_buyed = models.BooleanField(default=False)

def get_image_filename(instance, filename):
    title = instance.post.title
    slug = slugify(title)
    return "post_images/%s-%s" % (slug, filename) 

class Images(models.Model):
    post = models.ForeignKey(Product)
    image = models.ImageField(upload_to=get_image_path,verbose_name='Image')
class UserProfile(models.Model): 
	username=models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	province= models.CharField(max_length=100)
	postalnumber = models.IntegerField()

class Category(models.Model):
	name = models.CharField(max_length=100)
	
class Bill(models.Model):
	data = models.DateTimeField(auto_now=True, auto_now_add=False)
	adress = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	total = models.DecimalField(max_digits = 8,decimal_places = 2)
	class Meta:
		ordering =['data']
class Admin(models.Model):
	user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)

class Publish(models.Model):
	user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, related_name='fk_product_user', null=True)
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='fk_product_user', null=True)

class Owns(models.Model):
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='fk_product_category', null=True)
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='fk_product_category', null=True)
	
class Pay(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
	bill = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True)
	
	
