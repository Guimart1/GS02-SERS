import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

TARIFA = 0.90
CO2_POR_KWH = 0.07


# modelo básico dos dispositivos
def gerar_dispositivos():
    return [
        {"nome": "Ar-condicionado", "base": 3.5, "variabilidade": 1.2, "horario": lambda h: 8 <= h < 18},
        {"nome": "Iluminação", "base": 1.2, "variabilidade": 0.5, "horario": lambda h: True},
        {"nome": "Servidores", "base": 2.0, "variabilidade": 0.2, "horario": lambda h: True},
        {"nome": "Computadores", "base": 2.5, "variabilidade": 1.5, "horario": lambda h: 8 <= h < 18},
        {"nome": "Geladeira", "base": 0.8, "variabilidade": 0.3, "horario": lambda h: True},
        {"nome": "Máquinas industriais", "base": 8, "variabilidade": 3, "horario": lambda h: 14 <= h < 17},
        {"nome": "Consumo fantasma", "base": 0.5, "variabilidade": 0.3, "horario": lambda h: h < 8 or h >= 18},
    ]


# gera os dados de consumo total
@st.cache_data
def gerar_dados(dias=1):
    horas = pd.date_range("2025-01-01", periods=24 * dias, freq="H")
    dispositivos = gerar_dispositivos()
    consumo_total = []

    for dt in horas:
        h = dt.hour
        soma = 0
        for d in dispositivos:
            if d["horario"](h):
                c = np.random.normal(d["base"], d["variabilidade"])
                soma += max(c, 0)
        if np.random.rand() < 0.05:
            soma += np.random.uniform(5, 15)
        consumo_total.append(soma)

    df = pd.DataFrame({"hora": horas, "consumo_kWh": consumo_total})
    df["desperdicio"] = df["consumo_kWh"] > 12
    return df


# calcula ajustes e economia
def calcular_resultados(df, reducao):
    df = df.copy()
    df["excedente"] = np.where(df["desperdicio"], df["consumo_kWh"] - 12, 0)
    total = df["excedente"].sum()
    reduzido = total * (reducao / 100)
    df["consumo_ajustado"] = df["consumo_kWh"] - df["excedente"] * (reducao / 100)
    df["consumo_ajustado"] = df["consumo_ajustado"].clip(lower=12)

    economia = reduzido * TARIFA
    co2 = reduzido * CO2_POR_KWH

    return total, reduzido, economia, co2, df


# interface
st.set_page_config(page_title="Análise Energética", layout="wide")
st.title("Análise de Consumo Energético")

dias = st.slider("Dias para simular", 1, 30, 7)
reducao = st.slider("Percentual de redução do desperdício", 0, 100, 50)

total, reduzido, economia, co2, df = calcular_resultados(gerar_dados(dias), reducao)


# métricas
st.subheader("Resultados")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Desperdício total (kWh)", f"{total:.2f}")
c2.metric("Redução (kWh)", f"{reduzido:.2f}")
c3.metric("Economia (R$)", f"{economia:.2f}")
c4.metric("CO₂ evitado (kg)", f"{co2:.2f}")


# gráfico
df_long = pd.melt(df, id_vars=["hora"], value_vars=["consumo_kWh", "consumo_ajustado"])
df_long["Tipo"] = df_long["variable"].map({
    "consumo_kWh": "Original",
    "consumo_ajustado": "Ajustado"
})

fig = px.line(df_long, x="hora", y="value", color="Tipo")
fig.add_hline(y=12, line_dash="dash", line_color="red")
st.plotly_chart(fig, use_container_width=True)


# tabela simples
st.subheader("Horas com desperdício")
df_filtro = df[df["desperdicio"]]
st.dataframe(df_filtro, use_container_width=True)


# relatório sobre causas do desperdício
st.subheader("Relatório de Causas do Desperdício")

disps = gerar_dispositivos()
horas = df["hora"]
df_exp = pd.DataFrame({"hora": horas})

for d in disps:
    vals = []
    for dt in horas:
        h = dt.hour
        if d["horario"](h):
            c = np.random.normal(d["base"], d["variabilidade"])
            vals.append(max(c, 0))
        else:
            vals.append(0)
    df_exp[d["nome"]] = vals

df_exp["total"] = df_exp[[d["nome"] for d in disps]].sum(axis=1)
df_exp["excedente"] = (df_exp["total"] - 12).clip(lower=0)

impacto = {}
for d in disps:
    impacto[d["nome"]] = ((df_exp[d["nome"]] / df_exp["total"]) * df_exp["excedente"]).fillna(0).sum()

df_impacto = (pd.DataFrame.from_dict(impacto, orient="index", columns=["Excesso_kWh"])
              .sort_values("Excesso_kWh", ascending=False))

st.write("Dispositivos que mais contribuem para o desperdício")
st.dataframe(df_impacto)

st.write("Principais horários de pico")
horarios = df_exp.groupby(df_exp["hora"].dt.hour)["excedente"].sum().reset_index()
st.dataframe(horarios.sort_values("excedente", ascending=False))

st.success(f"Redução aplicada: {reducao}%. Economia estimada: R$ {economia:.2f}")


st.download_button(
    "Baixar CSV",
    df.to_csv(index=False).encode("utf-8"),
    file_name="consumo.csv",
    mime="text/csv"
)
