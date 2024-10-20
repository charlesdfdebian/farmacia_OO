import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Classe para gerar o gráfico de avaliações
class GraficoAvaliacao:
    def __init__(self, avaliacoes):
        self.categorias = [avaliacao[0] for avaliacao in avaliacoes]
        self.valores = [avaliacao[1] for avaliacao in avaliacoes]

    def gerar_grafico(self):
        # Criar o gráfico de barras
        fig, ax = plt.subplots()
        ax.bar(self.categorias, self.valores, color=['red', 'yellow', 'green'])
        ax.set_title('Avaliação de Desempenho')
        ax.set_xlabel('Categorias')
        ax.set_ylabel('Pontuação')

        # Salvar o gráfico em um buffer de memória
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        return img
