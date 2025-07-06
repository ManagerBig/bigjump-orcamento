import streamlit as st
import datetime
import pdfkit
import tempfile
import os

st.set_page_config(page_title="Orçamento de Aniversário - Big Jump", layout="centered")
st.title("🎂 Orçamento de Festa de Aniversário - Big Jump")

st.sidebar.header("Configurações da Festa")

# Data do evento para ajustar valor por dia da semana
data_evento = st.sidebar.date_input("Escolha a data da festa", value=datetime.date.today())
if data_evento.weekday() < 4:
    valor_dia = 1.00
    dia_texto = "Dia de semana (Seg a Qui)"
else:
    valor_dia = 2.00
    dia_texto = "Final de semana (Sex a Dom)"

# Escolha do salão
tipo_salao = st.sidebar.selectbox("Escolha o salão:", ["California", "Chicago", "Bevelerels"])
valores_saloes = {"California": 1.00, "Chicago": 1.00, "Bevelerels": 1.00}
valor_salao = valores_saloes[tipo_salao]

# Buffet (opcional)
uso_buffet = st.sidebar.checkbox("Incluir buffet?", value=False)
valor_buffet = 1.00 if uso_buffet else 0.00

# Convidados
tema = st.sidebar.selectbox("Tema da festa", ["Laser Tag", "Big Jump", "Frozen", "Super Heróis", "Minions", "Minecraft", "Patrulha Canina"])
num_convidados = st.sidebar.number_input("Número de convidados (R$1 por convidado)", min_value=0, value=10)
valor_convidado = num_convidados * 1.00

# Pulantes e cortesia
num_pulantes = st.sidebar.number_input("Número de convidados que vão pular (R$1 por pessoa)", min_value=0, value=5)
cortesia_pulantes = st.sidebar.number_input("Quantidade de cortesia para pulantes", min_value=0, max_value=num_pulantes, value=0)
valor_pulantes = max(0, num_pulantes - cortesia_pulantes) * 1.00

# Valor base + desconto
valor_base = 500.00
valor_desconto = st.sidebar.number_input("Desconto aplicado (R$)", min_value=0.00, max_value=valor_base, value=0.00, step=10.0)

total = valor_base + valor_salao + valor_buffet + valor_convidado + valor_pulantes + valor_dia - valor_desconto

# Mostrar orçamento
st.markdown("---")
st.subheader("🧾 Resumo do Orçamento")
st.write(f"**Data da festa:** {data_evento.strftime('%d/%m/%Y')} - {dia_texto} - R$ {valor_dia:.2f}")
st.write(f"**Salão escolhido:** {tipo_salao} - R$ {valor_salao:.2f}")
st.write(f"**Buffet:** {'Sim' if uso_buffet else 'Não'} - R$ {valor_buffet:.2f}")
st.write(f"**Convidados:** {num_convidados} - R$ {valor_convidado:.2f}")
st.write(f"**Pulantes:** {num_pulantes} ({cortesia_pulantes} cortesia) - R$ {valor_pulantes:.2f}")
st.write(f"**Tema da Festa:** {tema}")
st.write(f"**Desconto aplicado:** R$ {valor_desconto:.2f}")

st.markdown("---")
st.subheader("💰 Valor Total")
st.metric("Total a pagar", f"R$ {total:,.2f}")

# Gerar HTML para o PDF
html = f"""
<h2>Orçamento de Festa - Big Jump</h2>
<p><strong>Data:</strong> {data_evento.strftime('%d/%m/%Y')} ({dia_texto})</p>
<p><strong>Salão:</strong> {tipo_salao} - R$ {valor_salao:.2f}</p>
<p><strong>Buffet:</strong> {'Sim' if uso_buffet else 'Não'} - R$ {valor_buffet:.2f}</p>
<p><strong>Convidados:</strong> {num_convidados} - R$ {valor_convidado:.2f}</p>
<p><strong>Pulantes:</strong> {num_pulantes} (Cortesia: {cortesia_pulantes}) - R$ {valor_pulantes:.2f}</p>
<p><strong>Tema:</strong> {tema}</p>
<p><strong>Desconto:</strong> R$ {valor_desconto:.2f}</p>
<p><strong>Valor Total:</strong> R$ {total:,.2f}</p>
<p><em>Big Jump USA</em></p>
"""

if st.button("📄 Gerar PDF do orçamento"):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_html:
            tmp_html.write(html.encode("utf-8"))
            tmp_html_path = tmp_html.name

        pdf_path = tmp_html_path.replace(".html", ".pdf")
        pdfkit.from_file(tmp_html_path, pdf_path)

        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="📥 Baixar PDF do orçamento",
                data=pdf_file,
                file_name="orcamento_bigjump.pdf",
                mime="application/pdf"
            )

        os.remove(tmp_html_path)
        os.remove(pdf_path)
    except Exception as e:
        st.error(f"Erro ao gerar PDF: {e}")

st.markdown("---")
st.caption("Desenvolvido para Big Jump USA")
