# SSH Setup Notes — Módulo 1.4, Semana 20

Documentação do processo de geração e configuração de chave SSH no ambiente WSL Ubuntu.

⚠️ **Este arquivo nunca deve conter o conteúdo da chave privada (`id_ed25519`), apenas fingerprints, paths e comandos.**

---

## 1. Geração do par de chaves

Comando usado (ed25519 — mais moderno e compacto que RSA):

```bash
ssh-keygen -t ed25519 -C "arq.convtec.2026@gmail.com"
```

No prompt `Enter file in which to save the key (/home/ubuntu/.ssh/id_ed25519):` — apertar **Enter** para aceitar o caminho padrão. Passphrase configurada (não vazia).

**Resultado:**
- Chave privada: `~/.ssh/id_ed25519`
- Chave pública: `~/.ssh/id_ed25519.pub`
- Fingerprint: `SHA256:NEPNr8sW1V5YzIjgSkquIjJJa4GYaUyvDPgEgxMmY8k`

O próprio comando criou o diretório `~/.ssh` (`Created directory '/home/ubuntu/.ssh'`), confirmando que era a primeira chave gerada nesse ambiente.

---

## 2. Permissões (verificadas, não precisou de `chmod`)

```
-rw------- id_ed25519       (600 — só o dono lê/escreve)
-rw-r--r-- id_ed25519.pub   (644 — pública, leitura geral ok)
```

`ssh-keygen` já cria com as permissões corretas por padrão.

---

## 3. Adicionar ao ssh-agent

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

Evita digitar a passphrase a cada conexão. Verificado com:

```bash
ssh-add -l
# 256 SHA256:NEPNr8sW1V5YzIjgSkquIjJJa4GYaUyvDPgEgxMmY8k arq.convtec.2026@gmail.com (ED25519)
```

---

## 4. `~/.ssh/config` — atalho de conexão

```bash
cat >> ~/.ssh/config << 'EOF'
Host bandit
    HostName bandit.labs.overthewire.org
    User bandit0
    Port 2220
EOF

chmod 600 ~/.ssh/config
```

Permite `ssh bandit` em vez de `ssh bandit0@bandit.labs.overthewire.org -p 2220`.

O arquivo `config` também precisa de permissão restrita (`600`), assim como a chave privada — o SSH recusa usar arquivos de configuração com permissões abertas demais.

---

## 5. Teste de conexão

```bash
ssh bandit
```

Resultado: conexão estabelecida com sucesso, banner do Bandit exibido, autenticação por senha do wargame funcionando através do atalho configurado.

---

## 🚨 Troubleshooting real desta sessão

### Erro 1: Chave salva com nome errado

Ao gerar a chave pela primeira vez, no prompt de caminho:
```
Enter file in which to save the key (/home/ubuntu/.ssh/id_ed25519): y
```

Um `y` foi digitado (sobra de tecla de confirmação anterior) em vez de apertar Enter puro. Resultado: `ssh-keygen` salvou os arquivos como `y` e `y.pub` **no diretório atual do projeto**, não em `~/.ssh/`.

**Risco**: chaves fora do local padrão + dentro de uma pasta de projeto versionada no Git — risco real de commitar a chave privada por engano.

**Correção:**
```bash
rm y y.pub
ssh-keygen -t ed25519 -C "arq.convtec.2026@gmail.com"
# Desta vez: Enter puro no prompt do caminho
```

**Lição**: sempre conferir o prompt do caminho antes de confirmar — o padrão (`~/.ssh/id_ed25519`) quase sempre é a escolha certa.

### Erro 2: Confirmação de host key não aceitou "y"

Na primeira conexão (`ssh bandit`), o prompt de host key novo:
```
Are you sure you want to continue connecting (yes/no/[fingerprint])? y
Please type 'yes', 'no' or the fingerprint: yes
```

Diferente de prompts `[Y/n]` comuns em outras ferramentas, o SSH exige a palavra **completa** `yes` (ou `no`, ou o fingerprint) — abreviação não é aceita.

---

## 📌 Referência rápida

| Arquivo | Permissão | Pode publicar? |
|---|---|---|
| `~/.ssh/id_ed25519` | 600 | ❌ Nunca |
| `~/.ssh/id_ed25519.pub` | 644 | ✅ Sim |
| `~/.ssh/config` | 600 | ⚠️ Cuidado (pode conter hostnames internos) |

---

**Status**: Semana 20 concluída | Módulo 1.4 | Linguagem: PT-BR
