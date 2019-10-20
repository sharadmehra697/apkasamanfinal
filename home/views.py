from django.shortcuts import render, redirect,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from home.forms import regisForm,getForm,loginForm,imgForm 
from home.models import product_images,pcompany,kirana,shpimg,shpdocument,justExample,getExample,product_images,otd,registered_as,shops,category,products,shopkpr,cart_items,sub_category,sub_child,sub_daughter,customers,customer_address,orders,payments,flavourTable,shapeTable,proposeTable,soleMaterial,inMaterial,outMaterial,animalTable,subfields,colorTable,sizeTable,typeTable,statMaterial,bookSpecification,stationary
import string
import random
import ast
from django.template import RequestContext
from django.db import connection
from django.contrib import messages
from django.utils import timezone
from django.views import View
import json
import csv
import codecs
from home.models import perprod,perkirana,perpcompany

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def shopMain(request):
	if request.session.has_key('login_id'):
		if request.session.has_key('shop_id'):
			s=shops.objects.get(shop_id=request.session['shop_id'])
			for i in s.shop_image.all():
				si=i
			cg=category.objects.all()
			if request.session.has_key('additem'):
				p=request.session['additem']
				ash=zip(p[0],p[1],p[2],p[3])
				return render(request,'shopkprhome.html',{'simg':si,'n':range(3),'sS':s,'category':cg,'ash':ash})
			return render(request,'shopkprhome.html',{'simg':si,'n':range(3),'sS':s,'category':cg})
		else:
			return ifShop(request)
	else:
		return isLogged(request)

#for looged in if not
def isLogged(request,msg=''):
	if request.session.has_key('login_id'):
		 return redirect("/Shopmain")
	else:

		return render(request, 'login.html',{'login_quote':msg})

def ifShop(request):
	g=category.objects.all()
	if request.session.has_key('shop_id'):
		return shopMain(request)
	else:
		regis=registered_as.objects.get(regis_id=request.session['login_id'])
		try:
			getShop=shopkpr.objects.get(regis_id=regis)
			if getShop.shop_created==1:
				restShop=shops.objects.get(shopkpr_id=getShop)
				if restShop.shop_address==1:
					request.session['shop_id']=restShop.shop_id
					return shopMain(request)
				else:
					request.session['shop_address']=restShop.shop_id
					return showaddress(request)
			else:
				request.session['shopkpr_id']=getShop.shopkpr_id
				return render(request,'shop_regis.html',{'s':g,'shpname':getShop.shopkpr_name})
		except Exception as e:
			print(e)
			return render(request,'shop_regis.html',{'s':g})

def checkotp(request):
	cut=registered_as
	if request.method == 'POST':
		try:
			g=cut.objects.get(regis_mobile=request.POST.get('cust_num'))
			return HttpResponse('numExist')
		except Exception as e:
			randOtp=random.randint(1000,9999)
			return HttpResponse(randOtp)
	else:
		return HttpResponse("Not Access Direct")

class userRegis(View):
	def get(self,request):
		udict={'geterr':'Good'}
		if request.session.has_key('login_id'):
			logged=registered_as.objects.get(regis_id=request.session['login_id'])
			userNumber='You are Registered with this '+str(logged.regis_mobile)+' Number'
			udict.update({'userNumber':userNumber})
		return render(request, 'registration.html',udict)


	def post(self,request):
		try:
			g=cut.objects.get(regis_mobile=request.POST.get('user_mobile'))
			return HttpResponse('NumExist')
		except Exception as e:
			uNum=request.POST.get('user_mobile')
			uPass=request.POST.get('user_pass')
			uDate=request.POST.get('user_dob')
			uName=request.POST.get('user_name')
			gObj=registered_as()
			gObj.regis_name=uName
			gObj.regis_mobile=uNum
			gObj.regis_dob=uDate
			gObj.regis_pass=uPass
			gObj.save()
			return HttpResponse('Data Save')

#for user Login
class userLogin(View):
	def get(self,request):
		if request.session.has_key('login_id'):
			return redirect('/Shopmain')
		else:
			return render(request, 'login.html')

	def post(self,request):
		uNumber=request.POST.get('login_mobile')
		uPassword=request.POST.get('login_pass')
		checkMob=registered_as.objects.get(regis_mobile=uNumber)
		if uPassword == checkMob.regis_pass:
			request.session['login_id']=checkMob.regis_id
			if request.session.has_key('add_path'):
				next=request.session['add_path']
				return HttpResponseRedirect(next)
			return ifShop(request)
		else:
			msg='wrong'
			num=uNumber
			return render(request, 'login.html',{'passerr':msg,'num':num})

