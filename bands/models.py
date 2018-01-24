from django.db import models

# Create your models here.
class User_Data(models.Model):
    user_id = models.AutoField(primary_key=True,max_length=15)
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    user_email=models.EmailField(max_length=50,null=False)
    user_password=models.TextField(max_length=15,null=False)
    user_phone_no=models.CharField(max_length=12,null=False)

class Product_Ad(models.Model):
    ad_title = models.TextField(max_length=200,null=False)
    product_category = models.CharField(max_length=20,null=False)
    product_subcategory = models.CharField(max_length=20,null=False)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    product_description = models.TextField(max_length=1000,null=True)
    price = models.IntegerField(max_length=15,null=False)
    user_data = models.ForeignKey('User_Data',on_delete=models.CASCADE)
    ad_id = models.AutoField(primary_key=True,max_length=15)
    cover_image=models.ImageField(upload_to='static/product_cover_image/',null=True,blank=True)

class Images(models.Model):
    image_id = models.AutoField(primary_key=True,max_length=15)
    image_path = models.ImageField(upload_to='static/product_images/',null=True,blank=True)
    product_ad=models.ForeignKey('Product_Ad',on_delete=models.CASCADE)

class Category(models.Model):
    cat_id=models.AutoField(primary_key=True,max_length=15)
    cat_name=models.CharField(max_length=20)
    cat_image=models.ImageField(upload_to='static/category_images/',null=True,blank=True)

class SubCategory(models.Model):
    category=models.ForeignKey('Category',on_delete=models.CASCADE)
    subcat_id=models.AutoField(primary_key=True,max_length=15)
    subcat_name=models.CharField(max_length=20)

class Attributes(models.Model):
    subcategory=models.ForeignKey('SubCategory',on_delete=models.CASCADE)
    attribute_name=models.CharField(max_length=20)
    Att_id=models.AutoField(primary_key=True,max_length=15)

class Product_attribute(models.Model):
    product=models.ForeignKey('Product_Ad',on_delete=models.CASCADE)
    attributes=models.ForeignKey('Attributes',on_delete=models.CASCADE)
    attribute_value=models.CharField(max_length=30)