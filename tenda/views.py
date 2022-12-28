# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from django.shortcuts import render,redirect,get_object_or_404
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,HttpResponse,HttpResponseForbidden
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.generic import CreateView,View
from django.db.models import Q
from django import forms
from .forms import Consultaform,SignUpForm,RegisterForm,LoginForm,ProductForm,ProfileForm,CartAddProductForm,ProductEditForm,PaymentForm,Filtresform
from paypal.standard.forms import PayPalPaymentsForm
from .models import Product,UserProfile,Publish,Owns,Category,Pay,Bill,Images
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.conf import settings
from django.contrib import messages
import urllib,os,time
from cart import Cart




# Create your views here.
def admin_zone(request):
	#Imprimeix la pagina del administrador
	return render(request,'admin/admin.html')

# Aquesta view s'encarrega de crear el usuaris, regit pel el administrador
def admin_zone_create_users(request):
	
	if request.method =='POST':
			form = RegisterForm(request.POST)
			if form.is_valid():
				user = form.save(commit=False)
				#Agafem les dades de usuari i les guardem
				user.set_password(form.cleaned_data['password'])
				un = form.cleaned_data['username']
				em = form.cleaned_data['email']
				pas = form.cleaned_data['password']
				pro = form.cleaned_data['province']
				cp = form.cleaned_data['cp']
				#Comprobem que no existeixi un usuari amb el mateix nom
				data = UserProfile.objects.filter(username=un)
				
				if not data :
					print "No hi ha user amb el mateix nom"
					new_data = UserProfile.objects.create(username=un, email=em, password = pas,province=pro, postalnumber=cp)
					user.save()
					
				else:
					return HttpResponse("There are a user with the same username")
			return redirect('admin_zone_user_list')
	else:
		form = RegisterForm()
		return render(request,'admin/admin_zone_create_user.html',{'form': form })
		

#Aquesta view s'encarrega de editar les dades del usuari, sol el administrador
def admin_zone_edit_user(request,user_id):
		profile = UserProfile.objects.get(id=user_id)
		if request.method =='POST':
			form = ProfileForm(profile,request.POST)
			if form.is_valid():
				#Agafem les dades
				un = form.cleaned_data['username']
				e = form.cleaned_data['email']
				pas = form.cleaned_data['password']
				pro = form.cleaned_data['province']
				cp = form.cleaned_data['cp']
				#Comprovem que s'han replenat tots els forms.
				owner = User.objects.get(username=un)
				if un:
					owner.username = un
					profile.username = un
				if e:
					owner.email = e
					profile.email = e
				if pas:
					owner.set_password( pas)
					profile.password = pas
				if pro:
					profile.province = pro
				if cp:
					profile.postalnumber = cp
				#Guadem dades
				profile.save()
			
				return redirect('admin_zone_user_list')
		else:
			form = ProfileForm(profile)
		return render(request,'admin/admin_zone_edit_user.html',{'form': form })	
#Aquesta view s'encarrega de eliminar el usuaris, sol el administrador		
def admin_zone_eliminate_user(request,user_id):
			pu = Publish.objects.filter(id__in=user_id)
			if pu:
				pu.delete()
			u = UserProfile.objects.get(id__in=user_id)
			
			if u:
				own = User.objects.get(username=u.username)
				u.delete()
				own.delete()
			return redirect('admin_zone_user_list')
#Mostra una llista de usuaris registrats			
def admin_zone_user_list(request):
	users = UserProfile.objects.filter()
	return render(request,'admin/admin_zone_user_list.html',{'users':users})
#S'encarrega de crear productes com a administrador	
def admin_zone_create_product(request):
	if request.method=='POST':
		form = ProductForm(request.POST,request.FILES)
		if form.is_valid():
			#Agafem les dades
			n= form.cleaned_data.get('name')
			img = form.cleaned_data.get('image')
			desc = form.cleaned_data.get('description')
			p = form.cleaned_data.get('price')
			ca = form.cleaned_data.get('category')
			cat = Category.objects.get(name=ca)
			#Construir una nova instancia de producte.
			new_data = Product.objects.create(name=n, description=desc, price = p)
			#Pujem les fotos
			for count,x in enumerate(request.FILES.getlist('image')):
				handle_uploaded_file(x,str(x))
				Images.objects.create(post=new_data, image=str(x))
			Owns.objects.create(category=cat, product=new_data)
			#Guardem les dades
			new_data.save()
			messages.info(request, 'Three credits remain in your account.')
			return redirect('product_list')
	else:
		form = ProductForm()		
	return render(request,'admin/admin_zone_create_product.html',{'form': form,})
