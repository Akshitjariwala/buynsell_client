from django.template.response import TemplateResponse
from django.http import HttpResponse
from .models import User_Data,Category,SubCategory,Attributes,Product_attribute,Product_Ad,Images
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
# Create your views here.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
session = []

def updateuser(request):
    if not "active_user" in request.session:
        return login(request)
        # request.session['admin']="admin@gmail.com"
    if request.method == 'POST':
        f_name = request.POST['uname']
        l_name = request.POST['usurname']
        u_email = request.POST['uemail']
        old_pass = request.POST['oldpassword']
        new_pass = request.POST['upassword']
        re_pass = request.POST['cpassword']
        phone_no = request.POST['uphonenumber']
        old_email = request.session['active_user']
        old_user_data = User_Data.objects.filter(user_email=old_email)
        if not old_pass == old_user_data[0].user_password:
            return TemplateResponse(request, "edit_profile.html",
                                    {'Error': "Old Password did not matched", 'user_data': old_user_data})
        else:
            if not new_pass == re_pass:
                return TemplateResponse(request, "edit_admin.html",
                                        {'Error': "Password not matched", 'user_data': old_user_data})
            else:
                old_user_data[0].first_name = f_name
                old_user_data[0].last_name = l_name
                old_user_data[0].user_password = new_pass
                old_user_data[0].user_phone_no = phone_no
                old_user_data[0].save()
                return TemplateResponse(request, "edit_profile.html",
                                        {'Success': "Updated", 'user_data': old_user_data})


    else:
        user_email = request.session['active_user']
        userobj = User_Data.objects.filter(user_email=user_email)
        return render(request, 'edit_profile.html', {'user_data': userobj})

def product_page(request):
    id = request.GET.get('ad_id')
    email = request.session['active_user']
    active_user = User_Data.objects.filter(user_email = email)
    images_list = Images.objects.filter(product_ad_id=id)
    images = []
    for image in images_list:
        images.append(image.image_path)
    product_obj = Product_Ad.objects.filter(ad_id=id)

    first_name = request.session['first_name']
    last_name = request.session['last_name']
    return render(request,'product_page.html',{"user_data":active_user,"email":email,"image_list":images,"product":product_obj,"first_name":first_name,"last_name":last_name})

def category_page(request):
    first_name = request.session['first_name']
    last_name = request.session['last_name']
    category_data = Category.objects.all()
    subcategory_data = SubCategory.objects.all()
    category_name = request.GET.get('category')
    Data = Product_Ad.objects.filter(product_category=category_name)
    return render(request, 'category_page.html', {"category_data": category_data, "subcategory_data": subcategory_data,"productCategoryData":Data,"first_name":first_name,"last_name":last_name})

def submit_ad(request):
    attr = []
    attr_ids = []
    y = 0
    first_name = request.session['first_name']
    last_name = request.session['last_name']
    user_id = request.session['user_id']
    title = request.POST['ad_title']
    ad_price = request.POST['ad_price']
    description = request.POST['ad_description']
    category =  request.POST['category_select']
    subcat = request.POST['subcategory_select']
    ad_city = request.POST['secondlist']
    ad_state = request.POST['listBox']
    ad_cover_image = request.FILES['cover_image']
    image1 = request.FILES['item_photo1']
    image2 = request.FILES['item_photo2']
    image3 = request.FILES['item_photo3']
    fs1 = FileSystemStorage(location=os.path.join(BASE_DIR,'static/product_cover_image'))
    Cover_image = fs1.save(ad_cover_image.name,ad_cover_image)
    fs2 = FileSystemStorage(location=os.path.join(BASE_DIR,'static/product_images'))
    coverimage = fs2.save(ad_cover_image.name,ad_cover_image)
    Image1 = fs2.save(image1.name,image1)
    Image2 = fs2.save(image2.name,image2)
    Image3 = fs2.save(image3.name,image3)
    product_obj = Product_Ad(ad_title=title,product_category=category,product_subcategory=subcat,city=ad_city,state=ad_state,product_description=description,price=ad_price,cover_image='/static/product_cover_image/'+ad_cover_image.name,user_data_id=user_id)
    product_obj.save()
    product_id_ref = Product_Ad.objects.get(ad_title=title)
    product_id = product_id_ref.ad_id
    coverupload = Images(image_path='/static/product_images/'+ad_cover_image.name,product_ad_id=product_id)
    coverupload.save()
    imageupload1 = Images(image_path='/static/product_images/'+image1.name,product_ad_id=product_id)
    imageupload1.save()
    imageupload2 = Images(image_path='/static/product_images/' + image2.name, product_ad_id=product_id)
    imageupload2.save()
    imageupload3 = Images(image_path='/static/product_images/' + image3.name, product_ad_id=product_id)
    imageupload3.save()
    length = request.POST['attributes_length']
    length = int(length)
    subcat_list = SubCategory.objects.filter(subcat_name=subcat)
    subcat_id = subcat_list[0].subcat_id

    for x in range(0,length):
        x = str(x)
        temp = request.POST.get(x,'')
        attr.append(temp)

    attribute_list = Attributes.objects.filter(subcategory_id=subcat_id)

    for x in range(0,length):
        attr_ids.append(attribute_list[x].Att_id)

    for attri in attr:
        if y < length:
            attr_id = attr_ids[y]
            attri_obj = Product_attribute(attribute_value=attri,attributes_id=attr_id,product_id=product_id)
            attri_obj.save()
            y =+ 1

    success_msg = "Your ad is successlly posted"
    return TemplateResponse(request,"postad.html",{"Success_msg":success_msg})

