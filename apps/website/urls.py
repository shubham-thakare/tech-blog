from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('view/promote-products', views.promote_products, name='promote_products'),
    path('view/privacy-policy', views.privacy_policy, name='privacy_policy'),
    path('view/terms-of-service',
         views.terms_of_service,
         name='terms_of_service'),
    path('article/<int:article_id>/<str:page_name>', views.article_base, name='article_base'),
]
