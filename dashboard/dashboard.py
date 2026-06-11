import paho.mqtt.client as mqtt
import json
import datetime

BROKER = "localhost"
PORT = 1883
TOPICO = "medicamentos/lote/A7/temperatura"

TEMP_MIN = 2.0
TEMP_MAX = 8.0

def verificar_anomalia(temperatura):
    return temperatura < TEMP_MIN or temperatura > TEMP_MAX

def on_connect(cliente, userdata, flags, reason_code, properties):
    print(f"Conectado ao broker. Código: {reason_code}")
    cliente.subscribe(TOPICO)

def on_message(cliente, userdata, msg):
    payload = json.loads(msg.payload.decode())
    temperatura = payload["temperatura"]
    lote = payload["lote"]
    hora = datetime.datetime.now().strftime("%H:%M:%S")

    if verificar_anomalia(temperatura):
        print(f"[{hora}] ⚠ ANOMALIA — Lote {lote}: {temperatura}°C fora do intervalo [{TEMP_MIN}, {TEMP_MAX}]")
    else:
        print(f"[{hora}] OK — Lote {lote}: {temperatura}°C")

cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
cliente.on_connect = on_connect
cliente.on_message = on_message

cliente.connect(BROKER, PORT)

print(f"Escutando tópico: {TOPICO}\n")
cliente.loop_forever()
