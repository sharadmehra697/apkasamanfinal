from django.db import models
import jsonfield
import datetime
import ast

# Create your models here.
class sub_daughter(models.Model):
	sub_daughter_id=models.AutoField(primary_key=True)
	sub_daughter_name=models.CharField(max_length=50)
	sub_daughter_key=models.CharField(max_length=30)
	sub_daughter_childs=models.TextField()
	sub_daughter_parent=models.CharField(max_length=50)

	def __str__(self):
		return self.sub_daughter_key

class sub_child(models.Model):
	sub_child_id=models.AutoField(primary_key=True)
	sub_child_name=models.CharField(max_length=50)
	sub_child_key=models.CharField(max_length=30)
	sub_child_childs=models.ManyToManyField(sub_daughter)
	sub_child_parent=models.CharField(max_length=50)

	def __str__(self):
		return self.sub_child_key

class sub_category(models.Model):
	sub_category_id=models.AutoField(primary_key=True)
	sub_category_name=models.CharField(max_length=50)
	sub_category_key=models.CharField(max_length=30)
	sub_category_parent=models.CharField(max_length=50)
	#sub_category_head=models.ForeignKey('category',on_delete=models.CASCADE)
	sub_category_childs=models.ManyToManyField(sub_child)
	def __str__(self):
		return self.sub_category_key

class category(models.Model):
	category_id=models.AutoField(primary_key=True)
	category_name=models.CharField(max_length=50)
	category_key=models.CharField(max_length=30)
	subcategory=models.ManyToManyField(sub_category)
	category_hold=models.CharField(max_length=100,null=True)
	def __str__(self):
		return self.category_name


def increment_register_id():
	last_id=registered_as.objects.all().order_by('regis_id').last()
	if not last_id:
		return 'AKRI'+ str(datetime.date.today().month).zfill(2)+str(datetime.date.today().day).zfill(2) +'0000'
	major_id=last_id.regis_id
	major_id_int=int(major_id[8:12])
	new_major_id=major_id_int+1
	new_id='AKRI'+str(datetime.date.today().month).zfill(2)+ str(datetime.date.today().day).zfill(2) +str(new_major_id).zfill(4)
	return new_id

class registered_as(models.Model):
	regis_id=models.CharField(primary_key=True,max_length=20,default=increment_register_id,editable=False)
	regis_mobile=models.BigIntegerField(null=True)
	regis_email=models.EmailField(max_length=50,null=True)
	regis_dob=models.DateField(auto_now=False, auto_now_add=False)
	regis_name=models.CharField(max_length=50,null=True)
	regis_image=models.ImageField(upload_to='registered/images', height_field=None, width_field=None,null=True)
	regis_pass=models.CharField(max_length=50,null=True)
	regis_date=models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return self.regis_id

def increment_customer_id():
	last_id=customers.objects.all().order_by('customer_id').last()
	if not last_id:
		return 'ASCT'+ str(datetime.date.today().month).zfill(2)+str(datetime.date.today().day).zfill(2) +'0000'
	major_id=last_id.customer_id
	major_id=int(major_id[8:12])
	new_major_id=major_id+1
	new_id='ASCT'+str(datetime.date.today().month).zfill(2)+ str(datetime.date.today().day).zfill(2) +str(new_major_id).zfill(4)
	return new_id

class customers(models.Model):
	regis_id=models.OneToOneField(registered_as,on_delete=models.CASCADE,max_length=20)
	customer_id=models.CharField(primary_key=True,max_length=20,default=increment_customer_id,editable=False)
	house=models.CharField(max_length=10,null=True)
	street_name=models.CharField(max_length=30,null=True)
	neighbour_street=models.CharField(max_length=30,null=True)
	landmark=models.CharField(max_length=30,null=True)
	pincode=models.IntegerField(null=True)
	city=models.CharField(max_length=10,null=True)
	state=models.CharField(max_length=20,null=True)
	country=models.CharField(max_length=20,null=True)
	longitude=models.DecimalField(max_digits=20, decimal_places=15,default=0.0)
	latitude=models.DecimalField(max_digits=20, decimal_places=15,default=0.0)
	tot_orders=models.TextField(default=0)
	customer_date=models.DateTimeField(auto_now=False, auto_now_add=True)
	address_added=models.BooleanField(default=0)

