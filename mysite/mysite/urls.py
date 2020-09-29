
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from django.conf import settings
from django.conf.urls.static import static

sitemaps = {
    'posts': PostSitemap,
}



urlpatterns = [
        path('account/', include('account.urls')),
        path('social-auth/',include('social_django.urls', namespace='social')),
        path('admin/', admin.site.urls),
        path('blog/', include('blog.urls')),
        path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
            name='django.contrib.sitemaps.views.sitemap'),
    ] 

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL,
 document_root=settings.MEDIA_ROOT)
