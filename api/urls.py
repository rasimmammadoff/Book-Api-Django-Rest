from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name="home"),
    path('api/',views.ApiViewFunction),
    path('api/<int:pk>/',views.BookDetail),
    path('api-class/',views.ApiViewClass.as_view()),
    path('api-class/<int:pk>/',views.BookDetailClass.as_view()),
    path('api-class-mixins/', views.BookList.as_view()),
    path('api-class-generic/', views.BookListGeneric.as_view()),
    path('api-class-generic/<int:pk>/', views.BookDetailGeneric.as_view()),
]
