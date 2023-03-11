from django .urls import path
from django.contrib import admin
from app import views


urlpatterns=[
    path('views/',admin.site.urls),
    path('home/',views.home,name="home"),
    path('signin/',views.signin,name="signin"),
    path('signout/',views.signout,name="signout"),
    path('register/',views.register,name="register"),
    path('employee/',views.employee,name="employee"),
    path('customer/<str:username>',views.customer,name="customer"),
    path('active_users/',views.active_users,name="active_users"),
    path('admin_update/<str:username>',views.admin_update,name="admin_update"),
    path('admin_delete/<str:username>',views.admin_delete,name="admin_delete"),
    path('paswd_change/<str:username>',views.paswd_change,name="paswd_change"),
    path('leave_req/<str:username>',views.leave_req,name="leave_req"),
    path('user_summary/<str:username>',views.user_summary,name="user_summary"),
    path('leave_search/<str:username>',views.leave_search,name="leave_search"),
    path('pending/',views.pending,name="pending"),
    path('accepted/',views.accepted,name="accepted"),
    path('rejected/',views.rejected,name="rejected"),
    path('accept/<int:id>',views.accept,name="accept"),    
    path('reject/<int:id>',views.reject,name="reject"),  
]