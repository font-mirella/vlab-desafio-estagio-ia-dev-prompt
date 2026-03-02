# 🧠 Prompt Engineering Notes
Documentação técnica de todas as estratégias de **engenharia de prompt** utilizadas no **EducAI**.

---

## 1. Visão Geral

Este projeto foi desenvolvido com foco em **engenharia de prompt** aplicada à personalização educacional.

Todos os prompts do sistema foram construídos combinando quatro técnicas principais: **persona prompting**, **context setting**, **chain-of-thought** e **output formatting**.

O objetivo foi, além de gerar conteúdo, estruturar prompts que controlassem:

* Complexidade cognitiva
* Organização da resposta
* Progressão lógica
* Adaptação ao perfil do aluno
* Consistência estrutural entre diferentes tipos de conteúdo

Cada tipo de conteúdo (explicação, exemplos, perguntas e resumo visual) foi projetado com uma arquitetura de prompt específica e intencional.

---

## 2. Estratégias Utilizadas

### Persona Prompting

Todos os prompts abrem com a definição de uma persona especializada antes de qualquer instrução. Isso ancora o modelo em um papel com autoridade e foco pedagógico, melhorando a qualidade e o tom das respostas.

**Exemplo aplicado em `gerar_explicacao_conceitual`:**
```
Você é um professor especializado em Pedagogia Adaptativa e em didática
personalizada e foca no ensino de qualidade para seus alunos.
```
Modelos de Linguagem respondem melhor quanto têm um papel claro. A persona em casa prompt dá melhor direcionamento e mais consistência pedagógica para entregar o comportamento educacional adequado.

A persona varia sutilmente entre os prompts:
- Explicação conceitual → "especialista em didática personalizada"
- Gerar exemplos → "especialista em contextualização como forma de ensino"
- Perguntas de reflexão → "especialista em desenvolvimento do pensamento crítico"
- Resumo visual → "especialista em organização visual do conhecimento"

Isso especializa o modelo para cada tipo de tarefa.

---

### Context Setting 

Cada prompt insere dinamicamente os dados reais do aluno: `{idade}`, `{nivel}` e `{estilo_aprendizado}`. Isso garante que o modelo não gere conteúdo genérico, mas sim um material personalizado.

**Exemplo:**
```
...para um aluno de {idade} anos, que tem melhor rendimento de aprendizado
quando a explicação é mais voltada para o estilo {estilo_aprendizado} e tem
nível {nivel} de conhecimento sobre tudo, ou seja, não só sobre {conteudo} em si.
```

A observação "não só sobre {conteudo} em si" é intencional: instrui o modelo a considerar o nível cognitivo **geral** do aluno ao escolher vocabulário e referências, não apenas o quanto ele sabe sobre o tema.

Essas influenciam:

* Complexidade conceitual
* Profundidade da explicação
* Tipo de exemplo
* Estrutura das perguntas
* Nível de detalhamento do resumo

**Adaptações por nível (`nivel`):**

| Nível          | Estratégia                                                      |
|----------------|-----------------------------------------------------------------|
| Iniciante      | Linguagem simples, sem jargões, recapitulação de conceitos base |
| Intermediário  | Termos técnicos introduzidos com moderação e explicados         |
| Avançado       | Profundidade teórica, conexões abstratas, robustez conceitual   |

**Adaptações por estilo de aprendizado (`estilo_aprendizado`):**

| Estilo           | Estratégia                                                              |
|------------------|-------------------------------------------------------------------------|
| Visual           | Metáforas visuais, esquemas descritos, representações gráficas          |
| Auditivo         | Roteiro narrado, estratégias de captação da atenção, tom dialogado      |
| Leitura-escrita  | Texto estruturado com títulos, subtítulos e referências bibliográficas  |
| Cinestésico      | Atividades práticas, experimentos e simulações aplicáveis               |

---

### Chain-of-Thought

Esse princípio foi aplicado principalmente na função `gerar_explicacao_conceitual`. Em vez de pedir uma explicação direta, o prompt obriga o modelo a percorrer **etapas progressivas obrigatórias** antes de entregar a resposta final. Isso melhora a coerência e a qualidade pedagógica do conteúdo gerado.

