import pandas as pd
from pathlib import Path

# =========================================================
# 1. LOCALIZAÇÃO E LEITURA DA BASE
# =========================================================

# Pasta onde está este arquivo Python
pasta = Path(__file__).parent

# Caminho da base original
arquivo = pasta / "data v1.csv"

# Carregar a base
df = pd.read_csv(
    arquivo,
    encoding="latin1"
)

print("Base carregada com sucesso!")

# =========================================================
# 2. DIAGNÓSTICO INICIAL
# =========================================================

# Quantidade de linhas e colunas
print("\nDimensão da base:")
print("Linhas:", df.shape[0])
print("Colunas:", df.shape[1])

# Primeiras linhas
print("\nPrimeiras linhas:")
print(df.head())

# Nomes das colunas
print("\nColunas:")
print(df.columns.tolist())

# Tipos dos dados
print("\nTipos de dados:")
print(df.dtypes)

# Valores nulos
print("\nValores nulos:")
print(df.isnull().sum())

# Linhas totalmente duplicadas
print("\nLinhas duplicadas:")
print(df.duplicated().sum())

# =========================================================
# 3. CÓPIA PARA TRATAMENTO
# =========================================================

# Preservamos df como base original
# Todo tratamento será realizado em df_tratado
df_tratado = df.copy()

print("\nCópia para tratamento criada com sucesso.")
print("Base original:", df.shape)
print("Base de tratamento:", df_tratado.shape)

# =========================================================
# 4. TRATAMENTO DAS DATAS
# =========================================================

df_tratado["DATAVERIFICACAO"] = pd.to_datetime(
    df_tratado["DATAVERIFICACAO"],
    format="%d/%m/%y",
    errors="coerce"
)

df_tratado["DT_HORA_VERIF"] = pd.to_datetime(
    df_tratado["DT_HORA_VERIF"],
    format="%d/%m/%Y %H:%M:%S",
    errors="coerce"
)

print("\nDatas tratadas.")

print("\nPeríodo da base:")
print("Data inicial:", df_tratado["DATAVERIFICACAO"].min())
print("Data final:", df_tratado["DATAVERIFICACAO"].max())

print("\nDatas inválidas:")
print(
    "DATAVERIFICACAO:",
    df_tratado["DATAVERIFICACAO"].isna().sum()
)

print(
    "DT_HORA_VERIF:",
    df_tratado["DT_HORA_VERIF"].isna().sum()
)
# =========================================================
# 4.1 VALIDAÇÃO VISUAL DAS DATAS
# =========================================================

comparacao_datas = pd.DataFrame({
    "DATA_ORIGINAL": df["DATAVERIFICACAO"].head(20),
    "DATA_TRATADA": df_tratado["DATAVERIFICACAO"].head(20),
    "HORA_ORIGINAL": df["DT_HORA_VERIF"].head(20),
    "HORA_TRATADA": df_tratado["DT_HORA_VERIF"].head(20)
})

print("\nValidação das datas:")
print(comparacao_datas.to_string(index=False))

# =========================================================
# 5. PADRONIZAÇÃO DE CAMPOS DE TEXTO
# =========================================================

colunas_texto = [
    "SERVIÇO",
    "FISCAL",
    "MOTORISTA",
    "NOMEFANTASIA",
    "DESC_ITEM",
    "NR_SERIE",
    "ESPECIE",
    "RESULTADO",
    "ENDERECO_COMPLETO",
    "REGIONAL"
]

for coluna in colunas_texto:
    df_tratado[coluna] = (
        df_tratado[coluna]
        .astype("string")
        .str.strip()
    )

print("\nCampos de texto padronizados.")

# =========================================================
# 6. DIAGNÓSTICO DOS PRINCIPAIS CAMPOS LOGÍSTICOS
# =========================================================

print("\nRLDs únicos:")
print(df_tratado["RLD_ID"].nunique())

print("\nProprietários únicos:")
print(df_tratado["COD_PROPR"].nunique())

print("\nEndereços únicos:")
print(df_tratado["ENDERECO_COMPLETO"].nunique())

print("\nFiscais únicos:")
print(df_tratado["IDFISCAL"].nunique())

print("\nMotoristas únicos:")
print(df_tratado["IDMOTORISTA"].nunique())

print("\nResultados:")
print(df_tratado["RESULTADO"].value_counts())

print("\nServiços:")
print(df_tratado["SERVIÇO"].value_counts())
# =========================================================
# 7. ANÁLISE DA UNIDADE LOGÍSTICA
# =========================================================

# Quantos endereços diferentes existem dentro de cada RLD
enderecos_por_rld = (
    df_tratado
    .groupby("RLD_ID")["ENDERECO_COMPLETO"]
    .nunique()
    .sort_values(ascending=False)
)

print("\nQuantidade de endereços por RLD:")
print(enderecos_por_rld.describe())

print("\nRLDs com mais endereços distintos:")
print(enderecos_por_rld.head(20))


# Quantos proprietários diferentes existem dentro de cada RLD
proprietarios_por_rld = (
    df_tratado
    .groupby("RLD_ID")["COD_PROPR"]
    .nunique()
    .sort_values(ascending=False)
)

print("\nQuantidade de proprietários por RLD:")
print(proprietarios_por_rld.describe())

print("\nRLDs com mais proprietários:")
print(proprietarios_por_rld.head(20))


# Quantos fiscais existem dentro de cada RLD
fiscais_por_rld = (
    df_tratado
    .groupby("RLD_ID")["IDFISCAL"]
    .nunique()
)

print("\nQuantidade de fiscais por RLD:")
print(fiscais_por_rld.value_counts().sort_index())


# Quantos motoristas existem dentro de cada RLD
motoristas_por_rld = (
    df_tratado
    .groupby("RLD_ID")["IDMOTORISTA"]
    .nunique(dropna=True)
)

print("\nQuantidade de motoristas por RLD:")
print(motoristas_por_rld.value_counts().sort_index())

# =========================================================
# 8. ANÁLISE TEMPORAL DOS RLDs
# =========================================================

resumo_rld = (
    df_tratado
    .groupby("RLD_ID")
    .agg(
        data=("DATAVERIFICACAO", "first"),
        primeira_verificacao=("DT_HORA_VERIF", "min"),
        ultima_verificacao=("DT_HORA_VERIF", "max"),
        quantidade_registros=("RLD_ID", "size"),
        quantidade_enderecos=("ENDERECO_COMPLETO", "nunique"),
        quantidade_proprietarios=("COD_PROPR", "nunique"),
        quantidade_fiscais=("IDFISCAL", "nunique"),
        quantidade_motoristas=("IDMOTORISTA", "nunique")
    )
    .reset_index()
)

print("\nResumo dos RLDs:")
print(resumo_rld.head(20))
# =========================================================
# 9. VALIDAÇÃO DA DATA POR RLD
# =========================================================

datas_por_rld = (
    df_tratado
    .groupby("RLD_ID")["DATAVERIFICACAO"]
    .nunique()
)

print("\nQuantidade de datas diferentes dentro de cada RLD:")
print(datas_por_rld.value_counts().sort_index())

