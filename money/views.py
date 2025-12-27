from django.shortcuts import render
from pytrends.request import TrendReq

def get_trends(request):
    meu_id = "ofertasago05b-20" 
    dados_finais = {}
    
    # 1. Definir as categorias fixas primeiro
    categorias_fixas = {
        "Tecnologia": [
            "iPhone 15 Pro Max", "PlayStation 5 Slim", "Notebook Gamer Dell", "Kindle Paperwhite", 
            "Echo Dot 5ª Geração", "Smart TV 4K 55", "Monitor LG UltraWide", "Teclado Mecânico RGB",
            "SSD Kingston 1TB", "Placa de Vídeo RTX", "Console Nintendo Switch", "iPad Air Apple"
        ],
        "Produtos Femininos": [
            "Batom Matte Maybelline", "Kit de Pincéis de Maquiagem", "Paleta de Sombras Nude",
            "Base Líquida Boca Rosa", "Máscara de Cílios Sky High", "Perfume Feminino Importado",
            "Sérum Facial Vitamina C", "Vestido Feminino Tendência 2025", "Bolsa Feminina Transversal",
            "Escova Secadora de Cabelo", "Prancha de Cabelo Profissional", "Skincare Coreano Kit"
        ],
        "Cama, Mesa e Banho": [
            "Jogo de Lençol 1000 Fios", "Toalha de Banho Gigante", "Travesseiro Cervical",
            "Manta de Microfibra Soft", "Capa de Sofá Impermeável", "Jogo de Jantar 20 Peças",
            "Toalha de Mesa Retangular", "Edredom Queen Plush", "Tapete para Banheiro Antiderrapante"
        ],
        "Sports": [
            "Tapete de Yoga Antiderrapante", "Kit Halteres de Peso", "Tênis de Corrida Masculino",
            "Garrafa Térmica 1L", "Bicicleta Ergométrica", "Fone de Ouvido Esportivo",
            "Corda de Pular Digital", "Mochila de Hidratação", "Smartwatch com GPS"
        ]
    }

    # 2. Tentar buscar as tendências do Google
    try:
        pytrends = TrendReq(hl='pt-BR', tz=360, timeout=(10,25))
        df = pytrends.trending_searches(pn='brazil')
        
        if not df.empty:
            tendencias_google = []
            for tema in df[0].tolist()[:12]: # Pegar as 12 principais
                tendencias_google.append({
                    'termo': tema,
                    'url': f"https://www.amazon.com.br/s?k={tema.replace(' ', '+')}&tag={meu_id}"
                })
            # Adiciona no topo do dicionário
            dados_finais["🔥 Tendências do Momento"] = tendencias_google
    except Exception as e:
        print(f"Erro ao buscar Google Trends: {e}")

    # 3. Processar as categorias fixas para o formato final
    for nome_cat, produtos in categorias_fixas.items():
        links_cat = []
        for p in produtos:
            links_cat.append({
                'termo': p,
                'url': f"https://www.amazon.com.br/s?k={p.replace(' ', '+')}&tag={meu_id}"
            })
        dados_finais[nome_cat] = links_cat

    # 4. Retornar sempre a variável 'secoes'
    return render(request, 'money/money.html', {'secoes': dados_finais})