def increment_shpkpr_id():
	last_id=shopkpr.objects.all().order_by('shopkpr_id').last()
	if not last_id:
		return 'ASSK'+ str(datetime.date.today().month).zfill(2)+str(datetime.date.today().day).zfill(2) +'0000'
	major_id=last_id.shopkpr_id
	major_id=int(major_id[8:12])
	new_major_id=major_id+1
	new_id='ASSK'+str(datetime.date.today().month).zfill(2)+ str(datetime.date.today().day).zfill(2) +str(new_major_id).zfill(4)
	return new_id

class shopkpr(models.Model):
	regis_id=models.OneToOneField(registered_as,on_delete=models.CASCADE,max_length=20)
	shopkpr_id=models.CharField(primary_key=True,max_length=20,default=increment_shpkpr_id,editable=False)
	shop_created=models.BooleanField(default=0)
	shopkpr_name=models.CharField(max_length=30)

	def __str__(self):
		return self.shopkpr_id

def increment_otd_id():
	last_id=otd.objects.all().order_by('otd_id').last()
	if not last_id:
		return 'AOTD'+ str(datetime.date.today().month).zfill(2)+str(datetime.date.today().day).zfill(2) +'0000'
	major_id=last_id.otd_id
	major_id=int(major_id[8:12])
	new_major_id=major_id+1
	new_id='AOTD'+str(datetime.date.today().month).zfill(2)+ str(datetime.date.today().day).zfill(2) +str(new_major_id).zfill(4)
	return new_id

class otd(models.Model):
	regis_id=models.OneToOneField(registered_as,on_delete=models.CASCADE,max_length=20)
	otd_id=models.CharField(primary_key=True,max_length=20,default=increment_otd_id,editable=False)
	city=models.CharField(max_length=20)
	pincode=models.IntegerField(default=0)
	otd_contact=models.BigIntegerField(default=0)
	otd_image=models.ImageField(upload_to='otd/images', height_field=None, width_field=None,null=True)
	otd_otp=models.IntegerField(default=0)
	otd_verified=models.BooleanField(default=0)
	otd_lon=models.DecimalField(max_digits=30,decimal_places=15,default=0)
	otd_lat=models.DecimalField(max_digits=30,decimal_places=15,default=0)
	bike_details=models.CharField(max_length=100,null=True)
	verification_ids=models.CharField(max_length=20)
	live_order=models.CharField(max_length=40,default=0)
	all_order=models.CharField(max_length=40,default=0)
	wallet_id=models.CharField(max_length=20,default=0)
	current_location=models.DecimalField(max_digits=30,decimal_places=5,default=0.0)
	last_location=models.DecimalField(max_digits=30,decimal_places=5,default=0.0)
	otd_rating=models.IntegerField(default=0)
	def __str__(self):
		return self.otd_id

def increment_address_id():
	last_id=customer_address.objects.all().order_by('address_id').last()
	if not last_id:
		return 'ASCA'+ str(datetime.date.today().month).zfill(2)+str(datetime.date.today().day).zfill(2) +'0000'
	major_id=last_id.address_id
	major_id=int(major_id[8:12])
	new_major_id=major_id+1
	new_id='ASCA'+str(datetime.date.today().month).zfill(2)+ str(datetime.date.today().day).zfill(2) +str(new_major_id).zfill(4)
	return new_id

class customer_address(models.Model):
	address_id=models.CharField(primary_key=True,max_length=20,default=increment_address_id,editable=False)
	customer_id=models.OneToOneField(customers,max_length=20,on_delete=models.CASCADE)
	house=models.CharField(max_length=10,null=True)
	street_name=models.CharField(max_length=30,null=True)
	neighbour_street=models.CharField(max_length=30,null=True)
	landmark=models.CharField(max_length=30,null=True)
	pincode=models.IntegerField(null=True)
	state=models.CharField(max_length=20)
	city=models.CharField(max_length=20)
	add_contact=models.BigIntegerField(null=True)
	add_latitude=models.DecimalField(max_digits=30,decimal_places=15,default=0.0)
	add_longitude=models.DecimalField(max_digits=30,decimal_places=15,default=0.0)

class product_images(models.Model):
	img_id=models.AutoField(primary_key=True)
	img_name=models.ImageField(upload_to='Product/Images', height_field=None, width_field=None,null=True)
	img_key=models.CharField(max_length=10)

