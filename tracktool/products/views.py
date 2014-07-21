from django.views.generic.detail import DetailView

from .models import Product


class ApiProductOptions(DetailView):
    model = Product
    template_name = "products/api_options.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super(ApiProductOptions, self).get_context_data(**kwargs)
        options = self.object.options
        context['options'] = options.splitlines()
        return context