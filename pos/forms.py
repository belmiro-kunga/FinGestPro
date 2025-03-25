from django import forms
from .models import Venda, ItemVenda, Pagamento
from estoque.models import Produto
from faturacao.models import Clientes

class ItemVendaForm(forms.ModelForm):
    produto = forms.ModelChoiceField(
        queryset=Produto.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )
    quantidade = forms.DecimalField(
        min_value=0.01,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )

    class Meta:
        model = ItemVenda
        fields = ['produto', 'quantidade']

    def __init__(self, empresa=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if empresa:
            self.fields['produto'].queryset = Produto.objects.filter(empresa=empresa)

class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['valor', 'forma_pagamento']
        widgets = {
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'forma_pagamento': forms.Select(attrs={'class': 'form-control'})
        }

class VendaForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(
        queryset=Clientes.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )

    class Meta:
        model = Venda
        fields = ['cliente']

    def __init__(self, empresa=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if empresa:
            self.fields['cliente'].queryset = Clientes.objects.filter(empresa=empresa)
