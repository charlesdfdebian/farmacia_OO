import mysql.connector

import hashlib
from models.usuario import Usuario


class Clientes(Usuario):
    def __init__(self, idcliente,idusuario, login, email,   senha, ativo, datacriacao, nomecliente,  telefonecliente):
           super().__init__( idusuario, login, email,   senha, ativo, datacriacao)  # Inicializa atributos de Usuario
           self.idcliente = idcliente
           self.nomecliente = nomecliente
           self.telefonecliente = telefonecliente
 
  
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
            
            cursor.callproc('spi_inserir_usuario_cliente', (self.login, self.email, self.senha,  self.nomecliente, self.telefonecliente))
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


            sql = "SELECT SenhaClienteMD5,EmailCliente FROM clientes WHERE EmailCliente = %s"
            cursor.execute(sql, (username,))
            resultado = cursor.fetchone()

            if resultado:
                senha_md5_banco = resultado[0]
                usuario=resultado[1]
                
                senha_md5_input = Clientes._gerar_senha_md5_static(senha)

                if  senha_md5_banco == senha_md5_input:
                     return  usuario  
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

    
