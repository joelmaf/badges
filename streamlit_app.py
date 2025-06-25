import streamlit as st
import json
import os
import re

CAMINHO_JSON = "badges.json"

#def carregar_dados():
#    try:
#        with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
#            return json.load(f)
#    except Exception:
#        st.error("Erro ao buscar os dados.")
#        return []

def carregar_dados():
    try:
        conteudo = st.secrets["badges"]["conteudo"]
        return json.loads(conteudo)
    except Exception:
        st.error("Erro ao carregar os dados.")
        return []


def validar_dados(cpf, codigo, dados):
    cpf = cpf.strip()
    codigo = codigo.strip().upper()
    for item in dados:
        if item["cpf"] == cpf and item["codigo"].upper() == codigo:
            return item
    return None

def entrada_valida(texto, tipo="geral"):
    if tipo == "cpf":
        return bool(re.match(r"^\d{11}$", texto))
    if tipo == "codigo":
        return bool(re.match(r"^[a-zA-Z0-9]{4,15}$", texto))
    return False


st.set_page_config(page_title="Validação de Badge: Cursos de Tecnologia IPOG", page_icon="🎓")

st.title("🎓 Validação de Badge: Cursos de Tecnologia IPOG")
st.write("Para confirmar essa validação, caso queira pode enviar um email para: graduacao@ipog.edu.br , informar o Nome, CPF e Código do Badge.")

cpf = st.text_input("Digite o CPF (apenas números)")
codigo = st.text_input("Digite o código do badge")

if st.button("Validar Badge"):
    if not entrada_valida(cpf, tipo="cpf"):
        st.warning("CPF inválido. Deve conter 11 dígitos numéricos.")
    elif not entrada_valida(codigo, tipo="codigo"):
        st.warning("Código inválido. Use apenas letras e números, entre 4 e 15 caracteres.")
    else:
        dados = carregar_dados()
        resultado = validar_dados(cpf, codigo, dados)

        if resultado:
            st.success("✅ Badge encontrado!")
            st.write(f"**Nome:** {resultado['nome']}")
            st.write(f"**Faculdade:** Faculdade de Pós-Graduação e Graduação - IPOG")
            st.write(f"**Curso:** {resultado['curso']}")
            st.write(f"**Badge:** {resultado['badge']}")
            st.write(f"**Código:** {resultado['codigo']}")
        else:
            st.error("❌ CPF e código não correspondem a nenhum badge.")
