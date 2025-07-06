import streamlit as st
import datetime
import tempfile
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

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

# Tema e convidados
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

# Função para gerar PDF
if st.button("📄 Gerar PDF do orçamento"):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
            c = canvas.Canvas(tmpfile.name, pagesize=A4)
            width, height = A4

            y = height - 50
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, y, "Orçamento de Festa - Big Jump")

            c.setFont("Helvetica", 12)
            y -= 40
            c.drawString(50, y, f"Data da festa: {data_evento.strftime('%d/%m/%Y')} ({dia_texto})")
            y -= 25
            c.drawString(50, y, f"Salão: {tipo_salao} - R$ {valor_salao:.2f}")
            y -= 25
            c.drawString(50, y, f"Buffet: {'Sim' if uso_buffet else 'Não'} - R$ {valor_buffet:.2f}")
            y -= 25
            c.drawString(50, y, f"Convidados: {num_convidados} - R$ {valor_convidado:.2f}")
            y -= 25
            c.drawString(50, y, f"Pulantes: {num_pulantes} (Cortesia: {cortesia_pulantes}) - R$ {valor_pulantes:.2f}")
            y -= 25
            c.drawString(50, y, f"Tema: {tema}")
            y -= 25
            c.drawString(50, y, f"Desconto aplicado: R$ {valor_desconto:.2f}")
            y -= 40
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y, f"Valor Total: R$ {total:,.2f}")

            y -= 60
            c.setFont("Helvetica-Oblique", 10)
            c.drawString(50, y, "Desenvolvido para Big Jump USA")

            c.save()

        with open(tmpfile.name, "rb") as f:
            st.download_button(
                label="📥 Baixar PDF do orçamento",
                data=f,
                file_name="orcamento_bigjump.pdf",
                mime="application/pdf"
            )

        os.remove(tmpfile.name)

    except Exception as e:
        st.error(f"Erro ao gerar PDF: {e}")

st.markdown("---")
st.caption("Desenvolvido para Big Jump USA")
Atualiza app com geração de PDF estilizado
