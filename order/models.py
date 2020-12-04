from django.db import models


class Order(models.Model):
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    created = models.DateTimeField('Дата создания', auto_now_add=True)
    changed = models.DateTimeField('Дата изменения', auto_now=True)
    total = models.DecimalField('Сумма', max_digits=16, decimal_places=2)
    contractor = models.CharField('Контрагент', max_length=128)
    text = models.TextField('Текст заказа')

    def __str__(self):
        return f"Заказ #{self.id}"

    def brief_text(self):
        if len(self.text) > 32:
            return self.text[:29] + '...'
        return self.text

    brief_text.short_description = 'Текст заказа'