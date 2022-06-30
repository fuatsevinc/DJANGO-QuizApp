from rest_framework import routers
from quiz.views import QuizMVS


router = routers.DefaultRouter()
router.register('quiz', QuizMVS)

urlpatterns = [
]

urlpatterns += router.urls