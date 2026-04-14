from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ProdutoViewSet, CategoriaViewSet

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'produtos', ProdutoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]