def increment_product_id():
	last_id=products.objects.all().order_by('product_id').last()
	if not last_id:
		return 'AKPD'+ str(datetime.date.today().month).zfill(2)+str(datetime.date.today().day).zfill(2) +'0000'
	major_id=last_id.product_id
	major_id_int=int(major_id[8:12])
	new_major_id=major_id_int+1
	new_id='AKPD'+str(datetime.date.today().month).zfill(2)+ str(datetime.date.today().day).zfill(2) +str(new_major_id).zfill(4)
	return new_id

class products(models.Model):
	product_id=models.CharField(primary_key=True,max_length=20,default=increment_product_id,editable=False)
	product_name=models.CharField(max_length=100)
	product_price=models.FloatField(default=0)
	product_weight=models.FloatField(default=0)
	product_measure=models.CharField(max_length=20,null=True)
	product_image=models.ManyToManyField(product_images)
	product_quantity=models.IntegerField(null=True)
	product_offer=models.CharField(max_length=30,null=True)
	product_desp=models.CharField(max_length=200,null=True)
	product_category=models.CharField(max_length=20)
	product_subcategory=models.CharField(max_length=20)


	def __str__(self):
		return self.product_id

class pcompany(models.Model):
	pcompany=models.AutoField(primary_key=True)
	product_id=models.OneToOneField('products',on_delete=models.CASCADE,max_length=20)
	company=models.CharField(max_length=50,null=True)
	brand=models.CharField(max_length=50,null=True)

class shpimg(models.Model):
	shpimgid=models.AutoField(primary_key=True)
	shpimg_name=models.ImageField(upload_to='Shop', height_field=None, width_field=None,null=True)
	shpimg_key=models.CharField(max_length=10)
	def __str__(self):
		return self.shpimg_key

class shpdocument(models.Model):
	shpdocumentid=models.AutoField(primary_key=True)
	shpdocument_name=models.ImageField(upload_to='ShopDocument', height_field=None, width_field=None,null=True)
	shpdocument_key=models.CharField(max_length=10)
	def __str__(self):
		return self.shpdocument_key

def increment_shops_id():
	last_id=shops.objects.all().order_by('shop_id').last()
	if not last_id:
		return 'ASSP'+ str(datetime.date.today().month).zfill(2)+str(datetime.date.today().day).zfill(2) +'0000'
	major_id=last_id.shop_id
	major_id=int(major_id[8:12])
	new_major_id=major_id+1
	new_id='ASSP'+str(datetime.date.today().month).zfill(2)+ str(datetime.date.today().day).zfill(2) +str(new_major_id).zfill(4)
	return new_id

class shops(models.Model):
	shop_id=models.CharField(primary_key=True,max_length=20,default=increment_shops_id,editable=False)
	shopkpr_id=models.OneToOneField(shopkpr,on_delete=models.CASCADE,max_length=20)
	shop_name=models.CharField(max_length=50,null=True)
	shop_type=models.ManyToManyField(category)
	shop_open=models.TimeField(auto_now_add=False, blank=True,null=True)
	shop_close=models.TimeField(auto_now_add=False, blank=True,null=True)
	shop_holiday=models.CharField(max_length=20, null=True)
	shop_rating=models.IntegerField(default=0)
	shop_orders=models.TextField(null=True)
	shop_sale=models.DecimalField(max_digits=20,decimal_places=2,default=0.0)
	shop_liveorders=models.TextField(null=True)
	unpacked_orders=models.TextField(null=True)
	shop_verified=models.BooleanField(default=0)
	shop_products=models.ManyToManyField(products)
	shop_image=models.ManyToManyField(shpimg)
	shop_document=models.ManyToManyField(shpdocument)
	shop_address=models.BooleanField(default=0)
	def __str__(self):
		return self.shop_name

def increment_cart_item_id():
	last_id=cart_items.objects.all().order_by('cart_items_id').last()
	if not last_id:
		return 'CART'+ str(datetime.date.today().month).zfill(2)+str(datetime.date.today().day).zfill(2) +'0000'
	major_id=last_id.cart_items_id
	major_id=int(major_id[8:12])
	new_major_id=major_id+1
	new_id='CART'+str(datetime.date.today().month).zfill(2)+ str(datetime.date.today().day).zfill(2) +str(new_major_id).zfill(4)
	return new_id