#S'encarrega de editar la informacio dels productes com a administrador	
def admin_zone_edit_product(request,product_id):
		#Busquem el producte a editar
		product = Product.objects.get(id=product_id)
		if request.method =='POST':
			form = ProductEditForm(product,request.POST)
			if form.is_valid():
				#Agafem les dades
				un = form.cleaned_data['name']
				des = form.cleaned_data['description']
				pr = form.cleaned_data['price']
				ca = form.cleaned_data['category']
				isb= form.cleaned_data['is_buyed']
				#Comprovem el camps que s'han cambiat.
				if un:
					product.name = un
				if des:
					product.description = des
				if pr:
					product.price = pr
				if ca:
					product.category = ca

					
				product.is_buyed = isb
				
				#Guardem les dades
				product.save()
				
				return redirect('product_list')
		else:
			form = ProductEditForm(product)
		return render(request,'admin/admin_zone_edit_product.html',{'form': form })
		
#S'encarrega de eliminar productes com a administrador.
def admin_zone_eliminate_product(request,product_id):
			#Busquem les dades a elimninar i les borrem de la base de dades
			ow = Owns.objects.filter(product_id=product_id)
			if ow:
				ow.delete()
			pu = Publish.objects.filter(product_id=product_id)
			if pu:
				pu.delete()
			i = Images.objects.filter(post_id=product_id)
			if i:
				i.delete()
			p = Product.objects.filter(id=product_id)
			if p:
				p.delete()
			return redirect('product_list')
#Mostre una llista de productes registrats.			
def admin_zone_product_list(request):
	products = Product.objects.filter()
	return render(request,'admin/admin_zone_product_list.html',{'products':products})
	
	
#def admin_zone_create_payments(request):
def admin_zone_edit_payments(request,payment_id):
		pay = Pay.objects.get(id=payment_id)
		if request.method =='POST':
			form = ProductEditForm(pay,request.POST)
			if form.is_valid():
				un = form.cleaned_data['name']
				des = form.cleaned_data['description']
				pr = form.cleaned_data['price']
				ca = form.cleaned_data['category']
				isb= form.cleaned_data['is_buyed']
				print isb
				if un:
					product.name = un
				if des:
					product.description = des
				if pr:
					product.price = pr
				if ca:
					product.category = ca

					
				product.is_buyed = isb
				
					
				product.save()
				
				return redirect('product_list')
		else:
			form = ProductEditForm(product)
		return render(request,'admin/admin_zone_edit_product.html',{'form': form })
		
#def admin_zone_eliminate_payments(request):
def admin_zone_payments_list(request):
		payments = Pay.objects.filter()
		return render(request,'admin/admin_zone_payment_list.html',{'payments':payments})
#def admin_zone_create_category(request):
#def admin_zone_edit_category(request):
#def admin_zone_eliminate_category(request):
#def admin_zone_category_list(request):

#S'encarrega de procesar les cerques de usuari
def buscar(request):
	print request.POST
	if request.method =='POST':
		form = Consultaform(request.POST)
		form2 = Filtresform(request.POST)
		args ={}
		if form.is_valid():
			#Agafem les dades introduides als inputs
			data = form.cleaned_data['consulta']
			cat = form.cleaned_data['provincia']
			#Busquem productes a partir de les dades donades.
			resu = Product.objects.filter(Q(name__icontains=data)|Q(description__contains=data)).order_by('-data')
			res = UserProfile.objects.filter(province__icontains=cat).values('username')
			res2  = Publish.objects.filter(user__in=res)
			
			#Comprovem que hagi dades a mostrar
			if  res2:
				args ={'form':form,'form2':form2,'text':data,'result':res2,'user':res}
			if res:
				args ={'form':form,'form2':form2,'text':data,'result':resu,'user':res}
					
			

		
		#Retorne a la pagina on mostrara el productes.
		return render(request,'resultats_consulta.html',args)
	else:
		form = Consultaform()
		form2 = Filtresform()

		return render(request, 'category.html',)
