!pip install pymongo dnspython

from pymongo import MongoClient
from datetime import datetime

print("Conectando ao MongoDB Atlas...")

uri = #Link do cluster com a senha

try:
    # Estabelece a conexão com o cluster
    client = MongoClient(uri)
    
    # Criação do Banco de Dados
    db = client['projeto_integrador_educacao']
    
    # Criação das "Tabelas/Colunas" inserindo o primeiro documento de teste
    
    # --- COLEÇÃO 1: escolas_infra ---
    colecao_escolas = db['escolas_infra']
    documento_escola = {
        "Codigo_Escola": 999999,
        "Nome_Escola": "ESCOLA ESTADUAL DE TESTE PI",
        "Dependencia_Adm": "Estadual",
        "Quantidade_Alunos": 850,
        "Bairro": "Centro",
        "Localizacao": {
            "type": "Point",
            "coordinates": [-47.0608, -22.9056] # [Longitude, Latitude] de Campinas
        },
        "Infraestrutura": ["Internet", "Laboratorio_Informatica"]
    }
    # Insere o documento
    resultado_escola = colecao_escolas.insert_one(documento_escola)
    print(f"Coleção 'escolas_infra' criada com sucesso! ID: {resultado_escola.inserted_id}")

    # --- COLEÇÃO 2: desempenho_enem ---
    colecao_enem = db['desempenho_enem']
    documento_enem = {
        "Codigo_Escola": 999999, # Relacionamento com a escola acima
        "Nota_Matematica": 650.5,
        "Nota_Linguagens": 580.2,
        "Nota_Redacao": 800.0,
        "Renda_Familiar": "C", # Até R$ 2.000
        "Ano_Referencia": 2024
    }
    # Insere o documento
    resultado_enem = colecao_enem.insert_one(documento_enem)
    print(f"Coleção 'desempenho_enem' criada com sucesso! ID: {resultado_enem.inserted_id}")

    # --- COLEÇÃO 3: interacoes_tutoria ---
    colecao_tutoria = db['interacoes_tutoria']
    documento_tutoria = {
        "Data_Interacao": datetime.utcnow(),
        "Pergunta_Aluno": "Como eu calculo a área de um triângulo?",
        "Resposta_Tutor_IA": "Para calcular a área, você multiplica a base pela altura e divide por 2.",
        "Habilidade_BNCC_Associada": "EM13MAT307",
        "Tempo_Resposta_MS": 1200,
        "Feedback_Usuario": 5 # 5 estrelas
    }
    # Insere o documento
    resultado_tutoria = colecao_tutoria.insert_one(documento_tutoria)
    print(f"Coleção 'interacoes_tutoria' criada com sucesso! ID: {resultado_tutoria.inserted_id}")

    print("\nBanco de dados criado e inicializado com sucesso!")

except Exception as e:
    print(f"Erro ao conectar ou inserir dados: {e}")
