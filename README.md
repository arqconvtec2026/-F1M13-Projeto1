# F1M13-Projeto1 — Rede IoT Simulada com MQTT

Projeto prático do **Módulo 1.3 — Redes de Computadores** do roadmap  
*Arquiteto de Convergência Tecnológica (ACT)* — Fase 1, Semana 15.

## Descrição

Sistema de monitoramento de temperatura para rastreamento de medicamentos,  
simulando a comunicação entre sensores IoT e um dashboard via protocolo MQTT.

O projeto é a base do sistema de rastreamento e verificação de integridade  
de medicamentos que será expandido ao longo do roadmap com IoT (ESP32),  
IA (detecção de anomalias), Blockchain (audit trail) e Cibersegurança.

## Arquitetura

```
sensor\_temperatura.py  →  Broker MQTT (Mosquitto)  →  dashboard.py
     \[Publisher]              \[localhost:1883]           \[Subscriber]
```

## Estrutura

```
F1M13-Projeto1/
├── sensors/
│   └── sensor\_temperatura.py   # Publisher: simula leituras de temperatura
├── dashboard/
│   └── dashboard.py            # Subscriber: recebe e detecta anomalias
├── requirements.txt
└── .gitignore
```

## Tecnologias

* Python 3.12
* paho-mqtt 2.1.0
* Mosquitto 2.1.2
* WSL Ubuntu

## Como executar

### Pré-requisitos

```bash
# Instalar Mosquitto (WSL/Ubuntu)
sudo apt install mosquitto mosquitto-clients

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### Executar

**Terminal 1 — Verificar broker:**

```bash
sudo systemctl status mosquitto
```

**Terminal 2 — Dashboard (subscriber):**

```bash
python3 dashboard/dashboard.py
```

**Terminal 3 — Sensor (publisher):**

```bash
python3 sensors/sensor\_temperatura.py
```

## Comportamento esperado

```
\[19:17:04] ⚠ ANOMALIA — Lote A7: 8.62°C fora do intervalo \[2.0, 8.0]
\[19:17:06] OK — Lote A7: 3.51°C
\[19:17:08] OK — Lote A7: 7.59°C
```

## Tópico MQTT

```
medicamentos/lote/A7/temperatura
```

|Nível|Valor|Descrição|
|-|-|-|
|`medicamentos`|fixo|Sistema raiz|
|`lote`|fixo|Agrupamento por lote|
|`A7`|variável|Identificador do lote|
|`temperatura`|fixo|Tipo de dado|

## Limites de temperatura

|Parâmetro|Valor|
|-|-|
|Mínimo|2.0 °C|
|Máximo|8.0 °C|



