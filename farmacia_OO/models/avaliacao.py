import mysql.connector

from models.clientes import Clientes
from datetime import datetime


class Avaliacao(Clientes):
    def __init__(self, idavaliacao, tipoavaliacao,login, email, senha, ativo, datacriacao,  dataavaliacao, idcliente, usuario_id, nomecliente,  telefonecliente):
           super().__init__(idcliente, usuario_id, login, email, senha, ativo, datacriacao, nomecliente, telefonecliente)
           self.idavaliacao = idavaliacao
           self.tipoavaliacao = tipoavaliacao
           self.dataavaliacao = dataavaliacao
 
  
        

  # Método para salvar avaliacao no banco de dados
    def salvar(self, db):
       try:
            cursor = db.cursor()
            id=Avaliacao.proximaavaliacao(db)
            dataatual=datetime.now()
            
           # pdb.set_trace()  # Aqui você pode inspecionar variáveis antes de executar o INSERT


            query = "INSERT INTO avaliacao(id_avaliacao,id_cliente, avaliacao, data_avaliacao) VALUES (%s,%s, %s, %s)"
            #pdb.set_trace()  # Aqui você pode inspecionar variáveis antes de executar o INSERT

            cursor.execute(query, (id, self.idcliente, self.tipoavaliacao,dataatual ))
            db.commit()
            return   id, self.idcliente, self.tipoavaliacao,dataatual
              
       except mysql.connector.Error as err:
            print(f"Erro: {err}")
       finally:
          #cursor.close()
          db.close()        
    
    @staticmethod
    def proximaavaliacao( db):
         try:      
           
             cursor = db.cursor()

            
             sql="SELECT COALESCE(MAX(id_avaliacao) + 1, 1)  FROM avaliacao"
             cursor.execute(sql)
             avaliacao = cursor.fetchone()
             
             if avaliacao:
                 maximoID = avaliacao[0]
                 return maximoID   
             return None
             
         except mysql.connector.Error as err:
            print(f"Erro: {err}")      
            
    def obter_avaliacoes(db):
        try: 
                cursor = db.cursor()

                query = "SELECT avaliacao, count(avaliacao) FROM avaliacao GROUP BY avaliacao"
                cursor.execute(query)
                return cursor.fetchall()           
        except mysql.connector.Error as err:
            print(f"Erro: {err}") 
            
    def teste(self):
        teste= "deu certo porra"
        return teste
