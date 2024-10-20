from flask import Flask, render_template, request, redirect, session, url_for, make_response
#import mysql.connector
from db_config import get_db_connection
from models.clientes import Clientes
from models.produtos import Produtos
from models.usuario  import Usuario
from models.avaliacao  import Avaliacao
from models.grafico_avaliacao import GraficoAvaliacao
from models.grafico_levusuario import GraficoLevUsuario




app = Flask(__name__)
app.secret_key = '8714f3545df770ac8b40d7235a59562d'  # Necessário para exibir mensagens flash


# Rota principal (Página inicial com os botões de Login e Cadastro)
@app.route('/')
def home():
       return render_template('principal.html')

@app.route('/sobre')
def sobre():
       return render_template('sobre.html')

@app.route('/debugar')
def debugar():
       return render_template('debugar.html')

@app.route('/avaliacao', methods=['GET', 'POST'])
def avaliacao():
    
    if 'usuario' in session:
        
        db = get_db_connection()


        cliente_logado=session['usuario'] 
        idcliente_logado = Clientes.retornaIDcliente(cliente_logado, db)
        
#        if idcliente_logado:
#            return render_template('avaliacao.html', idcliente_logado=idcliente_logado)
#        return "Cliente não encontrado " + cliente_logado, 404
#        
        if request.method == 'POST':
             tpavaliacao = request.form['avaliacao']
            # A classe Avaliacao deve ser importada corretamente
             avaliacao = Avaliacao(None, tpavaliacao, None, None,'1',None,None,None,idcliente_logado, None, None, None)
             db = get_db_connection()
             avaliacao.salvar(db)
             #teste=avaliacao.proximaavaliacao(db)
             #retorna para testar se entrou
             #return teste
             db.close()
            # Aqui você deve chamar o método para salvar a avaliação no banco de dados
             #return render_template('debugar.html', avaliacao=avaliacao)
             #return redirect(url_for('success', message='Avaliação cadastrada com sucesso!'+str(avaliacao)))
             return redirect(url_for('success', message='Avaliação cadastrada com sucesso!'))
            
        # Renderize a página do formulário para o método GET
        return render_template('avaliacao.html')

    return render_template('index.html')

# Rota para exibir o gráfico de avaliação
@app.route('/graficoavaliacao')
def graficoavaliacao():
    return render_template('graficoavaliacao.html')
    
@app.route('/plot.png')
def plot_png():
    # Conectar ao banco de dados e obter os dados de avaliação
    db = get_db_connection()
    avaliacoes = Avaliacao.obter_avaliacoes(db)

    # Gerar o gráfico com os dados do MySQL
    grafico = GraficoAvaliacao(avaliacoes)
    img = grafico.gerar_grafico()

    # Retornar o gráfico como imagem
    response = make_response(img.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

# Rota para exibir o gráfico de avaliação
@app.route('/levusuario')
def levusuario():
    return render_template('levusuario.html')
    
@app.route('/levusuario.png')
def levusuario_png():
    # Conectar ao banco de dados e obter os dados de avaliação
    db = get_db_connection()
    usuario = Usuario.obter_levusuario(db)

    # Gerar o gráfico com os dados do MySQL
    grafico = GraficoLevUsuario(usuario)
    img = grafico.gerar_grafico()

    # Retornar o gráfico como imagem
    response = make_response(img.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response
    
## Página de login
@app.route('/login')
def login():
     return render_template('login.html')
    
# Verificar login
@app.route('/login', methods=['POST'])
def verificar_login():
    username = request.form['username']
    senha = request.form['password']
    db = get_db_connection()
    
    usuario = Usuario.verificar_login( username, senha, db)
    
    # Verificar login
    if usuario is not None and usuario[0] is not None:

        session['usuario'] = usuario[1]
        if 'usuario' in session:
            if usuario[2]==1:
                return   render_template('admin.html')
            elif  usuario[2]==2:
                return   render_template('funcionario.html')
            else:
                return   render_template('principal.html')
       
        return 'Você não está logado. <br><a href="/login">Login</a>'

    else:
        session['usuario'] = ""
        return  render_template('result.html', message="Usuário ou senha incorretos!")
    
    db.close()

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove o usuário da sessão
    return redirect(url_for('home'))
# Cadastro de clientes
@app.route('/inseri_clientes', methods=['GET', 'POST'])
def inseri_clientes():
  #if 'usuario' in session:
  
    if request.method == 'POST':
        # Coleta os dados do formulário
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        nomecompleto = request.form['nomecompleto']
        telefone = request.form['telefone']

        # Cria um objeto Customer e salva no banco de dados
        clientes = Clientes( None, None, nome, email, senha, None, None, nomecompleto, telefone)        
        db = get_db_connection()
        clientes.salvar(db)
        db.close()

        return redirect(url_for('success', message='Cliente cadastrado com sucesso!'))
    return render_template('inseri_clientes.html')
  #return render_template('index.html')
  # Cadastro de clientes
@app.route('/inseri_usuario', methods=['GET', 'POST'])
def inseri_usuario():
  #if 'usuario' in session:
  
    if request.method == 'POST':
        # Coleta os dados do formulário
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        nomecompleto = request.form['nomecompleto']
        telefone = request.form['telefone']
        status = request.form['status']
        
        # Cria um objeto Customer e salva no banco de dados
        clientes = Clientes( None, None, nome, email, senha, None, None, nomecompleto, telefone)        
        db = get_db_connection()
        clientes.salvar(db, status)
        db.close()

        return redirect(url_for('success', message='Usuário cadastrado com sucesso!'))
    return render_template('inseri_usuario.html')

# Cadastro de produtos
@app.route('/inseri_produtos', methods=['GET', 'POST'])
def inseri_produtos():
    if 'usuario' in session:

        if request.method == 'POST':
            # Coleta os dados do formulário
            nome_produto = request.form['nome_produto']
            preco = request.form['preco']
            estoque = request.form['estoque']

            preco = preco.replace(",", ".")
            
            # Cria um objeto Product e salva no banco de dados
            produtos = Produtos(nome_produto, preco, estoque)        
            db = get_db_connection()
            produtos.salvar(db)
            db.close()

            return redirect(url_for('success', message='Produto cadastrado com sucesso!'))

        return render_template('inseri_produtos.html')
    return render_template('index.html')
 
 
    
# lista  de produtos
@app.route('/listaproduto')
def listaproduto():
  if 'usuario' in session:

            
            db = get_db_connection()
            produtos =Produtos.listaproduto(db)
            return render_template('listaproduto.html', produtos=produtos)
            db.close()
  return render_template('index.html') 
    
# Página de sucesso
@app.route('/success')
def success():
    message = request.args.get('message')
    return render_template('success.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
