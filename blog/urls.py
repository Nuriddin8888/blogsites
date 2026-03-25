from django.urls import path
from .views import home_page, about_page, blog_page, contact_page, single_page, logout_view, register_view, login_view, update_profile, create_blog_view


urlpatterns = [
    path('', home_page, name="home"),
    path('about/<int:id>/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),

    # blogs
    path('create/blog/', create_blog_view, name='create_blog'),
    path('blog/', blog_page, name='blog'),
    path('single/<uuid:id>/', single_page, name='single'),

    # auth
    path('register/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('update/profile/', update_profile, name="update_profile"),
]