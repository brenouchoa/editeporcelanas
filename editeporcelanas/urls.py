from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic import DetailView, ListView
from loja.views import ArticleDetailView

from django.db.models.loading import cache as model_cache
if not model_cache.loaded:
    model_cache.get_models()

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    (r'^$', RedirectView.as_view(url='/admin/loja/')),
    #url(r'^$', 'editeporcelanas.views.home', name='home'),
    # url(r'^editeporcelanas/', include('editeporcelanas.foo.urls')),
    url(r'^loja/$', 'loja.views.index'),
#todo Test Caixa
    url(r'^caixa/$',
        ArticleDetailView.as_view(), name='Pagamentos'),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
