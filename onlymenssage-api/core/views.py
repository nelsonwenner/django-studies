from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .paginator import Paginator
from django.http import Http404
from .permissions import *
from .serializers import *
from .models import *

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ProfileListView(Paginator, APIView):

    pagination_class = PageNumberPagination
    
    def get(self, request, format=None):
        profiles = Profile.objects.get_queryset().order_by('id')
        page = self.paginate_queryset(profiles)
        context = {'request': request}
        profile_serializer = ProfileListViewSerializer(profiles, context=context, many=True)
        return self.get_paginated_response(profile_serializer.data)

    def post(self, request, format=None):
        profile_serializer = ProfileSerializer(data=request.data)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetailView(APIView):
    
    permission_classes = [IsAuthenticated, ProfileOwnerReadOnly]

    def get_object(self, obj, pk):
        try:
            return obj.objects.get(pk=pk)
        except obj.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        profile = self.get_object(Profile, pk)
        context = {'request': request}
        profile_serializer = ProfileDetailViewSerializer(profile, context=context, many=False)
        return Response(profile_serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, format=None):
        profile = self.get_object(Profile, pk)
        self.check_object_permissions(request, profile)
        profile_serializer = ProfileDetailViewSerializer(profile, data=request.data, partial=True)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data, status=status.HTTP_200_OK)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        profile = self.get_object(Profile, pk)
        self.check_object_permissions(request, profile)
        profile.delete()
        return Response(status=status.HTTP_200_OK)


class ContactCreateView(APIView):

    def get_object(self, obj, pk):
        try:
            return obj.objects.get(pk=pk)
        except obj.DoesNotExist:
            raise Http404
    
    def post(self, request, pk_sender, pk_target, format=None):
        sender = self.get_object(Profile, pk_sender)
        target = self.get_object(Profile, pk_target)
        request.data['profile'] = sender.pk
        request.data['friend'] = target.pk
        contact_serializer = ContactSerializer(data=request.data)
        if contact_serializer.is_valid():
            contact_serializer.save()
            return Response(contact_serializer.data, status=status.HTTP_201_CREATED)
        return Response(contact_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactView(Paginator, APIView):

    pagination_class = PageNumberPagination

    def get(self, request, format=None):
        contacts = Contact.objects.get_queryset().order_by('id')
        page = self.paginate_queryset(contacts)
        context = {'request': request}
        contact_serializer = ContactSerializer(contacts, context=context, many=True)
        return self.get_paginated_response(contact_serializer.data)


class ContactDetailView(APIView):
    
    def get_object(self, obj, pk):
        try:
            return obj.objects.get(pk=pk)
        except obj.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        contact = self.get_object(Contact, pk)
        context = {'request': request}
        contact_serializer = ContactDetailSerializer(contact, context=context, many=False)
        return Response(contact_serializer.data, status=status.HTTP_200_OK)


class SingleChatView(APIView):

    def get_object(self, obj, pk):
        try:
            return obj.objects.get(pk=pk)
        except obj.DoesNotExist:
            raise Http404
    
    def post(self, request, pk, format=None):
        contact = self.get_object(Contact, pk)
        singlechat = SingleChat.objects.filter(contact=contact).exists()
        request.data['contact'] = contact.pk
        single_chat_serializer = SingleChatViewSerializer(data=request.data)
        if not singlechat:
            if single_chat_serializer.is_valid():
                single_chat_serializer.save()
                return Response(single_chat_serializer.data, status=status.HTTP_201_CREATED)
            return Response(single_chat_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Singlechat already exists."}, status=status.HTTP_400_BAD_REQUEST)


class SingleChatList(APIView):

    def get_object(self, obj, pk):
        try:
            return obj.objects.get(pk=pk)
        except obj.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        single_chat = SingleChat.objects.all()
        singlechat = []
        for single in single_chat:
            if single.contact.pk == pk:
                singlechat.append(single)
        context = {'request': request}
        singlechat_serializer = SingleChatViewSerializer(singlechat, context=context, many=True)
        return Response(singlechat_serializer.data, status=status.HTTP_200_OK)


class ApiRoot(APIView):

    def get(self, request, *args, **kwargs):

        data = {
            
            'profiles': reverse('profile-list-view', request=request),
  
        }

        return Response(data, status=status.HTTP_200_OK)