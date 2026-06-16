# MQTT Topics — F1M13-Projeto1

Documentação dos tópicos MQTT utilizados no sistema de monitoramento ambiental
para rastreamento de medicamentos do **Lote A7**.

---

## Estrutura Hierárquica

```
medicamentos/lote/A7/temperatura
medicamentos/lote/A7/umidade
medicamentos/lote/A7/pressao
```

| Nível          | Valor         | Descrição                        |
|----------------|---------------|----------------------------------|
| `medicamentos` | fixo          | Sistema raiz                     |
| `lote`         | fixo          | Agrupamento por lote             |
| `A7`           | variável      | Identificador do lote            |
| `temperatura`  | fixo          | Tipo de dado — temperatura (°C)  |
| `umidade`      | fixo          | Tipo de dado — umidade (%RH)     |
| `pressao`      | fixo          | Tipo de dado — pressão (hPa)     |

---

## Tópicos Detalhados

### `medicamentos/lote/A7/temperatura`

| Campo       | Valor                          |
|-------------|--------------------------------|
| Publisher   | `sensors/sensor_temperatura.py` |
| Subscriber  | `dashboard/dashboard.py`        |
| QoS         | 0 (fire-and-forget)             |
| Intervalo   | 2 segundos                      |
| Faixa OK    | 2.0°C – 8.0°C                  |

**Payload exemplo:**
```json
{"lote": "A7", "temperatura": 5.23, "timestamp": 1748908624.3}
```

---

### `medicamentos/lote/A7/umidade`

| Campo       | Valor                        |
|-------------|------------------------------|
| Publisher   | `sensors/sensor_umidade.py`  |
| Subscriber  | `dashboard/dashboard.py`     |
| QoS         | 0 (fire-and-forget)          |
| Intervalo   | 2 segundos                   |
| Faixa OK    | 30.0%RH – 65.0%RH            |

**Payload exemplo:**
```json
{"lote": "A7", "umidade": 48.71, "timestamp": 1748908626.1}
```

---

### `medicamentos/lote/A7/pressao`

| Campo       | Valor                        |
|-------------|------------------------------|
| Publisher   | `sensors/sensor_pressao.py`  |
| Subscriber  | `dashboard/dashboard.py`     |
| QoS         | 0 (fire-and-forget)          |
| Intervalo   | 2 segundos                   |
| Faixa OK    | 980.0hPa – 1030.0hPa         |

**Payload exemplo:**
```json
{"lote": "A7", "pressao": 1013.45, "timestamp": 1748908628.7}
```

---

## Wildcards úteis para teste

```bash
# Escutar todos os sensores do lote A7
mosquitto_sub -h localhost -t "medicamentos/lote/A7/#"

# Escutar apenas temperatura
mosquitto_sub -h localhost -t "medicamentos/lote/A7/temperatura"

# Escutar todos os lotes (futuro: A7, B3, C1...)
mosquitto_sub -h localhost -t "medicamentos/lote/+/temperatura"
```

---

## Observações de Segurança

> ⚠️ MQTT padrão (porta 1883) transmite payload em **texto plano**.
> O JSON com lote/temperatura/timestamp fica exposto em qualquer captura de rede.
>
> **Fase 2.4 do roadmap ACT** implementará MQTT sobre TLS (porta 8883)
> com autenticação por certificado para resolver esta vulnerabilidade.
