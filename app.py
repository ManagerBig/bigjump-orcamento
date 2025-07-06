import streamlit as st

st.set_page_config(page_title="Orçamento de Aniversário - Big Jump", layout="centered")
st.title("🎂 Orçamento de Festa de Aniversário - Big Jump")

st.sidebar.header("Configurações da Festa")

# Escolha do salão
tipo_salao = st.sidebar.selectbox(
    "Escolha o salão:",
    ["California", "Chicago", "Bevelerels"]
)

# Valores fixos por salão (temporariamente R$1,00)
valores_saloes = {
    "California": 1.00,
    "Chicago": 1.00,
    "Bevelerels": 1.00
}
valor_salao = valores_saloes[tipo_salao]

# Buffet (opcional)
uso_buffet = st.sidebar.checkbox("Incluir buffet?", value=False)
valor_buffet = 1.00 if uso_buffet else 0.00

# Convidados gerais
num_convidados = st.sidebar.number_input("Número de convidados (R$1 por convidado)", min_value=0, value=10)
valor_convidado = num_convidados * 1.00

# Pulantes (opcional)
num_pulantes = st.sidebar.number_input("Número de convidados que vão pular (R$1 por pessoa)", min_value=0, value=5)
valor_pulantes = num_pulantes * 1.00

# Cálculo total
total = valor_salao + valor_buffet + valor_convidado + valor_pulantes

# Exibição
st.markdown("---")
st.subheader("🧾 Resumo do Orçamento")
st.write(f"**Salão escolhido:** {tipo_salao} - R$ {valor_salao:.2f}")
st.write(f"**Buffet:** {'Sim' if uso_buffet else 'Não'} - R$ {valor_buffet:.2f}")
st.write(f"**Convidados:** {num_convidados} - R$ {valor_convidado:.2f}")
st.write(f"**Pulantes:** {num_pulantes} - R$ {valor_pulantes:.2f}")

st.markdown("---")
st.subheader("💰 Valor Total")
st.metric("Total a pagar", f"R$ {total:,.2f}")

st.markdown("---")
st.caption("Desenvolvido para Big Jump USA")