#Permet afegir productes al carro
def cart_add(request,product_id):
	if request.method=='POST':
		#Busquem el producte per introduir al carro
		cart = Cart(request)
		product = get_object_or_404(Product,id=product_id)
		form = CartAddProductForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			#Afegim les dades del producte.Per saber com funcione el carro mirar cart.py.
			cart.add(product=product,quantity=1,update_quantity=cd['update'])
		return redirect('/cart')
#Permet eliminar productes del carro		
def cart_remove(request,product_id):
	cart = Cart(request)
	product = get_object_or_404(Product,id=product_id)
	cart.remove(product)
	return redirect('/cart')
	
#Mostra el contingut del carro
@login_required(login_url='login')
def cart_list(request):
	cart = Cart(request)
	return render(request,'cart.html',{'cart':cart})
	

#Permet crear productes com a usuari
@login_required(login_url='login')
def create_product(request):
	#dataset = Product.objects.filter(id=id)[0]
	if request.method=='POST':
		print "POST-Create_product"
		form = ProductForm(request.POST,request.FILES)
		if form.is_valid():
			n= form.cleaned_data.get('name')
			img = form.cleaned_data.get('image')
			desc = form.cleaned_data.get('description')
			p = form.cleaned_data.get('price')
			ca = form.cleaned_data.get('category')
			cat = Category.objects.get(name=ca)
			
			new_data = Product.objects.create(name=n, description=desc, price = p)
			for count,x in enumerate(request.FILES.getlist('image')):
				handle_uploaded_file(x,str(x))
				Images.objects.create(post=new_data, image=str(x))
			u = UserProfile.objects.get(username=request.user)
			Publish.objects.create(user=u, product=new_data)
			Owns.objects.create(category=cat, product=new_data)
			new_data.save()
			
			return render(request,'category.html')
	else:
		form = ProductForm()		
	return render(request,'create_product.html',{'form': form,})
	
# Permet eliminar productes com a usuari
@login_required(login_url='login')
def delete_product(request,product_id):
			pu = Publish.objects.filter(product_id=product_id)
			data = Product.objects.filter(id=product_id)
			pu.delete()
			data.delete()
			return redirect('product_list2')
#Permet editar informacio dels productes com a usuari
@login_required(login_url='login')
def edit_product(request,product_id):
	
		product = Product.objects.get(id=product_id)
		if request.method =='POST':
			form = ProductEditForm(product,request.POST)
			if form.is_valid():
				un = form.cleaned_data['name']
				des = form.cleaned_data['description']
				pr = form.cleaned_data['price']
				ca = form.cleaned_data['category']
				if un:
					product.name = un
				if des:
					product.description = des
				if pr:
					product.price = pr
				if ca:
					product.category = ca
				
					
				product.save()
				
				return redirect('product_list2')
		else:
			form = ProductEditForm(product)
		return render(request,'anunci_edit.html',{'form': form })
def filtra(request):
	if request.method == 'POST':
		form2 = Filtresform(request.POST)
		args ={}
		if form2.is_valid():
			p = form2.cleaned_data['preu']
			f = form2.cleaned_data['finsa']
		
			if p > f:
				resu = Product.objects.filter(price__range=(f, p)).order_by('-data')
				args ={'form2':form2,'result':resu}


			if p <= f:
				resu = Product.objects.filter(price__range=(p, f)).order_by('-data')
				args ={'form2':form2,'result':resu}
			
			return render(request,'resultats_consulta.html',args)	
	else:
		form = Filtresform(request.POST)
		return render(request,'resultats_consulta.html')
	
