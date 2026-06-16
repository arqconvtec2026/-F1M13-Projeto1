import paho.mqtt.client as mqtt
import json
import datetime

BROKER = "localhost"
PORT = 1883
TOPICO_WILDCARD = "medicamentos/lote/A7/#"

# Limites operacionais por tipo de sensor
LIMITES = {
    "temperatura": {"min": 2.0,   "max": 8.0,    "unidade": "°C"},
    "umidade":     {"min": 30.0,  "max": 65.0,   "unidade": "%RH"},
    "pressao":     {"min": 980.0, "max": 1030.0, "unidade": "hPa"},
}

def verificar_anomalia(tipo, valor):
    if tipo not in LIMITES:
        return False
    return valor < LIMITES[tipo]["min"] or valor > LIMITES[tipo]["max"]

def on_connect(cliente, userdata, flags, reason_code, properties):
    print(f"Conectado ao broker. Código: {reason_code}")
    cliente.subscribe(TOPICO_WILDCARD)
    print(f"Escutando: {TOPICO_WILDCARD}\n")

def on_message(cliente, userdata, msg):
    payload = json.loads(msg.payload.decode())
    lote = payload["lote"]
    hora = datetime.datetime.now().strftime("%H:%M:%S")

    # Determina tipo de sensor pelo último nível do tópico
    tipo = msg.topic.split("/")[-1]  # temperatura | umidade | pressao

    if tipo not in LIMITES:
        return

    valor = payload[tipo]
    unidade = LIMITES[tipo]["unidade"]

    if verificar_anomalia(tipo, valor):
        limites = LIMITES[tipo]
        print(
            f"[{hora}] ⚠ ANOMALIA — Lote {lote} | {tipo}: {valor}{unidade} "
            f"fora do intervalo [{limites['min']}, {limites['max']}]"
        )
    else:
        print(f"[{hora}] OK — Lote {lote} | {tipo}: {valor}{unidade}")

cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
cliente.on_connect = on_connect
cliente.on_message = on_message

cliente.connect(BROKER, PORT)
cliente.loop_forever()