#for shop registration
class shopkeeperRegis(View):
	def get(self,request):
		if request.session.has_key('login_id'):
			if request.session.has_key('shop_id'):
				return shopMain(request)
			else:
				return ifShop(request)
		else:
			return isLogged(request,msg='You must Login First')

	def insertShop(self,request,setShopkpr):
		sname=request.POST.get('sname')
		ssales=request.POST.getlist('ssales[]')
		sopen=request.POST.get('sopen')
		sclose=request.POST.get('sclose')
		sholiday=request.POST.get('sholiday')
		try:
			setShop=shops.objects.get(shopkpr_id=setShopkpr)
			if setShop.shop_verified==1:
				request.session['shop_id']=setShop.shop_id
				return shopMain(request)
			else:
				return HttpResponse('shopverify')
		except Exception as e:
			setShop=shops()
			setShop.shopkpr_id=setShopkpr
			setShop.shop_name=sname
			setShop.shop_open=sopen
			setShop.shop_close=sclose
			setShop.shop_holiday=sholiday
			setShop.unpacked_orders=[]
			setShop.shop_orders=[]
			setShop.shop_liveorders=[]
			setShop.save()
			for i in ssales:
				print(i)
				setShop.shop_type.add(category.objects.get(category_key=i))
			setShopkpr.shop_created=1
			setShopkpr.save()
			return HttpResponse('shopverify')

	def post(self,request):
		if request.session.has_key('login_id'):
			if request.session.has_key('shopkpr_id'):
				setShopkpr=request.session['shopkpr_id']
				del request.session['shopkpr_id']
				setShopkpr=shopkpr.objects.get(shopkpr_id=setShopkpr)
				return self.insertShop(request,setShopkpr)
			else:
				setShopkpr=shopkpr()
				cname=request.POST.get('cname')
				asregis=registered_as.objects.get(regis_id=request.session['login_id'])
				setShopkpr.regis_id=asregis
				setShopkpr.shopkpr_name=cname
				setShopkpr.save()
				return self.insertShop(request,setShopkpr)
		else:
			return isLogged(request,msg='You must Login First')

def shopverify(request):
	if request.session.has_key('login_id'):
		if request.session.has_key('shop_id'):
			sData=shops.objects.get(shop_id=request.session['shop_id'])
			sata=sData.shop_image.all()
			bata=sData.shop_document.all()
			return render(request,'shopverification.html',{'sImgs':sata,'sDocs':bata})
		else:
			return ifShop(request)
	else:
		return isLogged(request)

def showaddress(request):
	if request.session.has_key('login_id'):
		if request.session.has_key('shop_address'):
			if request.method =='POST':
				setAdd=shops.objects.get(shop_id=request.session['shop_address'])
				setAdd.shop_address=1
				setAdd.save()
				request.session['shop_id']=request.session['shop_address']
				del request.session['shop_address']
				return HttpResponse('shopverify')
			return render(request,'shop_address.html')
		else:
			return ifShop(request)
	else:
		return isLogged(request)

def insertDocument(request):
	if request.method=='POST':
		getFile=request.FILES['image']
		oShop=shops.objects.get(shop_id=request.session['shop_id'])
		ranKey=id_generator()
		pSave=shpdocument()
		pSave.shpdocument_name=getFile
		pSave.shpdocument_key=ranKey
		pSave.save()
		oShop.shop_document.add(pSave)
		return HttpResponse(ranKey)
	return HttpResponse('Not for Direct Use')

def insertImage(request):
	if request.method=='POST':
		getFile=request.FILES['image']
		oShop=shops.objects.get(shop_id=request.session['shop_id'])
		ranKey=id_generator()
		pSave=shpimg()
		pSave.shpimg_name=getFile
		pSave.shpimg_key=ranKey
		pSave.save()
		oShop.shop_image.add(pSave)
		return HttpResponse(ranKey)
	return HttpResponse('Not for Direct Use')