def ad_review(request):
    return render(request,'ad_review.html')

def admin(request):
    return render(request,'admin.html')

def homepage(request):
        queryset = Category.objects.all()
        first_name = request.session['first_name']
        last_name = request.session['last_name']
        subcategory_data = SubCategory.objects.all()
        return render(request, "homepage.html", {"category_data": queryset,"first_name":first_name,"last_name":last_name,"subcategory_data":subcategory_data})

def signup(request):
    return render(request,"signup.html")

def checkEmailandPassword(request):
    email = request.POST['uemail']
    password = request.POST['upassword']
    confirmpassword = request.POST['cpassword']
    user = User_Data.objects.filter(user_email=email)
    if user.count() == 0:
        if password == confirmpassword:
            return addUser(request)
        else:
            passwordError = "Both Password should match."
            return TemplateResponse(request, "signup.html", {"Error": passwordError})
    else:
        emailError = "Email address already exists."
        return TemplateResponse(request, "signup.html", {"Error": emailError})

def onaddCategoryclick(request):
    cats = Category.objects.all()
    if session:
       session[:] = []
    return render(request,'onaddCategoryclick.html',{'cats':cats})

def saveCategory(request):
    if request.method == 'POST':
        radio = request.POST.get('optradio',None)
        if radio == 'existing':
            category = request.POST.get('cat_option',None)
            cat = Category.objects.filter(cat_name=category)
            cat_message=""
            subcategory = request.POST.get('sub_cat', None)
            subcatobj = SubCategory(subcat_name=subcategory,category_id=cat[0].cat_id)
            subcatobj.save()
            subcat_message = subcategory+" Added.."
            att_message=""
            for x in session:
                att_value = x
                attobj = Attributes(attribute_name=att_value,subcategory_id=subcatobj.subcat_id)
                attobj.save()
                att_message = att_message+" "+x+" att added"
            msg_list={cat_message,subcat_message,att_message}
            return render(request,'result.html',{'msg_list':msg_list})
        if radio == 'new':
            category = request.POST.get('new_cat',None)
            image = request.FILES['category_image']
            fs=FileSystemStorage(location=os.path.join(BASE_DIR,'static/category_images'))
            filename = fs.save(image.name,image)
            catobj = Category(cat_name=category,cat_image='/static/category_images/'+image.name)
            catobj.save()
            cat_message = category+" Added"
            subcategory = request.POST.get('sub_cat', None)
            subcatobj = SubCategory(subcat_name=subcategory,category_id=catobj.cat_id)
            subcatobj.save()
            subcat_message = subcategory+" Added.."
            att_message=""
            for x in session:
                att_value = x
                attobj = Attributes(attribute_name=att_value,subcategory_id=subcatobj.subcat_id)
                attobj.save()
                att_message = att_message+" "+x+" att added. "
            msg_list = {cat_message,subcat_message,att_message}
            return render(request,'result.html',{'msg_list':msg_list})

@csrf_exempt
def addtosession(request):
    att_value = request.POST['myvalue']
    if not att_value in session:
        session.append(att_value)
        request.session[att_value] = att_value
        return HttpResponse(att_value+" added..")
    else:
        return HttpResponse("Attribute already added.!")

@csrf_exempt
def deletefromsession(request):
    att_value = request.POST['myvalue']
    if att_value in session:
        session.remove(att_value)
        del request.session[att_value]
        return HttpResponse(att_value+" deleted..")
    else:
        return HttpResponse("Attribute Not found..!")

def addUser(request):
    if request.method == 'POST':
        username = request.POST['uname']
        lastname = request.POST['usurname']
        email = request.POST['uemail']
        password = request.POST['upassword']
        confirmpassword = request.POST['cpassword']
        phone_no = request.POST['uphonenumber']
        userdata = User_Data(first_name=username ,last_name=lastname,user_email=email,user_password=password,user_phone_no=phone_no)
        userdata.save()
        return TemplateResponse(request,"login.html",{})

