import pandas as pd

caminho_resultados = "/content/DADOS/RESULTADOS_2024.csv"
caminho_participantes = "/content/DADOS/PARTICIPANTES_2024.csv"

print("--- COLUNAS DO ARQUIVO: RESULTADOS_2024.csv ---")
try:
    df_res = pd.read_csv(caminho_resultados, sep=';', encoding='latin-1', nrows=1)
    print(list(df_res.columns))
except Exception as e:
    print(f"Erro ao ler resultados: {e}")

print("\n--- COLUNAS DO ARQUIVO: PARTICIPANTES_2024.csv ---")
try:
    df_part = pd.read_csv(caminho_participantes, sep=';', encoding='latin-1', nrows=1)
    print(list(df_part.columns))
except Exception as e:
    print(f"Erro ao ler participantes: {e}")