print("\nRLDs com mais de uma data:")
print(datas_por_rld[datas_por_rld > 1])
# =========================================================
# 10. IDENTIFICAÇÃO DAS VISITAS
# =========================================================

visitas = (
    df_tratado
    .groupby([
        "RLD_ID",
        "DATAVERIFICACAO",
        "ENDERECO_COMPLETO"
    ])
    .agg(
        primeira_verificacao=("DT_HORA_VERIF", "min"),
        ultima_verificacao=("DT_HORA_VERIF", "max"),
        quantidade_instrumentos=("CODITEM", "size"),
        proprietarios=("COD_PROPR", "nunique")
    )
    .reset_index()
)

print("\nQuantidade total de visitas identificadas:")
print(len(visitas))

print("\nPrimeiras visitas:")
print(visitas.head(20))
# =========================================================
# 11. ORDENAÇÃO CRONOLÓGICA DAS VERIFICAÇÕES
# =========================================================

df_ordenado = (
    df_tratado
    .sort_values([
        "RLD_ID",
        "DT_HORA_VERIF"
    ])
    .copy()
)

print("\nBase ordenada cronologicamente.")
# =========================================================
# 12. IDENTIFICAÇÃO DE MUDANÇAS DE ENDEREÇO
# =========================================================

df_ordenado["ENDERECO_ANTERIOR"] = (
    df_ordenado
    .groupby("RLD_ID")["ENDERECO_COMPLETO"]
    .shift()
)

df_ordenado["NOVA_PARADA"] = (
    df_ordenado["ENDERECO_COMPLETO"]
    != df_ordenado["ENDERECO_ANTERIOR"]
)

# Primeira linha de cada RLD sempre é uma nova parada
df_ordenado.loc[
    df_ordenado["ENDERECO_ANTERIOR"].isna(),
    "NOVA_PARADA"
] = True

# Número sequencial da parada dentro do RLD
df_ordenado["ORDEM_PARADA"] = (
    df_ordenado
    .groupby("RLD_ID")["NOVA_PARADA"]
    .cumsum()
)# =========================================================
# 13. VERIFICAÇÃO DE RETORNOS AO MESMO ENDEREÇO
# =========================================================

paradas_por_rld = (
    df_ordenado
    .groupby("RLD_ID")["ORDEM_PARADA"]
    .max()
)

enderecos_unicos_por_rld = (
    df_ordenado
    .groupby("RLD_ID")["ENDERECO_COMPLETO"]
    .nunique()
)

comparacao_paradas = pd.DataFrame({
    "enderecos_unicos": enderecos_unicos_por_rld,
    "paradas_reais": paradas_por_rld
})

comparacao_paradas["possui_retorno"] = (
    comparacao_paradas["paradas_reais"]
    > comparacao_paradas["enderecos_unicos"]
)

print("\nRLDs com retorno ao mesmo endereço:")
print(comparacao_paradas["possui_retorno"].value_counts())

print("\nQuantidade total de paradas pela sequência:")
print(paradas_por_rld.sum())

print("\nRLDs que possuem retorno:")
print(
    comparacao_paradas[
        comparacao_paradas["possui_retorno"]
    ].head(20)
)
# =========================================================
# 14. CONSTRUÇÃO DA TABELA DE PARADAS HISTÓRICAS
# =========================================================

paradas = (
    df_ordenado
    .groupby([
        "RLD_ID",
        "ORDEM_PARADA"
    ])
    .agg(
        data=("DATAVERIFICACAO", "first"),

        id_fiscal=("IDFISCAL", "first"),
        fiscal=("FISCAL", "first"),

        id_motorista=("IDMOTORISTA", "first"),
        motorista=("MOTORISTA", "first"),

        endereco=("ENDERECO_COMPLETO", "first"),

        primeiro_horario=("DT_HORA_VERIF", "min"),
        ultimo_horario=("DT_HORA_VERIF", "max"),

        quantidade_verificacoes=("CODITEM", "size"),
        quantidade_proprietarios=("COD_PROPR", "nunique"),
        quantidade_itens=("CODITEM", "nunique")
    )
    .reset_index()
)

print("\nTabela de paradas criada.")

print("\nQuantidade de paradas:")
print(len(paradas))

print("\nPrimeiras paradas:")
print(paradas.head(20))
# =========================================================
# 15. TEMPO OBSERVADO EM CADA PARADA
# =========================================================

paradas["tempo_atendimento_min"] = (
    (
        paradas["ultimo_horario"]
        - paradas["primeiro_horario"]
    )
    .dt.total_seconds()
    / 60
)

print("\nTempo de atendimento por parada:")
print(paradas["tempo_atendimento_min"].describe())
# =========================================================
# 16. ANÁLISE DOS TEMPOS ZERO
# =========================================================

paradas_tempo_zero = (
    paradas["tempo_atendimento_min"] == 0
).sum()

print("\nParadas com tempo observado igual a zero:")
print(paradas_tempo_zero)

print("\nPercentual:")
print(
    round(
        paradas_tempo_zero
        / len(paradas)
        * 100,
        2
    ),
    "%"
)
# =========================================================
# 17. VOLUME DE VERIFICAÇÕES POR PARADA
# =========================================================

print("\nQuantidade de verificações por parada:")
print(
    paradas["quantidade_verificacoes"]
    .describe()
)

print("\nParadas com maior quantidade de verificações:")
print(
    paradas[
        [
            "RLD_ID",
            "ORDEM_PARADA",
            "endereco",
            "quantidade_verificacoes"
        ]
    ]
    .sort_values(
        "quantidade_verificacoes",
        ascending=False
    )
    .head(20)
)
# =========================================================
# 18. VALIDAÇÃO DA TABELA DE PARADAS
# =========================================================

erros_proprietarios = paradas[
    paradas["quantidade_proprietarios"]
    > paradas["quantidade_verificacoes"]
]

erros_itens = paradas[
    paradas["quantidade_itens"]
    > paradas["quantidade_verificacoes"]
]

print("\nVALIDAÇÃO DA TABELA DE PARADAS")

print("\nCasos impossíveis - proprietários > verificações:")
print(len(erros_proprietarios))

print("\nCasos impossíveis - itens > verificações:")
print(len(erros_itens))

print("\nPrimeiros casos problemáticos:")
print(
    paradas[
        [
            "RLD_ID",
            "ORDEM_PARADA",
            "quantidade_verificacoes",
            "quantidade_proprietarios",
            "quantidade_itens"
        ]
    ].head(20)
)
# =========================================================
# 19. INSPEÇÃO DE UMA PARADA
# =========================================================

teste = df_ordenado[
    (df_ordenado["RLD_ID"] == 1835000)
    & (df_ordenado["ORDEM_PARADA"] == 1)
]

print("\nREGISTROS BRUTOS DA PARADA TESTE:")

print(
    teste[
        [
            "RLD_ID",
            "ORDEM_PARADA",
            "DT_HORA_VERIF",
            "COD_PROPR",
            "CODITEM",
            "ENDERECO_COMPLETO"
        ]
    ].to_string(index=False)
)

print("\nQuantidade de linhas:")
print(len(teste))

print("\nProprietários únicos:")
print(teste["COD_PROPR"].nunique())

