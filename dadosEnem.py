import pandas as pd
import zipfile
import os

# ==========================================
# 1. CONFIGURAÇÕES INICIAIS
# ==========================================
# Insira aqui o nome exato dos seus arquivos .zip
arquivos_zip = ['microdados_enem_2022.zip', 'microdados_enem_2023.zip', 'microdados_enem_2024.zip']
cidade_alvo = 'Campinas'

# Mapeamento das colunas oficiais do ENEM para as que vocês definiram no relatório
# Dica: Q006 é a pergunta do questionário socioeconômico sobre a Renda Familiar
colunas_interesse = ['NO_MUNICIPIO_PROVA', 'NU_NOTA_MT', 'NU_NOTA_LC', 'NU_NOTA_REDACAO', 'Q006']

# Lista para guardar os dados filtrados de todos os anos
dados_campinas_totais = []

# ==========================================
# 2. PROCESSAMENTO DOS ARQUIVOS (COM CHUNKS)
# ==========================================
for arquivo in arquivos_zip:
    print(f"\nIniciando o processamento do arquivo: {arquivo}...")
    
    try:
        with zipfile.ZipFile(arquivo, 'r') as z:
            # O INEP costuma colocar o CSV dentro de uma pasta "DADOS" dentro do zip.
            # Vamos procurar o nome exato do arquivo .csv ou .txt
            nome_csv = [nome for nome in z.namelist() if nome.endswith('.csv') or nome.endswith('.txt')][0]
            
            with z.open(nome_csv) as f:
                # Lendo em "chunks" (lotes de 100.000 linhas por vez para não travar o PC)
                chunks = pd.read_csv(f, sep=';', encoding='ISO-8859-1', usecols=colunas_interesse, chunksize=100000)
                
                lote_num = 1
                for chunk in chunks:
                    # 1. Filtra apenas os alunos que fizeram prova em Campinas
                    chunk_filtrado = chunk[chunk['NO_MUNICIPIO_PROVA'] == cidade_alvo].copy()
                    
                    # 2. Remove alunos que faltaram e ficaram com nota NaN (Not a Number)
                    chunk_filtrado.dropna(subset=['NU_NOTA_MT', 'NU_NOTA_LC', 'NU_NOTA_REDACAO'], inplace=True)
                    
                    # 3. Adiciona esse lote limpo na nossa lista geral se ele não estiver vazio
                    if not chunk_filtrado.empty:
                        dados_campinas_totais.append(chunk_filtrado)
                    
                    print(f"Lote {lote_num} processado...")
                    lote_num += 1
                    
        print(f"Sucesso! Dados de Campinas extraídos de {arquivo}.")
        
    except Exception as e:
        print(f"Erro ao processar {arquivo}: {e}")

# ==========================================
# 3. CONSOLIDAÇÃO E EXPORTAÇÃO
# ==========================================
if dados_campinas_totais:
    print("\nJuntando todos os anos e renomeando as colunas...")
    # Une todos os pedaços filtrados em um único DataFrame
    df_final = pd.concat(dados_campinas_totais, ignore_index=True)
    
    # Renomeando as colunas para o padrão do relatório do projeto
    df_final.rename(columns={
        'NU_NOTA_MT': 'Nota_Matematica',
        'NU_NOTA_LC': 'Nota_Linguagens',
        'NU_NOTA_REDACAO': 'Nota_Redacao',
        'Q006': 'Renda_Familiar'
    }, inplace=True)
    
    # Removendo a coluna do município pois todos já são de Campinas
    df_final.drop(columns=['NO_MUNICIPIO_PROVA'], inplace=True)
    
    # Salva o arquivo tratado final. Esse arquivo será pequeno e fácil de enviar pro MongoDB!
    df_final.to_csv('microdados_campinas_tratado.csv', index=False)
    print(f"\nFinalizado! Arquivo 'microdados_campinas_tratado.csv' gerado com {len(df_final)} registros.")
else:
    print("\nNenhum dado de Campinas foi encontrado ou ocorreu um erro na leitura.")