**Etapas definidas no prompt:**
```
1. Comece com uma intuição inicial simples.
2. Depois defina formalmente o conceito.
3. Em seguida quebre esse conceito em partes.
4. Depois dê uma aplicação prática.
5. Por fim, conecte com o cotidiano do aluno.
```

A técnica de **chain-of-thought** força o modelo a "pensar em voz alta" de forma estruturada, evitando saltos conceituais e garantindo que cada etapa construa sobre a anterior.

---

### Output Formatting

Todos os prompts especificam explicitamente o formato de saída esperado, reduzindo variabilidade e garantindo respostas limpas e estruturadas.

**Padrão utilizado em todos os prompts:**
```
O formato de saída deve ser organizado em títulos claros e com separação de seções.
Não mencione nenhuma das instruções na resposta final.
O aluno deve receber APENAS o conteúdo pedagógico final.
Não precisa se introduzir. Não entregue NADA nem antes nem depois do conteúdo.
```

A instrução de "não entregar nada antes nem depois" é crítica: evita que o modelo produza frases introdutórias genéricas como "Claro! Vou te ajudar com isso..." que poluem o output e prejudicam a experiência do aluno.

**Formatação específica por função:**
- `gerar_explicacao_conceitual` → etapas formatads em lista alfabética progressiva
- `gerar_perguntas` → 5 perguntas numeradas progressivamente por taxonomia de Bloom (compreensão → aplicação → análise → avaliação → transferência)
- `gerar_resumo` → exclusivamente diagrama ASCII hierárquico, sem texto adicional
- `gerar_exemplos` → mínimo de 3 exemplos, cada um com: situação, aplicação do conceito e justificativa

---

## 3. Comparação entre Versões de Prompt

### Prompt simples (sem técnicas)
```
Explique o que é {conteudo}.
```
**Resultado:** Resposta genérica, sem adaptação de nível, sem estrutura pedagógica, sem consideração do estilo de aprendizado.

### Prompt otimizado (versão atual)
Combina *persona* + *context setting* + *chain-of-thought* + *output formatting*.

**Resultado:** Conteúdo estruturado em etapas progressivas, vocabulário calibrado para o nível do aluno, formato adaptado ao estilo de aprendizado, sem texto desnecessário no output.

Nota-se que a diferença de qualidade entre as duas versões é significativa especialmente para alunos iniciantes, onde o prompt simples frequentemente gera conteúdo com jargões técnicos inadequados para o perfil.

---

## 4. Progressão Cognitiva e Arquitetura Pedagógica

### Taxonomia de Bloom Implícita

Especialmente nas perguntas de reflexão, os prompts foram estruturados para escalar progressivamente os níveis cognitivos do aluno, seguindo a lógica da Taxonomia de Bloom:

| Nível | Tipo de Pergunta    | Objetivo                                      |
|-------|---------------------|-----------------------------------------------|
| 1     | Compreensão         | Verificar entendimento básico do conceito     |
| 2     | Aplicação           | Usar o conceito em uma situação prática       |
| 3     | Análise             | Comparar, relacionar ou decompor ideias       |
| 4     | Avaliação           | Emitir julgamento com justificativa           |
| 5     | Transferência       | Conectar o conceito com outro contexto ou área|

Essa progressão impede que o aluno receba perguntas além da sua capacidade de raciocínio atual, e garante que o pensamento crítico seja desenvolvido de forma gradual e estruturada.

### Modularidade da Arquitetura Pedagógica

Cada função de geração tem um papel cognitivo distinto e complementar no sistema:

| Função                  | Foco Cognitivo                    | Papel no Aprendizado                          |
|-------------------------|-----------------------------------|-----------------------------------------------|
| `gerar_explicacao`      | Decomposição conceitual           | Construir o modelo mental do conteúdo         |
| `gerar_exemplos`        | Aplicação contextual progressiva  | Ancorar o conceito na realidade do aluno      |
| `gerar_perguntas`       | Escalada cognitiva                | Estimular reflexão e pensamento independente  |
| `gerar_resumo`          | Síntese hierárquica               | Consolidar e organizar o conhecimento adquirido|

Essa modularidade permite que cada prompt seja otimizado para seu objetivo específico, além de possibilitar o uso isolado de qualquer tipo de conteúdo conforme a necessidade pedagógica.

