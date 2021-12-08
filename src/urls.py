
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap as sitemap_view
# internals
from blog.sitemaps import PostSitemap


sitemaps = {
    'posts': PostSitemap,
}
urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),
    path('sitemap.xml', sitemap_view, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
   
    path('qanda/', include('qanda.urls', namespace='qanda')),
    path('users/', include('users.urls', namespace='users')),
    # path('i18n/', include('django.conf.urls.i18n')),
    
    path('', include('home.urls', namespace='home')),

]
