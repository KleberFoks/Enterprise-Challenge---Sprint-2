import paho.mqtt.client as mqtt
import csv
import datetime
import matplotlib.pyplot as plt
import threading

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "esp32/flood/temperature_humidity"

CSV_FILE = "dados_simulados.csv"

# Listas globais para armazenar os dados recebidos (para plotagem)
timestamps = []
temperaturas = []
umidades = []

# Função para parsear o payload do MQTT
def parse_payload(payload):
    """
    Espera string do tipo 'temp:24.5,hum:55.8' e retorna floats temperatura e umidade.
    """
    try:
        parts = payload.split(',')
        temp = float(parts[0].split(':')[1])
        hum = float(parts[1].split(':')[1])
        return temp, hum
    except Exception as e:
        print(f"[ERRO] Falha no parse do payload '{payload}': {e}")
        return None, None

def salvar_csv(timestamp, temp, hum):
    """
    Salva uma linha no CSV com timestamp, temperatura e umidade.
    Se o arquivo não existir, cria e adiciona cabeçalho.
    """
    try:
        file_exists = False
        try:
            with open(CSV_FILE, 'r'):
                file_exists = True
        except FileNotFoundError:
            pass

        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['timestamp', 'temperatura', 'umidade'])
            writer.writerow([timestamp.isoformat(), temp, hum])
    except Exception as e:
        print(f"[ERRO] Falha ao salvar CSV: {e}")

def plotar_grafico():
    """
    Gera um gráfico simples (linha) para temperatura e umidade ao longo do tempo.
    """
    if not timestamps:
        print("Nenhum dado para plotar ainda.")
        return

    plt.figure(figsize=(10,5))
    plt.plot(timestamps, temperaturas, label='Temperatura (°C)', color='red')
    plt.plot(timestamps, umidades, label='Umidade (%)', color='blue')
    plt.xlabel('Tempo')
    plt.ylabel('Valores')
    plt.title('Dados Simulados do Sensor DHT22 - ESP32')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.show()

def on_message(client, userdata, msg):
    payload_str = msg.payload.decode()
    temp, hum = parse_payload(payload_str)
    if temp is not None and hum is not None:
        now = datetime.datetime.now()
        timestamps.append(now)
        temperaturas.append(temp)
        umidades.append(hum)

        print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Temperatura: {temp:.1f} °C, Umidade: {hum:.1f}%")

        salvar_csv(now, temp, hum)

        # Lógica simples para alerta
        if temp > 30 or hum > 80 and temp < -10 or hum < 20:
            print(">>> Alerta: Condições fora do padrão esperado!")
        else:
            print(">>> Condições normais.")
    else:
        print("Mensagem inválida recebida.")

def main():
    client = mqtt.Client()
    client.on_message = on_message

    print("Conectando ao broker MQTT...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.subscribe(MQTT_TOPIC)

    print(f"Aguardando dados no tópico '{MQTT_TOPIC}'... (Pressione Ctrl+F2 para sair)")

    try:
        client.loop_start()
        while True:
            # Aguarda para coleta contínua, aqui poderia implementar lógica para plotar periodicamente
            pass
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário. Gerando gráfico...")
        client.loop_stop()
        plotar_grafico()
        client.loop_stop()
        print("Encerrado.")

if __name__ == "__main__":
    main()
