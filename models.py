from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import random
import datetime
from faker import Faker

# Configurações do banco de dados
engine = create_engine("sqlite:///loja_material_construcao.db")
Base = declarative_base()

# Definição das classes (Tabelas)
class Cliente(Base):
    """
    Representa um cliente da loja de material de construção.

    Atributos:
        id_cliente (int): ID único do cliente.
        nome (str): Nome completo do cliente.
        cpf_cnpj (str): CPF ou CNPJ do cliente.
        endereco (str): Endereço completo do cliente.
        telefone (str): Telefone de contato do cliente.
        email (str): Endereço de e-mail do cliente.
        segmento (str): Segmento de mercado do cliente (Residencial, Comercial, Industrial).
        canal_compra (str): Canal de compra do cliente (Loja Física, Online).
    """
    __tablename__ = "clientes"
    id_cliente = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf_cnpj = Column(String)
    endereco = Column(String)
    telefone = Column(String)
    email = Column(String)
    segmento = Column(String)
    canal_compra = Column(String)

    vendas = relationship("Venda", backref="cliente")

class Produto(Base):
    """
    Representa um produto da loja de material de construção.

    Atributos:
        id_produto (int): ID único do produto.
        descricao (str): Descrição do produto.
        categoria (str): Categoria do produto (ex: Cimento e Argamassa, Tijolos e Blocos).
        preco_unitario (float): Preço unitário do produto.
        peso_sazonal (float): Fator de peso sazonal do produto (influencia na demanda).
        unidade_medida (str): Unidade de medida do produto (ex: UN, KG, M).
    """
    __tablename__ = "produtos"
    id_produto = Column(Integer, primary_key=True)
    descricao = Column(String)
    categoria = Column(String)
    preco_unitario = Column(Float)
    peso_sazonal = Column(Float)
    unidade_medida = Column(String)

    vendas = relationship("Venda", backref="produto")

class Caixa(Base):
    """
    Representa um caixa da loja de material de construção.

    Atributos:
        id_caixa (int): ID único do caixa.
        nome (str): Nome do caixa.
        funcao (str): Função do caixa (ex: Caixa, Gerente).
        data_admissao (datetime): Data de admissão do caixa.
    """
    __tablename__ = "caixas"
    id_caixa = Column(Integer, primary_key=True)
    nome = Column(String)
    funcao = Column(String)
    data_admissao = Column(DateTime)

    vendas = relationship("Venda", backref="caixa")

class FormaPagamento(Base):
    """
    Representa uma forma de pagamento.

    Atributos:
        id_forma_pagamento (int): ID único da forma de pagamento.
        descricao (str): Descrição da forma de pagamento (ex: Dinheiro, Cartão de Crédito).
        prazo_pagamento (int): Prazo de pagamento em dias (se aplicável).
        desconto (float): Percentual de desconto (se aplicável).
    """
    __tablename__ = "formas_pagamento"
    id_forma_pagamento = Column(Integer, primary_key=True)
    descricao = Column(String)
    prazo_pagamento = Column(Integer)
    desconto = Column(Float)

    vendas = relationship("Venda", backref="forma_pagamento")

class StatusEntrega(Base):
    """
    Representa o status de uma entrega.

    Atributos:
        id_status_entrega (int): ID único do status de entrega.
        descricao (str): Descrição do status de entrega (ex: Em processamento, Enviado, Entregue).
    """
    __tablename__ = "status_entrega"
    id_status_entrega = Column(Integer, primary_key=True)
    descricao = Column(String)

    vendas = relationship("Venda", backref="status_entrega") 

class Venda(Base):
    """
    Representa uma venda realizada na loja de material de construção.

    Atributos:
        id_venda (int): ID único da venda.
        id_cliente (int): ID do cliente que realizou a venda.
        id_produto (int): ID do produto vendido.
        data_venda (datetime): Data da venda.
        valor_venda (float): Valor total da venda.
        quantidade (int): Quantidade de itens vendidos.
        id_forma_pagamento (int): ID da forma de pagamento utilizada. 
        id_status_entrega (int): ID do status da entrega.
        data_entrega (datetime): Data da entrega (se aplicável).
        id_caixa (int): ID do caixa que realizou a venda. 
    """
    __tablename__ = "vendas"
    id_venda = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"))
    id_produto = Column(Integer, ForeignKey("produtos.id_produto"))
    data_venda = Column(DateTime)
    valor_venda = Column(Float)
    quantidade = Column(Integer)
    id_forma_pagamento = Column(Integer, ForeignKey("formas_pagamento.id_forma_pagamento"))
    id_status_entrega = Column(Integer, ForeignKey("status_entrega.id_status_entrega"))
    data_entrega = Column(DateTime)
    id_caixa = Column(Integer, ForeignKey("caixas.id_caixa"))


# Criação do banco de dados
Base.metadata.create_all(engine)

# Criação da sessão
Session = sessionmaker(bind=engine)
session = Session()

