
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap as sitemap_view
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
# internals
from blog.sitemaps import PostSitemap


sitemaps = {
    'posts': PostSitemap,
}
urlpatterns = [
    path('admin/', admin.site.urls),

    path('sitemap.xml', sitemap_view, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
   
    # path('i18n/', include('django.conf.urls.i18n')),
    

]
urlpatterns += i18n_patterns (
    path('', include('home.urls', namespace='home')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('qanda/', include('qanda.urls', namespace='qanda')),
    path('users/', include('users.urls', namespace='users')),
)