def login(request):
    if "active_admin" in request.session:
        return admin(request)
    elif "active_user" in request.session:
        return homepage(request)
    else:
        return render(request,'login.html')

def loginValidation(request):
    email_id = request.POST['uemail']
    password = request.POST['upassword']

    user = User_Data.objects.filter(user_email = email_id)
    user_firstname = user[0].first_name
    user_lastname = user[0].last_name
    user_id = user[0].user_id

    if user:
        correct_password = user[0].user_password
        if password == correct_password:
            if email_id == 'admin@gmail.com':
                request.session['active_admin'] = email_id
                request.session['first_name'] = user_firstname
                request.session['last_name'] = user_lastname
                request.session['user_id'] = user_id
                return admin(request)
            else:
                request.session['active_user'] = email_id
                request.session['first_name'] = user_firstname
                request.session['last_name'] = user_lastname
                request.session['user_id'] = user_id
                successMessage = "You are successfully logged in."
                return homepage(request)
        else:
            errorMessage = "Invalid credentials inserted"
            return TemplateResponse(request, "login.html", {"Success": errorMessage})
    else:
        errorMessage = "Email does not exist!"
        return TemplateResponse(request, "login.html", {"Success": errorMessage})

def ondeletecategoryclick(request):
    cat=Category.objects.all()
    sub_cat=SubCategory.objects.all()
    att=Attributes.objects.all()
    return render(request,'deletecategory.html',{'cat':cat,'sub_cat':sub_cat,'att':att})
	
@csrf_exempt
def delete_att(request):
    return HttpResponse("Response..!!")

def post_ad(request):
    if not "active_user" in request.session:
        return login(request)
    first_name = request.session['first_name']
    last_name = request.session['last_name']
    post_data = Product_Ad.objects.all()
    category_data = Category.objects.all()
    subcategory_data = SubCategory.objects.all()
    attributes_data = Attributes.objects.all()
    return render(request,'postad.html', {"category_data": category_data,"subcategory_data":subcategory_data,"attributes_data":attributes_data,"first_name":first_name,"last_name":last_name})

def logout(request):
    if "active_admin" in request.session:
        del request.session['active_admin']
    if "active_user" in request.session:
        del request.session['active_user']
    return login(request)

