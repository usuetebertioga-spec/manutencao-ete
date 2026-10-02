import base64
import calendar
from datetime import datetime
import json
import os
from fpdf import FPDF
import pandas as pd
import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="ETE Sesc Bertioga - Gestão de Manutenção",
    page_icon="🛠️",
    layout="wide",
)

# --- PROTEÇÃO POR SENHA ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    st.markdown("## 🔒 Acesso Restrito - Manutenção ETE Sesc Bertioga")
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

# --- ESTILIZAÇÃO CSS ADAPTATIVA (SUPORTE TOTAL A MODO CLARO E ESCURO) ---
st.markdown(
    """
    <style>
        /* Sidebar com adaptação automática ao tema */
        section[data-testid="stSidebar"] {
            border-right: 2px solid rgba(148, 163, 184, 0.3);
        }
        
        /* Rótulos e textos gerais adaptáveis */
        label, .stTextInput label, .stSelectbox label, .stMultiSelect label, .stDateInput label, .stRadio label {
            font-size: 19px !important;
            font-weight: 800 !important;
        }
        
        /* Botões grandes e destacados com excelente área de toque */
        .stButton>button {
            background-color: #003366 !important;
            color: #ffffff !important;
            font-size: 20px !important;
            font-weight: 900 !important;
            border-radius: 10px;
            border: 3px solid #001f3f;
            padding: 0.85rem 1.5rem;
            box-shadow: 0 6px 10px rgba(0,0,0,0.25);
            width: 100%;
            min-height: 56px;
        }
        .stButton>button:hover {
            background-color: #002244 !important;
            color: #ffffff !important;
        }
        
        /* Cabeçalhos de Seção com Fundo Azul Forte e Letras Brancas */
        .intervencao-header {
            background-color: #003366;
            color: #ffffff !important;
            padding: 18px 22px;
            border-radius: 10px;
            font-size: 24px;
            font-weight: 900;
            text-align: center;
            margin-top: 20px;
            margin-bottom: 25px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            border: 2px solid #001f3f;
        }
        
        .section-sub-title {
            background-color: #1e293b;
            color: #ffffff !important;
            padding: 14px 18px;
            border-radius: 8px;
            font-size: 20px;
            font-weight: 800;
            margin-top: 20px;
            margin-bottom: 15px;
            box-shadow: 0 3px 6px rgba(0,0,0,0.15);
        }
        
        /* Cards de Atividades com contraste otimizado para qualquer tema */
        .card-atividade {
            border: 2px solid rgba(148, 163, 184, 0.4);
            border-left: 8px solid #003366;
            padding: 16px 20px;
            border-radius: 8px;
            margin-bottom: 12px;
            box-shadow: 0 3px 6px rgba(0,0,0,0.1);
            font-size: 18px;
            font-weight: 700;
        }
        
        /* Tamanho de texto de Checkboxes e Radios ampliado */
        .stCheckbox span, .stRadio div[role="radiogroup"] label p {
            font-size: 18px !important;
            font-weight: 700 !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# --- PERSISTÊNCIA DE DADOS (JSON) ---
ARQUIVO_DADOS_MAN = "manutencao_ete.json"


def carregar_dados_manutencao():
  if os.path.exists(ARQUIVO_DADOS_MAN):
    try:
      with open(ARQUIVO_DADOS_MAN, "r", encoding="utf-8") as f:
        return json.load(f)
    except:
      return []
  return []


def salvar_dados_manutencao(dados):
  with open(ARQUIVO_DADOS_MAN, "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=4)


if "registros_manutencao" not in st.session_state:
  st.session_state["registros_manutencao"] = carregar_dados_manutencao()

# --- MAPEAMENTO DE EQUIPAMENTOS ---
EQUIPAMENTOS_MANUTENCAO = [
    {
        "id": 1,
        "nome": "BOMBA NEMO - ESGOTO EQUALIZADO (BL-110 A/B) - CP 150012433",
        "periodicidade": "Mensal",
        "atividades": [
            "Medição de tensão e corrente",
            "Verificação da pintura",
            "Verificação do aterramento",
            "Verificação do sistema de fixação",
            "Verificação quanto à vibrações",
            "Verificação quanto ao aquecimento do motor",
            "Verificação quanto à vazamentos no selo mecânico",
            "Verificar vazamento de óleo e água",
            "Verificar ruídos anormais",
            "Verificar o estado do acoplamento motor/bomba",
        ],
    },
    {
        "id": 2,
        "nome": (
            "BOMBA NEMO - LAVAGEM FILTRO AUTOLIMPANTE (BL-120 A/B) - CP"
            " 150012434"
        ),
        "periodicidade": "Mensal",
        "atividades": [
            "Medição de tensão e corrente",
            "Verificação da pintura",
            "Verificação do aterramento",
            "Verificação do sistema de fixação",
            "Verificação quanto à vibrações",
            "Verificação quanto ao aquecimento do motor",
            "Verificação quanto à vazamentos no selo mecânico",
            "Verificar vazamento de óleo e água",
            "Verificar ruídos anormais",
            "Verificar o estado do acoplamento motor/bomba",
        ],
    },
    {
        "id": 3,
        "nome": "BOMBA NEMO - DESCARTE DE LODO (BL-410 A/B) - CP 150012435",
        "periodicidade": "Mensal",
        "atividades": [
            "Medição de tensão e corrente",
            "Verificação da pintura",
            "Verificação do aterramento",
            "Verificação do sistema de fixação",
            "Verificação quanto à vibrações",
            "Verificação quanto ao aquecimento do motor",
            "Verificação quanto à vazamentos no selo mecânico",
            "Verificar vazamento de óleo e água",
            "Verificar ruídos anormais",
            "Verificar o estado do acoplamento motor/bomba",
        ],
    },
    {
        "id": 4,
        "nome": "BOMBA NEMO - LODO ADENSADO (BL-600 A/B) - CP 150012436",
        "periodicidade": "Mensal",
        "atividades": [
            "Medição de tensão e corrente",
            "Verificação da pintura",
            "Verificação do aterramento",
            "Verificação do sistema de fixação",
            "Verificação quanto à vibrações",
            "Verificação quanto ao aquecimento do motor",
            "Verificação quanto à vazamentos no selo mecânico",
            "Verificar vazamento de óleo e água",
            "Verificar ruídos anormais",
            "Verificar o estado do acoplamento motor/bomba",
        ],
    },
    {
        "id": 5,
        "nome": "BOMBA CENTRÍFUGA - ESGOTAMENTO DOS TANQUES (BC-300)",
        "periodicidade": "Mensal",
        "atividades": [
            "Medição de tensão e corrente",
            "Verificação do sistema de fixação",
            "Verificação quanto à vibrações",
            "Verificação quanto ao aquecimento do motor",
            "Verificar ruídos anormais",
        ],
    },
    {
        "id": 6,
        "nome": "BOMBA CENTRÍFUGA - RECIRCULAÇÃO DO LODO (BC-410 A/B)",
        "periodicidade": "Mensal",
        "atividades": [
            "Medição de tensão e corrente",
            "Verificação do sistema de fixação",
            "Verificação quanto à vibrações",
            "Verificação quanto ao aquecimento do motor",
            "Verificar ruídos anormais",
        ],
    },
    {
        "id": 7,
        "nome": "BOMBA CENTRÍFUGA - PERMEADO (BC-400 A/B)",
        "periodicidade": "Mensal",
        "atividades": [
            "Medição de tensão e corrente",
            "Verificação do sistema de fixação",
            "Verificação quanto à vibrações",
            "Verificação quanto ao aquecimento do motor",
            "Verificar ruídos anormais",
        ],
    },
    {
        "id": 8,
        "nome": "BOMBA CENTRÍFUGA - DESCARTE DE PERMEADO (BC-500 A/B)",
        "periodicidade": "Mensal",
        "atividades": [
            "Medição de tensão e corrente",
            "Verificação do sistema de fixação",
            "Verificação quanto à vibrações",
            "Verificação quanto ao aquecimento do motor",
            "Verificar ruídos anormais",
        ],
    },
    {
        "id": 9,
        "nome": "SOPRADOR DE AR (CP-100 A/B)",
        "periodicidade": "Mensal / Semanal",
        "atividades": [
            "Medição de tensão e corrente",
            "Verificação do filtro de ar",
            "Verificação do nível de óleo",
            "Verificação de ruídos e vibrações",
            "Verificação de temperatura do bloco",
        ],
    },
    {
        "id": 10,
        "nome": "SOPRADOR DE AR (CP-110 A/B)",
        "periodicidade": "Mensal / Semanal",
        "atividades": [
            "Medição de tensão e corrente",
            "Verificação do filtro de ar",
            "Verificação do nível de óleo",
            "Verificação de ruídos e vibrações",
            "Verificação de temperatura do bloco",
        ],
    },
    {
        "id": 11,
        "nome": "SOPRADOR DE AR (CP-300 A/B)",
        "periodicidade": "Mensal / Semanal",
        "atividades": [
            "Medição de tensão e corrente",
            "Verificação do filtro de ar",
            "Verificação do nível de óleo",
            "Verificação de ruídos e vibrações",
            "Verificação de temperatura do bloco",
        ],
    },
    {
        "id": 12,
        "nome": "SOPRADOR DE AR (CP-400 A/B)",
        "periodicidade": "Mensal / Semanal",
        "atividades": [
            "Medição de tensão e corrente",
            "Verificação do filtro de ar",
            "Verificação do nível de óleo",
            "Verificação de ruídos e vibrações",
            "Verificação de temperatura do bloco",
        ],
    },
    {
        "id": 13,
        "nome": "BOMBA DOSADORA - HIPOCLORITO DE SÓDIO (BP-415 A/B)",
        "periodicidade": "Semanal",
        "atividades": [
            "Verificação de vazamentos nas mangueiras",
            "Calibração de vazão",
            "Limpeza da válvula de pé e injeção",
        ],
    },
    {
        "id": 14,
        "nome": "BOMBA DOSADORA - ÁCIDO CÍTRICO (BP-420 A/B)",
        "periodicidade": "Semanal",
        "atividades": [
            "Verificação de vazamentos nas mangueiras",
            "Calibração de vazão",
            "Limpeza da válvula de pé e injeção",
        ],
    },
    {
        "id": 15,
        "nome": "BOMBA DOSADORA - POLÍMERO (BD-610 A/B) - CP 150012437",
        "periodicidade": "Semanal",
        "atividades": [
            "Verificação de vazamentos nas mangueiras",
            "Calibração de vazão",
            "Limpeza do sistema de dosagem",
        ],
    },
    {
        "id": 16,
        "nome": "CENTRÍFUGA DECANTER (CEN)",
        "periodicidade": "Mensal / Semestral",
        "atividades": [
            "Inspeção do painel de controle e inversores",
            "Verificação de vibração do tambor",
            "Lubrificação de mancais",
            "Verificação de vazamentos de selagem",
        ],
    },
    {
        "id": 17,
        "nome": "PENEIRA AUTO-LIMPANTE (FA)",
        "periodicidade": "Semanal / Mensal",
        "atividades": [
            "Limpeza e inspeção da rede filtrante",
            "Verificação do sistema de motoredutor",
            "Inspeção de esguichos de lavagem",
        ],
    },
    {
        "id": 18,
        "nome": "MEMBRANA MBR",
        "periodicidade": "Diária / Mensal",
        "atividades": [
            "Controle da pressão transmembrana (PTM)",
            "Execução de retrolavagem (backwash)",
            "Verificação química e limpeza CIP",
        ],
    },
    {
        "id": 19,
        "nome": "DIFUSORES DE AR",
        "periodicidade": "Semestral",
        "atividades": [
            "Inspeção de estanquidade e bolhas uniformes nos tanques",
            "Verificação de perda de carga no sistema de ar",
        ],
    },
    {
        "id": 20,
        "nome": "INSTRUMENTOS",
        "periodicidade": "Mensal",
        "atividades": [
            "Calibração e verificação de sensores de nível, pH e oxigênio dissolvido",
        ],
    },
    {
        "id": 21,
        "nome": "PAINÉIS DE COMANDO / PLC",
        "periodicidade": "Mensal",
        "atividades": [
            "Inspeção visual de bornes e disjuntores",
            "Limpeza de filtros de ventilação do painel",
            "Teste de sinalização e automação CLP",
        ],
    },
]

# --- PAINEL LATERAL (PAINEL DE CONTROLE) ---
st.sidebar.markdown(
    "<h2 style='text-align: center; font-size: 24px; font-weight:"
    " 900;'>Painel de Controle</h2>",
    unsafe_allow_html=True,
)

meses_pt = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}
ano = st.sidebar.selectbox("Ano", [2026, 2027], index=0)
mes_nome = st.sidebar.selectbox(
    "Mês",
    list(meses_pt.values()),
    index=list(meses_pt.values()).index(meses_pt[datetime.now().month]),
)
mes_num = [k for k, v in meses_pt.items() if v == mes_nome][0]

st.sidebar.markdown("---")

with st.sidebar.expander("📅 Calendário Operacional", expanded=True):
  st.markdown(f"<span style='font-size: 18px; font-weight: bold;'>{mes_nome} de {ano}</span>", unsafe_allow_html=True)
  cal = calendar.monthcalendar(ano, mes_num)
  dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

  cal_html = "<table style='width:100%; text-align:center; font-size:16px; border-collapse: collapse;'>"
  cal_html += (
      "<tr>"
      + "".join(
          [f"<th style='padding:8px; font-weight:bold;'>{d}</th>" for d in dias_semana]
      )
      + "</tr>"
  )
  dia_hoje = datetime.now().day if datetime.now().month == mes_num else -1

  for semana in cal:
    cal_html += "<tr>"
    for dia in semana:
      if dia == 0:
        cal_html += "<td style='padding:8px;'></td>"
      elif dia == dia_hoje:
        cal_html += (
            f"<td style='padding:8px; background-color:#003366; color:white;"
            f" font-weight:bold; border-radius:50%;'>{dia:02d}</td>"
        )
      else:
        cal_html += f"<td style='padding:8px; font-weight:bold;'>{dia:02d}</td>"
    cal_html += "</tr>"
  cal_html += "</table>"
  st.markdown(cal_html, unsafe_allow_html=True)

st.sidebar.markdown("---")
with st.sidebar.expander("📋 Gestão do Rascunho", expanded=True):
  st.markdown(
      f"<span style='font-size: 18px; font-weight: bold;'>**Itens no Rascunho:** {len(st.session_state['registros_manutencao'])}</span>",
      unsafe_allow_html=True,
  )

# --- CABEÇALHO COM LOGO E TÍTULO EM BLOCO AZUL ---
col_logo1, col_logo2 = st.columns([1, 5])
with col_logo1:
  if os.path.exists("logo.jpg"):
    st.image("logo.jpg", width=130)
  else:
    st.markdown("🛠️")
with col_logo2:
  st.markdown(
      "<div style='background-color: #003366; padding: 15px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); border: 2px solid #001f3f;'>"
      "<h2 style='color: white !important; margin: 0; font-size: 26px; font-weight: 900;'>ETE Sesc Bertioga — Módulo de Manutenção</h2>"
      "</div>",
      unsafe_allow_html=True,
  )

st.markdown("---")

st.markdown(
    "<div class='intervencao-header'>REGISTO DE INTERVENÇÃO PREVENTIVA / CORRETIVA</div>",
    unsafe_allow_html=True,
)

# 1. CAMPOS GERAIS
col_m1, col_m2 = st.columns(2)
with col_m1:
  opcoes_equipamentos = [
      f"{eq['id']} - {eq['nome']} ({eq['periodicidade']})"
      for eq in EQUIPAMENTOS_MANUTENCAO
  ]
  equipamento_selecionado_str = st.selectbox(
      "Equipamento / TAG (Cronograma Planilha)", opcoes_equipamentos
  )

  horimetro = st.text_input(
      "Horímetro / Leitura Atual (se aplicável)", placeholder="Ex: 4520 h"
  )

  tipo_manut = st.selectbox("Tipo de Manutenção", ["Preventiva", "Corretiva"])

  operadores = st.multiselect(
      "Operador(es)", ["Ícaro", "Lenine", "Matheus", "Wagner"]
  )
  mecanicos = st.multiselect("Mecânico(s)", ["Cesar"])
  eletricistas = st.multiselect("Eletricista(s)", ["Paulo"])

with col_m2:
  data_manut = st.date_input("Data da Intervenção", value=datetime.now().date())
  
  status_manut = st.radio(
      "Status da Ação",
      ["Concluído", "Parcialmente Concluído", "Equipamento Fora de Operação"],
      horizontal=True
  )

  observacao_equipamento = st.text_input(
      "Observação / Justificativa do Equipamento (Opcional)",
      placeholder="Informe observações específicas deste equipamento...",
  )

eq_obj = next(
    eq
    for eq in EQUIPAMENTOS_MANUTENCAO
    if f"{eq['id']} - {eq['nome']} ({eq['periodicidade']})"
    == equipamento_selecionado_str
)
atividades_do_equip = eq_obj["atividades"]

dados_atividades = {}
rastreabilidade_fora_op = {}

# 2. SEÇÃO DE RASTREABILIDADE
if status_manut == "Equipamento Fora de Operação":
  st.markdown("---")
  st.markdown(
      "<div style='background-color: #fee2e2; border: 2px solid #b91c1c; color: #b91c1c; padding: 14px; border-radius: 8px; font-size: 20px; font-weight: 900; text-align: center;'>⚠️ Rastreabilidade de Equipamento Fora de Operação</div>",
      unsafe_allow_html=True,
  )
  st.markdown("<br>", unsafe_allow_html=True)

  col_f1, col_f2 = st.columns(2)
  with col_f1:
    rastreabilidade_fora_op["data_parada"] = str(
        st.date_input("Data em que Parou de Funcionar", value=datetime.now().date(), key="d_parada")
    )
  with col_f2:
    rastreabilidade_fora_op["data_saida_manut"] = str(
        st.date_input("Data de Saída para Manutenção / Aguardando", value=datetime.now().date(), key="d_saida")
    )

  rastreabilidade_fora_op["motivo_anomalia"] = st.text_area(
      "Motivo / Descrição da Anomalia da Paralisação",
      placeholder="Descreva detalhadamente o motivo da interrupção...",
      key="txt_anomalia"
  )

# 3. ATIVIDADES PREVENTIVAS
st.markdown("---")
st.markdown(
    "<div class='section-sub-title'>📋 Atividades Preventivas do Equipamento</div>",
    unsafe_allow_html=True,
)

default_checkbox_value = (status_manut != "Equipamento Fora de Operação")

for i, atividade in enumerate(atividades_do_equip):
  st.markdown(
      f"<div class='card-atividade'><strong>{atividade}</strong></div>",
      unsafe_allow_html=True,
  )

  col_a1, col_a2 = st.columns([1, 2])
  with col_a1:
    executado = st.checkbox(
        f"Realizado? [{status_manut}]", value=default_checkbox_value, key=f"ativ_exec_{i}"
    )

  detalhe_ativ = {}
  with col_a2:
    if not executado:
      detalhe_ativ["status"] = (
          "Paralisado (Fora de Operação)"
          if status_manut == "Equipamento Fora de Operação"
          else "Pendente / Não Executado"
      )
      detalhe_ativ["motivo"] = st.text_input(
          f"Justificativa / Estado ({i})",
          value=(
              "Equipamento Fora de Operação"
              if status_manut == "Equipamento Fora de Operação"
              else ""
          ),
          placeholder="Informe o motivo...",
          key=f"mot_{i}",
      )
    else:
      detalhe_ativ["status"] = status_manut

  dados_atividades[atividade] = {
      "executado": executado,
      "detalhes": detalhe_ativ,
  }

st.markdown("<br>", unsafe_allow_html=True)
descricao_servico = st.text_area(
    "Descrição Detalhada Geral do Serviço / Peças Substituídas", key="desc_geral"
)

st.markdown("---")

# 4. BOTÃO FINAL DE REGISTRO
if st.button("➕ REGISTAR / SALVAR RASCUNHO DA MANUTENÇÃO"):
  erro_validacao = False
  equip_nome_atual = eq_obj["nome"]
  data_atual_str = str(data_manut)

  duplicado = any(
      r["equipamento"] == equip_nome_atual and r["data"] == data_atual_str
      for r in st.session_state["registros_manutencao"]
  )

  if duplicado:
    st.error(
        "⚠️ Já existe um registro de manutenção para este equipamento nesta"
        " mesma data. Evite duplicidade."
    )
    erro_validacao = True
  elif status_manut == "Equipamento Fora de Operação":
    if not rastreabilidade_fora_op.get("motivo_anomalia", "").strip():
      st.error("⚠️ Preencha o motivo/anomalia da parada do equipamento.")
      erro_validacao = True
  else:
    for atv, info in dados_atividades.items():
      if not info["executado"] and not info["detalhes"].get("motivo", "").strip():
        st.error(f"⚠️ Informe a justificativa para a atividade não executada: '{atv}'")
        erro_validacao = True
        break

  if not erro_validacao:
    if status_manut == "Equipamento Fora de Operação":
      detalhes_atividades_str = "Equipamento Fora de Operação"
    else:
      atividades_realizadas_count = sum(
          1 for info in dados_atividades.values() if info["executado"]
      )
      detalhes_atividades_str = (
          f"{atividades_realizadas_count}/{len(atividades_do_equip)} concluídas"
      )

    equipe_responsavel = []
    if operadores:
      equipe_responsavel.append(f"Op: {', '.join(operadores)}")
    if mecanicos:
      equipe_responsavel.append(f"Mec: {', '.join(mecanicos)}")
    if eletricistas:
      equipe_responsavel.append(f"Elet: {', '.join(eletricistas)}")
    str_equipe = (
        " | ".join(equipe_responsavel) if equipe_responsavel else "Não informada"
    )

    nova_manut = {
        "id": len(st.session_state["registros_manutencao"]) + 1,
        "data": str(data_manut),
        "equipamento": eq_obj["nome"],
        "periodicidade": eq_obj["periodicidade"],
        "tipo": tipo_manut,
        "equipe": str_equipe,
        "status": status_manut,
        "observacao_equipamento": observacao_equipamento,
        "horimetro": horimetro,
        "atividades_realizadas": detalhes_atividades_str,
        "detalhes_atividades": dados_atividades,
        "rastreabilidade_fora_op": (
            rastreabilidade_fora_op
            if status_manut == "Equipamento Fora de Operação"
            else {}
        ),
        "descricao": descricao_servico,
    }
    st.session_state["registros_manutencao"].append(nova_manut)
    salvar_dados_manutencao(st.session_state["registros_manutencao"])
    st.success("✅ Registo de manutenção guardado com sucesso no rascunho!")
    st.rerun()

# --- HISTÓRICO E GESTÃO DOS REGISTOS & GERAÇÃO DE PDF ---
if len(st.session_state["registros_manutencao"]) > 0:
  st.markdown("---")
  st.markdown("<div style='font-size: 22px; font-weight: bold;'>📋 Histórico de Manutenções Registradas</div>", unsafe_allow_html=True)
  df_manut = pd.DataFrame(st.session_state["registros_manutencao"])
  st.dataframe(df_manut, use_container_width=True)


  def gerar_pdf_manutencao(registros):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    if os.path.exists("logo.jpg"):
      try:
        pdf.image("logo.jpg", x=10, y=8, w=25)
      except:
        pass

    pdf.set_font("Arial", "B", 15)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(
        0, 10, "ETE Sesc Bertioga - Relatório de Manutenção", 0, 1, "C"
    )

    pdf.set_font("Arial", "", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(
        0,
        6,
        f"Emitido em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}",
        0,
        1,
        "C",
    )
    pdf.ln(10)

    pdf.set_text_color(0, 0, 0)
    for reg in registros:
      pdf.set_font("Arial", "B", 11)
      pdf.set_fill_color(240, 240, 240)
      pdf.cell(
          0,
          8,
          f" Equipamento: {reg['equipamento']}",
          1,
          1,
          "L",
          fill=True,
      )

      pdf.set_font("Arial", "", 9)
      pdf.cell(
          95,
          6,
          f"Data: {reg['data']} | Tipo: {reg['tipo']}",
          1,
          0,
          "L",
      )
      pdf.cell(
          95,
          6,
          f"Status: {reg['status']} | Horímetro: {reg['horimetro']}",
          1,
          1,
          "L",
      )
      pdf.cell(
          0,
          6,
          f"Equipe: {reg['equipe']}",
          1,
          1,
          "L",
      )
      
      if reg['status'] != "Equipamento Fora de Operação":
        pdf.cell(
            0,
            6,
            f"Atividades Realizadas: {reg['atividades_realizadas']}",
            1,
            1,
            "L",
        )

      if reg.get("observacao_equipamento"):
        pdf.cell(
            0,
            6,
            f"Observação do Equipamento: {reg['observacao_equipamento']}",
            1,
            1,
            "L",
        )

      if reg.get("rastreabilidade_fora_op") and reg["rastreabilidade_fora_op"]:
        r_op = reg["rastreabilidade_fora_op"]
        pdf.set_font("Arial", "B", 9)
        pdf.cell(0, 6, "Dados de Parada / Fora de Operação:", 1, 1, "L", fill=True)
        pdf.set_font("Arial", "", 8)
        pdf.multi_cell(
            0,
            5,
            f"- Data Parada: {r_op.get('data_parada')} | Saída Manut.: {r_op.get('data_saida_manut')}\n- Motivo/Anomalia: {r_op.get('motivo_anomalia')}",
            1,
            "L",
        )

      if reg['status'] != "Equipamento Fora de Operação" and reg.get("detalhes_atividades") and reg["detalhes_atividades"]:
        pdf.set_font("Arial", "B", 9)
        pdf.cell(0, 6, "Detalhes das Atividades:", 1, 1, "L", fill=True)
        pdf.set_font("Arial", "", 8)
        for atv_nome, info_ativ in reg["detalhes_atividades"].items():
          status_txt = info_ativ["detalhes"].get("status", "")
          extra = ""
          if not info_ativ["executado"]:
            extra = f" | Justificativa: {info_ativ['detalhes'].get('motivo')}"
          pdf.multi_cell(0, 5, f"- {atv_nome} [{status_txt}]{extra}", 1, "L")

      pdf.multi_cell(
          0,
          6,
          f"Descrição do Serviço / Peças: {reg['descricao']}",
          1,
          "L",
      )
      pdf.ln(5)

    filename = "relatorio_manutencao_ete.pdf"
    pdf.output(filename)
    return filename


  col_b1, col_b2 = st.columns(2)
  with col_b1:
    if st.button("📄 GERAR RELATÓRIO PDF"):
      pdf_file = gerar_pdf_manutencao(st.session_state["registros_manutencao"])
      with open(pdf_file, "rb") as f:
        pdf_bytes = f.read()

      st.download_button(
          label="⬇ DESCARREGAR RELATÓRIO PDF (.pdf)",
          data=pdf_bytes,
          file_name="relatorio_manutencao_ete.pdf",
          mime="application/pdf",
      )
      st.success("✅ Relatório PDF gerado com sucesso!")

  with col_b2:
    if st.button("🗑️ LIMPAR HISTÓRICO DE MANUTENÇÃO"):
      st.session_state["registros_manutencao"] = []
      if os.path.exists(ARQUIVO_DADOS_MAN):
        os.remove(ARQUIVO_DADOS_MAN)
      st.success("Histórico de manutenção limpo com sucesso!")
      st.rerun()