def delImage(request):
	if request.method=='POST':
		if(int(request.POST.get('dbName'))==0):
			getFile=request.POST.get('delVal')
			shpDoc=shops.objects.get(shop_id=request.session['shop_id'])
			shpDoc=shpDoc.shop_document.all()
			print(len(shpDoc))
			for i in shpDoc:
				if i.shpdocument_key==getFile:
					i.delete()
					return HttpResponse('done')
			return HttpResponse('Not Exist')
		elif(int(request.POST.get('dbName'))==1):
			getFile=request.POST.get('delVal')
			shpIm=shops.objects.get(shop_id=request.session['shop_id'])
			shpIm=shpIm.shop_image.all()
			for i in shpIm:
				if i.shpimg_key==getFile:
					i.delete()
					return HttpResponse('done')
			return HttpResponse('Not Exist')
		else:
			getFile=request.POST.get('delVal')
			try:
				prdIm=product_images.objects.get(img_key=getFile)
				prdIm.delete()
				return HttpResponse('Done')
			except Exception as e:
				return HttpResponse(e)
	return HttpResponse('Not for Direct Use')


def nameSearch(request):
	search_text=request.GET.get('search_text')
	if search_text is not None and search_text != u"":
		search_text = request.GET.get('search_text')
		statuss=perprod.objects.filter(product_category=request.GET.get('cat'),product_name__icontains= search_text)
	else:
		statuss=[]
	return render(request, 'namesearch.html', {'status':statuss})

def showfield(request):
	getFields=subfields.objects.get(fkey=request.GET.get('cat_val'))
	animal=animalTable.objects.filter(catname=request.GET.get('catkey'))
	flavour=flavourTable.objects.filter(catname=request.GET.get('catkey'))
	shape=shapeTable.objects.filter(catname=request.GET.get('catkey'))
	propose=proposeTable.objects.filter(catname=request.GET.get('catkey'))
	solem=soleMaterial.objects.filter(catname=request.GET.get('catkey'))
	statm=statMaterial.objects.filter(catname=request.GET.get('catkey'))
	inm=inMaterial.objects.filter(catname=request.GET.get('catkey'))
	outm=outMaterial.objects.filter(catname=request.GET.get('catkey'))
	typet=typeTable.objects.filter(catname=request.GET.get('catkey'))
	sizet=sizeTable.objects.filter(catname=request.GET.get('catkey'))
	colort=colorTable.objects.filter(catname=request.GET.get('catkey'))
	ps=[]
	pimgs=[]
	if request.GET.get('pid'):
		ps=perprod.objects.get(perprod_id=request.GET.get('pid'))
		pimgs=ps.product_image.all()

	data={
		'pimgs':pimgs,'ps':ps,'c':getFields,'animal':animal,'flavour':flavour,'shape':shape,'propose':propose,
		'solem':solem,'inm':inm,'statm':statm,'outm':outm,'typet':typet,'sizet':sizet,'colort':colort
	}
	return render(request,'sendField.html',data)

def talpha(request,table,typeid,cat):
	if table == typeTable:
		tp,tpc=table.objects.get_or_create(typename=typeid)
		print(tpc)
		if tpc:
			tp.typename=typeid
	elif table == flavourTable:
		tp.flavourname=typeid
		tp,tpc=table.objects.get_or_create(flavourname=typeid)
		if tpc:
			tp.flavourname=typeid
	elif table == animalTable:
		tp.animalname=typeid
		tp,tpc=table.objects.get_or_create(animalname=typeid)
		if tpc:
			tp.animalname=typeid
	elif table == shapeTable:
		tp.shapename=typeid
		tp,tpc=table.objects.get_or_create(shapename=typeid)
		if tpc:
			tp.shapename=typeid
	elif table == proposeTable:
		tp.proposename=typeid
		tp,tpc=table.objects.get_or_create(proposename=typeid)
		if tpc:
			tp.proposename=typeid
	tp.catname=cat
	tp.save()
	return tp