print("\nItens únicos:")
print(teste["CODITEM"].nunique())
# =========================================================
# 20. VALIDAÇÃO DA ORDEM CRONOLÓGICA DAS PARADAS
# =========================================================

enderecos_mesmo_horario = (
    df_tratado
    .groupby(
        ["RLD_ID", "DT_HORA_VERIF"]
    )["ENDERECO_COMPLETO"]
    .nunique()
)

conflitos_horario = enderecos_mesmo_horario[
    enderecos_mesmo_horario > 1
]

print("\nVALIDAÇÃO DA ORDEM CRONOLÓGICA")

print("\nRLD + horário com mais de um endereço:")
print(len(conflitos_horario))

if len(conflitos_horario) > 0:

    print("\nPrimeiros conflitos:")
    print(conflitos_horario.head(20))

else:

    print(
        "\nNenhum conflito encontrado."
        "\nA ordem cronológica pode ser utilizada."
    )

# =========================================================
# 22. AUDITORIA DOS ENDEREÇOS
# =========================================================

enderecos = (
    df_tratado[
        ["ENDERECO_COMPLETO"]
    ]
    .drop_duplicates()
    .copy()
)

print("\nQuantidade de endereços únicos:")
print(len(enderecos))

# Verifica presença de CEP
enderecos["TEM_CEP"] = (
    enderecos["ENDERECO_COMPLETO"]
    .str.contains(
        r"CEP\s*:",
        case=False,
        na=False,
        regex=True
    )
)

print("\nEndereços com CEP:")
print(enderecos["TEM_CEP"].value_counts())

print("\nPercentual com CEP:")
print(
    round(
        enderecos["TEM_CEP"].mean() * 100,
        2
    ),
    "%"
)
# =========================================================
# 23. EXTRAÇÃO DO CEP
# =========================================================

enderecos["CEP"] = (
    enderecos["ENDERECO_COMPLETO"]
    .str.extract(
        r"CEP\s*:\s*(\d{8})",
        expand=False
    )
)

print("\nCEPs extraídos:")
print(enderecos["CEP"].notna().sum())

print("\nEndereços sem CEP identificado:")
print(enderecos["CEP"].isna().sum())

print("\nExemplos sem CEP:")
print(
    enderecos[
        enderecos["CEP"].isna()
    ]["ENDERECO_COMPLETO"]
    .head(30)
    .to_string(index=False)
)
# =========================================================
# 24. INSPEÇÃO DA ESTRUTURA DOS ENDEREÇOS
# =========================================================

print("\nAmostra de endereços completos:")
print(
    enderecos["ENDERECO_COMPLETO"]
    .sample(
        min(30, len(enderecos)),
        random_state=42
    )
    .to_string(index=False)
)
# =========================================================
# 25. SEPARAÇÃO ESTRUTURAL DO ENDEREÇO
# =========================================================

enderecos_geo = enderecos.copy()

# Remove espaços extras apenas nas extremidades
enderecos_geo["ENDERECO_LIMPO"] = (
    enderecos_geo["ENDERECO_COMPLETO"]
    .str.strip()
)

# Extrai qualquer sequência numérica depois de "CEP:"
# sem exigir ainda exatamente 8 dígitos
enderecos_geo["CEP_BRUTO"] = (
    enderecos_geo["ENDERECO_LIMPO"]
    .str.extract(
        r"CEP\s*:\s*(\d+)",
        expand=False
    )
)

# Quantidade de dígitos encontrada
enderecos_geo["TAMANHO_CEP"] = (
    enderecos_geo["CEP_BRUTO"]
    .str.len()
)

print("\nQuantidade por tamanho de CEP:")
print(
    enderecos_geo["TAMANHO_CEP"]
    .value_counts(dropna=False)
    .sort_index()
)

print("\nEndereços cujo CEP não possui 8 dígitos:")
print(
    enderecos_geo[
        enderecos_geo["TAMANHO_CEP"] != 8
    ][
        [
            "ENDERECO_COMPLETO",
            "CEP_BRUTO",
            "TAMANHO_CEP"
        ]
    ]
    .head(50)
    .to_string(index=False)
)
# =========================================================
# 26. EXTRAÇÃO DE MUNICÍPIO E BAIRRO
# =========================================================

# Retira somente a parte final do CEP
enderecos_geo["SEM_CEP"] = (
    enderecos_geo["ENDERECO_LIMPO"]
    .str.replace(
        r"\s*-\s*CEP\s*:.*$",
        "",
        regex=True,
        case=False
    )
    .str.strip()
)

# Município = último bloco depois de " - "
enderecos_geo["MUNICIPIO"] = (
    enderecos_geo["SEM_CEP"]
    .str.rsplit(" - ", n=1)
    .str[-1]
    .str.strip()
)

# Retira município
enderecos_geo["SEM_MUNICIPIO"] = (
    enderecos_geo["SEM_CEP"]
    .str.rsplit(" - ", n=1)
    .str[0]
    .str.strip()
)

# Bairro = último bloco restante
enderecos_geo["BAIRRO"] = (
    enderecos_geo["SEM_MUNICIPIO"]
    .str.rsplit(" - ", n=1)
    .str[-1]
    .str.strip()
)

# Parte anterior = logradouro + número
enderecos_geo["LOGRADOURO_NUMERO"] = (
    enderecos_geo["SEM_MUNICIPIO"]
    .str.rsplit(" - ", n=1)
    .str[0]
    .str.strip()
)

print("\nQuantidade de municípios identificados:")
print(enderecos_geo["MUNICIPIO"].nunique())

print("\nMunicípios com mais endereços:")
print(
    enderecos_geo["MUNICIPIO"]
    .value_counts()
    .head(30)
)

print("\nExemplo da separação:")
print(
    enderecos_geo[
        [
            "LOGRADOURO_NUMERO",
            "BAIRRO",
            "MUNICIPIO",
            "CEP_BRUTO"
        ]
    ]
    .head(30)
    .to_string(index=False)
)
# =========================================================
# 27. PREPARAÇÃO DOS ENDEREÇOS PARA GEOCODIFICAÇÃO
# =========================================================

enderecos_geo["ENDERECO_GEOCODIFICACAO"] = (
    enderecos_geo["LOGRADOURO_NUMERO"].astype("string").str.strip()
    + ", "
    + enderecos_geo["BAIRRO"].astype("string").str.strip()
    + ", "
    + enderecos_geo["MUNICIPIO"].astype("string").str.strip()
    + ", SP, Brasil"
)

print("\nEndereços preparados para geocodificação:")

print(
    enderecos_geo[
        [
            "ENDERECO_COMPLETO",
            "ENDERECO_GEOCODIFICACAO"
        ]
    ]
    .head(20)
    .to_string(index=False)
)

print("\nQuantidade preparada:")
print(len(enderecos_geo))

print("\nEndereços de geocodificação vazios:")
print(
    enderecos_geo[
        "ENDERECO_GEOCODIFICACAO"
    ]
    .isna()
    .sum()
)
# =========================================================
# 28. TESTE DE GEOCODIFICAÇÃO - AMOSTRA CONTROLADA
# =========================================================

