from django.http import HttpResponse, JsonResponse, Http404
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import mixins
from .serializers import BookTableSerializer
from .models import BookTable


def home(request):
    return HttpResponse("<h1>Welcome to Book Store Api</h1>"
                        "<h2>Api Function based view (JsonResponse) url /api</h2>"
                        "<h2>Api Class based view (Response)  url /api-class</h2>"
                        "<h2>Api Class based view with mixins  url /api-class-mixins</h2>"
                        "<h2>Api Class based view with generic  url /api-class-generic</h2>")


# Function based view
@csrf_exempt
def ApiViewFunction(request):
    if request.method == 'GET':
        books = BookTable.objects.all()
        serializer = BookTableSerializer(books, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BookTableSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


# Usage of api_view decorator
@api_view(['GET', 'DELETE', 'PUT'])
def BookDetail(request, pk):
    try:
        book = BookTable.objects.get(pk=pk)
    except BookTable.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = BookTableSerializer(book)
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = BookTableSerializer(book, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        book.delete()
        return HttpResponse(status=204)


# Class Based View

class ApiViewClass(APIView):
    def post(self, request):
        data = JSONParser().parse(self.request)
        serializer = BookTableSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request):
        books = BookTable.objects.all()
        serializer = BookTableSerializer(books, many=True)
        return Response(serializer.data)


class BookDetailClass(APIView):
    def get_object(self, pk):
        try:
            book = BookTable.objects.get(pk=pk)
            return book
        except BookTable.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        serializer = BookTableSerializer(self.get_object(pk))
        return Response(serializer.data)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=204)

    def put(self, request, pk):
        serializer = BookTableSerializer(self.get_object(pk), request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


# Usage of mixin

class BookList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    queryset = BookTable.objects.all()
    serializer_class = BookTableSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# Generic views

class BookListGeneric(generics.ListCreateAPIView):
    queryset = BookTable.objects.all()
    serializer_class = BookTableSerializer


class BookDetailGeneric(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookTable.objects.all()
    serializer_class = BookTableSerializer
