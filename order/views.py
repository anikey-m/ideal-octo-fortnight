from django import http
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.core import serializers
from django.forms import model_to_dict
from django.urls import reverse_lazy
from django.views import generic

from . import models


class OrderListView(generic.ListView):
    model = models.Order

    def setup(self, request, *args, **kwargs):
        self.paginate_by = request.GET.get('paginate_by', 20)
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except http.Http404:
            return redirect('order-list')


class OrderDetailView(generic.DetailView):
    model = models.Order


class OrderCreateView(generic.CreateView):
    model = models.Order
    fields = ('contractor', 'total', 'text')
    success_url = reverse_lazy('order_list')


class OrderUpdateView(generic.UpdateView):
    model = models.Order
    fields = ('contractor', 'total', 'text')


class OrderDeleteView(generic.DeleteView):
    model = models.Order
    success_url = reverse_lazy('order_list')