class cart_items(models.Model):
	cart_items_id=models.CharField(primary_key=True,max_length=20,default=increment_cart_item_id,editable=False)
	customer_id=models.OneToOneField(customers,on_delete=models.CASCADE,max_length=20)
	product_id=models.OneToOneField(products,on_delete=models.CASCADE,max_length=20)
	shop_id=models.OneToOneField(shops,on_delete=models.CASCADE,max_length=20)
	quantity=models.IntegerField()
	size=models.CharField(max_length=30,null=True)
	color=models.CharField(max_length=30,null=True)
	weight=models.DecimalField(max_digits=20, decimal_places=2)
	measure=models.CharField(max_length=20,default='None')
	amount=models.DecimalField(max_digits=20, decimal_places=2)
	discount=models.DecimalField(max_digits=20, decimal_places=2,null=True)
	cart_item_life=models.BooleanField()

	def __str__(self):
		return self.cart_items_id

def increment_order_id():
	last_id=orders.objects.all().order_by('order_id').last()
	if not last_id:
		return 'ASOD'+ str(datetime.date.today().month).zfill(2)+str(datetime.date.today().day).zfill(2) +'0000'
	major_id=last_id.order_id
	major_id=int(major_id[8:12])
	new_major_id=major_id+1
	new_id='ASOD'+str(datetime.date.today().month).zfill(2)+ str(datetime.date.today().day).zfill(2) +str(new_major_id).zfill(4)
	return new_id

class orders(models.Model):
	order_id=models.CharField(primary_key=True,max_length=20,default=increment_order_id,editable=False)
	customer_id=models.OneToOneField(customers,on_delete=models.CASCADE,max_length=20)
	order_amount=models.DecimalField(max_digits=20, decimal_places=2)
	offers_apllied=models.CharField(max_length=50,null=True)
	discount_value=models.DecimalField(max_digits=20,decimal_places=2,null=True)
	payment_option=models.CharField(max_length=20)
	delivery_address=models.CharField(max_length=100)
	cart_items_id=models.CharField(max_length=100)
	order_weight=models.DecimalField(max_digits=20,decimal_places=2)
	order_estimatedtime=models.DateTimeField(auto_now=False, auto_now_add=False,null=True)
	order_quantity=models.IntegerField()
	order_datetime=models.DateTimeField(auto_now=False,auto_now_add=True)
	order_attemptby=models.CharField(max_length=20,null=True)
	order_verficationlevel=models.CharField(max_length=20,null=True)
	order_location=models.DecimalField(max_digits=20,decimal_places=2,null=True)
	order_deliverytime=models.DateTimeField(auto_now=False, auto_now_add=False,null=True)
	order_rate=models.IntegerField(null=True)
	order_packagingstatus=models.IntegerField(null=True)
	order_package_shop=models.CharField(max_length=100,null=True)
	order_package_done=models.CharField(max_length=100,null=True)
	order_payment=models.BooleanField(null=True)
	order_shops=models.CharField(max_length=100)
	order_pickup_longitude=models.DecimalField(max_digits=30,decimal_places=5,null=True)
	order_pickup_latitude=models.DecimalField(max_digits=30,decimal_places=5,null=True)
	payment_id=models.CharField(max_length=30,null=True)
	order_key=models.IntegerField(null=True)
	otd_key=models.IntegerField(null=True)
	order_completed=models.BooleanField(default=0)
	order_attempted=models.BooleanField(default=0)
	otd_assigned=models.BooleanField(default=0)
	assigned_otd=models.CharField(max_length=50,null=True)

	def __str__(self):
		return self.order_id
def increment_payment_id():
	last_id=payments.objects.all().order_by('payment_id').last()
	if not last_id:
		return 'ASPD'+ str(datetime.date.today().month).zfill(2)+str(datetime.date.today().day).zfill(2) +'0000'
	major_id=last_id.payment_id
	major_id=int(major_id[8:12])
	new_major_id=major_id+1
	new_id='ASPD'+str(datetime.date.today().month).zfill(2)+ str(datetime.date.today().day).zfill(2) +str(new_major_id).zfill(4)
	return new_id

