# Análise de Consumo Energético

Aplicação interativa desenvolvida em Streamlit para simular, visualizar e reduzir o desperdício de energia em ambientes corporativos ou industriais.

---

## 📌 Intuito do Projeto

O sistema foi criado para analisar padrões de consumo energético ao longo do dia, identificar horas de desperdício, estimar economia financeira e calcular redução de emissões de CO₂.  
A simulação considera diversos dispositivos (como ar-condicionado, iluminação, servidores e máquinas industriais) e gera gráficos e métricas automaticamente.

---

## ⚙️ Como Funciona

A aplicação:

- Simula consumo energético hora a hora por dispositivo.  
- Detecta momentos em que o consumo excede **12 kWh**.  
- Permite ao usuário aplicar um percentual de redução para ver o impacto.  
- Gera gráficos comparativos entre consumo real e ajustado.  
- Informa economia em dinheiro e CO₂ evitado.  
- Mostra quais dispositivos mais contribuíram para o desperdício.  
- Permite baixar um CSV completo da simulação.

A interface possui dois controles principais:

- **Dias para simular**  
- **Percentual de redução do desperdício**

---

## 🖥️ Como Rodar Localmente

### 1. Instale o Python  
Recomendado: **Python 3.10+**  
Download: https://www.python.org/downloads/

---

### 2. Crie e ative um ambiente virtual (venv)

No terminal, dentro da pasta do projeto:

**Criar o ambiente virtual:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as bibliotecas necessárias:
```bash
pip install streamlit pandas numpy plotly
```
### 4. Execute o sistema:
```
streamlit run app.py
```
