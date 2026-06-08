import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pymongo import MongoClient

# 1. Conexão com o seu MongoDB Atlas para buscar os dados salvos
uri = "mongodb+srv://arthurbc1:km15u11Sw48v11Ot@aulamongo.jrraoqr.mongodb.net/"
client = MongoClient(uri)
db = client['projeto_integrador_educacao']
colecao_enem = db['desempenho_enem']

# Puxa todos os registros de Campinas do banco para um DataFrame do Pandas
dados_banco = list(colecao_enem.find({}, {"_id": 0}))
df_enem = pd.DataFrame(dados_banco)

# Configuração visual dos gráficos
sns.set_theme(style="whitegrid")
plt.figure(figsize=(15, 6))

# =========================================================================
# GRÁFICO 1: DISTRIBUIÇÃO (HISTOGRAMA) DAS NOTAS DE MATEMÁTICA E LINGUAGENS
# =========================================================================
plt.subplot(1, 2, 1) # Lado esquerdo
sns.kdeplot(data=df_enem['NU_NOTA_MT'], fill=True, color="crimson", label="Matemática", alpha=0.4)
sns.kdeplot(data=df_enem['NU_NOTA_LC'], fill=True, color="dodgerblue", label="Linguagens", alpha=0.4)

plt.title("Distribuição das Notas no ENEM 2024\n(Candidatos de Campinas)", fontsize=13, fontweight='bold')
plt.xlabel("Nota Obtida", fontsize=11)
plt.ylabel("Densidade de Alunos", fontsize=11)
plt.xlim(300, 1000)
plt.legend(loc="upper right")

# =========================================================================
# GRÁFICO 2: MÉDIA DAS NOTAS POR DEPENDÊNCIA ADMINISTRATIVA (TIPO DE ESCOLA)
# =========================================================================
# Mapeamento dos números do INEP para os nomes reais das redes
mapeamento_escolas = {1: 'Federal', 2: 'Estadual', 3: 'Municipal', 4: 'Privada'}
df_enem['Tipo_Escola'] = df_enem['TP_DEPENDENCIA_ADM_ESC'].map(mapeamento_escolas)

# Agrupa os dados para calcular as médias por tipo de escola
df_medias = df_enem.groupby('Tipo_Escola')[['NU_NOTA_MT', 'NU_NOTA_REDACAO']].mean().reset_index()
# Transforma o formato para facilitar a plotagem de barras duplas
df_melted = df_medias.melt(id_vars='Tipo_Escola', value_vars=['NU_NOTA_MT', 'NU_NOTA_REDACAO'],
                           var_name='Prova', value_name='Nota_Media')

plt.subplot(1, 2, 2) # Lado direito
sns.barplot(data=df_melted, x='Tipo_Escola', y='Nota_Media', hue='Prova', palette=["#e74c3c", "#2ecc71"])

plt.title("Desempenho Médio por Tipo de Escola\nem Campinas (ENEM 2024)", fontsize=13, fontweight='bold')
plt.xlabel("Dependência Administrativa", fontsize=11)
plt.ylabel("Nota Média", fontsize=11)
plt.ylim(0, 1000)
plt.legend(labels=['Matemática', 'Redação'], loc="lower right")

# Ajusta o espaçamento e mostra os gráficos
plt.tight_layout()
plt.show()