class payments(models.Model):
	payment_id=models.CharField(primary_key=True,max_length=20,default=increment_payment_id,editable=False)
	unique_pay=models.CharField(max_length=30,null=True)
	order_id=models.CharField(max_length=20,null=True)
	card_detail=models.BigIntegerField(null=True)
	customer_id=models.CharField(max_length=30)
	wallet_id=models.CharField(max_length=30,null=True)
	bankdetail=models.CharField(max_length=50,null=True)
	payment_status=models.IntegerField(default=0)
	def __str__(self):
		return self.payment_id
class vshopimg(models.Model):
	vshopimgid=models.AutoField(primary_key=True)
	vimage=models.ImageField(upload_to='shopVerify/Images', height_field=None, width_field=None,null=True)

class verify_shopid(models.Model):
	verify_id=models.AutoField(primary_key=True)
	shop_id=models.OneToOneField(shops,on_delete=models.CASCADE,max_length=20)
	verify_type=models.CharField(max_length=20)
	verify_no=models.CharField(max_length=20)
	verify_images=models.ManyToManyField(vshopimg)

def increment_id():
	last_booking=justExample.objects.all().order_by('ide').last()
	if not last_booking:
		return 'ASSP'+ str(datetime.date.today().month).zfill(2)+str(datetime.date.today().day).zfill(2) +'0000'
	booking=last_booking.ide
	booking_int=int(booking[8:12])
	new_booking_int=booking_int +1
	new_id='ASSP'+str(datetime.date.today().month).zfill(2)+ str(datetime.date.today().day).zfill(2) +str(new_booking_int).zfill(4)
	return new_id

class justExample(models.Model):
	ide=models.CharField(primary_key=True,max_length=20,default = increment_id, editable=False)
	name=models.CharField(max_length=20)
	key= models.CharField(max_length=20)
	def __str__(self):
		return "%s %s" %(self.name,self.key)

class getExample(models.Model):
	geta=models.ManyToManyField(category)
	ide=models.OneToOneField(justExample,on_delete=models.CASCADE,primary_key=True)

	def __str__(self):
		return self.geta

	def save(self,*args,**kwargs):
		super(getExample, self).save(*args, **kwargs)
	
class colorTable(models.Model):
	colorid=models.AutoField(primary_key=True)
	colorname=models.CharField(max_length=30)
	catname=models.CharField(max_length=20,default=0)

class sizeTable(models.Model):
	sizeid=models.AutoField(primary_key=True)
	sizename=models.CharField(max_length=30)
	catname=models.CharField(max_length=20,default=0)

class typeTable(models.Model):
	typeid=models.AutoField(primary_key=True)
	typename=models.CharField(max_length=30)
	catname=models.CharField(max_length=20,default=0)

class statMaterial(models.Model):
	materialid=models.AutoField(primary_key=True)
	materialname=models.CharField(max_length=30)
	catname=models.CharField(max_length=20,default=0)

class outMaterial(models.Model):
	materialid=models.AutoField(primary_key=True)
	materialname=models.CharField(max_length=30)
	catname=models.CharField(max_length=20,default=0)

class inMaterial(models.Model):
	materialid=models.AutoField(primary_key=True)
	materialname=models.CharField(max_length=30)
	catname=models.CharField(max_length=20,default=0)

class soleMaterial(models.Model):
	materialid=models.AutoField(primary_key=True)
	materialname=models.CharField(max_length=30)
	catname=models.CharField(max_length=20,default=0)

class proposeTable(models.Model):
	proposeid=models.AutoField(primary_key=True)
	proposename=models.CharField(max_length=20)
	catname=models.CharField(max_length=20,default=0)

class shapeTable(models.Model):
	shapeid=models.AutoField(primary_key=True)
	shapename=models.CharField(max_length=20)
	catname=models.CharField(max_length=20,default=0)

class animalTable(models.Model):
	animalid=models.AutoField(primary_key=True)
	animalname=models.CharField(max_length=20)
	catname=models.CharField(max_length=20,default=0)

class flavourTable(models.Model):
	flavourid=models.AutoField(primary_key=True)
	flavourname=models.CharField(max_length=20)
	catname=models.CharField(max_length=20,default=0)

class bookSpecification(models.Model):
	book_id=models.AutoField(primary_key=True)
	product_id=models.OneToOneField(products,on_delete=models.CASCADE,max_length=20)
	author=models.CharField(max_length=20)
	editor=models.CharField(max_length=20)
	addition=models.CharField(max_length=20)
	publication=models.CharField(max_length=20)

