DELIMITER //


CREATE PROCEDURE spi_inserir_usuario_cliente(
    IN p_nome VARCHAR(100),
    IN p_email VARCHAR(100),
    IN p_senha CHAR(32),
    IN p_nomecliente  VARCHAR(100),
    IN p_telefone VARCHAR(20),
    IN p_permissao_id int DEFAULT 0)

BEGIN
    DECLARE v_usuario_id INT;
    DECLARE v_permissao_id INT;
    DECLARE v_cliente_id INT;

   DECLARE excessao SMALLINT DEFAULT 0;
  	DECLARE EXIT HANDLER FOR SQLEXCEPTION SET excessao = 1;
  
     
 
 	  -- Iniciar a transação
    START TRANSACTION;
      
 	   SET v_usuario_id = (SELECT COALESCE(MAX(id) + 1, 1) AS proximo_id FROM Usuario);
   	SET v_permissao_id = (select COALESCE(MAX(id) + 1, 1) AS proximo_id from UsuarioPermissao );
    	SET v_cliente_id = (select COALESCE(MAX(IDCliente) + 1, 1 ) from Clientes );    

    	IF p_permissao_id = 0 THEN
    		SET p_permissao_id=3
    	END IF;

    	-- Inserir o usuário
    	INSERT INTO Usuario (id,nome, email,senha,ativo,datacriacao) VALUES (v_usuario_id,	p_nome, p_email,p_senha,1,now());

    	-- Inserir a permissão
    	INSERT INTO UsuarioPermissao (id,usuario_id,permissao_id) VALUES (v_permissao_id,v_usuario_id,p_permissao_id);

    	-- Inserir o cliente
    	INSERT INTO 	Clientes (IDCliente,usuario_id, NomeCliente, TelefoneCliente) VALUES (v_cliente_id,v_usuario_id, p_nomecliente, p_telefone);
      
      IF excessao = 1
    		THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Usuário já existe!', MYSQL_ERRNO = 23000;
            ROLLBACK;
      END IF;

        
    -- Confirma a transação se não houver erros
    COMMIT;
    
END //

DELIMITER ;
