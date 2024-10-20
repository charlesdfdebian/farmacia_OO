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
        # Definir cores com base no tipo de avaliação
        cores = []
        for categoria in self.categorias:
            if categoria == 'ruim':  # Avaliação ruim
                cores.append('red')
            elif categoria == 'bom':  # Avaliação boa
                cores.append('green')
            elif categoria == 'ótimo':  # Avaliação ótima
                cores.append('blue')
            else:
                cores.append('gray')  # Cor padrão para categorias desconhecidas

        # Criar o gráfico de barras
        fig, ax = plt.subplots()
        ax.bar(self.categorias, self.valores, color=cores)
        ax.set_title('Avaliação de Desempenho')
        ax.set_xlabel('Categorias')
        ax.set_ylabel('Qtde de avaliações')

        # Salvar o gráfico em um buffer de memória
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        return img
