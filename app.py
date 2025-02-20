import streamlit as st
import datetime

# Configuração da página e título
st.set_page_config(page_title="Ideias 5S - WEG", layout="wide")

# CSS customizado para melhorar a aparência
st.markdown("""
    <style>
    /* Centralizar o título principal */
    .main > div:first-child {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
    /* Caixa do formulário mais larga */
    .css-1l02zno {
        max-width: 700px;
        margin: 0 auto;
    }
    /* Botões, textos e fundo */
    .stButton button {
        background-color: #004A99;
        color: white;
        border: none;
        padding: 0.6em 1.2em;
        margin-top: 0.5em;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #003366;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializa a lista de ideias no session_state
if "ideias" not in st.session_state:
    st.session_state.ideias = []

# Menu de navegação
menu = ["Registrar Ideia", "Lista de Ideias"]
escolha = st.sidebar.selectbox("Navegação", menu)

def registrar_ideia():
    """Página para registrar nova ideia 5S."""
    st.title("Registro de Ideias 5S - WEG")
    st.write("Insira as informações da sua ideia nos campos abaixo.")

    with st.form(key="form_ideia"):
        titulo = st.text_input("Título da Ideia")
        descricao = st.text_area("Descrição da Ideia")
        categoria = st.selectbox("Categoria 5S", ["Seiri", "Seiton", "Seiso", "Seiketsu", "Shitsuke"])
        status = st.selectbox("Status Inicial", ["Pendente", "Em Avaliação", "Aprovada", "Implementada"])
        submit = st.form_submit_button("Registrar Ideia")

    if submit:
        if not titulo.strip():
            st.error("O título não pode ser vazio.")
        else:
            data_atual = datetime.date.today()
            # Cria o dicionário da ideia
            nova_ideia = {
                "titulo": titulo,
                "descricao": descricao,
                "categoria": categoria,
                "status": status,
                "data_criacao": data_atual,
                "data_atualizacao": data_atual
            }
            # Adiciona ao estado
            st.session_state.ideias.append(nova_ideia)
            st.success("Ideia registrada com sucesso!")

def listar_ideias():
    """Página para listar as ideias já cadastradas e gerenciar status."""
    st.title("Lista de Ideias 5S")
    st.write("Visualize e gerencie as ideias registradas.")

    if not st.session_state.ideias:
        st.warning("Nenhuma ideia registrada até o momento.")
        return

    # Opção de filtrar por status
    status_filtro = st.selectbox("Filtrar por Status", ["Todos", "Pendente", "Em Avaliação", "Aprovada", "Implementada"])

    # Opção de ordenar por data de criação (mais recente primeiro)
    ordenar_por_data_criacao = st.checkbox("Ordenar por Data de Criação (mais recente primeiro)")

    # Realiza o filtro
    ideias_filtradas = st.session_state.ideias
    if status_filtro != "Todos":
        ideias_filtradas = [ideia for ideia in ideias_filtradas if ideia["status"] == status_filtro]

    # Ordenação
    if ordenar_por_data_criacao:
        ideias_filtradas = sorted(ideias_filtradas, key=lambda x: x["data_criacao"], reverse=True)

    # Exibe cada ideia em um "expander" para ficar mais organizado
    for idx, ideia in enumerate(ideias_filtradas, 1):
        with st.expander(f"{idx}. {ideia['titulo']}"):
            st.write(f"**Categoria:** {ideia['categoria']}")
            st.write(f"**Descrição:** {ideia['descricao']}")
            st.write(f"**Status Atual:** {ideia['status']}")
            st.write(f"**Data de Criação:** {ideia['data_criacao']}")
            st.write(f"**Última Atualização:** {ideia['data_atualizacao']}")

            # Seletor para atualizar o status
            novo_status = st.selectbox(
                f"Atualizar Status (Ideia {idx})",
                ["Pendente", "Em Avaliação", "Aprovada", "Implementada"],
                index=["Pendente", "Em Avaliação", "Aprovada", "Implementada"].index(ideia["status"])
            )

            # Botão para salvar alterações de status
            if st.button(f"Salvar Alterações - Ideia {idx}"):
                if novo_status != ideia["status"]:
                    ideia["status"] = novo_status
                    ideia["data_atualizacao"] = datetime.date.today()
                    st.success(f"Status da ideia '{ideia['titulo']}' atualizado para '{novo_status}'.")
                    st.experimental_rerun()  # Atualiza a tela imediatamente

# Carrega a função de acordo com a escolha no menu
if escolha == "Registrar Ideia":
    registrar_ideia()
elif escolha == "Lista de Ideias":
    listar_ideias()
