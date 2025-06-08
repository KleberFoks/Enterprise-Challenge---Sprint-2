# 📡 Projeto de Monitoramento com ESP32 + DHT22

Este projeto simula um sistema de coleta de dados ambientais usando ESP32 e sensor DHT22, com envio via MQTT e análise em Python.  
Faz parte da Fase 4 do desafio Hermes Reply – Indústria 4.0.

## 🧩 Componentes e Ferramentas

- **ESP32** – Microcontrolador com Wi-Fi integrado  
- **Sensor DHT22** – Mede temperatura e umidade  
- **Wokwi** – Simulação do circuito virtual  
- **MQTT (HiveMQ)** – Comunicação entre ESP32 e Python  
- **Python** – Análise e visualização dos dados com:
  - `paho-mqtt`
  - `matplotlib`
  - `pandas`

## 🔧 Funcionamento

- O ESP32 lê dados do DHT22 e envia via MQTT a cada 5 segundos.
- O script Python recebe os dados, classifica as condições e gera um gráfico.
- Os dados recebidos são salvos automaticamente em `dados_simulados.csv`.

### 💡 Lógica de Classificação

```python
if (temp > 35 or hum > 85):
    status = "Crítico"
elif (temp > 30 or hum > 80) or (temp < -10 or hum < 20):
    status = "Alerta"
else:
    status = "Condições normais"
````

## 📁 Conteúdo do Repositório

* `codigo_esp32.ino` – Código do ESP32
* `cliente_mqtt.py` – Script Python para receber, classificar e salvar os dados
* `dados_simulados.csv` – Dados coletados durante a simulação
* `imagens/` – Prints da simulação, terminal e gráfico gerado (presentes no repositório)

## 📈 Resultado

* Gráfico de temperatura e umidade ao longo do tempo
* Classificação automática das condições (normal, alerta, crítico)

## ✅ Requisitos Python

```bash
pip install paho-mqtt matplotlib pandas
```

## Participante:
Kleber Foks RM562225
