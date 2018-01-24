from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^savecategory', views.saveCategory, name='saveCategory'),
    url(r'^onaddCategoryclick', views.onaddCategoryclick, name='onaddCategoryclick'),
    url(r'^signup/',views.signup,name="signup"),
    url(r'^addUser/$',views.addUser,name="addUser"),
    url(r'^login/$',views.login,name="login"),
    url(r'^loginValidation',views.loginValidation,name="loginValidation"),
    url(r'^checkEmailandPassword/$',views.checkEmailandPassword,name="checkEmailandPassword"),
    url(r'^homepage/$',views.homepage,name="homepage"),
    url(r'^admin/$',views.admin,name='admin'),
    url(r'^addtosession/$',views.addtosession,name='addtosession'),
    url(r'^deletefromsession/$',views.deletefromsession,name='deletefromsession'),
	url(r'^deletecategory/$',views.ondeletecategoryclick,name='ondeletecategoryclick'),
    url(r'^delete_att/$',views.delete_att,name='delete_att'),
    url(r'^post_ad/$',views.post_ad,name='post_ad'),
    url(r'^submit_ad/$',views.submit_ad,name='submit_ad'),
    url(r'^ad_review/$',views.ad_review,name='ad_review'),
    url(r'^category_page/$',views.category_page,name='category_page'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^product_page/$', views.product_page, name='product_page'),
    url(r'^updateuser/$',views.updateuser,name='updateuser'),
    url(r'^search_result/$',views.search_result,name='search_result')
]