import json
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# ---------------------------------------------------------
# 28.1 SELEÇÃO DA AMOSTRA
# ---------------------------------------------------------

# Escolhe 1 endereço por município
# e limita o teste a 10 municípios diferentes
amostra_geo = (
    enderecos_geo
    .groupby("MUNICIPIO", as_index=False)
    .first()
    .head(10)
    .copy()
)

print("\n=========================================")
print("TESTE DE GEOCODIFICAÇÃO")
print("=========================================")

print("\nQuantidade de endereços na amostra:")
print(len(amostra_geo))

print("\nMunicípios selecionados:")
print(
    amostra_geo[
        [
            "MUNICIPIO",
            "ENDERECO_GEOCODIFICACAO"
        ]
    ].to_string(index=False)
)


# ---------------------------------------------------------
# 28.2 FUNÇÃO DE GEOCODIFICAÇÃO
# ---------------------------------------------------------

def geocodificar_endereco(endereco):

    url_base = (
        "https://nominatim.openstreetmap.org/search"
    )

    parametros = {
        "q": endereco,
        "format": "jsonv2",
        "limit": 1,
        "addressdetails": 1,
        "countrycodes": "br"
    }

    url = (
        url_base
        + "?"
        + urlencode(parametros)
    )

    requisicao = Request(
        url,
        headers={
            "User-Agent": (
                "SafeFlow-Fatec-SJC/0.1 "
                "(academic logistics project)"
            )
        }
    )

    try:

        with urlopen(
            requisicao,
            timeout=20
        ) as resposta:

            dados = json.loads(
                resposta.read().decode("utf-8")
            )

        if len(dados) == 0:

            return {
                "latitude": None,
                "longitude": None,
                "endereco_encontrado": None,
                "status_geocodificacao": "NAO_ENCONTRADO"
            }

        resultado = dados[0]

        return {
            "latitude": float(resultado["lat"]),
            "longitude": float(resultado["lon"]),
            "endereco_encontrado": resultado[
                "display_name"
            ],
            "status_geocodificacao": "ENCONTRADO"
        }

    except HTTPError as erro:

        return {
            "latitude": None,
            "longitude": None,
            "endereco_encontrado": None,
            "status_geocodificacao":
                f"ERRO_HTTP_{erro.code}"
        }

    except URLError:

        return {
            "latitude": None,
            "longitude": None,
            "endereco_encontrado": None,
            "status_geocodificacao":
                "ERRO_CONEXAO"
        }

    except Exception as erro:

        return {
            "latitude": None,
            "longitude": None,
            "endereco_encontrado": None,
            "status_geocodificacao":
                f"ERRO_{type(erro).__name__}"
        }


# ---------------------------------------------------------
# 28.3 EXECUÇÃO CONTROLADA
# ---------------------------------------------------------

resultados_geo = []

for numero, (_, linha) in enumerate(
    amostra_geo.iterrows(),
    start=1
):

    endereco = linha[
        "ENDERECO_GEOCODIFICACAO"
    ]

    print(
        f"\n[{numero}/{len(amostra_geo)}]"
        f" Consultando:"
    )

    print(endereco)

    resultado = geocodificar_endereco(
        endereco
    )

    resultados_geo.append(resultado)

    print(
        "Status:",
        resultado[
            "status_geocodificacao"
        ]
    )

    # Política do Nominatim:
    # máximo de 1 requisição por segundo.
    # Usamos 1,1 segundo por segurança.
    time.sleep(1.1)


# ---------------------------------------------------------
# 28.4 JUNÇÃO DOS RESULTADOS
# ---------------------------------------------------------

resultado_geo_df = pd.DataFrame(
    resultados_geo
)

amostra_geo = pd.concat(
    [
        amostra_geo.reset_index(drop=True),
        resultado_geo_df
    ],
    axis=1
)


# ---------------------------------------------------------
# 28.5 VALIDAÇÃO
# ---------------------------------------------------------

print("\n=========================================")
print("RESULTADO DA GEOCODIFICAÇÃO")
print("=========================================")

print(
    amostra_geo[
        [
            "MUNICIPIO",
            "ENDERECO_GEOCODIFICACAO",
            "latitude",
            "longitude",
            "status_geocodificacao"
        ]
    ].to_string(index=False)
)

print("\nResumo:")

print(
    amostra_geo[
        "status_geocodificacao"
    ].value_counts(
        dropna=False
    )
)


# ---------------------------------------------------------
# 28.6 CACHE LOCAL
# ---------------------------------------------------------

arquivo_cache = (
    pasta
    / "geocodificacao_amostra.csv"
)

amostra_geo.to_csv(
    arquivo_cache,
    index=False,
    encoding="utf-8-sig"
)

print("\nCache salvo em:")
print(arquivo_cache)

print(
    "\nFonte geográfica:"
    " OpenStreetMap / Nominatim"
)
# =========================================================
# 29. TESTE DE GEOCODIFICAÇÃO PROGRESSIVA
# =========================================================

print("\n=========================================")
print("GEOCODIFICAÇÃO PROGRESSIVA")
print("=========================================")


def consultar_nominatim(endereco):

    url_base = (
        "https://nominatim.openstreetmap.org/search"
    )

    parametros = {
        "q": endereco,
        "format": "jsonv2",
        "limit": 1,
        "addressdetails": 1,
        "countrycodes": "br"
    }

    url = (
        url_base
        + "?"
        + urlencode(parametros)
    )

    requisicao = Request(
        url,
        headers={
            "User-Agent": (
                "SafeFlow-Fatec-SJC/0.1 "
                "(academic logistics project)"
            )
        }
    )

    try:

        with urlopen(
            requisicao,
            timeout=20
        ) as resposta:

            dados = json.loads(
                resposta.read().decode("utf-8")
            )

        if len(dados) == 0:
            return None

        resultado = dados[0]

        return {
            "latitude": float(resultado["lat"]),
            "longitude": float(resultado["lon"]),
            "endereco_encontrado":
                resultado["display_name"]
        }

    except Exception:
        return None


def geocodificar_progressivo(linha):

    logradouro_numero = str(
        linha["LOGRADOURO_NUMERO"]
    ).strip()

    municipio = str(
        linha["MUNICIPIO"]
    ).strip()

    bairro = str(
        linha["BAIRRO"]
    ).strip()

    # Remove o número para criar
    # uma consulta menos específica
    logradouro = (
        logradouro_numero
        .split(",")[0]
        .strip()
    )

    tentativas = [
        (
            "COMPLETO",
            f"{logradouro_numero}, "
            f"{bairro}, "
            f"{municipio}, SP, Brasil"
        ),

        (
            "SEM_BAIRRO",
            f"{logradouro_numero}, "
            f"{municipio}, SP, Brasil"
        ),

        (
            "SEM_NUMERO",
            f"{logradouro}, "
            f"{municipio}, SP, Brasil"
        )
    ]

    for estrategia, consulta in tentativas:

        print(
            f"   Tentativa {estrategia}: "
            f"{consulta}"
        )

        resultado = consultar_nominatim(
            consulta
        )

        # Respeita o limite do serviço
        time.sleep(1.1)

        if resultado is not None:

            resultado[
                "estrategia_geocodificacao"
            ] = estrategia

            resultado[
                "consulta_utilizada"
            ] = consulta

            resultado[
                "status_geocodificacao"
            ] = "ENCONTRADO"

            return resultado

    return {
        "latitude": None,
        "longitude": None,
        "endereco_encontrado": None,
        "estrategia_geocodificacao": None,
        "consulta_utilizada": None,
        "status_geocodificacao":
            "NAO_ENCONTRADO"
    }