#S'encarrega de pujar arxius, en aquest cas fotografies del producte
def handle_uploaded_file(file, filename):
	filename = filename.decode('utf-8')
	BASE_DIR = '/home/rokanas/rummi/'
	STATIC_ROOT = os.path.join(BASE_DIR, 'static')
	print os.path.join(STATIC_ROOT,'/fotos/')
	if not os.path.exists(os.path.join(STATIC_ROOT,'fotos/')):
			os.mkdir(os.path.join(STATIC_ROOT,'fotos/'),777)
			print('Arribe')
	with open(os.path.join(STATIC_ROOT,'fotos/' + filename), 'wb+') as destination:
		for chunk in file.chunks():
			destination.write(chunk)
			print("Pujada correcta")
	return 'fotos/' + filename 
#Mostra el producte amb el seus detalls          
def product(request,id_product):
	data = Product.objects.get(id=id_product)
	form = CartAddProductForm()
	args ={'texts':data,'form':form,'id_product':data.id}
	return render(request,'product.html',args)	
#S'encarrega de registrar un usuari a la pagina
class RegisterUserView(CreateView):
	form_class = RegisterForm
	template_name = "registre_usuari.html"
	
	def dispatch(self,request,*args,**kwargs):
		if request.user.is_authenticated():
			return render(request,'/category.html')
			
		return super(RegisterUserView,self).dispatch(request,*args,**kwargs)
		
	def form_valid(self,form):
		
		user = form.save(commit=False)
		user.set_password(form.cleaned_data['password'])
		un = form.cleaned_data['username']
		em = form.cleaned_data['email']
		pas = form.cleaned_data['password']
		pro = form.cleaned_data['province']
		cp = form.cleaned_data['cp']
		data = UserProfile.objects.filter(username=un)
		print data
		if not data :
			new_data = UserProfile.objects.create(username=un, email=em, password = pas,province=pro, postalnumber=cp)
			user.save()
		else:
			return HttpResponse("There are a user with the same username")
		HttpResponse('User registered')
		time.sleep(3)
		return redirect('/login')
#Permet a l'usuari conectar a la pagina 
class LoginView(CreateView):
	  form_class = LoginForm
	  template_name = "iniciar_sessio.html"
	  
	  def post(self, request):
		  print"Entra login"
		  if request.user.is_authenticated():
			  return HttpResponse('You are logged')
		  else:
				
				username = request.POST['username']
				password = request.POST['password']
				user = authenticate(username=username, password=password)
				if user is not None:
					if user.is_active:
						login(request, user)
						return HttpResponseRedirect('/')
					else:
						return HttpResponse("Inactive user.")
				else:
					return HttpResponseRedirect('iniciar_sessio.html')
			  
		  return render_to_string(request, template_name,{'form': form})
				
				
#Permet a l'usuari desconnectar el compte de la pagina.		
class LogoutView(CreateView):
	template_name = "logout.html"
	def dispatch(self,request,*args,**kwargs):
		if request.user.is_authenticated():
			logout(request)
			return HttpResponse('Logged out')
		else:
			return render(request, 'iniciar_sessio.html')

def logout_session(request):
	if request.method== 'POST':
		if request.user.is_authenticated():
			logout(request)
			return render(request,'category.html')
		
	return render(request, 'logout.html')
#S'encarrega de procesar el pagament mitjançant paypal i crea un ticket per al usuari
@login_required(login_url='login')
def payment(request):
	cart = Cart(request)
	paypal_dict = {"business": "rokanas666@gmail.com","amount": cart.get_total_price(),"item_name": "Rummi transaction","currency_code": "EUR","invoice": "unique-invoice-id","notify_url": request.build_absolute_uri(reverse('paypal-ipn')),"return": request.build_absolute_uri(reverse('success_payment')),"cancel_return": request.build_absolute_uri(reverse('unsuccess_payment')),"custom": "premium_plan", }
	form2 = PayPalPaymentsForm(initial=paypal_dict)
	user = UserProfile.objects.get(username=request.user)
	if request.method=='POST':
		form = PaymentForm(user,request.POST)
		
		if form.is_valid():
			a = form.cleaned_data['adress']
			c = form.cleaned_data['city']
			p = form.cleaned_data['province']
			cp = form.cleaned_data['cp']
			u = UserProfile.objects.get(username=request.user)

			request.session['adress']= a
			request.session['city']= c
			request.session['province']=p
			request.session['codipostal']=cp
			return render(request,'payment_last.html',{"form":form,"form2":form2,"adress":a,"city":c,"user":u,"province":p,"codipostal":cp})

	
	# Create the instance.
	else:
		form = PaymentForm(user)
		return render(request, "payment.html",{"form":form,"form2":form2})

