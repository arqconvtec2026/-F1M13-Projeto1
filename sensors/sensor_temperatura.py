import paho.mqtt.client as mqtt
import json
import time
import random

BROKER = "localhost"
PORT = 1883
TOPICO = "medicamentos/lote/A7/temperatura"

cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
cliente.connect(BROKER, PORT)
cliente.loop_start()

print(f"Publicando em: {TOPICO}")
print("Ctrl+C para parar\n")

try:
    while True:
        temperatura = round(random.uniform(2.0, 10.0), 2)
        payload = json.dumps({
            "lote": "A7",
            "temperatura": temperatura,
            "timestamp": time.time()
        })
        cliente.publish(TOPICO, payload)
        print(f"Enviado: {payload}")
        time.sleep(2)

except KeyboardInterrupt:
    print("\nPublisher encerrado.")
    cliente.loop_stop()
    cliente.disconnect()
