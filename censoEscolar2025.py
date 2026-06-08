import pandas as pd
import os

# 1. COLA AQUI O CAMINHO DO SEU ARQUIVO DE ESCOLAS DE 2025
caminho_censo_escolas = "/content/DADOS_CENSO/microdados_censo_escolar_2025/dados/Tabela_Escola_2025.csv"

if not os.path.exists(caminho_censo_escolas):
    print("ERRO: Arquivo do Censo Escolar não encontrado no caminho!")
else:
    print("Arquivo localizado! Iniciando filtragem para Campinas...")
    
    blocos_escolas_campinas = []
    
    # Colunas 100% atualizadas com base na leitura do arquivo de 2025
    colunas_interesse = [
        'CO_MUNICIPIO', 
        'TP_DEPENDENCIA', 
        'IN_INTERNET', 
        'IN_BANDA_LARGA', 
        'IN_LABORATORIO_INFORMATICA', 
        'IN_DESKTOP_ALUNO'  # O nome atualizado para computadores de alunos
    ]
    
    try:
        for bloco in pd.read_csv(caminho_censo_escolas, sep=';', encoding='latin-1', 
                                 chunksize=50000, usecols=colunas_interesse, low_memory=False):
            
            # Filtra estritamente por Campinas (Código IBGE: 3509502)
            bloco_filtrado = bloco[bloco['CO_MUNICIPIO'] == 3509502]
            
            if not bloco_filtrado.empty:
                blocos_escolas_campinas.append(bloco_filtrado)
                
        if len(blocos_escolas_campinas) == 0:
            print("Aviso: Nenhuma escola foi encontrada com os filtros.")
        else:
            df_escolas_campinas = pd.concat(blocos_escolas_campinas, ignore_index=True)
            print(f"Filtragem concluída! Encontradas {len(df_escolas_campinas)} escolas em Campinas (Base 2025).")
            
            # Salva o arquivo limpo na raiz do Colab
            df_escolas_campinas.to_csv("/content/escolas_campinas_infra_limpo.csv", index=False)
            print("Sucesso! O arquivo 'escolas_campinas_infra_limpo.csv' foi gerado e está pronto para o banco de dados.")
            
    except Exception as e:
        print(f"Erro inesperado: {e}")
