import mysql.connector
import hashlib

class Usuario:
    def __init__(self,  idusuario, login, email,   senha, ativo, datacriacao):
        self.idusuario = idusuario
        self.login = login
        self.email = email
        self.senha = self._gerar_senha_md5(senha)
        self.ativo = ativo
        self.datacriacao=datacriacao
   
   # Função para gerar a senha em MD5
    def _gerar_senha_md5(self, senha):
        """Gera o hash MD5 da senha fornecida."""
        md5_hash = hashlib.md5()
        md5_hash.update(senha.encode('utf-8'))
        return md5_hash.hexdigest()
        
    # Método para salvar cliente no banco de dados
    def salvar(self, db):
        """Salva o usuário no banco de dados."""
        try:
            cursor = db.cursor()
            cursor.callproc('spi_inserir_usuario_cliente', (self.nome, self.email, self.senha,  self.nome_cliente, self.telefone))
            db.cursor.commit()
            
        except mysql.connector.Error as err:
            print(f"Erro: {err}")
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def verificar_login(  username, senha, db):
        """Verifica o login de um usuário, comparando a senha fornecida com a armazenada."""
        try:
            cursor = db.cursor()


            sql = """
                SELECT u.senha,u.nome,up.permissao_id FROM Usuario u
                inner join UsuarioPermissao up on u.id = up.usuario_id
                where u.nome= %s
                """
            cursor.execute(sql, (username,))
            resultado = cursor.fetchone()

            if resultado:
                senha_md5_banco = resultado[0]
                usuario=resultado[1]
                permissao = resultado[2]
                
                senha_md5_input = Usuario._gerar_senha_md5_static(senha)

                if  senha_md5_banco == senha_md5_input:
                     return  [senha_md5_banco, usuario,permissao ]  
                else:
                     return None

        except mysql.connector.Error as err:
            print(f"Erro: {err}")
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def _gerar_senha_md5_static(senha):
        """Gera o hash MD5 de uma senha para comparação."""
        md5_hash = hashlib.md5()
        md5_hash.update(senha.encode('utf-8'))
        return md5_hash.hexdigest()

    