def search_result(request):
    if not "active_user" in request.session:
        return login(request)
    first_name = request.session['first_name']
    last_name = request.session['last_name']
    category_list = Category.objects.all()
    subcategory_list = SubCategory.objects.all()
    global ad_list
    if request.method == 'POST':
        state = request.POST['listBox']
        city = request.POST['secondlist']
        category = request.POST['category_select']
        sub_category = request.POST['subcategory_select']
        search_text = request.POST['search_text']
        if search_text is not None:
            ad_list = Product_Ad.objects.filter(product_description__icontains = search_text)
            request.session['search_text'] = search_text
            if state == 'SELECT STATE':
                if "selected_city" in request.session:
                    del request.session['selected_city']
                if "selected_state" in request.session:
                    del request.session['selected_state']
                if category == 'Category':
                    if "selected_subcategory" in request.session:
                        del request.session['selected_subcategory']
                    if "selected_category" in request.session:
                        del request.session['selected_category']
                    ad_list = ad_list.all()
                else:
                    request.session['selected_category'] = category
                    if sub_category == 'Sub Category':
                        if "selected_subcategory" in request.session:
                            del request.session['selected_subcategory']
                        ad_list = ad_list.filter(product_category=category)
                    else:
                        request.session['selected_subcategory'] = sub_category
                        ad_list = ad_list.filter(product_category=category, product_subcategory=sub_category)
            else:
                request.session['selected_state'] = state
                if city == 'Select city':
                    if "selected_city" in request.session:
                        del request.session['selected_city']
                    if category == 'Category':
                        if "selected_category" in request.session:
                            del request.session['selected_category']
                        if "selected_subcategory" in request.session:
                            del request.session['selected_subcategory']
                        ad_list = ad_list.filter(state=state)
                    else:
                        request.session['selected_category'] = category
                        if sub_category == 'Sub Category':
                            if "selected_subcategory" in request.session:
                                del request.session['selected_subcategory']
                            ad_list = ad_list.filter(state=state, product_category=category)
                        else:
                            request.session['selected_subcategory'] = sub_category
                            ad_list = ad_list.filter(state=state, product_category=category, product_subcategory=sub_category)
                else:
                    request.session['selected_city'] = city
                    if category == 'Category':
                        if "selected_category" in request.session:
                            del request.session['selected_category']
                        if "selected_subcategory" in request.session:
                            del request.session['selected_subcategory']
                        ad_list = ad_list.filter(state=state, city=city)
                    else:
                        request.session['selected_category'] = category
                        if sub_category == 'Sub Category':
                            if "selected_subcategory" in request.session:
                                del request.session['selected_subcategory']
                            ad_list = ad_list.filter(state=state, city=city, product_category=category)
                        else:
                            request.session['selected_subcategory'] = sub_category
                            ad_list = ad_list.filter(state=state, city=city, product_category=category, product_subcategory=sub_category)
        else:
            if "search_text" in request.session:
                del request.session['search_text']
            ad_list = Product_Ad.objects.all()
            if state == 'SELECT STATE':
                if "selected_city" in request.session:
                    del request.session['selected_city']
                if "selected_state" in request.session:
                    del request.session['selected_state']
                if category == 'Category':
                    if "selected_subcategory" in request.session:
                        del request.session['selected_subcategory']
                    if "selected_category" in request.session:
                        del request.session['selected_category']
                    ad_list = ad_list.all()
                else:
                    request.session['selected_category'] = category
                    if sub_category == 'Sub Category':
                        if "selected_subcategory" in request.session:
                            del request.session['selected_subcategory']
                        ad_list = ad_list.filter(product_category=category)
                    else:
                        request.session['selected_subcategory'] = sub_category
                        ad_list = ad_list.filter(product_category=category, product_subcategory=sub_category)
            else:
                request.session['selected_state'] = state
                if city == 'Select city':
                    if "selected_city" in request.session:
                        del request.session['selected_city']
                    if category == 'Category':
                        if "selected_subcategory" in request.session:
                            del request.session['selected_subcategory']
                        if "selected_category" in request.session:
                            del request.session['selected_category']
                        ad_list = ad_list.filter(state=state)
                    else:
                        request.session['selected_category'] = category
                        if sub_category == 'Sub Category':
                            if "selected_subcategory" in request.session:
                                del request.session['selected_subcategory']
                            ad_list = ad_list.filter(state=state, product_category=category)
                        else:
                            request.session['selected_subcategory'] = sub_category
                            ad_list = ad_list.filter(state=state, product_category=category, product_subcategory=sub_category)
                else:
                    request.session['selected_city'] = city
                    if category == 'Category':
                        if "selected_subcategory" in request.session:
                            del request.session['selected_subcategory']
                        if "selected_category" in request.session:
                            del request.session['selected_category']
                        ad_list = ad_list.filter(state=state, city=city)
                    else:
                        request.session['selected_category'] = category
                        if sub_category == 'Sub Category':
                            if "selected_subcategoy" in request.session:
                                del request.session['selected_subcategory']
                            ad_list = ad_list.filter(state=state, city=city, product_category=category)
                        else:
                            request.session['selected_subcategory'] = sub_category
                            ad_list = ad_list.filter(state=state, city=city, product_category=category, product_subcategory=sub_category)
        # print(ad_list.values())
        page = request.GET.get('page', 1)
        paginator = Paginator(ad_list, 5)
        # try:
        #     paginator = Paginator(ad_list, 5)
        # except :
        #     print("hello")
        try:
            adobj = paginator.page(page)
        except PageNotAnInteger:
            adobj = paginator.page(1)
        except EmptyPage:
            adobj = paginator.page(paginator.num_pages)
        # request.session['ad_list'] = ad_list
        return render(request, 'search_result.html', {'ads': adobj, 'cat_list': category_list, 'subcat_list': subcategory_list,"first_name":first_name,"last_name":last_name})
    elif request.method == 'GET' and 'page' in request.GET:
        # if "ad_list" in request.session:
        #     ad_list=request.session['ad_list']
        # ad_list=Product_Ad.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(ad_list, 5)
        try:
            adobj = paginator.page(page)
        except PageNotAnInteger:
            adobj = paginator.page(1)
        except EmptyPage:
            adobj = paginator.page(paginator.num_pages)

        return render(request, 'search_result.html', {'ads': adobj, 'cat_list': category_list, 'subcat_list': subcategory_list,"first_name":first_name,"last_name":last_name})
    else:
        if "selected_state" in request.session:
            del request.session['selected_state']
        if "selected_city" in request.session:
            del request.session['selected_city']
        if "selected_category" in request.session:
            del request.session['selected_category']
        if "selected_subcategory" in request.session:
            del request.session['selected_subcategory']
        if "search_text" in request.session:
            del request.session['search_text']
        ad_list = Product_Ad.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(ad_list, 5)
        try:
            adobj = paginator.page(page)
        except PageNotAnInteger:
            adobj = paginator.page(1)
        except EmptyPage:
            adobj = paginator.page(paginator.num_pages)

        return render(request, 'search_result.html', {'ads': adobj, 'cat_list': category_list, 'subcat_list': subcategory_list,"first_name":first_name,"last_name":last_name})
