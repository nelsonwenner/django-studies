from django.urls import path, include
from .views import *


urlpatterns = [

    path('', ApiRoot.as_view()),

    path('api-token/', MyTokenObtainPairView.as_view(), name='api-token'),

    path('api/v1/profiles/', ProfileListView.as_view(), name='profile-list-view'),

    path('api/v1/profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail-view'),

    path('api/v1/contacts/', ContactView.as_view(), name='contact-list-view'),

    path('api/v1/contacts/<int:pk>/', ContactDetailView.as_view(), name='contact-detail-view'),

    path('api/v1/profiles/<int:pk_sender>/contacts/<int:pk_target>/', ContactCreateView.as_view(), name='contact-create-view'),

    path('api/v1/contacts/<int:pk>/singlechats/', SingleChatView.as_view(), name='singlechat-view'),

    path('api/v1/contacts/singlechats/<int:pk>/', SingleChatList.as_view(), name='singlechat-list-view'),

    #path('api/v1/contacts/<int:pk_contact>/singlechats/<int:pk_singlechat>/', SingleChatList.as_view(), name='singlechat-list-view'),
    

    #path('api/v1/contacts/<int:pk>/', ContactDetailView.as_view(), name='contact-detail-view'),
    
    path('api/v1/profiles-contacts/<int:pk>/', ContactDetailView.as_view(), name='contact-detail'),

]