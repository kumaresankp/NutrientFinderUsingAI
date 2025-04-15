from django.contrib import admin
from django.urls import path
from app import views 
from django.conf import settings
from django.conf.urls.static import static 
from app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

urlpatterns+= static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

