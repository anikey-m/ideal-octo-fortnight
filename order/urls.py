from django.urls import path

from . import views

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order_list'),
    path('add/', views.OrderCreateView.as_view(), name='order_add'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_view'),
    path('<int:pk>/edit', views.OrderUpdateView.as_view(), name='order_edit'),
    path('<int:pk>/delete', views.OrderDeleteView.as_view(), name='order_delete'),
]