# ---------------------------------------------------------
# EXECUTA SOMENTE NOS 5 QUE FALHARAM
# ---------------------------------------------------------

falhas_amostra = amostra_geo[
    amostra_geo[
        "status_geocodificacao"
    ] == "NAO_ENCONTRADO"
].copy()


print("\nEndereços que serão retestados:")
print(len(falhas_amostra))


resultados_fallback = []

for numero, (_, linha) in enumerate(
    falhas_amostra.iterrows(),
    start=1
):

    print(
        f"\n[{numero}/{len(falhas_amostra)}]"
    )

    print(
        "Original:",
        linha["ENDERECO_COMPLETO"]
    )

    resultado = geocodificar_progressivo(
        linha
    )

    resultados_fallback.append(
        resultado
    )

    print(
        "Resultado:",
        resultado[
            "status_geocodificacao"
        ]
    )

    print(
        "Estratégia:",
        resultado[
            "estrategia_geocodificacao"
        ]
    )


# ---------------------------------------------------------
# RESULTADO
# ---------------------------------------------------------

resultado_fallback_df = pd.DataFrame(
    resultados_fallback
)

falhas_amostra = pd.concat(
    [
        falhas_amostra.reset_index(
            drop=True
        ),
        resultado_fallback_df.add_prefix(
            "FALLBACK_"
        )
    ],
    axis=1
)


print("\n=========================================")
print("RESULTADO DO FALLBACK")
print("=========================================")

print(
    falhas_amostra[
        [
            "MUNICIPIO",
            "ENDERECO_COMPLETO",
            "FALLBACK_latitude",
            "FALLBACK_longitude",
            "FALLBACK_estrategia_geocodificacao",
            "FALLBACK_status_geocodificacao"
        ]
    ].to_string(index=False)
)


print("\nResumo das estratégias:")

print(
    falhas_amostra[
        "FALLBACK_estrategia_geocodificacao"
    ].value_counts(
        dropna=False
    )
)
# =========================================================
# 30. AUDITORIA DA QUALIDADE DA GEOCODIFICAÇÃO
# =========================================================

print("\n=========================================")
print("AUDITORIA DA QUALIDADE GEOGRÁFICA")
print("=========================================")

# Resultados encontrados diretamente no bloco 28
encontrados_diretos = amostra_geo[
    amostra_geo["status_geocodificacao"] == "ENCONTRADO"
].copy()

print("\n-----------------------------------------")
print("RESULTADOS DIRETOS")
print("-----------------------------------------")

for _, linha in encontrados_diretos.iterrows():

    print("\nMunicípio:")
    print(linha["MUNICIPIO"])

    print("Consulta enviada:")
    print(linha["ENDERECO_GEOCODIFICACAO"])

    print("Resultado retornado:")
    print(linha["endereco_encontrado"])

    print("Coordenadas:")
    print(
        linha["latitude"],
        linha["longitude"]
    )


# Resultados recuperados pelo fallback
encontrados_fallback = falhas_amostra[
    falhas_amostra[
        "FALLBACK_status_geocodificacao"
    ] == "ENCONTRADO"
].copy()

print("\n-----------------------------------------")
print("RESULTADOS RECUPERADOS POR FALLBACK")
print("-----------------------------------------")

for _, linha in encontrados_fallback.iterrows():

    print("\nMunicípio:")
    print(linha["MUNICIPIO"])

    print("Endereço histórico:")
    print(linha["ENDERECO_COMPLETO"])

    print("Estratégia:")
    print(
        linha[
            "FALLBACK_estrategia_geocodificacao"
        ]
    )

    print("Consulta utilizada:")
    print(
        linha[
            "FALLBACK_consulta_utilizada"
        ]
    )

    print("Resultado retornado:")
    print(
        linha[
            "FALLBACK_endereco_encontrado"
        ]
    )

    print("Coordenadas:")
    print(
        linha["FALLBACK_latitude"],
        linha["FALLBACK_longitude"]
    )


# Casos ainda não encontrados
nao_encontrados = falhas_amostra[
    falhas_amostra[
        "FALLBACK_status_geocodificacao"
    ] == "NAO_ENCONTRADO"
]

print("\n-----------------------------------------")
print("CASOS AINDA NÃO LOCALIZADOS")
print("-----------------------------------------")

print(
    nao_encontrados[
        [
            "MUNICIPIO",
            "ENDERECO_COMPLETO"
        ]
    ].to_string(index=False)
)


print("\n=========================================")
print("RESUMO DA AMOSTRA")
print("=========================================")

diretos = len(encontrados_diretos)
fallback = len(encontrados_fallback)
falhas = len(nao_encontrados)
total = len(amostra_geo)

print("Total testado:", total)
print("Encontrados diretamente:", diretos)
print("Recuperados por fallback:", fallback)
print("Não encontrados:", falhas)

print(
    "Cobertura final:",
    round(
        (diretos + fallback)
        / total
        * 100,
        2
    ),
    "%"
)
# =========================================================
# 31. VALIDAÇÃO REGIONAL DA GEOCODIFICAÇÃO
# =========================================================

print("\n=========================================")
print("VALIDAÇÃO REGIONAL DA GEOCODIFICAÇÃO")
print("=========================================")


# ---------------------------------------------------------
# 31.1 SELEÇÃO DA AMOSTRA REGIONAL
# ---------------------------------------------------------

# Um endereço por município.
# Não altera a base principal.
amostra_regional = (
    enderecos_geo
    .sort_values(
        [
            "MUNICIPIO",
            "ENDERECO_COMPLETO"
        ]
    )
    .groupby(
        "MUNICIPIO",
        as_index=False
    )
    .first()
    .copy()
)

print("\nMunicípios identificados:")
print(
    amostra_regional[
        "MUNICIPIO"
    ].nunique()
)

print("\nEndereços selecionados:")
print(len(amostra_regional))


# ---------------------------------------------------------
# 31.2 CACHE EM MEMÓRIA DOS TESTES ANTERIORES
# ---------------------------------------------------------

cache_geo = {}


# Resultados diretos do bloco 28
for _, linha in amostra_geo.iterrows():

    if (
        linha["status_geocodificacao"]
        == "ENCONTRADO"
    ):

        chave = linha[
            "ENDERECO_COMPLETO"
        ]

        cache_geo[chave] = {
            "latitude":
                linha["latitude"],

            "longitude":
                linha["longitude"],

            "endereco_encontrado":
                linha["endereco_encontrado"],

            "estrategia":
                "DIRETO",

            "classe_qualidade":
                "A",

            "status":
                "ENCONTRADO"
        }


