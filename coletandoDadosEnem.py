import pandas as pd
import os

# Caminho completo para o arquivo de resultados
caminho_arquivo_inep = "/content/DADOS/RESULTADOS_2024.csv"

if not os.path.exists(caminho_arquivo_inep):
    print("ERRO: Arquivo não encontrado. Verifique o caminho!")
else:
    print("Arquivo RESULTADOS_2024.csv localizado com sucesso! Filtrando dados...")
    
    blocos_campinas = []
    
    # Lista limpa e corrigida com os nomes REAIS das colunas do seu arquivo
    colunas_interesse = [
        'CO_MUNICIPIO_ESC',         # Código do município da escola
        'NO_MUNICIPIO_ESC',         # Nome do município da escola
        'TP_DEPENDENCIA_ADM_ESC',   # Tipo de rede (1-Federal, 2-Estadual, 3-Municipal, 4-Privada)
        'NU_NOTA_MT',               # Nota de Matemática
        'NU_NOTA_LC',               # Nota de Linguagens
        'NU_NOTA_REDACAO'           # Nota de Redação
    ]
    
    # Lendo o arquivo em blocos de 100.000 linhas
    for bloco in pd.read_csv(caminho_arquivo_inep, sep=';', encoding='latin-1', 
                             chunksize=100000, usecols=colunas_interesse, low_memory=False):
        
        # Filtra estritamente pelo código IBGE de Campinas (3509502)
        bloco_filtrado = bloco[bloco['CO_MUNICIPIO_ESC'] == 3509502]
        
        if not bloco_filtrado.empty:
            blocos_campinas.append(bloco_filtrado)
            
    if len(blocos_campinas) == 0:
        print("Aviso: Nenhum dado de Campinas foi encontrado. Verifique os filtros.")
    else:
        # Junta todos os pedaços filtrados
        df_enem_campinas_2024 = pd.concat(blocos_campinas, ignore_index=True)
        print(f"Filtragem concluída! Encontrados {len(df_enem_campinas_2024)} candidatos de Campinas.")
        
        # Limpeza: Remove linhas com notas nulas (faltantes/eliminados)
        df_enem_campinas_2024 = df_enem_campinas_2024.dropna(subset=['NU_NOTA_MT', 'NU_NOTA_LC', 'NU_NOTA_REDACAO'])
        print(f"Dados limpos (sem faltantes): {len(df_enem_campinas_2024)} registros em Campinas.")
        
        # Salva o arquivo final compactado e leve na raiz do Colab
        df_enem_campinas_2024.to_csv("/content/enem_campinas_2024_limpo.csv", index=False)
        print("Sucesso absoluto! O arquivo 'enem_campinas_2024_limpo.csv' foi gerado.")
