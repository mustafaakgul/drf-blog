# from articles.api.views import ArticleViewSet
# from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register(r'', ArticleViewSet)
# urlpatterns = router.urls


from django.urls import path
from django.views.decorators.cache import cache_page
from articles.api.views import (
    ArticleListAPIView,
    ArticleDetailAPIView,
    ArticleCreateAPIView,
    ArticleUpdateAPIView,
    ArticleDeleteAPIView
)
from django.views.generic import TemplateView, RedirectView


app_name = 'articles'


urlpatterns = [
    path('', about, name='about'),
    # path('about', TemplateView.as_view(
    #     template_name='pages/about.html'
    # ), name='about'),
    path('send_email', TemplateView.as_view(
        template_name='pages/email-gonderildi.html'
    ), name='send-email'),
    path('redirection', RedirectView.as_view(
        url='www.google.com'
    ), name='redirection'),

    path('list', cache_page(60 * 1)(ArticleListAPIView.as_view()), name='list'),
    path('listfilter', PostListAPIViewFilter.as_view(), name='list2'),
    path('', ArticleListAPIView.as_view()),
    path('create/', ArticleCreateAPIView.as_view(), name='create'),
    path('<pk>', ArticleDetailAPIView.as_view()),
    path('<pk>/update/', ArticleUpdateAPIView.as_view()),
    path('<pk>/delete/', ArticleDeleteAPIView.as_view()),
    path('detail/<slug>', ArticleDetailAPIView.as_view(), name='detail'),
    path('detailId/<pk>', ArticleDetailAPIViewId.as_view(), name='detailId'),
    path('update/<slug>', ArticleUpdateAPIView.as_view(), name='update'),
    path('delete/<slug>', ArticleDeleteAPIView.as_view(), name='delete'),
]