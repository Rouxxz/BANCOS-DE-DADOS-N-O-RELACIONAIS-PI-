import pandas as pd
import os
from pymongo import MongoClient

caminho_censo_escolas = "/content/DADOS_CENSO/microdados_censo_escolar_2025/dados/Tabela_Escola_2025.csv"

if not os.path.exists(caminho_censo_escolas):
    print("ERRO: Arquivo do Censo não encontrado!")
else:
    print("Lendo o Censo para resgatar Nomes das Escolas e Bairros...")

    blocos_escolas_campinas = []

    # Adicionamos NO_ENTIDADE e NO_BAIRRO na lista!
    colunas_interesse = [
        'NO_ENTIDADE', 'NO_BAIRRO', 'CO_MUNICIPIO', 'TP_DEPENDENCIA',
        'IN_INTERNET', 'IN_BANDA_LARGA', 'IN_LABORATORIO_INFORMATICA', 'IN_DESKTOP_ALUNO'
    ]

    try:
        # Lendo com o separador ';' que descobrimos antes
        for bloco in pd.read_csv(caminho_censo_escolas, sep=';', encoding='latin-1',
                                 chunksize=50000, usecols=colunas_interesse, low_memory=False):

            bloco_filtrado = bloco[bloco['CO_MUNICIPIO'] == 3509502]
            if not bloco_filtrado.empty:
                blocos_escolas_campinas.append(bloco_filtrado)

        df_atualizado = pd.concat(blocos_escolas_campinas, ignore_index=True)

        # Tratamento de valores nulos (bairros em branco viram "Não Informado")
        df_atualizado['NO_BAIRRO'] = df_atualizado['NO_BAIRRO'].fillna("Não Informado")
        df_atualizado = df_atualizado.fillna(0)

        print("Enviando dados atualizados para o MongoDB Atlas...")
        uri = "LINK MONGODB"
        client = MongoClient(uri)
        db = client['projeto_integrador_educacao']
        colecao_escolas = db['escolas_infra']

        # Limpa a coleção antiga e insere a nova com os nomes
        colecao_escolas.delete_many({})
        colecao_escolas.insert_many(df_atualizado.to_dict(orient='records'))

        print("Banco atualizado com sucesso! Agora temos Nomes e Bairros.")

    except Exception as e:
        print(f"Erro inesperado: {e}")
