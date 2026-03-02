# 📚 EducAI — Gerador de Materiais Educativos Personalizados

Plataforma educativa que gera conteúdo didático hiper-personalizado com base no perfil do aluno, utilizando a API **Google Gemini** e técnicas avançadas de engenharia de prompt.

---

## 🎯 O que o projeto faz

Dado um perfil de aluno (nome, idade, nível de conhecimento e estilo de aprendizado) e um tópico qualquer, o sistema gera automaticamente 4 tipos de conteúdo educativo:

1. **Explicação Conceitual** — estruturada em etapas progressivas com chain-of-thought
2. **Exemplos Práticos** — contextualizados para a realidade e nível do aluno
3. **Perguntas de Reflexão** — organizadas por taxonomia de Bloom para estimular pensamento crítico
4. **Resumo Visual** — diagrama ASCII hierárquico do conteúdo

Todo conteúdo gerado é salvo em JSON e na cache, evitando chamadas desnecessárias à API.

---

## 🗂️ Estrutura do Projeto

```
educai/
├── main.py                    # Interface CLI
├── app.py                     # Interface web (Streamlit)
├── motor_prompts.py           # Motor de engenharia de prompt
├── data/
│   ├── alunos.json            # Perfis de alunos
│   └── cache_registro.json    # Registro de cache
├── samples/                   # Outputs JSON gerados
├── .env                       # Chave de API (não versionado)
├── .env.example               # Modelo de variáveis de ambiente
├── requirements.txt           # Dependências Python
├── PROMPT_ENGINEERING_NOTES.md
└── README.md
```

---

## ⚙️ Setup e Instalação

### Pré-requisitos
- Python 3.9+
- Conta no [Google AI Studio](https://aistudio.google.com/) com chave de API Gemini

### 1. Clone o repositório
```bash
git clone https://github.com/font-mirella/api-educational-prompt-engineering.git
cd api-educational-prompt-engineering
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure a chave de API
Crie um arquivo `.env` na raiz do projeto com base no `.env.example`:
```bash
cp .env.example .env
```
Edite o `.env` e insira sua chave:
```
GEMINI_API_KEY=chave
```

### 4. Execute

**Interface web (recomendado):**
```bash
streamlit run app.py
```

**Interface CLI:**
```bash
python main.py
```

---

## 👤 Perfis de Alunos

Os perfis ficam em `data/alunos.json`. Exemplo de estrutura:

```json
[
  {
    "nome": "Miguel",
    "idade": 14,
    "nivel": "iniciante",
    "estilo_aprendizado": "visual"
  },
  {
    "nome": "Ana",
    "idade": 16,
    "nivel": "intermediário",
    "estilo_aprendizado": "auditivo"
  }
]
```

**Valores aceitos:**
- `nivel`: `iniciante` | `intermediário` | `avançado`
- `estilo_aprendizado`: `visual` | `auditivo` | `leitura-escrita` | `cinestésico`

---

## 💾 Sistema de Cache

O sistema verifica automaticamente se um conteúdo já foi gerado para aquele aluno e tópico antes de chamar a API. A chave de cache é formada por `nome_aluno + conteúdo` (normalizado).

- Cache registrado em: `data/cache_registro.json`
- Outputs salvos em: `samples/<timestamp>_<nome_aluno>.json`

Se o conteúdo já existir, ele é carregado localmente sem nenhuma chamada à API.

---

## 📤 Exemplo de Output JSON

```json
{
  "aluno": "Ana",
  "idade": 14,
  "nivel": "iniciante",
  "estilo_aprendizado": "visual",
  "conteudo": "fotossíntese",
  "ensino_gerado": {
    "explicacao_conceitual": "...",
    "exemplos_praticos": "...",
    "perguntas_reflexao": "...",
    "resumo_visual": "..."
  }
}
```

---

## 🛠️ Dependências

```
google-genai
python-dotenv
streamlit
```

> Veja `requirements.txt` para versões exatas.

---

## 📋 Variáveis de Ambiente

| Variável         | Descrição                        |
|------------------|----------------------------------|
| `GEMINI_API_KEY` | Chave de API do Google Gemini    |

---

## 📝 Engenharia de Prompt

As estratégias e justificativas técnicas de cada prompt estão documentadas em detalhe no arquivo [`PROMPT_ENGINEERING_NOTES.md`](./PROMPT_ENGINEERING_NOTES.md).