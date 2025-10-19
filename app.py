import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date
import re

# Configuração da página
st.set_page_config(
    page_title="Cadastro de Colaboradores",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Lê o conteúdo do arquivo Markdown
with open("conteudo.md", "r", encoding="utf-8") as f:
    conteudo_md = f.read()
    
# CSS personalizado com Markdown
st.markdown(conteudo_md, unsafe_allow_html=True)

class DatabaseManager:
    def __init__(self, db_name="colaboradores.db"):
        self.db_name = db_name
        self.create_table()
    
    def create_table(self):
        """Cria a tabela de colaboradores se não existir"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS colaboradores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_completo TEXT NOT NULL,
                endereco TEXT,
                bairro TEXT,
                cidade TEXT,
                estado TEXT,
                cep TEXT,
                telefone TEXT,
                data_nascimento DATE,
                cargo TEXT,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def inserir_colaborador(self, dados):
        """Insere um novo colaborador no banco de dados"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO colaboradores 
            (nome_completo, endereco, bairro, cidade, estado, cep, telefone, data_nascimento, cargo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, dados)
        
        conn.commit()
        conn.close()
        return cursor.lastrowid
    
    def listar_colaboradores(self):
        """Lista todos os colaboradores"""
        conn = sqlite3.connect(self.db_name)
        df = pd.read_sql_query("SELECT * FROM colaboradores ORDER BY id DESC", conn)
        conn.close()
        return df
    
    def excluir_colaborador(self, id_colaborador):
        """Exclui um colaborador pelo ID"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM colaboradores WHERE id = ?", (id_colaborador,))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0

def validar_cep(cep):
    """Valida formato do CEP"""
    return re.match(r'^\d{5}-?\d{3}$', cep) is not None

def validar_telefone(telefone):
    """Valida formato do telefone"""
    telefone_limpo = re.sub(r'[^\d]', '', telefone)
    return len(telefone_limpo) >= 10

def main():
    # Inicializar o gerenciador de banco de dados
    db = DatabaseManager()
    
    # Título principal
    st.markdown("# 📋 Cadastro de Colaboradores")
    
    # Sidebar para navegação
    st.sidebar.title("Menu")
    opcao = st.sidebar.selectbox(
        "Escolha uma opção:",
        ["Novo Cadastro", "Listar Colaboradores", "Estatísticas"]
    )
    
    if opcao == "Novo Cadastro":
        cadastrar_colaborador(db)
    elif opcao == "Listar Colaboradores":
        listar_colaboradores(db)
    else:
        mostrar_estatisticas(db)

def cadastrar_colaborador(db):
    st.subheader("🆕 Novo Colaborador")
    
    with st.form("form_colaborador"):
        # Primeira linha
        col1, col2, col3 = st.columns(3)
        
        with col1:
            nome_completo = st.text_input("Nome completo *", placeholder="Digite o nome completo")
        
        with col2:
            cidade = st.text_input("Cidade", placeholder="Digite a cidade")
        
        with col3:
            telefone = st.text_input("Telefone", placeholder="(11) 99999-9999")
        
        # Segunda linha
        col4, col5, col6 = st.columns(3)
        
        with col4:
            endereco = st.text_input("Endereço", placeholder="Digite o endereço")
        
        with col5:
            estados_brasil = [
                "", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", 
                "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", 
                "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
            ]
            estado = st.selectbox("Estado (UF)", estados_brasil)
        
        with col6:
            data_nascimento = st.date_input(
                "Data de nascimento",
                value=None,
                min_value=date(1900, 1, 1),
                max_value=date.today()
            )
        
        # Terceira linha
        col7, col8, col9 = st.columns(3)
        
        with col7:
            bairro = st.text_input("Bairro", placeholder="Digite o bairro")
        
        with col8:
            cep = st.text_input("CEP", placeholder="12345-678")
        
        with col9:
            cargos_comuns = [
                "", "Analista", "Desenvolvedor", "Gerente", "Coordenador", 
                "Assistente", "Diretor", "Supervisor", "Técnico", "Estagiário",
                "Consultor", "Especialista", "Outro"
            ]
            cargo = st.selectbox("Cargo", cargos_comuns)
        
        # Botão de submissão
        submitted = st.form_submit_button("💾 Salvar Cadastro", use_container_width=True)
        
        if submitted:
            # Validações
            erros = []
            
            if not nome_completo.strip():
                erros.append("Nome completo é obrigatório")
            
            if cep and not validar_cep(cep):
                erros.append("CEP deve ter o formato 12345-678")
            
            if telefone and not validar_telefone(telefone):
                erros.append("Telefone deve ter pelo menos 10 dígitos")
            
            if erros:
                for erro in erros:
                    st.error(f"❌ {erro}")
            else:
                try:
                    # Preparar dados para inserção
                    dados = (
                        nome_completo.strip(),
                        endereco.strip() if endereco else None,
                        bairro.strip() if bairro else None,
                        cidade.strip() if cidade else None,
                        estado if estado else None,
                        cep.strip() if cep else None,
                        telefone.strip() if telefone else None,
                        data_nascimento,
                        cargo if cargo else None
                    )
                    
                    # Inserir no banco de dados
                    id_colaborador = db.inserir_colaborador(dados)
                    
                    st.success(f"✅ Colaborador cadastrado com sucesso! ID: {id_colaborador}")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ Erro ao cadastrar colaborador: {e}")

def listar_colaboradores(db):
    st.subheader("📋 Lista de Colaboradores")
    
    # Buscar dados
    df = db.listar_colaboradores()
    
    if df.empty:
        st.info("ℹ️ Nenhum colaborador cadastrado ainda.")
        return
    
    # Filtros
    col1, col2 = st.columns(2)
    
    with col1:
        filtro_nome = st.text_input("🔍 Filtrar por nome:", placeholder="Digite parte do nome")
    
    with col2:
        filtro_cargo = st.selectbox(
            "🔍 Filtrar por cargo:",
            [""] + sorted(df['cargo'].dropna().unique().tolist())
        )
    
    # Aplicar filtros
    df_filtrado = df.copy()
    
    if filtro_nome:
        df_filtrado = df_filtrado[df_filtrado['nome_completo'].str.contains(filtro_nome, case=False, na=False)]
    
    if filtro_cargo:
        df_filtrado = df_filtrado[df_filtrado['cargo'] == filtro_cargo]
    
    # Mostrar estatísticas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Colaboradores", len(df))
    with col2:
        st.metric("Resultados da Busca", len(df_filtrado))
    with col3:
        if not df['cargo'].isna().all():
            cargo_mais_comum = df['cargo'].value_counts().index[0]
            st.metric("Cargo Mais Comum", cargo_mais_comum)
    
    # Exibir tabela
    if not df_filtrado.empty:
        # Preparar dados para exibição
        df_display = df_filtrado[[
            'id', 'nome_completo', 'cidade', 'estado', 'telefone', 
            'cargo', 'data_nascimento', 'data_cadastro'
        ]].copy()
        
        # Renomear colunas
        df_display.columns = [
            'ID', 'Nome Completo', 'Cidade', 'UF', 'Telefone', 
            'Cargo', 'Nascimento', 'Cadastrado em'
        ]
        
        st.dataframe(df_display, use_container_width=True)
        
        # Opção para excluir colaborador
        st.subheader("🗑️ Excluir Colaborador")
        
        colaborador_excluir = st.selectbox(
            "Selecione o colaborador para excluir:",
            [""] + [f"{row['id']} - {row['nome_completo']}" for _, row in df_filtrado.iterrows()]
        )
        
        if colaborador_excluir:
            id_colaborador = int(colaborador_excluir.split(" - ")[0])
            
            if st.button(f"🗑️ Confirmar Exclusão", type="secondary"):
                if db.excluir_colaborador(id_colaborador):
                    st.success("✅ Colaborador excluído com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao excluir colaborador")
    else:
        st.warning("⚠️ Nenhum colaborador encontrado com os filtros aplicados.")

def mostrar_estatisticas(db):
    st.subheader("📊 Estatísticas")
    
    df = db.listar_colaboradores()
    
    if df.empty:
        st.info("ℹ️ Nenhum dado disponível para estatísticas.")
        return
    
    # Métricas gerais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Colaboradores", len(df))
    
    with col2:
        if not df['cidade'].isna().all():
            cidades_unicas = df['cidade'].nunique()
            st.metric("Cidades Diferentes", cidades_unicas)
    
    with col3:
        if not df['estado'].isna().all():
            estados_unicos = df['estado'].nunique()
            st.metric("Estados Diferentes", estados_unicos)
    
    with col4:
        if not df['cargo'].isna().all():
            cargos_unicos = df['cargo'].nunique()
            st.metric("Cargos Diferentes", cargos_unicos)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição por cargo
        if not df['cargo'].isna().all():
            st.subheader("Distribuição por Cargo")
            cargo_counts = df['cargo'].value_counts()
            st.bar_chart(cargo_counts)
    
    with col2:
        # Distribuição por estado
        if not df['estado'].isna().all():
            st.subheader("Distribuição por Estado")
            estado_counts = df['estado'].value_counts()
            st.bar_chart(estado_counts)
    
    # Cadastros por mês
    if len(df) > 0:
        st.subheader("Cadastros por Período")
        df['data_cadastro'] = pd.to_datetime(df['data_cadastro'])
        df['mes_cadastro'] = df['data_cadastro'].dt.to_period('M')
        cadastros_por_mes = df['mes_cadastro'].value_counts().sort_index()
        st.line_chart(cadastros_por_mes)

if __name__ == "__main__":
    main()
