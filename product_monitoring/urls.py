"""
URL configuration for product_monitoring project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from product_monitoring_app import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signout/', views.signout_user, name="signout"),
    path('signin/', views.signin_user, name="signin"),
    path('singup/', views.signup_user, name="signup"),
    path('', views.index, name="index"),
    path('dashboard/', views.dashboard, name='dashboard'),
    # FITUR TAMBAHAN
    path('statistik/', views.statistik_panen, name='statistik_panen'),
    # biaya operasional
    path('add/biaya/', views.input_biaya_operasional, name='add_biaya'),
    path('update/biaya/<int:id>', views.edit_biaya_operasional, name='update_biaya'),
    path('delete/biaya/<int:id>', views.delete_biaya_operasional, name='delete_biaya'),
    # pendapatan
    path('add/pendapatan/', views.input_pendapatan, name='add_pendapatan'),
    path('update/pendapatan/<int:id>', views.edit_pendapatan, name='update_pendapatan'),
    path('delete/pendapatan/<int:id>', views.delete_pendapatan, name='delete_pendapatan'),
    path('pendapatan/', views.pendapatan, name='pendapatan'),
    # hasil panen
    path('add/hasil_panen/', views.input_hasil_panen, name='add_hasil_panen'),
    path('update/hasil_panen/<int:id>', views.edit_hasil_panen, name='update_hasil_panen'),
    path('delete/hasil_panen/<int:id>', views.delete_hasil_panen, name='delete_hasil_panen'),
    path('hasil_panen/', views.hasil_panen, name='hasil_panen'),
    # tanaman
    path('add/tanaman/', views.input_tanaman, name='add_tanaman'),
    path('update/tanaman/<int:id>', views.edit_tanaman, name='update_tanaman'),
    path('delete/tanaman/<int:id>', views.delete_tanaman, name='delete_tanaman'),
    path('tanaman/', views.tanaman, name='tanaman'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
