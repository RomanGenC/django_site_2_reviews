from django.urls import path
from recipient import views
from django.contrib.auth import views as auth_views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('base/', views.base_page, name='base_page'),
    path('self-cabinet/', views.self_cabinet, name='self_cabinet'),
    path('all-recipients/', views.recipients_info, name='all_recipients'),
    path('recipient-info/<int:recipient_id>/', views.recipient_info, name='recipient_info'),
    path('user-info/<int:user_id>/', views.user_info, name='user_info'),
    path('add-review/<int:recipient_id>/', views.add_review, name='add_review'),
    path('success-review/', views.success_review, name='success_review'),
    path('search/', views.recipient_search, name='recipient_search'),
    path('edit_review/<int:pk>/', views.edit_review, name='edit_review'),
    path('not_published_reviews/', views.not_published_reviews, name='not_published_reviews'),
    path('<int:recipient_id>/share.html/', views.recipient_share, name='recipient_share'),

    path('politika-konfidencialnosti/', views.politika_konfidencialnosti, name='politika_konfidencialnosti'),
    path('polzovatelskoe-soglashenie/', cache_page(timeout=60, key_prefix='polzovatelskoe')(views.polzovatelskoe_soglashenie), name='polzovatelskoe_soglashenie'),
    path('o-kompanii/', views.o_kompanii, name='o_kompanii'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]