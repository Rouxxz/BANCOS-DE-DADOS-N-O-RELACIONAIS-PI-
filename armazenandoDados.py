import pandas as pd
from pymongo import MongoClient

print("1. Lendo o arquivo limpo de Campinas...")
# Carrega o arquivo que você acabou de gerar
df_campinas = pd.read_csv("/content/enem_campinas_2024_limpo.csv")

# Transforma as linhas do DataFrame do Pandas em formato de Dicionário (JSON), que é o que o MongoDB aceita
dados_para_banco = df_campinas.to_dict(orient='records')
print(f"Total de {len(dados_para_banco)} registros prontos para envio.")

print("\n2. Conectando ao seu MongoDB Atlas...")
# Sua string de conexão segura
uri = "LINK MONGODB"

try:
    client = MongoClient(uri)
    
    # Aponta para o seu banco de dados do projeto
    db = client['projeto_integrador_educacao']
    
    # Aponta para a coleção de desempenho
    colecao_enem = db['desempenho_enem']
    
    print("\n3. Limpando dados antigos de teste (se houver)...")
    # Remove aquele documento de teste que criamos antes para não misturar
    colecao_enem.delete_many({})
    
    print("4. Inserindo os dados reais de Campinas no banco (Aguarde alguns segundos)...")
    # Insere todos os milhares de registros de uma vez só (Bulk Insert)
    resultado = colecao_enem.insert_many(dados_para_banco)
    
    print(f"Foram inseridos {len(resultado.inserted_ids)} alunos de Campinas no seu banco de dados NoSQL!")

except Exception as e:
    print(f"\n Erro ao conectar ou enviar dados para o MongoDB: {e}")
