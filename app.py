import streamlit as st
import pandas as pd

# ----------------- Configuração da página -----------------
st.set_page_config(page_title="Dashboard Dinâmico - Rodobras Foods", layout="wide")
st.markdown(
    """
    <style>
    .main {background-color: #f9f9f9;}
    .stSidebar .sidebar-content {background-color: #0B3C5D; color: white;}
    .stButton>button {background-color: #1C6EA4; color: white;}
    .stMetricValue {color: #1C6EA4; font-weight:bold;}
    </style>
    """, unsafe_allow_html=True
)

# Logo
st.image("https://www.rodobrastransp.com.br/img/att/logo-foods.png", width=150)
st.title("Dashboard Dinâmico - Rodobras Foods")

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
    df_main['Data_formatada'] = df_main['Data'].dt.strftime('%d/%m/%Y')

    # ----------------- Carregar base de referência -----------------
    df_ref = pd.read_excel("FROTA AGREGADOS.XLSX", sheet_name="Plan1")
    df_ref.rename(columns={
        df_ref.columns[0]: 'Placa',
        df_ref.columns[1]: 'Tipo_Veiculo',
        df_ref.columns[2]: 'Motorista'
    }, inplace=True)

    # Merge
    df_merged = df_main.merge(df_ref, on='Placa', how='left')

    # ----------------- Filtros dependentes -----------------
    st.sidebar.header("Filtros")
    tipos = df_merged['Tipo_Veiculo'].dropna().unique().tolist()
    tipo_selecionado = st.sidebar.multiselect("Tipo de veículo", tipos)

    if tipo_selecionado:
        df_motoristas = df_merged[df_merged['Tipo_Veiculo'].isin(tipo_selecionado)]
    else:
        df_motoristas = df_merged
    motoristas_disponiveis = df_motoristas['Motorista'].dropna().unique().tolist()
    motorista_selecionado = st.sidebar.multiselect("Motorista", motoristas_disponiveis)

    data_min = df_merged['Data'].min()
    data_max = df_merged['Data'].max()
    data_selecionada = st.sidebar.date_input("Período", [data_min, data_max])

    if isinstance(data_selecionada, list) and len(data_selecionada) == 2:
        st.sidebar.markdown(
            f"**Período selecionado:** {data_selecionada[0].strftime('%d/%m/%Y')} – {data_selecionada[1].strftime('%d/%m/%Y')}"
        )

    # ----------------- Aplicar filtros -----------------
    df_filtered = df_merged[
        ((df_merged['Tipo_Veiculo'].isin(tipo_selecionado)) if tipo_selecionado else True) &
        ((df_merged['Motorista'].isin(motorista_selecionado)) if motorista_selecionado else True) &
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

    resumo_motorista = df_filtered.groupby('Motorista')['Valor'].agg(['sum', 'count', 'mean']).reset_index()
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

    st.dataframe(resumo_motorista)