# Resultados recuperados no bloco 29
for _, linha in falhas_amostra.iterrows():

    if (
        linha[
            "FALLBACK_status_geocodificacao"
        ]
        == "ENCONTRADO"
    ):

        estrategia = linha[
            "FALLBACK_estrategia_geocodificacao"
        ]

        if estrategia == "SEM_BAIRRO":
            classe = "B"

        elif estrategia == "SEM_NUMERO":
            classe = "C"

        else:
            classe = None

        chave = linha[
            "ENDERECO_COMPLETO"
        ]

        cache_geo[chave] = {
            "latitude":
                linha["FALLBACK_latitude"],

            "longitude":
                linha["FALLBACK_longitude"],

            "endereco_encontrado":
                linha[
                    "FALLBACK_endereco_encontrado"
                ],

            "estrategia":
                estrategia,

            "classe_qualidade":
                classe,

            "status":
                "ENCONTRADO"
        }


print("\nResultados anteriores carregados no cache:")
print(len(cache_geo))


# ---------------------------------------------------------
# 31.3 FUNÇÃO REGIONAL
# ---------------------------------------------------------

def geocodificar_regional(linha):

    endereco_original = linha[
        "ENDERECO_COMPLETO"
    ]

    # -------------------------------------
    # Primeiro verifica o cache
    # -------------------------------------

    if endereco_original in cache_geo:

        resultado_cache = (
            cache_geo[
                endereco_original
            ].copy()
        )

        resultado_cache[
            "origem_resultado"
        ] = "CACHE"

        return resultado_cache


    # -------------------------------------
    # Montagem das consultas
    # -------------------------------------

    logradouro_numero = str(
        linha["LOGRADOURO_NUMERO"]
    ).strip()

    bairro = str(
        linha["BAIRRO"]
    ).strip()

    municipio = str(
        linha["MUNICIPIO"]
    ).strip()

    logradouro = (
        logradouro_numero
        .split(",")[0]
        .strip()
    )


    tentativas = [

        (
            "DIRETO",
            "A",
            f"{logradouro_numero}, "
            f"{bairro}, "
            f"{municipio}, SP, Brasil"
        ),

        (
            "SEM_BAIRRO",
            "B",
            f"{logradouro_numero}, "
            f"{municipio}, SP, Brasil"
        ),

        (
            "SEM_NUMERO",
            "C",
            f"{logradouro}, "
            f"{municipio}, SP, Brasil"
        )
    ]


    # -------------------------------------
    # Execução progressiva
    # -------------------------------------

    for estrategia, classe, consulta in tentativas:

        print(
            "   Tentativa",
            estrategia + ":",
            consulta
        )

        resultado = consultar_nominatim(
            consulta
        )

        # Segurança para respeitar
        # o limite da API pública.
        time.sleep(1.1)

        if resultado is not None:

            return {
                "latitude":
                    resultado["latitude"],

                "longitude":
                    resultado["longitude"],

                "endereco_encontrado":
                    resultado[
                        "endereco_encontrado"
                    ],

                "estrategia":
                    estrategia,

                "classe_qualidade":
                    classe,

                "status":
                    "ENCONTRADO",

                "origem_resultado":
                    "NOMINATIM"
            }


    # -------------------------------------
    # Nenhuma tentativa funcionou
    # -------------------------------------

    return {
        "latitude": None,
        "longitude": None,
        "endereco_encontrado": None,
        "estrategia": None,
        "classe_qualidade": "D",
        "status": "NAO_ENCONTRADO",
        "origem_resultado": "NOMINATIM"
    }


# ---------------------------------------------------------
# 31.4 EXECUÇÃO DA AMOSTRA REGIONAL
# ---------------------------------------------------------

resultados_regionais = []

total_regional = len(
    amostra_regional
)


for numero, (_, linha) in enumerate(
    amostra_regional.iterrows(),
    start=1
):

    print("\n-----------------------------------------")

    print(
        f"[{numero}/{total_regional}]"
    )

    print(
        "Município:",
        linha["MUNICIPIO"]
    )

    print(
        "Endereço:",
        linha["ENDERECO_COMPLETO"]
    )


    resultado = geocodificar_regional(
        linha
    )


    resultados_regionais.append(
        resultado
    )


    print(
        "Status:",
        resultado["status"]
    )

    print(
        "Classe:",
        resultado[
            "classe_qualidade"
        ]
    )

    print(
        "Estratégia:",
        resultado[
            "estrategia"
        ]
    )

    print(
        "Origem:",
        resultado[
            "origem_resultado"
        ]
    )


# ---------------------------------------------------------
# 31.5 CRIAÇÃO DO DATAFRAME
# ---------------------------------------------------------

resultado_regional_df = pd.DataFrame(
    resultados_regionais
)

amostra_regional_resultado = pd.concat(
    [
        amostra_regional.reset_index(
            drop=True
        ),

        resultado_regional_df
    ],
    axis=1
)


# ---------------------------------------------------------
# 31.6 RESUMO DE QUALIDADE
# ---------------------------------------------------------

print("\n=========================================")
print("RESULTADO REGIONAL")
print("=========================================")

print(
    amostra_regional_resultado[
        [
            "MUNICIPIO",
            "classe_qualidade",
            "estrategia",
            "status",
            "origem_resultado",
            "latitude",
            "longitude"
        ]
    ].to_string(index=False)
)


print("\n=========================================")
print("DISTRIBUIÇÃO POR CLASSE")
print("=========================================")

distribuicao_classes = (
    amostra_regional_resultado[
        "classe_qualidade"
    ]
    .value_counts(
        dropna=False
    )
    .sort_index()
)

print(
    distribuicao_classes
)


# ---------------------------------------------------------
# 31.7 COBERTURA
# ---------------------------------------------------------

total = len(
    amostra_regional_resultado
)

encontrados = (
    amostra_regional_resultado[
        "status"
    ]
    == "ENCONTRADO"
).sum()

nao_encontrados = (
    amostra_regional_resultado[
        "status"
    ]
    == "NAO_ENCONTRADO"
).sum()


cobertura = (
    encontrados
    / total
    * 100
)


print("\n=========================================")
print("COBERTURA REGIONAL")
print("=========================================")

print(
    "Total de municípios:",
    total
)

print(
    "Localizados:",
    encontrados
)

print(
    "Não localizados:",
    nao_encontrados
)

print(
    "Cobertura:",
    round(cobertura, 2),
    "%"
)


# ---------------------------------------------------------
# 31.8 LISTA DE EXCEÇÕES
# ---------------------------------------------------------

excecoes_regionais = (
    amostra_regional_resultado[
        amostra_regional_resultado[
            "classe_qualidade"
        ]
        == "D"
    ]
    .copy()
)


print("\n=========================================")
print("MUNICÍPIOS COM FALHA")
print("=========================================")

if len(excecoes_regionais) == 0:

    print(
        "Nenhuma falha na amostra regional."
    )

else:

    print(
        excecoes_regionais[
            [
                "MUNICIPIO",
                "ENDERECO_COMPLETO"
            ]
        ].to_string(
            index=False
        )
    )


# ---------------------------------------------------------
# 31.9 SALVAMENTO DO RESULTADO
# ---------------------------------------------------------

arquivo_regional = (
    pasta
    / "validacao_geocodificacao_regional.csv"
)

