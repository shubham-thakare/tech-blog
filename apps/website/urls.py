from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('view/contact-us', views.contact_us, name='contact_us'),
    path('view/privacy-policy', views.privacy_policy, name='privacy_policy'),
    path('view/terms-of-service',
         views.terms_of_service,
         name='terms_of_service'),
    path('article/<int:article_id>/<str:page_name>',
         views.article_base,
         name='article_base'),
    path('article/search',
         views.search,
         name='article_search'),
]