#for adding product to database
class getshopitem(View):
	allproductid=[]
	allname=[]
	allprice=[]
	allquantity=[]
	def addBag(self,request,padd):
		return HttpResponse('done')
	def addKirana(self,request,padd):
		pricekg=request.GET.get('pricekg')
		packed=request.GET.get('packedtype')
		expdate=request.GET.get('expdate')
		flavour=request.GET.get('flavour')
		propose=request.GET.get('propose')
		animal=request.GET.get('animal')
		shape=request.GET.get('shape')
		vegtype=request.GET.get('vegtype')
		typeid=request.GET.get('typeid')
		cat=request.GET.get('category')
		pget,pcrt=kirana.objects.get_or_create(product_id=padd)
		if pcrt:
			print('created')
			pget.product_id=padd
			pget.pricekg=pricekg
			pget.packedtype=packed
			if typeid:
				pget.typeid=talpha(request,typeTable,typeid,cat)
			pget.expdate=expdate
			if flavour:
				pget.flavour=talpha(request,flavourTable,flavour,cat)
			if propose:
				pget.propose=talpha(request,proposeTable,propose,cat)
			if animal:
				pget.animal=talpha(request,animalTable,animal,cat)
			if shape:
				pget.shape=talpha(request,shapeTable,shape,cat)
			pget.vegtype=vegtype
			pget.save()
			return HttpResponse('create done')
		else:
			print('already Exists')
			return HttpResponse('already done')

	#for permanent kirana
	def perkirana(self,request,pmadd):
		pricekg=request.GET.get('pricekg')
		packed=request.GET.get('packedtype')
		expdate=request.GET.get('expdate')
		flavour=request.GET.get('flavour')
		propose=request.GET.get('propose')
		animal=request.GET.get('animal')
		shape=request.GET.get('shape')
		vegtype=request.GET.get('vegtype')
		typeid=request.GET.get('typeid')
		cat=request.GET.get('category')
		pget,pcrt=perkirana.objects.get_or_create(perprod_id=pmadd)
		if pcrt:
			pget.perprod_id=pmadd
			pget.pricekg=pricekg
			pget.packedtype=packed
			if typeid:
				pget.typeid=talpha(request,typeTable,typeid,cat)
			pget.expdate=expdate
			if flavour:
				pget.flavour=talpha(request,flavourTable,flavour,cat)
			if propose:
				pget.propose=talpha(request,proposeTable,propose,cat)
			if animal:
				pget.animal=talpha(request,animalTable,animal,cat)
			if shape:
				pget.shape=talpha(request,shapeTable,shape,cat)
			pget.vegtype=vegtype
			pget.save()
			return HttpResponse('permananet prodeduct create done')
		else:
			print('permananet already Exists')
			return HttpResponse('already done')

	def get(self,request):
		if request.session.has_key('additem'):
			p=request.session['additem']
			self.allproductid=p[0]
			self.allname=p[1]
			self.allprice=p[2]
			self.allquantity=p[3]
		name=request.GET.get('name')
		price=request.GET.get('price')
		weight=request.GET.get('weight')
		quantity=request.GET.get('quantity')
		company=request.GET.get('company')
		brand=request.GET.get('brand')
		cat=request.GET.get('category')
		subcat=request.GET.get('subcategory')
		images=request.GET.getlist('images[]')
		try:
			pmadd=perprod.objects.get(product_name=name)
		except Exception as e:
			pmadd=perprod()
			pmadd.product_name=name
			pmadd.product_price=price
			pmadd.product_quantity=quantity
			pmadd.product_category=cat
			pmadd.product_subcategory=subcat
			pmadd.product_weight=weight
			pmadd.save()
			try:
				ppm=perpcompany()
				ppm.perprod_id=pmadd
				ppm.company=company
				ppm.brand=brand
				ppm.save()
				h=self.perkirana(request,pmadd)
			except Exception as e:
				print(e)

		padd=products()
		padd.product_name=name
		padd.product_price=price
		padd.product_quantity=quantity
		padd.product_category=cat
		padd.product_subcategory=subcat
		padd.product_weight=weight
		padd.save()
		try:
			pcom=pcompany()
			pcom.product_id=padd
			pcom.company=company
			pcom.brand=brand
			pcom.save()
			for i in images:
				padd.product_image.add(product_images.objects.get(img_key=i))
				pmadd.product_image.add(product_images.objects.get(img_key=i))
			shp=shops.objects.get(shop_id=request.session['shop_id'])
			shp.shop_products.add(padd)
		except Exception as e:
			padd.delete()
		if cat =='KR':
			h=self.addKirana(request,padd)
		elif cat =='BG':
			h=self.addBag(request,padd)
		self.allproductid.append(padd.product_id)
		self.allprice.append(price)
		self.allquantity.append(quantity)
		self.allname.append(name)
		request.session['additem']=[self.allproductid,self.allname,self.allprice,self.allquantity]
		return HttpResponse(padd.product_id)

