from rest_framework.routers import DefaultRouter
from .views import AlunoViewSet

router = DefaultRouter()
router.register(r'', AlunoViewSet, basename='id')

urlpatterns = router.urls