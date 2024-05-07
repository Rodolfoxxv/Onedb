from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
import datetime
from faker import Faker


# Importar as classes do arquivo onde estão definidas
from models import Cliente, Produto, Venda, Caixa, FormaPagamento, StatusEntrega

# Configurações do banco de dados (mesmo banco de dados anterior)
engine = create_engine("sqlite:///loja_material_construcao.db")

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


# Adicionar novos produtos
for _ in range(400):
    session.add(gerar_produto())

# Adicionar novos clientes
for _ in range(80):
    session.add(gerar_cliente())

# Gerar novas vendas com os novos produtos e clientes
for _ in range(200):
    session.add(gerar_venda())

# Commit das alterações no banco de dados
session.commit()

# Fecha a sessão
session.close()