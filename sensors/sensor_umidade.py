import paho.mqtt.client as mqtt
import json
import time
import random

BROKER = "localhost"
PORT = 1883
TOPICO = "medicamentos/lote/A7/umidade"

# Faixa aceitável para armazenamento de medicamentos (RH%)
UMIDADE_MIN = 30.0
UMIDADE_MAX = 65.0

cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
cliente.connect(BROKER, PORT)
cliente.loop_start()

print(f"Publicando em: {TOPICO}")
print("Ctrl+C para parar\n")

try:
    while True:
        # Simula umidade com variações ocasionais fora do limite
        umidade = round(random.uniform(20.0, 75.0), 2)
        payload = json.dumps({
            "lote": "A7",
            "umidade": umidade,
            "timestamp": time.time()
        })
        cliente.publish(TOPICO, payload)
        print(f"Enviado: {payload}")
        time.sleep(2)

except KeyboardInterrupt:
    print("\nPublisher encerrado.")
    cliente.loop_stop()
    cliente.disconnect()
