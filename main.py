import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Sistema de Colaboradores",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado - Paleta Suave Terrosa
st.markdown("""
<style>
.main {
    background-color: #f5f3f0;
    color: #3a3a3a;
}

.stApp {
    background-color: #e8e4df;
}

.css-1d391kg {
    background-color: #e8e4df;
}

.stTextInput > div > div > input {
    background-color: #ffffff;
    color: #3a3a3a;
    border: 1px solid #c9c0b5;
    border-radius: 8px;
}

.stSelectbox > div > div > div {
    background-color: #ffffff;
    color: #3a3a3a;
    border: 1px solid #c9c0b5;
    border-radius: 8px;
}

.stDateInput > div > div > input {
    background-color: #ffffff;
    color: #3a3a3a;
    border: 1px solid #c9c0b5;
    border-radius: 8px;
}

h1 {
    color: #6b5b47;
    text-align: center;
    padding: 20px;
    background: linear-gradient(135deg, #d4c7b8, #c9bcac);
    border-radius: 12px;
    margin-bottom: 30px;
    box-shadow: 0 2px 8px rgba(139, 125, 107, 0.2);
}

h2, h3 {
    color: #6b5b47;
}

.success-message {
    background-color: #7d8471;
    color: white;
    padding: 12px;
    border-radius: 8px;
    text-align: center;
    margin: 10px 0;
    box-shadow: 0 2px 4px rgba(125, 132, 113, 0.3);
}

.error-message {
    background-color: #a67c52;
    color: white;
    padding: 12px;
    border-radius: 8px;
    text-align: center;
    margin: 10px 0;
    box-shadow: 0 2px 4px rgba(166, 124, 82, 0.3);
}

/* Estilo do navegador superior */
.st-emotion-cache-1jicfl2 {
    background: linear-gradient(90deg, #8b7d6b, #9d8f7c) !important;
    border-bottom: 2px solid #6b5b47;
}

.st-emotion-cache-1jicfl2 .st-emotion-cache-10trblm {
    color: #f5f3f0 !important;
    font-weight: 500;
}

/* Botões principais */
.stButton > button {
    background: linear-gradient(135deg, #b8860b, #cd853f);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 500;
    transition: all 0.3s ease;
    box-shadow: 0 2px 6px rgba(184, 134, 11, 0.3);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #cd853f, #daa520);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(184, 134, 11, 0.4);
}

/* Métricas */
[data-testid="metric-container"] {
    background-color: #ffffff;
    border: 1px solid #d4c7b8;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 2px 6px rgba(139, 125, 107, 0.15);
}

[data-testid="metric-container"] > div {
    color: #6b5b47;
}

/* Sidebar */
.css-1d391kg {
    background-color: #ebe7e2;
}

/* Formulários */
.stForm {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 12px;
    border: 1px solid #d4c7b8;
    box-shadow: 0 4px 12px rgba(139, 125, 107, 0.1);
}

/* Tabelas */
.dataframe {
    background-color: #ffffff;
    border-radius: 8px;
    border: 1px solid #d4c7b8;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background-color: #ebe7e2;
    border-radius: 8px;
}

.stTabs [data-baseweb="tab"] {
    color: #6b5b47;
    background-color: transparent;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background-color: #b8860b;
    color: white;
    border-radius: 6px;
}

/* Expander */
.streamlit-expanderHeader {
    background-color: #ebe7e2;
    color: #6b5b47;
    border-radius: 8px;
}

/* Info boxes */
.stInfo {
    background-color: #d4c7b8;
    color: #6b5b47;
    border-radius: 8px;
}

.stSuccess {
    background-color: #7d8471;
    color: white;
    border-radius: 8px;
}

.stWarning {
    background-color: #cd853f;
    color: white;
    border-radius: 8px;
}

.stError {
    background-color: #a67c52;
    color: white;
    border-radius: 8px;
}

/* Selectbox melhorado */
.stSelectbox > div > div > div > div {
    background-color: #ffffff;
    color: #3a3a3a;
}

/* Text area */
.stTextArea > div > div > textarea {
    background-color: #ffffff;
    color: #3a3a3a;
    border: 1px solid #c9c0b5;
    border-radius: 8px;
}

/* Radio buttons */
.stRadio > div {
    background-color: #ffffff;
    border-radius: 8px;
    padding: 10px;
    border: 1px solid #d4c7b8;
}

/* Checkbox */
.stCheckbox > div {
    background-color: #ffffff;
    border-radius: 6px;
    padding: 8px;
}

/* Slider */
.stSlider > div > div > div > div {
    background-color: #b8860b;
}

/* Progress bar */
.stProgress > div > div > div > div {
    background-color: #b8860b;
}

/* Links */
a {
    color: #b8860b;
    text-decoration: none;
}

a:hover {
    color: #cd853f;
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# Páginas do sistema
pages = {
    "Menu": [
        st.Page("cadastro.py", title="Cadastro de colaboradores"),
        st.Page("listagem.py", title="Listar/Atualizar/Excluir cadastros")
    ],
    "Sistema": [
        st.Page("sobre.py", title="Sobre o Sistema")
    ]
}

# Navegação no topo
pg = st.navigation(pages, position="top")
pg.run()