def productimage(request):
	if request.method=='POST':
		getFile=request.FILES['image']
		ranKey=id_generator()
		pSave=product_images()
		pSave.img_name=getFile
		pSave.img_key=ranKey
		pSave.save()
		return HttpResponse(ranKey)
	return HttpResponse('Not for Direct Use')

def delProduct(request):
	try:
		pkey=request.GET.get('pkey')
		ps=products.objects.get(product_id=pkey)
		ps.delete()
		sd=request.session['additem']
		k=sd[0].index(pkey)
		for i in range(len(sd)):
			sd[i].pop(k)
		request.session['additem']=sd
		return HttpResponse('done')
	except Exception as e:
		return HttpResponse(e)

def getSubchild(request):
	if request.method=='GET':
		content=request.GET.get('intype')
		selectC=request.GET.get('select_subcategory')
		if selectC is not None and selectC != u"":
			if content == 'subcategory':
				selectC=request.GET['select_subcategory']
				isf='apka_shop_data_subchild'
				name='Select Subchild'
				data=sub_child.objects.filter(sub_child_parent=selectC)
				print(len(data))
			elif content == 'category':
				selectC=request.GET['select_subcategory']
				isf='apka_shop_data_subcategory'
				name='Select Subcategory'
				data=sub_category.objects.filter(sub_category_parent=selectC)
			else:
				selectC=request.GET['select_subcategory']
				isf='apka_shop_data_subdaughter'
				name='Select Subdaughter'
				data=sub_daughter.objects.filter(sub_daughter_parent=selectC)

		else:
			data=[]
			isf=''
			name=''

		if len(data) < 1:
			return HttpResponse('')

		return render(request,'setCategory.html',{'data':data,'isf':isf,'name':name})

#for adding product to database
class setItemSession(View):
	def get(self,request):
		return HttpResponse('Not Direct use setItemSession')

	def post(self,request):
		if request.session.has_key('additem'):
			g=list(request.session['additem'])
			print(g)
			cData=request.POST['allSet']
			cData=json.loads(cData)
			for i in cData:
				pdUp=products.objects.get(product_id=i['uid'])
				pdUp.product_price=i['pdprice']
				pdUp.product_quantity=i['pdquan']
				pdUp.save()
			del request.session['additem']
			return HttpResponse('Done')
		else:
			return HttpResponse('You Must Enter Some Product First')

def getShopinventry(request):
	if request.session.has_key('shop_id'):
		s=shops.objects.get(shop_id=request.session['shop_id'])
		gcat=s.shop_products.all().values('product_category').distinct()
		gscat=s.shop_products.all().values('product_subcategory').distinct()
		totalcat=[]
		for i in gcat:
			temp=category.objects.get(category_key=i['product_category'])
			sh=[]
			for j in gscat:
				temp2=sub_category.objects.get(sub_category_key=j['product_subcategory'],sub_category_parent=i['product_category'])
				temp2.sub_category_parent= s.shop_products.filter(product_subcategory=j['product_subcategory'],product_category=i['product_category'])
				sh.append(temp2)
			temp.category_hold=sh
			totalcat.append(temp)
		return render(request,'shopinventry.html',{'sItems':totalcat})
	else:
		return ifShop(request)

def getOrdersItems(request):
	if request.session.has_key('shop_id'):
		return render(request,'getShop_orders.html')
	else:
		return ifShop(request)

def updateQuantity(request):
	pup=products.objects.get(product_id=request.GET['pid'])
	pup.product_quantity=request.GET.get('pquan')
	pup.save()
	return HttpResponse(request.GET.get('pquan'))

def getProductinfo(request):
	g=products.objects.get(product_id=request.GET.get('pid'))
	g.product_category=category.objects.get(category_key=g.product_category)
	g.product_subcategory=sub_category.objects.get(sub_category_key=g.product_subcategory)
	a=request.GET.get('stype')
	if int(a)==0:
		return render(request,'productinfo.html',{'g':g})
	else:
		return render(request,'productinfo.html',{'g':g,'sedit':1})
 