---

## 5. Análise Comparativa: Prompt Simples vs. Prompt Otimizado

O teste foi realizado com o mesmo tópico em ambas as versões:
- **Tópico:** Engenharia de Prompt

---

### Prompt Simples (sem técnicas)
```
Explique o que é engenharia de prompt.
```

Nenhuma informação do aluno foi fornecida. O modelo não sabe com quem está falando.

**Trecho do output gerado:**
> *"A Engenharia de Prompt (do inglês, Prompt Engineering) é a arte e a ciência de criar e refinar as instruções (prompts) que são dadas a um modelo de inteligência artificial, especialmente a modelos de linguagem grandes (LLMs) como GPT-3, GPT-4, LLaMA, Bard, Claude, etc."*

**Problemas identificados:**

| Dimensão              | Avaliação                                                                 |
|-----------------------|---------------------------------------------------------------------------|
| Vocabulário           | ❌ Usa termos como "LLMs", "bias", "temperatura", "API" sem explicação    |
| Estrutura             | ❌ Texto corrido sem progressão pedagógica, saltos conceituais abruptos   |
| Adaptação de estilo   | ❌ Nenhuma metáfora visual, nenhuma ancora na realidade de uma criança    |
| Adaptação de nível    | ❌ Conteúdo de nível intermediário/avançado para um aluno iniciante       |
| Engajamento           | ❌ Tom enciclopédico e distante, não cativa a atenção do aluno            |

---

### Prompt Otimizado (versão do projeto)

Combina **persona prompting** + **context setting** + **chain-of-thought** + **output formatting** + adaptação por nível e estilo de aprendizado.

**Trecho do output gerado:**
> *"Imagine que você tem um robô desenhista super inteligente! Ele pode desenhar qualquer coisa que você pedir. Mas tem um segredo: para ele desenhar exatamente o que está na sua cabeça, você precisa dar as melhores instruções possíveis! [...] A Engenharia de Prompt é como aprender a dar essas instruções superpoderosas..."*

**Avaliação:**

| Dimensão              | Avaliação                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Vocabulário           | ✅ Simples, sem jargões, conceitos novos sempre explicados com analogias          |
| Estrutura             | ✅ Progressão em 5 etapas: intuição → definição → partes → prática → cotidiano   |
| Adaptação de estilo   | ✅ Metáforas visuais ("caixa de tesouros", "chave dourada"), sugestões de desenho |
| Adaptação de nível    | ✅ Linguagem de 10 anos, exemplos do cotidiano infantil (lanche, jogos)           |
| Engajamento           | ✅ Tom narrativo, usa "você", cria identificação e curiosidade no aluno            |

---

### Conclusão da Comparação

A diferença mais crítica está na **ausência total de informações do aluno** no prompt simples. Sem elas, o modelo não tem como adaptar vocabulário, tom ou estrutura — e cai no padrão seguro: um texto enciclopédico, correto, mas pedagogicamente inadequado para qualquer perfil específico.

Vale notar que inserir as especificações manualmente no prompt simples (idade, nível, estilo) melhoraria o resultado — mas isso seria, por definição, fazer engenharia de prompt à mão. O que o projeto automatiza é exatamente isso: **garantir que as informações certas sempre cheguem à IA, estruturadas da forma certa, sem depender do usuário saber como formular um bom prompt.**

O output do prompt simples também foi consideravelmente mais longo e denso, o que em contexto educacional para iniciantes é contraproducente: mais conteúdo não significa melhor aprendizado.

---

## 6. Conclusão

O foco deste projeto foi demonstrar que engenharia de prompt não é apenas escrever instruções longas — é uma disciplina de design que exige intenção em cada escolha.

Os prompts do EducAI foram construídos para controlar estrutura, reduzir ambiguidade, modularizar objetivos e aplicar princípios pedagógicos reais. Cada técnica utilizada tem uma justificativa clara: a persona direciona o comportamento do modelo, o context setting personaliza o output, o chain-of-thought garante progressão lógica, e o output formatting elimina ruído desnecessário.

O resultado é um sistema que gera conteúdo educacional adaptativo, com arquitetura cognitiva definida e experiência calibrada para cada aluno.