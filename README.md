# Bem-vindo ao teu Primeiro Projeto de Código

Este é um projeto simples para te ajudar a começar com Python no teu IDE preferido.
Aqui vais escrever os teus primeiros scripts, enquanto o teu assistente de IA atua como tutor e guia.  
Vamos explorar este espaço de trabalho juntos:

---

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Conhecer o teu IDE](#conhecer-o-teu-ide)
   - [Explorar os Ficheiros do Projeto](#explorar-os-ficheiros-do-projeto)
   - [Como Executar Código](#como-executar-código)
   - [Configuração](#configuração)
     - [Início Rápido: Ativar o Ambiente](#início-rápido-ativar-o-ambiente)
     - [Configuração Inicial](#configuração-inicial)
   - [Trabalhar com Segredos](#trabalhar-com-segredos-chaves-api-passwords)
3. [Primeiro Desafio: Entender o Código](#primeiro-desafio-entender-o-código)
4. [Referência Rápida de Comandos](#referência-rápida-de-comandos)

---

## Pré-requisitos

Antes de começares a programar, certifica-te de que tens estas ferramentas instaladas no teu computador:

- [🪟 Guia de Configuração Windows](setup_windows.md)
- [🍎 Guia de Configuração Mac](setup_mac.md)

---

## Conhecer o teu IDE

O teu ecrã tem algumas áreas principais:

- **Explorer (Lado Esquerdo)**: Como um armário de ficheiros — mostra todos os ficheiros do projeto (como `main.py`). Clica num ficheiro para o abrir.
- **Editor (Centro)**: A tua bancada de trabalho. Aqui vais escrever e editar código.
- **Terminal (Em baixo)**: O teu centro de comando. Executa comandos aqui para correr os teus scripts e ver os resultados.
- **Painel de Chat IA (Lado Direito)**: O teu assistente de IA. Podes fazer perguntas sobre o teu código, conceitos ou próximos passos.  
  Lembra-te: a IA vai explicar a lógica de forma simples, não vai sobrecarregar-te com detalhes de código.

### Explorar os Ficheiros do Projeto

- **`main.py`**: Este é o ficheiro principal onde vais escrever o teu código Python. Por agora, é o único ficheiro em que precisas de te concentrar.
- **Outros Ficheiros**: Podes ver ficheiros de configuração como `.github/copilot-instructions.md` e `CLAUDE.md`, além de ficheiros como `requirements.txt` e `.vscode`. Não te preocupes com estes — existem para facilitar o ambiente e orientar o assistente de IA.

---

### Como Executar Código

Vamos executar o código que acabaste de explorar:

1. Certifica-te de que `main.py` está aberto no **Editor**.
2. Clica no **Terminal** em baixo.
3. Executa este comando:

```bash
python main.py
```

4. Deves ver esta mensagem aparecer no terminal:

```sh
Hello, world!
```

🎉 Parabéns, acabaste de executar o teu primeiro programa Python no IDE!

---

### Configuração

**Boas notícias!** Um ambiente Python já está preparado para ti. 🎉

Quando abres um terminal, podes ver `(.venv)` no início da linha, assim:

```sh
(.venv) vibecoding-02-03-68307615:$
```

Isto significa que o teu ambiente está pronto! Se vires isto, passa para [O Teu Primeiro Desafio](#primeiro-desafio-entender-o-código).

---

#### Início Rápido: Ativar o Ambiente

Se não vires `(.venv)` no teu terminal, executa este comando:

**🪟 Windows:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**🍎 Mac/Linux:**

```bash
source .venv/bin/activate
```

---

#### Configuração Inicial

Precisas de criar o teu ambiente do zero? Segue o guia completo para o teu sistema:

- **[🪟 Guia de Configuração Windows](setup_windows.md)** — Instruções completas incluindo instalação do Python
- **[🍎 Guia de Configuração Mac](setup_mac.md)** — Instruções completas incluindo instalação do Python

---

### Trabalhar com Segredos (Chaves API, Passwords)

**Importante:** Nunca coloque passwords ou chaves API diretamente no teu código!

#### Usar um Ficheiro `.env`

Quando precisares de guardar segredos (como chaves API), cria um ficheiro chamado `.env` na pasta do teu projeto:

1. Clica com o botão direito no Explorer → Novo Ficheiro → Chama-lhe `.env`
2. Adiciona os teus segredos, um por linha:

   ```sh
   API_KEY=a_tua_chave_secreta_aqui
   PASSWORD=a_tua_password_aqui
   ```

3. Pede ao teu assistente de IA: **"Usa a minha chave API do ficheiro .env"**

O teu assistente de IA vai ajudar-te a carregar e usar estes segredos corretamente no teu código.

> **💡 Dica:** O teu ficheiro `.env` já está protegido pelo `.gitignore`, por isso não será enviado para o GitHub. Os teus segredos ficam privados!

#### ⚠️ Regras Importantes

- **Nunca** escrevas segredos diretamente no teu código
- **Sempre** usa um ficheiro `.env` para passwords, chaves API e tokens
- **Pede ao teu assistente de IA** ajuda para usar variáveis de ambiente quando precisares

---

## Primeiro Desafio: Entender o Código

Antes de executar qualquer coisa, vamos pedir ao teu assistente de IA para explicar o que o código faz.

No **painel de Chat IA**, no lado direito, escreve:

```text
Podes explicar o que o código em `main.py` faz?
```

Vais receber uma explicação simples e lógica do que o programa faz, não apenas uma análise do código.

---

## App de notícias agribusiness

Esta aplicação recolhe notícias do setor de agribusiness de fontes credíveis em Portugal, União Europeia, Reino Unido e Estados Unidos.

- Gera uma página `index.html` com uma seleção semanal de até 10 notícias.
- Ordena as notícias por data de publicação.
- Evita repetir notícias que já foram publicadas em versões anteriores.
- Inclui botões de partilha por email e WhatsApp.

### Como usar

1. Instala as dependências:

```powershell
pip install -r requirements.txt
```

2. Executa o gerador de notícias:

```powershell
python main.py
```

3. Abre `index.html` no teu navegador para ver a seleção semanal.

### GitHub e deploy

- O ficheiro `index.html` fica no root do repositório.
- Para publicar no GitHub Pages, faz um push para o teu repositório e depois ativa o Pages na branch `main` com a pasta `/root`.
- Há também uma ação GitHub (`.github/workflows/weekly-news.yml`) que pode atualizar semanalmente a página.

### Atualização semanal automática

A ação está configurada para correr uma vez por semana e gerar uma nova seleção. Quando o GitHub Pages estiver ativo no teu repositório, a página será atualizada automaticamente.
