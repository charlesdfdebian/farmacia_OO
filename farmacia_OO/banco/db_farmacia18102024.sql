-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Tempo de geração: 18/10/2024 às 14:11
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `db_farmacia`
--
CREATE DATABASE IF NOT EXISTS `db_farmacia` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `db_farmacia`;

DELIMITER $$
--
-- Procedimentos
--
DROP PROCEDURE IF EXISTS `spi_inserir_usuario_cliente`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `spi_inserir_usuario_cliente` (IN `p_nome` VARCHAR(100), IN `p_email` VARCHAR(100), IN `p_senha` CHAR(32), IN `p_nomecliente` VARCHAR(100), IN `p_telefone` VARCHAR(20))   BEGIN
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

    	-- Inserir o usuário
    	INSERT INTO Usuario (id,nome, email,senha,ativo,datacriacao) VALUES (v_usuario_id,	p_nome, p_email,p_senha,1,now());

    	-- Inserir a permissão
    	INSERT INTO UsuarioPermissao (id,usuario_id,permissao_id) VALUES (v_permissao_id,v_usuario_id,3);

    	-- Inserir o cliente
    	INSERT INTO 	Clientes (IDCliente,usuario_id, NomeCliente, TelefoneCliente) VALUES (v_cliente_id,v_usuario_id, p_nomecliente, p_telefone);
      
      IF excessao = 1
    		THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Usuário já existe!', MYSQL_ERRNO = 23000;
            ROLLBACK;
      END IF;

        
    -- Confirma a transação se não houver erros
    COMMIT;
    
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Estrutura para tabela `Clientes`
--

DROP TABLE IF EXISTS `Clientes`;
CREATE TABLE IF NOT EXISTS `Clientes` (
  `IDCliente` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `NomeCliente` varchar(100) NOT NULL,
  `TelefoneCliente` varchar(20) NOT NULL,
  PRIMARY KEY (`IDCliente`),
  KEY `usuario_id` (`usuario_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `Clientes`
--

INSERT INTO `Clientes` (`IDCliente`, `usuario_id`, `NomeCliente`, `TelefoneCliente`) VALUES
(1, 1, 'charles junqueira', '61999128035'),
(2, 2, 'diana rocha', '61991476896');

-- --------------------------------------------------------

--
-- Estrutura para tabela `Funcionarios`
--

DROP TABLE IF EXISTS `Funcionarios`;
CREATE TABLE IF NOT EXISTS `Funcionarios` (
  `IDFuncionario` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `NomeFuncionario` varchar(100) NOT NULL,
  `EmailFuncionario` varchar(100) NOT NULL,
  `TelefoneFuncionario` varchar(20) NOT NULL,
  PRIMARY KEY (`IDFuncionario`),
  KEY `usuario_id` (`usuario_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `Permissao`
--

DROP TABLE IF EXISTS `Permissao`;
CREATE TABLE IF NOT EXISTS `Permissao` (
  `id` int(11) NOT NULL,
  `nome` varchar(50) NOT NULL,
  `descricao` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nome` (`nome`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `Permissao`
--

INSERT INTO `Permissao` (`id`, `nome`, `descricao`) VALUES
(1, 'Administrador', 'Responsável pela admin do sistema'),
(2, 'Funcionario', 'Responsavel pelo cadastramento de produtos e serviços'),
(3, 'Cliente', 'Pessoa que acessa o site para adquirir, produtos e serviços');

-- --------------------------------------------------------

--
-- Estrutura para tabela `Usuario`
--

DROP TABLE IF EXISTS `Usuario`;
CREATE TABLE IF NOT EXISTS `Usuario` (
  `id` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `senha` char(32) NOT NULL,
  `ativo` bit(1) NOT NULL,
  `datacriacao` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `Usuario`
--

INSERT INTO `Usuario` (`id`, `nome`, `email`, `senha`, `ativo`, `datacriacao`) VALUES
(1, 'charlesdfjj', 'charlesdfjj@gmail.com', '202cb962ac59075b964b07152d234b70', b'1', '2024-10-18 05:58:10'),
(2, 'dianadfjj', 'dianadfjj@gmail.com', 'c20ad4d76fe97759aa27a0c99bff6710', b'1', '2024-10-18 07:10:17');

-- --------------------------------------------------------

--
-- Estrutura para tabela `UsuarioPermissao`
--

DROP TABLE IF EXISTS `UsuarioPermissao`;
CREATE TABLE IF NOT EXISTS `UsuarioPermissao` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `permissao_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_id` (`usuario_id`,`permissao_id`),
  KEY `permissao_id` (`permissao_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `UsuarioPermissao`
--

INSERT INTO `UsuarioPermissao` (`id`, `usuario_id`, `permissao_id`) VALUES
(1, 1, 3),
(2, 2, 3);

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `Clientes`
--
ALTER TABLE `Clientes`
  ADD CONSTRAINT `Clientes_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `Usuario` (`id`);

--
-- Restrições para tabelas `Funcionarios`
--
ALTER TABLE `Funcionarios`
  ADD CONSTRAINT `Funcionarios_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `Usuario` (`id`);

--
-- Restrições para tabelas `UsuarioPermissao`
--
ALTER TABLE `UsuarioPermissao`
  ADD CONSTRAINT `UsuarioPermissao_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `Usuario` (`id`),
  ADD CONSTRAINT `UsuarioPermissao_ibfk_2` FOREIGN KEY (`permissao_id`) REFERENCES `Permissao` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
