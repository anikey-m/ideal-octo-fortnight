from django import http
from django.contrib.messages import views as messages_views
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from . import models, forms


class OrderListView(generic.ListView):
    model = models.Order

    def setup(self, request, *args, **kwargs):
        self.paginate_by = request.GET.get('paginate_by', 20)
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except http.Http404:
            return redirect('order_list')


class FormContextMixin:
    form_class = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = form = forms.OrderForm(instance=self.object)
        for field in form.fields.values():
            field.widget.attrs['disabled'] = True
        return context


class OrderDetailView(FormContextMixin, generic.DetailView):
    model = models.Order
    from_class = forms.OrderForm


class OrderCreateView(messages_views.SuccessMessageMixin, generic.CreateView):
    model = models.Order
    form_class = forms.OrderForm
    success_url = reverse_lazy('order_list')

    def get_success_message(self, cleaned_data):
        return f"Заказ #{self.object.id} создан!"


class OrderUpdateView(generic.UpdateView):
    model = models.Order
    form_class = forms.OrderForm


class OrderDeleteView(FormContextMixin, generic.DeleteView):
    model = models.Order
    from_class = forms.OrderForm
    success_url = reverse_lazy('order_list')
