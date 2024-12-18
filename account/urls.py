from django.urls import path
from django.conf.urls.static import static

from PlantPulse import settings
from .views import account,auth, user_register, user_login, user_logout, update_general_info, update_profile_picture, update_address, upload_product, add_review, review_page

urlpatterns = [
    path('account', account, name='my-account'),
    path('auth', auth, name = 'auth'),
    path('register', user_register, name='register'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('update/general-info/', update_general_info, name='update_general_info'),
    path('update/address/', update_address, name='update_address'),
    path('update-profile-picture/', update_profile_picture, name='update_profile_picture'),
    path('upload-product/', upload_product, name='upload_product'),
    path('review/<str:order_id>', review_page, name='review'),
    path('add-review/<str:id>', add_review, name='add-review')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)