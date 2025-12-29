from django.shortcuts import render
from .models import Produto

def get_trends(request):
    produtos_banco = Produto.objects.all()
    dados_finais = {}
    
    for p in produtos_banco:
        if p.categoria not in dados_finais:
            dados_finais[p.categoria] = []
        
        dados_finais[p.categoria].append({
            'termo': p.termo,
            'url': p.url_amazon,
            'imagem_url': p.url_imagem
        })
    
    # Se dados_finais estiver vazio aqui, o HTML não mostrará nada.
    return render(request, 'money/money.html', {'secoes': dados_finais})