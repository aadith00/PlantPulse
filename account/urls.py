from django.urls import path
from django.conf.urls.static import static

from PlantPulse import settings
<<<<<<< HEAD
from .views import account, wishlist,auth, user_register, user_login, user_logout, update_general_info, update_profile_picture, update_address, upload_product
=======
from .views import account, add_review,auth, user_register, user_login, user_logout, update_general_info, update_profile_picture, update_address
>>>>>>> ece678c62d309765f7a77cb7eafe726329886f2b

urlpatterns = [
    path('account', account, name='my-account'),
    # path('wishlist', wishlist, name='wishlist'),
    path('auth', auth, name = 'auth'),
    path('register', user_register, name='register'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('update/general-info/', update_general_info, name='update_general_info'),
    path('update/address/', update_address, name='update_address'),
    path('update-profile-picture/', update_profile_picture, name='update_profile_picture'),
<<<<<<< HEAD
    path('upload-product/', upload_product, name='upload_product'),
=======
    path('add-review/<str:id>', add_review, name='add_review'),

>>>>>>> ece678c62d309765f7a77cb7eafe726329886f2b
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)