amostra_regional_resultado.to_csv(
    arquivo_regional,
    index=False,
    encoding="utf-8-sig"
)


print("\n=========================================")
print("ARQUIVO SALVO")
print("=========================================")

print(arquivo_regional)
# =========================================================
# 32. VALIDAÇÃO DO MUNICÍPIO RETORNADO
# =========================================================

print("\n=========================================")
print("VALIDAÇÃO GEOGRÁFICA DO MUNICÍPIO")
print("=========================================")


def consultar_nominatim_detalhado(endereco):

    url_base = (
        "https://nominatim.openstreetmap.org/search"
    )

    parametros = {
        "q": endereco,
        "format": "jsonv2",
        "limit": 1,
        "addressdetails": 1,
        "countrycodes": "br"
    }

    url = (
        url_base
        + "?"
        + urlencode(parametros)
    )

    requisicao = Request(
        url,
        headers={
            "User-Agent": (
                "SafeFlow-Fatec-SJC/0.1 "
                "(academic logistics project)"
            )
        }
    )

    try:

        with urlopen(
            requisicao,
            timeout=20
        ) as resposta:

            dados = json.loads(
                resposta.read().decode(
                    "utf-8"
                )
            )

        if len(dados) == 0:
            return None

        resultado = dados[0]

        endereco_api = resultado.get(
            "address",
            {}
        )

        return {

            "latitude":
                float(resultado["lat"]),

            "longitude":
                float(resultado["lon"]),

            "display_name":
                resultado.get(
                    "display_name"
                ),

            "road":
                endereco_api.get(
                    "road"
                ),

            "suburb":
                endereco_api.get(
                    "suburb"
                ),

            "city":
                endereco_api.get(
                    "city"
                ),

            "town":
                endereco_api.get(
                    "town"
                ),

            "municipality":
                endereco_api.get(
                    "municipality"
                ),

            "county":
                endereco_api.get(
                    "county"
                ),

            "state":
                endereco_api.get(
                    "state"
                ),

            "postcode":
                endereco_api.get(
                    "postcode"
                ),

            "country":
                endereco_api.get(
                    "country"
                ),

            "country_code":
                endereco_api.get(
                    "country_code"
                )
        }

    except Exception as erro:

        print(
            "Erro:",
            type(erro).__name__,
            erro
        )

        return None


# ---------------------------------------------------------
# CASOS PARA AUDITORIA
# ---------------------------------------------------------

casos_auditoria = [
    (
        "APARECIDA",
        "1O DE MAIO, 296, APARECIDA, SP, Brasil"
    ),

    (
        "TREMEMBÉ",
        "A, 1497, TREMEMBÉ, SP, Brasil"
    ),

    (
        "AREIAS",
        "ALVES MARQUES, 129, CENTRO, AREIAS, SP, Brasil"
    ),

    (
        "JACAREÍ",
        "ALFREDO BLOIS, 376, JARDIM MARIA AMÉLIA, JACAREÍ, SP, Brasil"
    ),

    (
        "UBATUBA",
        "13 DE MAIO, 170, CENTRO, UBATUBA, SP, Brasil"
    )
]


resultados_auditoria = []


for numero, (
    municipio_esperado,
    consulta
) in enumerate(
    casos_auditoria,
    start=1
):

    print("\n-----------------------------------------")

    print(
        f"[{numero}/{len(casos_auditoria)}]"
    )

    print(
        "Município esperado:",
        municipio_esperado
    )

    print(
        "Consulta:",
        consulta
    )


    resultado = (
        consultar_nominatim_detalhado(
            consulta
        )
    )

    time.sleep(1.1)


    if resultado is None:

        print(
            "Resultado: NÃO ENCONTRADO"
        )

        continue


    print(
        "\nDisplay name:"
    )

    print(
        resultado[
            "display_name"
        ]
    )


    print(
        "\nLatitude:",
        resultado["latitude"]
    )

    print(
        "Longitude:",
        resultado["longitude"]
    )


    print(
        "\nCity:",
        resultado["city"]
    )

    print(
        "Town:",
        resultado["town"]
    )

    print(
        "Municipality:",
        resultado[
            "municipality"
        ]
    )

    print(
        "County:",
        resultado["county"]
    )

    print(
        "State:",
        resultado["state"]
    )

    print(
        "Postcode:",
        resultado["postcode"]
    )

    print(
        "Country:",
        resultado["country"]
    )

    print(
        "Country code:",
        resultado[
            "country_code"
        ]
    )


    resultados_auditoria.append(
        {
            "municipio_esperado":
                municipio_esperado,

            "consulta":
                consulta,

            **resultado
        }
    )


auditoria_geo_df = pd.DataFrame(
    resultados_auditoria
)


print("\n=========================================")
print("RESUMO DA AUDITORIA")
print("=========================================")

if len(auditoria_geo_df) > 0:

    print(
        auditoria_geo_df[
            [
                "municipio_esperado",
                "city",
                "town",
                "municipality",
                "county",
                "state",
                "postcode",
                "latitude",
                "longitude"
            ]
        ].to_string(
            index=False
        )
    )
    # =========================================================
# 33. MOTOR DE VALIDAÇÃO TERRITORIAL
# =========================================================

print("\n=========================================")
print("MOTOR DE VALIDAÇÃO TERRITORIAL")
print("=========================================")

import unicodedata
import re


# ---------------------------------------------------------
# 33.1 NORMALIZAÇÃO PARA COMPARAÇÃO
# ---------------------------------------------------------

def normalizar_geo(valor):

    if valor is None:
        return ""

    valor = str(valor).strip().upper()

    valor = unicodedata.normalize(
        "NFD",
        valor
    )

    valor = "".join(
        caractere
        for caractere in valor
        if unicodedata.category(
            caractere
        ) != "Mn"
    )

    valor = re.sub(
        r"[^A-Z0-9 ]",
        " ",
        valor
    )

    valor = re.sub(
        r"\s+",
        " ",
        valor
    ).strip()

    return valor


# ---------------------------------------------------------
# 33.2 EXTRAÇÃO DO MUNICÍPIO ADMINISTRATIVO
# ---------------------------------------------------------

def extrair_municipio_retornado(resultado):

    campos = [
        ("city", resultado.get("city")),
        ("town", resultado.get("town")),
        ("municipality", resultado.get("municipality"))
    ]

    for campo, valor in campos:

        if (
            valor is not None
            and str(valor).strip() != ""
        ):
            return campo, valor

    return None, None


# ---------------------------------------------------------
# 33.3 VALIDAÇÃO TERRITORIAL
# ---------------------------------------------------------

