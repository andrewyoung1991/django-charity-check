from rest_framework import routers

router = routers.SimpleRouter()
router.register("charity-verification", views.CharityCheckViewset,
                base_name="charity-check")

urlpatterns = router.urls