class stationary(models.Model):
	statid=models.AutoField(primary_key=True)
	product_id=models.OneToOneField(products,on_delete=models.CASCADE,max_length=20)
	color=models.ManyToManyField(colorTable)
	typeid=models.ForeignKey(typeTable,on_delete=models.CASCADE,max_length=20)
	refillable=models.CharField(max_length=20,null=True)
	captype=models.CharField(max_length=20,null=True)
	size=models.ForeignKey(sizeTable,on_delete=models.CASCADE,max_length=20)
	pages=models.IntegerField(null=True)
	rulled_type=models.CharField(max_length=20,null=True)
	binding=models.CharField(max_length=20,null=True)
	materialid=models.ForeignKey(statMaterial,on_delete=models.CASCADE,max_length=20)
	packsize=models.CharField(max_length=20,null=True)

class footware(models.Model):
	footwareid=models.AutoField(primary_key=True)
	product_id=models.OneToOneField(products,on_delete=models.CASCADE,max_length=20)
	color=models.ManyToManyField(colorTable)
	gender=models.CharField(max_length=20,null=True)
	size=models.OneToOneField(sizeTable,on_delete=models.CASCADE,max_length=20)
	materialid=models.OneToOneField(statMaterial,on_delete=models.CASCADE,max_length=20)
	typeid=models.OneToOneField(typeTable,on_delete=models.CASCADE,max_length=20)
	closure=models.CharField(max_length=20,null=True)
	solematerial=models.OneToOneField(soleMaterial,on_delete=models.CASCADE,max_length=20)
	healtype=models.IntegerField(null=True)
	agegroup=models.CharField(max_length=20,null=True)
	warranty=models.CharField(max_length=20,null=True)
	guarantee=models.CharField(max_length=20,null=True)
	occassion=models.CharField(max_length=20,null=True)


class bags(models.Model):
	bagid=models.AutoField(primary_key=True)
	product_id=models.OneToOneField(products,on_delete=models.CASCADE,max_length=20)
	color=models.ManyToManyField(colorTable)
	materialid=models.OneToOneField(statMaterial,on_delete=models.CASCADE,max_length=20)
	outtermaterial=models.OneToOneField(outMaterial,on_delete=models.CASCADE,max_length=20)
	innermaterial=models.OneToOneField(inMaterial,on_delete=models.CASCADE,max_length=20)
	capacity=models.CharField(max_length=20,null=True)
	sizespecification=models.OneToOneField(sizeTable,on_delete=models.CASCADE,max_length=20)
	warranty=models.CharField(max_length=20,null=True)
	guarantee=models.CharField(max_length=20,null=True)
	typeid=models.OneToOneField(typeTable,on_delete=models.CASCADE,max_length=20)

class clothing(models.Model):
	clothingid=models.AutoField(primary_key=True)
	product_id=models.OneToOneField(products,on_delete=models.CASCADE,max_length=20)
	color=models.ManyToManyField(colorTable)
	materialid=models.ForeignKey(statMaterial,on_delete=models.CASCADE,max_length=20)
	typespecification=models.ForeignKey(typeTable,on_delete=models.CASCADE,max_length=20)
	sizes=models.ForeignKey(sizeTable,on_delete=models.CASCADE,max_length=20)
	agegroup=models.CharField(max_length=20,null=True)
	occasion=models.CharField(max_length=20,null=True)
	gender=models.CharField(max_length=20,null=True)

class kirana(models.Model):
	kiranaid=models.AutoField(primary_key=True)
	product_id=models.OneToOneField(products,on_delete=models.CASCADE,max_length=20)
	pricekg=models.IntegerField(null=True)
	packedtype=models.CharField(max_length=20,null=True)
	typeid=models.ForeignKey('typeTable',on_delete=models.CASCADE,max_length=20,null=True)
	expdate=models.DateField(auto_now=False,auto_now_add=False,null=True)
	flavour=models.ForeignKey('flavourTable',on_delete=models.CASCADE,max_length=20,null=True)
	propose=models.ForeignKey('proposeTable',on_delete=models.CASCADE,max_length=20,null=True)
	animal=models.ForeignKey('animalTable',on_delete=models.CASCADE,max_length=20,null=True)
	shape=models.ForeignKey('shapeTable',on_delete=models.CASCADE,max_length=20,null=True)
	vegtype=models.BooleanField(default=1,null=True)