# Faker para geração de dados realistas
fake = Faker('pt_BR')

# Categorias de produtos com pesos
categorias_produtos = {
    "Cimento e Argamassa": 0.2,
    "Tijolos e Blocos": 0.15,
    "Telhas e Coberturas": 0.1,
    "Madeiras": 0.1,
    "Hidráulica": 0.15,
    "Elétrica": 0.1,
    "Ferramentas": 0.1,
    "Tintas": 0.1,
}

# Formas de pagamento com pesos
formas_pagamento = {
    "Dinheiro": 0.1,
    "Cartão de Crédito": 0.6,
    "Cartão de Débito": 0.2,
    "Boleto": 0.1,
}

# Status de entrega
status_entrega = ["Em processamento", "Enviado", "Entregue"]


# Funções para geração de dados realistas
def gerar_cliente():
    """
    Gera um cliente aleatório com dados fictícios.

    Returns:
        Cliente: Uma instância da classe Cliente com dados gerados aleatoriamente.
    """
    cliente = Cliente(
        nome=fake.name(),
        cpf_cnpj=fake.cpf(),
        endereco=fake.address(),
        telefone=fake.phone_number(),
        email=fake.email(),
        segmento=random.choice(["Residencial", "Comercial", "Industrial"]),
        canal_compra=random.choice(["Loja Física", "Online"])
    )
    return cliente

def gerar_produto():
    """
    Gera um produto aleatório com dados fictícios.

    Returns:
        Produto: Uma instância da classe Produto com dados gerados aleatoriamente.
    """
    categoria = random.choices(list(categorias_produtos.keys()), weights=categorias_produtos.values())[0]
    produto = Produto(
        descricao=fake.sentence(nb_words=4),
        categoria=categoria,
        preco_unitario=round(random.uniform(10, 500), 2),
        peso_sazonal=random.uniform(0.8, 1.2),
        unidade_medida=random.choice(["UN", "KG", "M", "M2", "M3"])
    )
    return produto

def gerar_caixa():
    """
    Gera um caixa aleatório com dados fictícios.

    Returns:
        Caixa: Uma instância da classe Caixa com dados gerados aleatoriamente.
    """
    caixa = Caixa(
        nome=fake.name(),
        funcao=random.choice(["Caixa", "Gerente"]),
        data_admissao=fake.date_between(start_date="-5y", end_date="today")
    )
    return caixa

def gerar_forma_pagamento():
    """
    Gera uma forma de pagamento aleatória com dados fictícios.

    Returns:
        FormaPagamento: Uma instância da classe FormaPagamento com dados gerados aleatoriamente.
    """
    descricao = random.choices(list(formas_pagamento.keys()), weights=formas_pagamento.values())[0]
    forma_pagamento = FormaPagamento(
        descricao=descricao,
        prazo_pagamento=random.randint(0, 30) if descricao == "Boleto" else 0,
        desconto=random.uniform(0, 0.1) if descricao == "Dinheiro" else 0
    )
    return forma_pagamento

def gerar_status_entrega(lista_status):
    """
    Gera um status de entrega aleatório a partir de uma lista de status.

    Args:
        lista_status (list): Uma lista de strings que representam os possíveis status de entrega.

    Returns:
        StatusEntrega: Uma instância da classe StatusEntrega com um status escolhido aleatoriamente da lista.
    """
    status_entrega = StatusEntrega(descricao=random.choice(lista_status))
    return status_entrega

def gerar_venda():
    """
    Gera uma venda aleatória com dados fictícios, incluindo cliente, produto, forma de pagamento, etc.

    Returns:
        Venda: Uma instância da classe Venda com dados gerados aleatoriamente. 
    """
    cliente = random.choice(session.query(Cliente).all())
    produto = random.choice(session.query(Produto).all())
    forma_pagamento = random.choice(session.query(FormaPagamento).all())
    status_entrega = random.choice(session.query(StatusEntrega).all())
    caixa = random.choice(session.query(Caixa).all())

    venda = Venda(
        id_cliente=cliente.id_cliente,
        id_produto=produto.id_produto,
        data_venda=fake.date_between(start_date="-1y", end_date="today"),
        valor_venda=produto.preco_unitario * random.randint(1, 10), 
        quantidade=random.randint(1, 10), 
        id_forma_pagamento=forma_pagamento.id_forma_pagamento,
        id_status_entrega=status_entrega.id_status_entrega,
        data_entrega=fake.date_between(start_date="-30d", end_date="today") if status_entrega.descricao == "Entregue" else None,
        id_caixa=caixa.id_caixa 
    )
    return venda

# Popular o banco de dados
for _ in range(100):
    session.add(gerar_cliente())
    session.add(gerar_produto())
    session.add(gerar_caixa())
    session.add(gerar_forma_pagamento())
    session.add(gerar_status_entrega(status_entrega))

for _ in range(500):
    session.add(gerar_venda())

# Commit das alterações no banco de dados
session.commit()

# Fecha a sessão
session.close()