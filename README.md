# F1M13-Projeto1 — Rede IoT Simulada com MQTT

Projeto prático do **Módulo 1.3 — Redes de Computadores** do roadmap  
*Arquiteto de Convergência Tecnológica (ACT)* — Fase 1, Semanas 15–17.

## Descrição

Sistema de monitoramento ambiental para rastreamento de medicamentos,  
simulando a comunicação entre 3 sensores IoT e um dashboard via protocolo MQTT.

O projeto é a base do sistema de rastreamento e verificação de integridade  
de medicamentos que será expandido ao longo do roadmap com IoT (ESP32),  
IA (detecção de anomalias), Blockchain (audit trail) e Cibersegurança.

## Arquitetura

```
sensor_temperatura.py  ──┐
                         │
sensor_umidade.py      ──┼──►  Broker MQTT (Mosquitto)  ──►  dashboard.py
                         │       localhost:1883               [Subscriber]
sensor_pressao.py      ──┘                                  + Anomaly Detection
   [Publishers]
```

Para diagrama completo: [`docs/architecture.txt`](docs/architecture.txt)

## Estrutura

```
F1M13-Projeto1/
├── sensors/
│   ├── sensor_temperatura.py   # Publisher: temperatura do lote A7 (°C)
│   ├── sensor_umidade.py       # Publisher: umidade relativa do ar (%RH)
│   └── sensor_pressao.py       # Publisher: pressão atmosférica (hPa)
├── dashboard/
│   └── dashboard.py            # Subscriber: recebe os 3 sensores e detecta anomalias
├── docs/
│   ├── architecture.txt        # Diagrama ASCII da arquitetura
│   └── mqtt_topics.md          # Documentação dos tópicos MQTT
├── mosquitto.conf              # Configuração do broker local
├── requirements.txt
└── .gitignore
```

## Tópicos MQTT

| Tópico                              | Sensor               | Faixa OK            |
|-------------------------------------|----------------------|---------------------|
| `medicamentos/lote/A7/temperatura`  | sensor_temperatura   | 2.0°C – 8.0°C       |
| `medicamentos/lote/A7/umidade`      | sensor_umidade       | 30.0%RH – 65.0%RH   |
| `medicamentos/lote/A7/pressao`      | sensor_pressao       | 980.0hPa – 1030.0hPa|

Wildcard do dashboard: `medicamentos/lote/A7/#`

Documentação completa: [`docs/mqtt_topics.md`](docs/mqtt_topics.md)

## Tecnologias

- Python 3.12
- paho-mqtt 2.1.0 (CallbackAPIVersion.VERSION2)
- Mosquitto 2.1.x
- WSL Ubuntu

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

**Terminal 1 — Broker MQTT:**

```bash
mosquitto -c mosquitto.conf -v
```

**Terminal 2 — Dashboard (subscriber):**

```bash
python3 dashboard/dashboard.py
```

**Terminal 3 — Sensor de temperatura:**

```bash
python3 sensors/sensor_temperatura.py
```

**Terminal 4 — Sensor de umidade:**

```bash
python3 sensors/sensor_umidade.py
```

**Terminal 5 — Sensor de pressão:**

```bash
python3 sensors/sensor_pressao.py
```

## Comportamento esperado

```
[19:17:04] ⚠ ANOMALIA — Lote A7 | temperatura: 8.62°C fora do intervalo [2.0, 8.0]
[19:17:06] OK — Lote A7 | temperatura: 3.51°C
[19:17:07] OK — Lote A7 | umidade: 52.30%RH
[19:17:08] ⚠ ANOMALIA — Lote A7 | pressao: 955.20hPa fora do intervalo [980.0, 1030.0]
[19:17:09] OK — Lote A7 | pressao: 1012.40hPa
```

## Próximos passos no roadmap ACT

| Fase           | Expansão                                                          |
|----------------|-------------------------------------------------------------------|
| Fase 2 — IoT   | Substituir simuladores por ESP32 + DHT22 (hardware real)          |
| Fase 2 — IA    | Isolation Forest para anomalias em séries temporais               |
| Fase 2 — Web3  | Smart contract ERC-721 (Polygon Sepolia) para audit trail imutável|
| Fase 2 — Cyber | TLS/MQTT (porta 8883), autenticação JWT, OWASP IoT Top 10         |

> Alvo regulatório: ANVISA — RDC 430/2020 (rastreamento de medicamentos)
