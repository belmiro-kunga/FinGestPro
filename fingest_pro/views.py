from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Sum, Count
from django.contrib.auth import logout
from pos.models import Venda, ItemVenda
from clientes.models import Cliente
from estoque.models import EstoqueProdutos

@login_required
def dashboard(request):
    hoje = timezone.now()
    inicio_mes = hoje.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Estatísticas para os cards
    context = {
        'vendas_hoje': Venda.objects.filter(data_venda__date=hoje.date()).count(),
        'faturamento_mensal': Venda.objects.filter(
            data_venda__gte=inicio_mes
        ).aggregate(total=Sum('total'))['total'] or 0,
        'clientes_ativos': Cliente.objects.filter(ativo=True).count(),
        'produtos_estoque': EstoqueProdutos.objects.aggregate(total=Sum('stock'))['total'] or 0,
    }
    
    # Dados para o gráfico de vendas
    ultimos_6_meses = []
    vendas_por_mes = []
    
    for i in range(5, -1, -1):
        mes = hoje - timedelta(days=30*i)
        inicio_mes = mes.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        fim_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        vendas = Venda.objects.filter(
            data_venda__gte=inicio_mes,
            data_venda__lte=fim_mes
        ).count()
        
        ultimos_6_meses.append(mes.strftime('%B'))
        vendas_por_mes.append(vendas)
    
    context['meses'] = ultimos_6_meses
    context['vendas_por_mes'] = vendas_por_mes
    
    # Top produtos mais vendidos
    context['top_produtos'] = EstoqueProdutos.objects.annotate(
        vendas=Count('itemvenda')
    ).order_by('-vendas')[:5]
    
    return render(request, 'dashboard/index.html', context)

@login_required
def index(request):
    if request.user.is_superuser:
        return dashboard(request)
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    return redirect('login')
