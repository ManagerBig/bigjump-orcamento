import streamlit as st
import datetime
import tempfile
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
import urllib.parse
import csv

st.set_page_config(page_title="Orçamento de Aniversário - Big Jump", layout="centered")
st.title("🎂 Orçamento de Festa de Aniversário - Big Jump")

st.sidebar.header("Dados do Cliente")
nome_cliente = st.sidebar.text_input("Nome do cliente")
nome_aniversariante = st.sidebar.text_input("Nome do aniversariante")

st.sidebar.header("Configurações da Festa")

# Data do evento para ajustar valor por dia da semana
data_evento = st.sidebar.date_input("Escolha a data da festa", value=datetime.date.today())
if data_evento.weekday() < 4:
    valor_dia = 100.00
    dia_texto = "Dia de semana (Seg a Qui)"
else:
    valor_dia = 300.00
    dia_texto = "Final de semana (Sex a Dom)"

# Escolha do salão
tipo_salao = st.sidebar.selectbox("Escolha o salão:", ["California", "Chicago", "Bevelerels"])
valores_saloes = {"California": 1500.00, "Chicago": 1200.00, "Bevelerels": 1700.00}
valor_salao = valores_saloes[tipo_salao]

# Buffet (opcional)
uso_buffet = st.sidebar.checkbox("Incluir buffet?", value=False)
valor_buffet = 120.00 if uso_buffet else 0.00

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
st.write(f"**Cliente:** {nome_cliente}")
st.write(f"**Aniversariante:** {nome_aniversariante}")
st.write(f"**Data da festa:** {data_evento.strftime('%d/%m/%Y')} - {dia_texto} - R$ {valor_dia:.2f}")
st.write(f"**Salão escolhido:** {tipo_salao} - R$ {valor_salao:.2f}")
st.write(f"**Buffet:** {'Sim' if uso_buffet else 'Não'} - R$ {valor_buffet:.2f}")
st.write(f"**Convidados:** {num_convidados} - R$ {valor_convidado:.2f}")
st.write(f"**Pulantes:** {num_pulantes} ({cortesia_pulantes} cortesia) - R$ {valor_pulantes:.2f}")
st.write(f"**Tema da Festa:** {tema}")
if valor_desconto > 0:
    st.write(f"**Desconto aplicado:** R$ {valor_desconto:.2f}")

st.markdown("---")
st.subheader("💰 Valor Total")
st.metric("Total a pagar", f"R$ {total:,.2f}")

# Gerar PDF estilizado
if st.button("📄 Gerar PDF do orçamento"):
    try:
        logo_path = "logo.png"
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
            c = canvas.Canvas(tmpfile.name, pagesize=A4)
            width, height = A4
            y = height - 50

            try:
                logo = ImageReader(logo_path)
                c.drawImage(logo, width/2 - 60, y - 80, width=120, preserveAspectRatio=True, mask='auto')
            except:
                pass

            y -= 120
            c.setFillColor(colors.HexColor("#E63946"))
            c.setFont("Helvetica-Bold", 16)
            c.drawCentredString(width/2, y, "ORÇAMENTO DE FESTA - BIG JUMP USA")
            y -= 30
            c.setFont("Helvetica", 12)
            c.setFillColor(colors.black)
            c.drawString(50, y, f"Cliente: {nome_cliente}")
            y -= 20
            c.drawString(50, y, f"Aniversariante: {nome_aniversariante}")
            y -= 25
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
            if valor_desconto > 0:
                y -= 25
                c.drawString(50, y, f"Desconto aplicado: R$ {valor_desconto:.2f}")

            y -= 40
            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(colors.darkblue)
            c.drawString(50, y, f"VALOR TOTAL: R$ {total:,.2f}")
            y -= 60
            c.setFont("Helvetica-Oblique", 10)
            c.setFillColor(colors.black)
            c.drawString(50, y, "Observações: Este orçamento é válido por 5 dias úteis. Consulte disponibilidade de datas.")
            y -= 30
            c.drawString(50, y, "Big Jump USA agradece o seu contato!")
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

# Enviar WhatsApp
st.markdown("---")
st.subheader("📲 Enviar pelo WhatsApp")

mensagem = f"Olá, aqui está o orçamento da festa para {nome_aniversariante}:\n" \
           f"Cliente: {nome_cliente}\n" \
           f"Data: {data_evento.strftime('%d/%m/%Y')} ({dia_texto})\n" \
           f"Salão: {tipo_salao}\n" \
           f"Buffet: {'Sim' if uso_buffet else 'Não'}\n" \
           f"Convidados: {num_convidados}\n" \
           f"Pulantes: {num_pulantes} (Cortesia: {cortesia_pulantes})\n" \
           f"Tema: {tema}\n"
if valor_desconto > 0:
    mensagem += f"Desconto: R$ {valor_desconto:.2f}\n"
mensagem += f"Total: R$ {total:,.2f}"

numero = st.text_input("Número de WhatsApp (somente números com DDD, ex: 11999998888)")
if st.button("📤 Enviar orçamento pelo WhatsApp") and numero:
    url = f"https://wa.me/{numero}?text={urllib.parse.quote(mensagem)}"
    st.markdown(f"[Clique aqui para enviar 📲]({url})", unsafe_allow_html=True)

# Salvar orçamento em CSV
st.markdown("---")
st.subheader("🗂️ Salvar Orçamento")

if st.button("💾 Salvar orçamento em arquivo CSV"):
    dados = [
        nome_cliente, nome_aniversariante, data_evento.strftime('%d/%m/%Y'),
        tipo_salao, uso_buffet, tema, num_convidados, num_pulantes,
        cortesia_pulantes, valor_desconto, total
    ]

    cabecalho = [
        "Cliente", "Aniversariante", "Data da Festa", "Salão", "Buffet", "Tema",
        "Convidados", "Pulantes", "Cortesia Pulantes", "Desconto", "Total"
    ]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(cabecalho)
        writer.writerow(dados)

    with open(csvfile.name, "rb") as f:
        st.download_button(
            label="📥 Baixar arquivo CSV",
            data=f,
            file_name="orcamento_bigjump.csv",
            mime="text/csv"
        )
    os.remove(csvfile.name)

st.markdown("---")
st.caption("Desenvolvido para Big Jump USA")
