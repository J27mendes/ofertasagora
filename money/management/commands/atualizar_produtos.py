import time
import random
import requests
import urllib.parse
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from money.models import Produto

class Command(BaseCommand):
    help = 'Atualiza apenas produtos que ainda não possuem imagem real da Amazon'

    def handle(self, *args, **kwargs):
        meu_id = "ofertasago05b-20"
        categorias_fixas = {
            "Tecnologia": ["iPhone 15 Pro Max", "PlayStation 5 Slim", "Notebook Gamer Dell", "Airfryer", "Echo Dot 5ª Geração", "Smart TV 4K 55", "Monitor LG UltraWide", "Teclado Mecânico RGB", "SSD Kingston 1TB", "Placa de Vídeo RTX", "Console Nintendo Switch", "iPad Air Apple"],
            "Produtos Femininos": ["Batom Matte Maybelline", "Kit de Pincéis de Maquiagem", "Paleta de Sombras Nude", "Base Líquida Boca Rosa", "Máscara de Cílios Sky High", "Perfume Feminino Importado", "Sérum Facial Vitamina C", "Vestido Feminino Tendência 2025", "Bolsa Feminina Transversal", "Escova Secadora de Cabelo", "Prancha de Cabelo Profissional", "Skincare Coreano Kit"],
            "Cama, Mesa e Banho": ["Jogo de Lençol 1000 Fios", "Toalha de Banho Gigante", "Travesseiro Cervical", "Manta de Microfibra Soft", "Capa Impermeável para Sofá", "Jogo de Jantar 20 Peças", "Toalha de Mesa Retangular", "Edredom Queen Plush", "Tapete para Banheiro Antiderrapante"],
            "Sports": ["Tapete de Yoga Antiderrapante", "Kit Halteres de Peso", "Tênis de Corrida Masculino", "Garrafa Térmica 1L", "Bicicleta Ergométrica", "Fone de Ouvido Esportivo", "Corda de Pular Digital", "Mochila de Hidratação", "Smartwatch com GPS"]
        }

        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        ]

        for cat, produtos in categorias_fixas.items():
            for p in produtos:
                # 1. TRAVA DE SEGURANÇA: Só tenta buscar se não tiver imagem oficial no banco
                prod_db = Produto.objects.filter(termo=p).first()
                if prod_db and prod_db.url_imagem and "media-amazon.com" in prod_db.url_imagem:
                    self.stdout.write(self.style.SUCCESS(f" [OK] {p} já está garantido."))
                    continue

                # 2. SE CHEGOU AQUI, É PORQUE PRECISA DE IMAGEM
                self.stdout.write(f"Tentando recuperar imagem para: {p}...")
                img_url = f"https://loremflickr.com/400/400/{urllib.parse.quote(p + ' product')}"
                
                try:
                    query = urllib.parse.quote(p)
                    url = f"https://www.amazon.com.br/s?k={query}"
                    headers = {"User-Agent": random.choice(user_agents), "Accept-Language": "pt-BR,pt;q=0.9"}
                    
                    time.sleep(random.uniform(5, 12)) # Pausa longa para limpar o bloqueio
                    
                    response = requests.get(url, headers=headers, timeout=15)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        img_tag = soup.select_one('.s-image')
                        if img_tag and img_tag.get('src') and "amazon_logo" not in img_tag.get('src'):
                            img_url = img_tag.get('src')
                            self.stdout.write(self.style.SUCCESS(f"  --> SUCESSO! Imagem Amazon obtida."))
                        else:
                            self.stdout.write(self.style.WARNING(f"  --> Amazon respondeu mas sem imagem real."))
                    else:
                        self.stdout.write(self.style.ERROR(f"  --> Erro {response.status_code}. Mantendo Backup."))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"  --> Falha na conexão: {e}"))

                # 3. ATUALIZA APENAS O NECESSÁRIO
                Produto.objects.update_or_create(
                    termo=p,
                    defaults={
                        'categoria': cat,
                        'url_amazon': f"https://www.amazon.com.br/s?k={p.replace(' ', '+')}&tag={meu_id}",
                        'url_imagem': img_url
                    }
                )

        self.stdout.write(self.style.SUCCESS('--- Processo de recuperação finalizado! ---'))