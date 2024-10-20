import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class GraficoLevUsuario:
    def __init__(self, permissoes):
        self.categorias = [permissao[0] for permissao in permissoes]
        self.valores = [permissao[1] for permissao in permissoes]
        self.cores = self.definir_cores()

    def definir_cores(self):
        cores = []
        for permissao in self.categorias:
            if permissao == "Administrador":
                cores.append('red')
            elif permissao == "Cliente":
                cores.append('green')
            elif permissao == "Funcionario":
                cores.append('blue')
            else:
                cores.append('gray')
        return cores

    def gerar_grafico(self):
        # Criar o gráfico de barras com cores personalizadas
        fig, ax = plt.subplots()
        ax.bar(self.categorias, self.valores, color=self.cores)
        ax.set_title('Quantidade de Usuários por Permissão')
        ax.set_xlabel('Permissão')
        ax.set_ylabel('Quantidade de Usuários')

        # Ajuste para melhor visualização dos rótulos
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # Salvar o gráfico em um buffer de memória
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        return img
