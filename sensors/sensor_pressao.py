import paho.mqtt.client as mqtt
import json
import time
import random

BROKER = "localhost"
PORT = 1883
TOPICO = "medicamentos/lote/A7/pressao"

# Faixa aceitável de pressão atmosférica (hPa) em ambiente controlado
PRESSAO_MIN = 980.0
PRESSAO_MAX = 1030.0

cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
cliente.connect(BROKER, PORT)
cliente.loop_start()

print(f"Publicando em: {TOPICO}")
print("Ctrl+C para parar\n")

try:
    while True:
        # Simula pressão com variações ocasionais fora do limite
        pressao = round(random.uniform(960.0, 1050.0), 2)
        payload = json.dumps({
            "lote": "A7",
            "pressao": pressao,
            "timestamp": time.time()
        })
        cliente.publish(TOPICO, payload)
        print(f"Enviado: {payload}")
        time.sleep(2)

except KeyboardInterrupt:
    print("\nPublisher encerrado.")
    cliente.loop_stop()
    cliente.disconnect()