def validar_territorio(
    municipio_esperado,
    resultado
):

    if resultado is None:

        return {
            "validacao_territorial":
                "NAO_ENCONTRADO",

            "motivo_territorial":
                "SEM_RESULTADO",

            "campo_municipio_api":
                None,

            "municipio_api":
                None
        }


    # -------------------------------------
    # País
    # -------------------------------------

    country_code = normalizar_geo(
        resultado.get(
            "country_code"
        )
    )

    if country_code != "BR":

        return {
            "validacao_territorial":
                "REJEITADO",

            "motivo_territorial":
                "PAIS_DIVERGENTE",

            "campo_municipio_api":
                None,

            "municipio_api":
                None
        }


    # -------------------------------------
    # Estado
    # -------------------------------------

    estado = normalizar_geo(
        resultado.get("state")
    )

    if estado != "SAO PAULO":

        return {
            "validacao_territorial":
                "REJEITADO",

            "motivo_territorial":
                "ESTADO_DIVERGENTE",

            "campo_municipio_api":
                None,

            "municipio_api":
                None
        }


    # -------------------------------------
    # Município administrativo
    # -------------------------------------

    (
        campo_municipio,
        municipio_api
    ) = extrair_municipio_retornado(
        resultado
    )


    esperado_normalizado = (
        normalizar_geo(
            municipio_esperado
        )
    )

    api_normalizado = (
        normalizar_geo(
            municipio_api
        )
    )


    # -------------------------------------
    # API forneceu município explícito
    # -------------------------------------

    if api_normalizado != "":

        if (
            api_normalizado
            == esperado_normalizado
        ):

            return {
                "validacao_territorial":
                    "VALIDADO",

                "motivo_territorial":
                    "MUNICIPIO_CONFIRMADO",

                "campo_municipio_api":
                    campo_municipio,

                "municipio_api":
                    municipio_api
            }

        else:

            return {
                "validacao_territorial":
                    "REJEITADO",

                "motivo_territorial":
                    "MUNICIPIO_DIVERGENTE",

                "campo_municipio_api":
                    campo_municipio,

                "municipio_api":
                    municipio_api
            }


    # -------------------------------------
    # Sem city/town/municipality:
    # não aprovamos automaticamente.
    # -------------------------------------

    return {
        "validacao_territorial":
            "SUSPEITO",

        "motivo_territorial":
            "MUNICIPIO_NAO_ESTRUTURADO",

        "campo_municipio_api":
            None,

        "municipio_api":
            None
    }


# =========================================================
# 33.4 TESTE CONTROLADO COM OS 5 CASOS DO BLOCO 32
# =========================================================

print("\n-----------------------------------------")
print("TESTE CONTROLADO")
print("-----------------------------------------")


resultados_validacao_territorial = []


for numero, (
    municipio_esperado,
    consulta
) in enumerate(
    casos_auditoria,
    start=1
):

    print("\n=========================================")

    print(
        f"[{numero}/{len(casos_auditoria)}]"
    )

    print(
        "Município esperado:",
        municipio_esperado
    )


    resultado = (
        consultar_nominatim_detalhado(
            consulta
        )
    )

    time.sleep(1.1)


    validacao = validar_territorio(
        municipio_esperado,
        resultado
    )


    print(
        "Validação:",
        validacao[
            "validacao_territorial"
        ]
    )

    print(
        "Motivo:",
        validacao[
            "motivo_territorial"
        ]
    )

    print(
        "Campo usado:",
        validacao[
            "campo_municipio_api"
        ]
    )

    print(
        "Município retornado:",
        validacao[
            "municipio_api"
        ]
    )


    if resultado is not None:

        print(
            "Resultado completo:"
        )

        print(
            resultado[
                "display_name"
            ]
        )


    resultados_validacao_territorial.append(
        {
            "municipio_esperado":
                municipio_esperado,

            **validacao
        }
    )


# =========================================================
# 33.5 RESUMO
# =========================================================

validacao_territorial_df = (
    pd.DataFrame(
        resultados_validacao_territorial
    )
)


print("\n=========================================")
print("RESUMO DA VALIDAÇÃO TERRITORIAL")
print("=========================================")

print(
    validacao_territorial_df.to_string(
        index=False
    )
)


print("\n-----------------------------------------")
print("DISTRIBUIÇÃO")
print("-----------------------------------------")

print(
    validacao_territorial_df[
        "validacao_territorial"
    ]
    .value_counts(
        dropna=False
    )
)
# =========================================================
# 34. EXPORTAÇÃO DA BASE TRATADA
# =========================================================

arquivo_saida = pasta / "data_tratada_safeflow.csv"

df_tratado.to_csv(
    arquivo_saida,
    index=False,
    encoding="utf-8-sig"
)

print("\n=========================================")
print("BASE TRATADA EXPORTADA")
print("=========================================")

print("Arquivo criado em:")
print(arquivo_saida)

print("\nDimensão da base exportada:")
print(df_tratado.shape)
# =========================================================
# 35. CADASTRO DA SEDE OPERACIONAL
# =========================================================

sedes = pd.DataFrame([
    {
        "ID_SEDE": "SEDE_001",
        "NOME_SEDE": "Regional São José dos Campos",
        "LOGRADOURO": "Rua Sebastião Hummel",
        "NUMERO": "759",
        "BAIRRO": "Centro",
        "MUNICIPIO": "São José dos Campos",
        "UF": "SP",
        "PAIS": "Brasil",
        "LATITUDE": pd.NA,
        "LONGITUDE": pd.NA,
        "STATUS_COORDENADAS": "PENDENTE_VALIDACAO",
        "FONTE": "Vídeo do representante do IPEM"
    }
])

arquivo_sedes = pasta / "sedes_safeflow.csv"

sedes.to_csv(
    arquivo_sedes,
    index=False,
    encoding="utf-8-sig"
)

print("\n=========================================")
print("CADASTRO DE SEDES")
print("=========================================")

print(sedes.to_string(index=False))

print("\nArquivo criado:")
print(arquivo_sedes)
# =========================================================
# 36. AUDITORIA DA BASE TRATADA EXPORTADA
# =========================================================

arquivo_tratado = pasta / "data_tratada_safeflow.csv"

print("\n=========================================")
print("36. AUDITORIA DA BASE TRATADA")
print("=========================================")

if not arquivo_tratado.exists():
    print("ERRO: A base tratada ainda não foi exportada.")

else:
    base_exportada = pd.read_csv(
        arquivo_tratado,
        encoding="utf-8-sig",
        low_memory=False
    )

    print("\nRegistros da base original:", len(df))
    print("Registros da base tratada:", len(df_tratado))
    print("Registros do arquivo exportado:", len(base_exportada))

    print("\nColunas da base original:", len(df.columns))
    print("Colunas da base tratada:", len(df_tratado.columns))
    print("Colunas do arquivo exportado:", len(base_exportada.columns))

    registros_preservados = (
        len(df)
        == len(df_tratado)
        == len(base_exportada)
    )

    colunas_preservadas = (
        list(df_tratado.columns)
        == list(base_exportada.columns)
    )

    print("\nRegistros preservados:", registros_preservados)
    print("Estrutura de colunas preservada:", colunas_preservadas)

    print("\nRLDs distintos na base tratada:")
    print(df_tratado["RLD_ID"].nunique())

    print("\nDatas inválidas:")
    print(df_tratado["DATAVERIFICACAO"].isna().sum())
    print(df_tratado["DT_HORA_VERIF"].isna().sum())

    if registros_preservados and colunas_preservadas:
        print("\nAUDITORIA ESTRUTURAL: APROVADA")
    else:
        print("\nAUDITORIA ESTRUTURAL: REQUER INVESTIGAÇÃO")
