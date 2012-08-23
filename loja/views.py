from django.http import HttpResponse
from loja.models import Pessoa
from django.template import Context, loader

def index(request):
    latest_poll_list = Pessoa.objects.all().order_by('-data_criacao')[:5]
    t = loader.get_template('loja/index.html')
    c = Context({
        'latest_poll_list': latest_poll_list,
        })
    return HttpResponse(t.render(c))


from django.views.generic.detail import DetailView
from django.utils import timezone

from loja.models import Pagamento_Pedido

class ArticleDetailView(DetailView):

    model = Pagamento_Pedido

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context