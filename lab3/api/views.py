from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import json
from .serializers import CatSerializer
from django.core.exceptions import ObjectDoesNotExist

from .models import Cat


@api_view(['GET'])
def get_all_cats(request):
    cats = Cat.objects.all().order_by('id')
    serializer = CatSerializer(cats, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def get_cat_by_id(request, pk):
    try: cats = Cat.objects.get(id=pk)
    except ObjectDoesNotExist as e: return Response('null') #если не нашел
    serializer = CatSerializer(cats, many = False)
    return Response(serializer.data)


@api_view(['GET'])
def get_cat_by_name(request, cat_name):
    cats = Cat.objects.all().order_by('-id')
    serializer = CatSerializer(cats.filter(name=cat_name), many = True)
    if len(serializer.data) == 0:  return Response('null')
    return Response(serializer.data)

@api_view(['POST'])
def create_cat(request):
    serializer = CatSerializer(data=request.data)
    if serializer.is_valid():
        f_cats = Cat.objects.filter(name=serializer.validated_data['name']).filter(sex = serializer.validated_data['sex']).filter(age = serializer.validated_data['age'])
        if len(f_cats) == 0:
            serializer.save()
            return Response(serializer.data) #если всё ок
        else: 
            return Response(status=status.HTTP_400_BAD_REQUEST) # если уже сохранен
    
    return Response(status=status.HTTP_400_BAD_REQUEST) #если что-то не так с json
 
@api_view(['PATCH'])
def patch_cat(request, pk):
    try: cats = Cat.objects.get(pk=pk)
    except ObjectDoesNotExist: return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CatSerializer(cats, data=request.data, many = False)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def put_cat(request, pk):
    try: cats = Cat.objects.get(pk=pk)
    except cats.DoesNotExist: return Response(status=status.HTTP_404_NOT_FOUND)

    filels = ['name', 'age', 'sex']
    data = json.loads(request.body)

    serializer = CatSerializer(cats, data=request.data, many = False, required=True)
    if set(filels).issubset(set(data.keys())): # смотрим все ли поля присутствуют
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)
