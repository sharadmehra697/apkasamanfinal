from django.urls import path
from home import views
app_name='home'
urlpatterns=[
	path('',views.shopMain, name='Shopmain'),
	path('Registration',views.userRegis.as_view(), name='Registration'),#customer registration if u r login then not open
	path('checkotp',views.checkotp,name='UserLogin'),#for checkotp registration page
	path('Login',views.userLogin.as_view(), name='Login'),#login form not open if u r login already
	path('Shopregis',views.shopkeeperRegis.as_view(), name='ShopRegistration'),#for shop registration
	path('shopverify',views.shopverify,name='shopverify'),#for enter shop verification detail
	path('insertDocument',views.insertDocument,name='insertDocument'),#for insert document in shopverify
	path('insertImage',views.insertImage,name='insertImage'),#for insert imafge in shop verification
	path('delImage',views.delImage,name='delImage'),#for delete image in the shop verification poage
	path('shopaddress',views.showaddress,name='shopaddress'),#for shop enter address
	path('Shopmain',views.shopMain,name='shopMain'),#for shopkeeper home
	path('nameSearch',views.nameSearch,name='nameSearch'),#for database already names
	path('getField',views.showfield,name='getField'),# for getting category fields
	path('getshopitem',views.getshopitem.as_view(),name='getshopitem'),# get shop items inside database
	path('productimage',views.productimage,name='productimage'),# for product image upload 
	path('delProduct',views.delProduct,name='delProduct'),#for product image delete
	path('getSubchild',views.getSubchild, name='getSubchild'),#for subchild category
	path('setItemSession', views.setItemSession.as_view(), name='setItemSession'),#for backend use only not access directly
	path('getShopinventry',views.getShopinventry,name='getShopinventry'),#for getting shop  inventry backend only
	path('updateQuantity',views.updateQuantity,name='updateQuantity'),#for product quantity update
	path('getProductinfo',views.getProductinfo,name='getProductinfo'),#product infor for nventry
	path('getOrdersItems',views.getOrdersItems,name='getOrdersItems'),#for attach shop items not access directly
	path('getupexcel',views.getupexcel,name='getupexcel'),
	path('changeProductdetail',views.changeProductdetail,name='changeProductdetail'),#for inventry product detail change
	path('getOut',views.getOut,name='getOut'),#for logout the user
	path('forgottenPass',views.forgottenPass,name='forgottenPass'),#for forgotton password
	path('forgetsendOtp',views.forgetsendOtp,name='forgetsendOtp'),#for send otp to forget number
	path('changePass',views.changePass,name='changePass'),
]
