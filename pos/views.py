from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from decimal import Decimal
from .models import Venda, ItemVenda, Pagamento
from .forms import VendaForm, ItemVendaForm, PagamentoForm
from estoque.models import Produto
from django.contrib.auth.models import User
from django.db.models import models
from usuarios.models import Usuario

@login_required
def iniciar_venda(request):
    """Inicia uma nova venda"""
    if request.method == 'POST':
        form = VendaForm(request.user.empresa, request.POST)
        if form.is_valid():
            venda = form.save(commit=False)
            venda.empresa = request.user.empresa
            venda.usuario = request.user
            venda.save()
            return redirect('adicionar_item', venda_id=venda.id)
    else:
        form = VendaForm(request.user.empresa)
    
    return render(request, 'pos/iniciar_venda.html', {'form': form})

@login_required
def adicionar_item(request, venda_id):
    """Adiciona itens à venda"""
    venda = get_object_or_404(Venda, id=venda_id, empresa=request.user.empresa)
    
    if venda.status != 'pendente':
        messages.error(request, 'Esta venda não pode mais ser modificada.')
        return redirect('lista_vendas')

    if request.method == 'POST':
        form = ItemVendaForm(request.user.empresa, request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.venda = venda
            
            # Verifica estoque
            produto = item.produto
            if produto.quantidade < item.quantidade:
                messages.error(request, f'Estoque insuficiente para {produto.nome}')
                return redirect('adicionar_item', venda_id=venda.id)
            
            # Define o preço unitário atual do produto
            item.preco_unitario = produto.preco_unitario
            item.save()
            
            # Atualiza o estoque
            produto.quantidade -= item.quantidade
            produto.save()
            
            messages.success(request, 'Item adicionado com sucesso!')
            return redirect('adicionar_item', venda_id=venda.id)
    else:
        form = ItemVendaForm(request.user.empresa)
    
    itens = venda.itens.all()
    total = venda.total
    
    context = {
        'venda': venda,
        'form': form,
        'itens': itens,
        'total': total
    }
    return render(request, 'pos/adicionar_item.html', context)

@login_required
def remover_item(request, item_id):
    """Remove um item da venda"""
    item = get_object_or_404(ItemVenda, id=item_id, venda__empresa=request.user.empresa)
    venda = item.venda
    
    if venda.status != 'pendente':
        messages.error(request, 'Esta venda não pode mais ser modificada.')
        return redirect('lista_vendas')
    
    with transaction.atomic():
        # Devolve ao estoque
        produto = item.produto
        produto.quantidade += item.quantidade
        produto.save()
        
        # Remove o item
        item.delete()
    
    messages.success(request, 'Item removido com sucesso!')
    return redirect('adicionar_item', venda_id=venda.id)

@login_required
def processar_pagamento(request, venda_id):
    """Processa o pagamento da venda"""
    venda = get_object_or_404(Venda, id=venda_id, empresa=request.user.empresa)
    
    if venda.status != 'pendente':
        messages.error(request, 'Esta venda não pode mais ser modificada.')
        return redirect('lista_vendas')
    
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            pagamento = form.save(commit=False)
            pagamento.venda = venda
            
            # Verifica se o valor não excede o restante a pagar
            total_pago = venda.pagamentos.aggregate(
                total=models.Sum('valor')
            )['total'] or Decimal('0.00')
            valor_restante = venda.total - total_pago
            
            if pagamento.valor > valor_restante:
                messages.error(request, 'Valor do pagamento excede o total restante.')
                return redirect('processar_pagamento', venda_id=venda.id)
            
            pagamento.save()
            
            # Se pagamento completo, finaliza a venda
            if total_pago + pagamento.valor >= venda.total:
                venda.status = 'concluida'
                venda.save()
                
                # Gera a fatura
                try:
                    venda.gerar_fatura()
                    messages.success(request, 'Venda concluída e fatura gerada com sucesso!')
                except Exception as e:
                    messages.warning(request, f'Venda concluída, mas houve um erro ao gerar a fatura: {str(e)}')
                
                return redirect('lista_vendas')
            
            messages.success(request, 'Pagamento registrado com sucesso!')
            return redirect('processar_pagamento', venda_id=venda.id)
    else:
        # Calcula valor restante
        total_pago = venda.pagamentos.aggregate(
            total=models.Sum('valor')
        )['total'] or Decimal('0.00')
        valor_restante = venda.total - total_pago
        
        form = PagamentoForm(initial={'valor': valor_restante})
    
    context = {
        'venda': venda,
        'form': form,
        'pagamentos': venda.pagamentos.all(),
        'total_pago': total_pago,
        'valor_restante': valor_restante
    }
    return render(request, 'pos/processar_pagamento.html', context)

@login_required
def cancelar_venda(request, venda_id):
    """Cancela uma venda pendente"""
    venda = get_object_or_404(Venda, id=venda_id, empresa=request.user.empresa)
    
    if venda.status != 'pendente':
        messages.error(request, 'Apenas vendas pendentes podem ser canceladas.')
        return redirect('lista_vendas')
    
    with transaction.atomic():
        # Devolve os itens ao estoque
        for item in venda.itens.all():
            produto = item.produto
            produto.quantidade += item.quantidade
            produto.save()
        
        # Cancela a venda
        venda.status = 'cancelada'
        venda.save()
    
    messages.success(request, 'Venda cancelada com sucesso!')
    return redirect('lista_vendas')

@login_required
def lista_vendas(request):
    # Obtém todas as vendas da empresa do usuário
    vendas = Venda.objects.filter(
        empresa=request.user.empresa
    ).select_related(
        'usuario',
        'usuario_destino'
    ).order_by('-data_criacao')

    # Filtra por status se especificado
    status = request.GET.get('status')
    if status:
        vendas = vendas.filter(status=status)
    else:
        # Por padrão, mostra apenas vendas abertas
        vendas = vendas.filter(status='aberta')

    return render(request, 'pos/lista_vendas.html', {
        'vendas': vendas,
        'status_atual': status or 'aberta',
        'status_choices': Venda.STATUS_CHOICES
    })

@login_required
def detalhes_venda(request, venda_id):
    """Mostra os detalhes de uma venda"""
    venda = get_object_or_404(Venda, id=venda_id, empresa=request.user.empresa)
    return render(request, 'pos/detalhes_venda.html', {'venda': venda})

@login_required
def transferir_venda(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id)

    # Verifica se o usuário atual tem permissão (pertence à mesma empresa)
    if request.user.empresa != venda.empresa:
        messages.error(request, 'Você não tem permissão para transferir esta venda')
        return redirect('lista_vendas')

    if request.method == 'POST':
        novo_usuario_id = request.POST.get('novo_usuario')
        motivo = request.POST.get('motivo')
        
        try:
            novo_usuario = Usuario.objects.get(id=novo_usuario_id)
            
            # Verifica se o novo usuário pertence à mesma empresa
            if novo_usuario.empresa == venda.empresa:
                venda.transferir_para(novo_usuario, motivo)
                messages.success(request, 'Venda transferida com sucesso')
                return redirect('lista_vendas')
            else:
                messages.error(request, 'O usuário selecionado não pertence à mesma empresa')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuário não encontrado')
        except ValueError as e:
            messages.error(request, str(e))

    # Lista apenas usuários da mesma empresa, exceto o atual
    usuarios = Usuario.objects.filter(
        empresa=venda.empresa
    ).exclude(
        id=request.user.id
    ).filter(
        is_active=True
    )
    
    return render(request, 'pos/transferir_venda.html', {
        'venda': venda,
        'usuarios': usuarios
    })

@login_required
def aceitar_transferencia(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id)
    
    try:
        venda.aceitar_transferencia(request.user)
        messages.success(request, 'Transferência aceita com sucesso')
    except ValueError as e:
        messages.error(request, str(e))
    
    return redirect('lista_vendas')

@login_required
def rejeitar_transferencia(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id)
    
    if request.method == 'POST':
        motivo = request.POST.get('motivo', '')
        try:
            venda.rejeitar_transferencia(request.user, motivo)
            messages.success(request, 'Transferência rejeitada com sucesso')
        except ValueError as e:
            messages.error(request, str(e))
        return redirect('lista_vendas')
    
    return render(request, 'pos/rejeitar_transferencia.html', {'venda': venda})

@login_required
def minhas_transferencias(request):
    # Vendas que foram transferidas para mim
    vendas_recebidas = Venda.objects.filter(
        usuario_destino=request.user,
        status='em_transferencia'
    )
    
    # Vendas que eu transferi e estão aguardando aceitação
    vendas_enviadas = Venda.objects.filter(
        usuario=request.user,
        status='em_transferencia'
    )
    
    return render(request, 'pos/minhas_transferencias.html', {
        'vendas_recebidas': vendas_recebidas,
        'vendas_enviadas': vendas_enviadas
    })
