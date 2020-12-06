import datetime
from urllib.parse import urlencode

from django.contrib.messages import views as messages_views, success
from django.urls import reverse_lazy
from django.views import generic

from . import models, forms


class OrderListView(generic.ListView):
    model = models.Order
    paginate_by = 15

    def get(self, request, *args, **kwargs):
        get_copy = request.GET.copy()
        get_copy.pop('page', None)
        self.extra_context = {
            'pager_url': '{}?{}'.format(request.path, urlencode(get_copy, encoding='utf-8'))
        }
        for key in ('start', 'end'):
            try:
                self.extra_context[key] = datetime.datetime.strptime(request.GET[key], '%Y-%m-%dT%H:%M')
            except (KeyError, ValueError, TypeError):
                self.extra_context[key] = None
        return super().get(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        try:
            res = int(self.request.GET.get('paginate_by', self.paginate_by))
            if res > 0:
                return res
        except (ValueError, TypeError):
            pass
        return self.paginate_by

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.extra_context['start']:
            queryset = queryset.filter(created__gte=self.extra_context['start'])
        if self.extra_context['end']:
            queryset = queryset.filter(created__lte=self.extra_context['end'])
        return queryset


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

    def get_success_url(self):
        if '_continue' in self.request.POST:
            return reverse_lazy('order_edit', args=(self.object.id,))
        elif '_new' in self.request.POST:
            return reverse_lazy('order_add')
        return reverse_lazy('order_list')


class OrderUpdateView(messages_views.SuccessMessageMixin, generic.UpdateView):
    model = models.Order
    form_class = forms.OrderForm

    def get_success_message(self, cleaned_data):
        return f"Заказ #{self.object.id} сохранён!"


class OrderDeleteView(FormContextMixin, messages_views.SuccessMessageMixin, generic.DeleteView):
    model = models.Order
    from_class = forms.OrderForm
    success_url = reverse_lazy('order_list')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg)
        success(request, f"Заказ #{pk} удалён!")
        return response
