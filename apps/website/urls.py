from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('view/privacy-policy', views.privacy_policy, name='privacy_policy'),
    path('view/terms-and-conditions',
         views.terms_and_conditions,
         name='terms_and_conditions'),
    path('view/sitemap', views.sitemap, name='sitemap'),
]