class subfields(models.Model):
	fid=models.AutoField(primary_key=True)
	fname=models.CharField(max_length=20)
	fkey=models.CharField(max_length=10)
	color=models.BooleanField(default=0)
	typeid=models.BooleanField(default=0)
	refillable=models.BooleanField(default=0)
	captype=models.BooleanField(default=0)
	size=models.BooleanField(default=0)
	pages=models.BooleanField(default=0)
	rulled_type=models.BooleanField(default=0)
	binding=models.BooleanField(default=0)
	materialid=models.BooleanField(default=0)
	packsize=models.BooleanField(default=0)
	gender=models.BooleanField(default=0)
	closure=models.BooleanField(default=0)
	solematerial=models.BooleanField(default=0)
	healtype=models.BooleanField(default=0)
	warranty=models.BooleanField(default=0)
	guarantee=models.BooleanField(default=0)
	agegroup=models.BooleanField(default=0)
	occasion=models.BooleanField(default=0)
	outtermaterial=models.BooleanField(default=0)
	innermaterial=models.BooleanField(default=0)
	capacity=models.BooleanField(default=0)
	pricekg=models.BooleanField(default=0)
	packedtype=models.BooleanField(default=0)
	expdate=models.BooleanField(default=0)
	flavour=models.BooleanField(default=0)
	propose=models.BooleanField(default=0)
	animal=models.BooleanField(default=0)
	shape=models.BooleanField(default=0)
	vegtype=models.BooleanField(default=1)
	parentdb=models.CharField(max_length=10,default=0)


#for permanent database

def increment_perprod_id():
	last_id=perprod.objects.all().order_by('perprod_id').last()
	if not last_id:
		return 'AKPP'+ str(datetime.date.today().month).zfill(2)+str(datetime.date.today().day).zfill(2) +'0000'
	major_id=last_id.perprod_id
	major_id_int=int(major_id[8:12])
	new_major_id=major_id_int+1
	new_id='AKPP'+str(datetime.date.today().month).zfill(2)+ str(datetime.date.today().day).zfill(2) +str(new_major_id).zfill(4)
	return new_id

class perprod(models.Model):
	perprod_id=models.CharField(primary_key=True,max_length=20,default=increment_perprod_id,editable=False)
	product_name=models.CharField(max_length=100)
	product_price=models.FloatField(default=0)
	product_weight=models.FloatField(default=0)
	product_measure=models.CharField(max_length=20,null=True)
	product_image=models.ManyToManyField(product_images)
	product_quantity=models.IntegerField(null=True)
	product_offer=models.CharField(max_length=30,null=True)
	product_desp=models.CharField(max_length=200,null=True)
	product_category=models.CharField(max_length=20)
	product_subcategory=models.CharField(max_length=20)

	def __str__(self):
		return self.perprod_id

class perkirana(models.Model):
	perkiranaid=models.AutoField(primary_key=True)
	perprod_id=models.OneToOneField('perprod',on_delete=models.CASCADE,max_length=20)
	pricekg=models.IntegerField(null=True)
	packedtype=models.CharField(max_length=20,null=True)
	typeid=models.ForeignKey('typeTable',on_delete=models.CASCADE,max_length=20,null=True)
	expdate=models.DateField(auto_now=False,auto_now_add=False,null=True)
	flavour=models.ForeignKey('flavourTable',on_delete=models.CASCADE,max_length=20,null=True)
	propose=models.ForeignKey('proposeTable',on_delete=models.CASCADE,max_length=20,null=True)
	animal=models.ForeignKey('animalTable',on_delete=models.CASCADE,max_length=20,null=True)
	shape=models.ForeignKey('shapeTable',on_delete=models.CASCADE,max_length=20,null=True)
	vegtype=models.BooleanField(default=1,null=True)

class perpcompany(models.Model):
	perpcompany=models.AutoField(primary_key=True)
	perprod_id=models.OneToOneField('perprod',on_delete=models.CASCADE,max_length=20)
	company=models.CharField(max_length=50,null=True)
	brand=models.CharField(max_length=50,null=True)