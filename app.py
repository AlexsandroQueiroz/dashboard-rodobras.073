import streamlit as st
import pandas as pd

# ----------------- Configuração da página -----------------
st.set_page_config(page_title="Dashboard Dinâmico - 073", layout="wide")
st.markdown(
    """
    <style>
    .main {background-color: #fefefe;} /* fundo principal */
    .stSidebar .sidebar-content {background-color: #0B3C5D; color: white;} /* sidebar azul escuro */
    .stButton>button {background-color: #1C6EA4; color: white;} /* botões azul médio */
    .stMetricValue {color: #1C6EA4; font-weight:bold;} /* métrica azul */
    </style>
    """, unsafe_allow_html=True
)

# ----------------- Logo e título -----------------
st.image(
    "data:image/png;base64,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",
    width=150
)
st.title("Dashboard Dinâmico - 073")

# ----------------- Upload colapsável -----------------
if 'expander_open' not in st.session_state:
    st.session_state.expander_open = True

with st.expander("📂 Upload do arquivo (clique para abrir/fechar)", expanded=st.session_state.expander_open):
    uploaded_file = st.file_uploader("Escolha o arquivo principal", type=["xlsx"])

if uploaded_file:
    st.session_state.expander_open = False
    df_main = pd.read_excel(uploaded_file)

    # ----------------- Remover linhas REMUNERACAO -----------------
    coluna_tipo = df_main.columns[2]  # Coluna C
    df_main = df_main[df_main[coluna_tipo] != "REMUNERACAO"].copy()

    # ----------------- Renomear colunas importantes -----------------
    df_main.rename(columns={
        df_main.columns[8]: 'Placa',
        df_main.columns[27]: 'Valor',
        df_main.columns[4]: 'Data'
    }, inplace=True)
    df_main['Data'] = pd.to_datetime(df_main['Data'], errors='coerce')

    # ----------------- Carregar base de referência -----------------
    df_ref = pd.read_excel("FROTA AGREGADOS.XLSX", sheet_name="Plan1")
    df_ref.rename(columns={
        df_ref.columns[0]: 'Placa',
        df_ref.columns[1]: 'Tipo_Veiculo',
        df_ref.columns[2]: 'Motorista'
    }, inplace=True)

    # Merge
    df_merged = df_main.merge(df_ref, on='Placa', how='left')

    # ----------------- Criar Placa_Motorista e flag -----------------
    df_merged['Placa_Motorista'] = df_merged.apply(
        lambda x: f"{x['Placa']}_{x['Motorista']}" if pd.notna(x['Motorista']) else f"{x['Placa']}_Terceiro",
        axis=1
    )
    df_merged['is_terceiro'] = df_merged['Motorista'].isna()

    # ----------------- Filtros -----------------
    st.sidebar.header("Filtros")
    tipos = df_merged['Tipo_Veiculo'].dropna().unique().tolist()
    tipo_selecionado = st.sidebar.multiselect("Tipo de veículo", tipos)
    if tipo_selecionado:
        df_motoristas = df_merged[df_merged['Tipo_Veiculo'].isin(tipo_selecionado)]
    else:
        df_motoristas = df_merged
    motoristas_disponiveis = df_motoristas['Motorista'].dropna().unique().tolist()
    motorista_selecionado = st.sidebar.multiselect("Motorista", motoristas_disponiveis)

    filtro_tipo_veiculo = st.sidebar.radio(
        "Seleção de Veículo",
        options=["Todos Veículos", "Apenas Terceiros", "Apenas Agregados"],
        index=0
    )

    # ----------------- Período -----------------
    data_min = df_merged['Data'].min()
    data_max = df_merged['Data'].max()
    data_selecionada = st.sidebar.date_input(
        "Período",
        [data_min, data_max],
        format="DD/MM/YYYY"
    )
    if isinstance(data_selecionada, list) and len(data_selecionada) == 2:
        st.sidebar.markdown(
            f"**Período selecionado:** {data_selecionada[0].strftime('%d/%m/%Y')} – {data_selecionada[1].strftime('%d/%m/%Y')}"
        )

    # ----------------- Aplicar filtros -----------------
    df_filtered = df_merged[
        ((df_merged['Tipo_Veiculo'].isin(tipo_selecionado)) if tipo_selecionado else True) &
        ((df_merged['Motorista'].isin(motorista_selecionado)) if motorista_selecionado else True) &
        (
            (df_merged['is_terceiro'] if filtro_tipo_veiculo == "Apenas Terceiros" else
             (~df_merged['is_terceiro'] if filtro_tipo_veiculo == "Apenas Agregados" else True))
        ) &
        (df_merged['Data'].between(pd.to_datetime(data_selecionada[0]),
                                   pd.to_datetime(data_selecionada[1])))
    ].copy()

    # ----------------- Formatar valores em BRL -----------------
    df_filtered['Valor_formatado'] = df_filtered['Valor'].apply(
        lambda x: f"R$ {x:,.2f}".replace(',', 'v').replace('.', ',').replace('v', '.')
    )

    # ----------------- Resumo -----------------
    st.subheader("Resumo de Valores")
    total_geral = df_filtered['Valor'].sum()
    st.metric(
        "Total Geral de Valor",
        f"R$ {total_geral:,.2f}".replace(',', 'v').replace('.', ',').replace('v', '.')
    )

    resumo_motorista = df_filtered.groupby('Placa_Motorista')['Valor'].agg(['sum', 'count', 'mean']).reset_index()
    resumo_motorista.rename(columns={
        'sum': 'Valor_Total',
        'count': 'Carregamentos',
        'mean': 'Valor_Médio'
    }, inplace=True)
    resumo_motorista['Valor_Total'] = resumo_motorista['Valor_Total'].apply(
        lambda x: f"R$ {x:,.2f}".replace(',', 'v').replace('.', ',').replace('v', '.')
    )
    resumo_motorista['Valor_Médio'] = resumo_motorista['Valor_Médio'].apply(
        lambda x: f"R$ {x:,.2f}".replace(',', 'v').replace('.', ',').replace('v', '.')
    )

    # ----------------- Estilo visual -----------------
    def color_rows(row):
        if "_Terceiro" in row['Placa_Motorista']:
            return ['background-color:  #99ff99']*len(row)  # verde escuro para terceiros
        else:
            return ['background-color: #DFFFD6']*len(row)  # verde claro para agregados

    st.dataframe(resumo_motorista.style.apply(color_rows, axis=1))