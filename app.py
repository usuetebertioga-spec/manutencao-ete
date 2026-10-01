import streamlit as st
import json
import os
from datetime import datetime
from fpdf import FPDF

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Manutenção - ETE Sesc Bertioga",
    page_icon="🔧",
    layout="wide"
)

# --- PROTEÇÃO POR SENHA ---
def check_password():
    """Retorna True se o usuário inseriu a senha correta."""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    st.markdown("## 🔒 Acesso Restrito - Manutenção ETE")
    st.markdown("Por favor, digite a senha para acessar o aplicativo.")
    
    password = st.text_input("Senha", type="password")
    
    if st.button("Entrar"):
        if password == "bertioga2026":
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("Senha incorreta. Tente novamente.")
            
    return False

if not check_password():
    st.stop()

# --- ESTILO VISUAL OTIMIZADO PARA TABLET (Acessibilidade) ---
st.markdown("""
    <style>
    .main {
        background-color: #FFFFFF;
    }
    h1, h2, h3 {
        color: #0b3c5d !important;
        font-weight: bold;
    }
    .stButton>button {
        font-size: 20px !important;
        font-weight: bold !important;
        padding: 12px 24px !important;
        background-color: #0b3c5d !important;
        color: white !important;
        border-radius: 8px !important;
        width: 100%;
    }
    label {
        font-size: 18px !important;
        font-weight: bold !important;
        color: #1d2731 !important;
    }
    .stAlert {
        font-size: 18px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- ARQUIVO DE BANCO DE DADOS LOCAL (JSON) ---
DATA_FILE = "manutencao_data.json"

def carregar_dados():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def salvar_dados(dados):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

# --- CABEÇALHO DO APLICATIVO ---
if os.path.exists("logo.jpg"):
    st.image("logo.jpg", width=200)

st.title("🔧 Painel de Manutenção - ETE Sesc Bertioga")
st.markdown("Controle de rotinas preventivas, corretivas e inspeções de equipamentos.")

# --- MENU DE NAVEGAÇÃO ---
menu = ["Registrar Manutenção", "Histórico de Registros", "Gerar Relatório PDF"]
escolha = st.sidebar.selectbox("Menu de Navegação", menu)

registros = carregar_dados()

# --- ABA 1: REGISTRAR MANUTENÇÃO ---
if escolha == "Registrar Manutenção":
    st.subheader("📝 Novo Registro de Manutenção")
    
    with st.form("form_manutencao"):
        data_manutencao = st.date_input("Data da Manutenção", value=datetime.now())
        equipamento = st.selectbox(
            "Equipamento / Setor",
            [
                "Gradeamento / Caixa de Areia",
                "Reator Anaeróbio",
                "Tanque de Aeração (SOP / MBR)",
                "Decantador Secundário",
                "Tanque de Reúso (Efluente Clarificado)",
                "Sist. de Desinfecção (Cloro)",
                "Bombas de Recirculação / Lodo",
                "Sopradores de Ar",
                "Painel Elétrico Geral"
            ]
        )
        
        tipo_manutencao = st.radio("Tipo de Intervenção", ["Preventiva", "Corretiva", "Inspeção Rotineira"])
        descricao = st.text_area("Descrição do Serviço Realizado / Peças Substituídas")
        responsavel = st.text_input("Técnico / Operador Responsável")
        
        submitted = st.form_submit_button("Salvar Registro")
        
        if submitted:
            if responsavel.strip() == "":
                st.error("Por favor, preencha o nome do responsável.")
            else:
                novo_registro = {
                    "data": str(data_manutencao),
                    "equipamento": equipamento,
                    "tipo": tipo_manutencao,
                    "descricao": descricao,
                    "responsavel": responsavel
                }
                registros.append(novo_registro)
                salvar_dados(registros)
                st.success("✅ Manutenção registrada com sucesso!")

# --- ABA 2: HISTÓRICO ---
elif escolha == "Histórico de Registros":
    st.subheader("📋 Histórico de Manutenções Realizadas")
    
    if not registros:
        st.info("Nenhum registro encontrado até o momento.")
    else:
        for i, reg in enumerate(reversed(registros), 1):
            with st.expander(f"📌 {reg['data']} - {reg['equipamento']} ({reg['tipo']})"):
                st.write(f"**Equipamento:** {reg['equipamento']}")
                st.write(f"**Tipo:** {reg['tipo']}")
                st.write(f"**Descrição:** {reg['descricao']}")
                st.write(f"**Responsável:** {reg['responsavel']}")

# --- ABA 3: GERAR RELATÓRIO PDF ---
elif escolha == "Gerar Relatório PDF":
    st.subheader("📄 Exportar Relatório em PDF")
    
    if not registros:
        st.warning("Não há dados suficientes para gerar o relatório.")
    else:
        if st.button("Gerar PDF de Manutenção"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, txt="Relatorio de Manutencao - ETE Sesc Bertioga", ln=True, align="C")
            pdf.set_font("Arial", "", 12)
            pdf.ln(10)
            
            for reg in registros:
                pdf.cell(200, 8, txt=f"Data: {reg['data']} | Equipamento: {reg['equipamento']}", ln=True)
                pdf.cell(200, 8, txt=f"Tipo: {reg['tipo']} | Resp: {reg['responsavel']}", ln=True)
                pdf.multi_cell(200, 8, txt=f"Descricao: {reg['descricao']}")
                pdf.ln(5)
                
            pdf_output = "relatorio_manutencao_ete.pdf"
            pdf.output(pdf_output)
            
            with open(pdf_output, "rb") as f:
                st.download_button(
                    label="📥 Baixar PDF Gerado",
                    data=f,
                    file_name=pdf_output,
                    mime="application/pdf"
                )