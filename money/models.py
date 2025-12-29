from django.db import models

class Trend(models.Model):
    keyword = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    interest = models.FloatField(default=0.0)

    def __str__(self):
        return self.keyword

class Produto(models.Model): # Corrigido de db.Model para models.Model
    categoria = models.CharField(max_length=100)
    termo = models.CharField(max_length=200, unique=True)
    url_amazon = models.TextField()
    url_imagem = models.TextField(blank=True, null=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.categoria} - {self.termo}"