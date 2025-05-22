from django.http import Http404


class UserQuerySetMixin:
    """ Миксин для автоматической фильтрации queryset по текущему пользователю """
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    def get_object(self, queryset=None):
        """ Защита от доступа к чужим объектам """
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404("Объект не найден.")
        return obj
