# 🏥 Anamnese de Dor · HC-FMUSP
## Guia de Configuração e Deploy

---

## O que você vai precisar (conta gratuita em tudo)
- [ ] Conta no **GitHub** (github.com)
- [ ] Conta no **Render** (render.com)
- [ ] Conta no **Google** (para Google Sheets + Cloud Console)

---

## PASSO 1 — Criar a planilha no Google Sheets

1. Acesse **sheets.google.com** e crie uma planilha nova
2. Dê o nome: `Anamnese Dor HC-FMUSP`
3. Copie o **ID da planilha** da URL:
   ```
   https://docs.google.com/spreadsheets/d/  👉ESTE_TRECHO👈  /edit
   ```
4. Repita para criar uma segunda planilha chamada `Anamnese Dor HC-FMUSP — BACKUP`
5. Guarde os dois IDs

---

## PASSO 2 — Criar a Service Account no Google Cloud

> A Service Account é o "usuário robô" que escreve na planilha automaticamente.

1. Acesse **console.cloud.google.com**
2. Clique em **"Selecionar projeto"** → **"Novo projeto"**
   - Nome: `anamnese-dor`
   - Clique **Criar**
3. No menu esquerdo → **APIs e Serviços → Biblioteca**
4. Busque e ative **"Google Sheets API"** → Ativar
5. Busque e ative **"Google Drive API"** → Ativar
6. No menu esquerdo → **APIs e Serviços → Credenciais**
7. Clique **"+ Criar credenciais" → "Conta de serviço"**
   - Nome: `anamnese-bot`
   - Clique **Criar e continuar** → **Concluído**
8. Clique na service account criada → aba **"Chaves"**
9. **"Adicionar chave" → "Criar nova chave" → JSON → Criar**
10. Um arquivo JSON será baixado automaticamente → **guarde bem este arquivo!**

---

## PASSO 3 — Compartilhar a planilha com a Service Account

1. Abra o arquivo JSON baixado
2. Procure o campo `"client_email"` — será algo como:
   ```
   anamnese-bot@anamnese-dor.iam.gserviceaccount.com
   ```
3. Na **planilha principal** → clique em **Compartilhar**
4. Cole o e-mail da service account → permissão **Editor** → Confirmar
5. Repita para a **planilha de backup**

---

## PASSO 4 — Subir o código no GitHub

1. Crie uma conta em **github.com** se não tiver
2. Crie um **repositório novo** (pode ser privado)
   - Nome: `anamnese-dor`
3. Faça upload de todos os arquivos deste projeto
   *(ou use Git no terminal se souber)*

> ⚠️ **NUNCA suba** o arquivo `credentials.json` nem o `.env` para o GitHub!
> O `.gitignore` já os bloqueia automaticamente.

---

## PASSO 5 — Deploy no Render

1. Acesse **render.com** e crie uma conta (gratuita)
2. Clique **"New +" → "Web Service"**
3. Conecte sua conta do GitHub e selecione o repositório `anamnese-dor`
4. Configure:
   - **Name:** `anamnese-dor-hcfmusp`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
5. Vá em **"Environment Variables"** e adicione:

   | Variável | Valor |
   |---|---|
   | `GOOGLE_SHEET_ID` | ID da planilha principal |
   | `GOOGLE_BACKUP_SHEET_ID` | ID da planilha backup |
   | `GOOGLE_CREDENTIALS_JSON` | Cole TODO o conteúdo do arquivo JSON da service account |

   > Para copiar o JSON em uma linha: abra o arquivo .json, selecione tudo e cole diretamente no campo

6. Clique **"Create Web Service"**
7. Aguarde o deploy (2-5 minutos)
8. Seu site estará em: `https://anamnese-dor-hcfmusp.onrender.com`

---

## Estrutura de arquivos do projeto

```
anamnese-dor/
├── app.py                 ← Backend (FastAPI + Google Sheets + PDF)
├── requirements.txt       ← Dependências Python
├── render.yaml            ← Configuração do deploy
├── .env.example           ← Modelo das variáveis de ambiente
├── .gitignore             ← Proteção das credenciais
├── static/
│   ├── style.css          ← Estilos (tema clínico HC-FMUSP)
│   ├── body_map.js        ← Mapa corporal interativo
│   └── form.js            ← Lógica do formulário
└── templates/
    └── index.html         ← Interface completa do formulário
```

---

## Para testar localmente (opcional)

```bash
# 1. Crie um ambiente virtual
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Copie o arquivo de credenciais JSON para a raiz do projeto
cp ~/Downloads/anamnese-dor-xxxx.json credentials.json

# 4. Crie o .env
cp .env.example .env
# Edite o .env com os IDs das planilhas

# 5. Inicie o servidor
uvicorn app:app --reload

# 6. Acesse no navegador
# http://localhost:8000
```

---

## Dúvidas frequentes

**"Onde fica salvo o histórico de pacientes?"**
Na planilha Google Sheets — cada linha é uma anamnese completa.

**"O backup é automático?"**
Sim — toda vez que uma anamnese é salva, ela vai para a planilha principal E para a de backup.

**"Posso usar em tablet/celular?"**
Sim — o design é responsivo.

**"O Render gratuito desliga o servidor?"**
Sim — no plano gratuito o servidor "dorme" após 15min sem uso. Na primeira visita pode demorar ~30 segundos para acordar. Para uso clínico contínuo, recomendo o plano Starter (~$7/mês).