def getupexcel(request):
	
	data = {}
	if "GET" == request.method:
		return render(request, "upload_csv.html")
    # if not GET, then proceed
	try:
		csv_file = request.FILES["csv_file"]
		dbname=request.POST['db_name']
		dbpass=request.POST['db_pass']
		if dbpass == 'apkadatabase':
			reader = csv.DictReader(codecs.iterdecode(csv_file, 'utf-8'))
			if dbname == 'home_category':
				for i in reader:
					tbe,tbc=category.objects.get_or_create(category_id=i['id'])
					tbe.category_name=i['name']
					tbe.category_key=i['key']
					tbe.category_hold=i['hold']
					tbe.save()
			elif dbname == 'home_sub_category':
				for i in reader:
					tbe,tbc=sub_category.objects.get_or_create(sub_category_id=i['id'])
					tbe.sub_category_name=i['name']
					tbe.sub_category_key=i['key']
					tbe.sub_category_parent=i['parent']
					tbe.save()
			elif dbname == 'home_subfields':
				for i in reader:
					tbe,tbc=subfields.objects.get_or_create(fid=i['id'])
					tbe.fname=i['name']
					tbe.fkey=i['key']
					tbe.color=i['color']
					tbe.typeid=i['typeid']
					tbe.refillable=i['refillable']
					tbe.captype=i['captype']
					tbe.size=i['size']
					tbe.pages=i['pages']
					tbe.rulled_type=i['rulled_type']
					tbe.binding=i['binding']
					tbe.materialid=i['materialid']
					tbe.packsize=i['packsize']
					tbe.gender=i['gender']
					tbe.closure=i['closure']
					tbe.solematerial=i['solematerial']
					tbe.healtype=i['healtype']
					tbe.warranty=i['warranty']
					tbe.guarantee=i['guarantee']
					tbe.agegroup=i['agegroup']
					tbe.occasion=i['occasion']
					tbe.outtermaterial=i['outtermaterial']
					tbe.innermaterial=i['innermaterial']
					tbe.capacity=i['capacity']
					tbe.pricekg=i['pricekg']
					tbe.packedtype=i['packedtype']
					tbe.expdate=i['expdate']
					tbe.flavour=i['flavour']
					tbe.propose=i['propose']
					tbe.animal=i['animal']
					tbe.shape=i['shape']
					tbe.vegtype=i['vegtype']
					tbe.parentdb=i['parentdb']
					tbe.save()
			elif dbname == 'home_sub_child':
				pass
			elif dbname == 'home_typetable':
				for i in reader:
					tbe,tbc=typeTable.objects.get_or_create(typeid=i['id'])
					tbe.typename=i['name']
					tbe.catname=i['key']
					tbe.save()
			else:
				return render(request,'upload_csv.html',{'quote':'Table Not Available'})
		else:
			return render(request,'upload_csv.html',{'quote':'Enter Correct Passcode'})
	except Exception as e:
		print(e)
		return render(request,'upload_csv.html',{'quote':e})

	return render(request,'upload_csv.html',{'quote':'Entry Done'})

def changeProductdetail(request):
	pcg=products.objects.get(product_id=request.GET.get('ppid'))
	pcg.product_price=request.GET['pprice']
	pcg.product_quantity=request.GET['pquantity']
	pcg.product_measure=request.GET['pmeasure']
	pcg.product_name=request.GET['pname']
	pcg.product_weight=request.GET['pweight']
	pcg.save()
	cis=pcompany.objects.get(product_id=pcg)
	cis.company=request.GET['pcompany']
	cis.brand=request.GET['pbrand']
	cis.save()
	return HttpResponse('Done')

def getOut(request):
	del request.session['shop_id']
	del request.session['login_id']
	return HttpResponseRedirect('Shopmain')

def forgottenPass(request):
	if request.method=='POST':
		get=registered_as.objects.get(regis_mobile=request.POST['user_mobile'])
		get.regis_pass=request.POST['user_pass']
		get.save()
		return HttpResponse('done')
	return render(request,'forgottenpass.html')

def forgetsendOtp(request):
	if request.method == 'POST':
		try:
			g=registered_as.objects.get(regis_mobile=request.POST.get('cust_num'))
			randOtp=random.randint(1000,9999)
			return HttpResponse(randOtp)
		except Exception as e:
			return HttpResponse('numNotExist')
	else:
		return HttpResponse("Not Access Direct")

def changePass(request):
	if request.session.has_key('login_id'):
		return render(request,'changepass.html')
	else:
		return isLogged(request)