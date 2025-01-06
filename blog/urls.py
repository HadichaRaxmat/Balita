from django.urls import path
from .views import home_view, category_view, about_view, contact_view, blog_detail_view

urlpatterns = [
    path('', home_view),
    path('category/<int:id>/', category_view),
    path('about/', about_view),
    path('contact/', contact_view),
    path('blog/<int:id>/', blog_detail_view, name='blog_detail'),
]