#Mostra el anuncis que ha creat el usuari
@login_required(login_url='login')
def product_list(request):
	listaproducts = []
	profile = UserProfile.objects.get(username=request.user)
	pu = Publish.objects.filter(user_id=profile.id)
	for product in pu:
		listaproducts.append(Product.objects.get(id=product.product_id))
		

	return render(request,'anuncis_user.html',{'listaproducts':listaproducts})
	
#Permet editar les dades personals com a usuari.
@login_required(login_url='login')
def profile_edit(request):
	#Busquem el usuari a editar les dades.
	profile = UserProfile.objects.get(username=request.user)
	if request.method == 'POST':
		form = ProfileForm(profile,request.POST)
		if form.is_valid():
			#Agafem les dades.
			un = form.cleaned_data['username']
			e = form.cleaned_data['email']
			pas = form.cleaned_data['password']
			pro = form.cleaned_data['province']
			cp = form.cleaned_data['cp']
			owner = User.objects.get(username=request.user)
			#Comprobem el camps modificats.
			if un:
				owner.username = un
				profile.username = un
			if e:
				owner.email = e
				profile.email = e
			if pas:
				owner.set_password( pas)
				profile.password = pas
			if pro:
				profile.province = pro
			if cp:
				profile.postalnumber = cp
			#Guardem les dades.
			profile.save()
			owner.save() 
			messages.success(request, 'El teu perfil ha sigut actualitzat',extra_tags='alert')  # <-
			return render(request,	'profile.html',{'form': form })	
	else:
		form = ProfileForm(profile)
	return render(request,	'profile.html',{'form': form })		

#S'encarrega de filtar productes per categoria seleccionada per l'usuari
def search_category(request):
	if request.method=='GET':
		form = Filtresform(request.GET)
		sku = request.GET.get('query_name')
		ow = Owns.objects.filter(category_id__in=sku).values('product_id')
		res = Product.objects.filter(id__in=ow)
		args ={'result':res,'form':form}
		
		return render(request,'resultats_consulta.html',args)
	
	else:
		form = Consultaform()
		return render(request, 'category.html',)
		
#Si el pagament s'ha realizat amb exit, crida aquesta view
def success_payment(request):
	user = UserProfile.objects.get(username=request.user)
	cart = Cart(request)
	for i in cart:
		pro = Product.objects.get(id=i["product"].id)
		bi = Bill.objects.create(total=float(pro.price),adress=request.session['adress'],city=request.session['city'])
		Pay.objects.create(user=user,product=pro,bill=bi)
	
	cart.clear()
	pay = Pay.objects.filter(user_id=user.id)
	for i in pay:
		i.product.is_buyed = True
		i.product.save()
	
	return render(request,'success_payment.html')	

#Permet veure el tickets que te l'usuari.
@login_required(login_url='login')	
def tickets_list(request):
	
	listaproducts = []
	bills= []
	profile = UserProfile.objects.get(username=request.user)
	pu = Pay.objects.filter(user_id=profile.id)
	
	for product in pu:
		listaproducts.append(Product.objects.get(id=product.product_id))
		bills.append(Bill.objects.get(id=product.bill_id))

	return render(request,'tickets_list.html',{'listaproducts':listaproducts,"bill":bills})
#Si la compra no s'ha realizat amb exit,crida aquesta view
def unsuccess_payment(request):
	
	return render(request,'unsuccess_payment.html')

def anunci(request):
	return render(request,'anunci.html')
def ajuda(request):
	return render(request,'ajuda.html')
def resultats_consulta(request):
	if request.method == 'GET':
		print request.GET
		data = request.GET.get('consulta')
	if request.method == 'POST':
		data = request.POST.get('consulta')

	
	return render_to_string(request,'resultats_consulta.html',data)


