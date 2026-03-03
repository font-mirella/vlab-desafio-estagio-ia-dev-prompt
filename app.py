import streamlit as st
import json
import time
from datetime import datetime
from google.genai import errors

from motor_prompts import gerar_explicacao_conceitual
from motor_prompts import gerar_exemplos
from motor_prompts import gerar_perguntas 
from motor_prompts import gerar_resumo

# configuração da página
st.set_page_config(page_title="EducAI", page_icon="📚", layout="centered")

st.title("📚 EducAI")
st.markdown("Para gerar materiais educativos hiper-personalizados com base no seu perfil ;).")
st.write("") 

# carregamento de dados
with open("data/alunos.json", "r", encoding="utf-8") as arquivo_alunos:
    lista_alunos = json.load(arquivo_alunos)

try:
    with open("data/cache_registro.json", "r", encoding="utf-8") as arquivo_cache:
        registro_cache = json.load(arquivo_cache)
except (FileNotFoundError, json.JSONDecodeError): 
    registro_cache = {}

# feature: registro de novos perfis
with st.expander("➕ Deseja criar um perfil novo? Clique aqui!"):
    with st.form("form_novo_aluno", clear_on_submit=True):
        novo_nome = st.text_input("Nome do Estudante")
        nova_idade = st.number_input("Idade", min_value=5, max_value=100, step=1)
        novo_nivel = st.selectbox("Nível de conhecimento", ["Iniciante", "Intermediário", "Avançado"])
        novo_estilo = st.selectbox("Estilo de aprendizado", ["Visual", "Auditivo", "Cinestésico", "Leitura/escrita"])
        
        botao_salvar = st.form_submit_button("Salvar Perfil", use_container_width=True)
        
        if botao_salvar:
            if not novo_nome:
                st.error("O perfil obrigatoriamente precisa de um nome!")
            else:
                novo_perfil = {
                    "nome": novo_nome.strip(),
                    "idade": int(nova_idade),
                    "nivel": novo_nivel.lower(),
                    "estilo_aprendizado": novo_estilo.lower()
                }
                
                lista_alunos.append(novo_perfil)
                with open("data/alunos.json", "w", encoding="utf-8") as f:
                    json.dump(lista_alunos, f, ensure_ascii=False, indent=4)
                
                st.success(f"✅ O perfil de {novo_nome} foi salvo.")
                time.sleep(1) 
                st.rerun()

# área de inputs
nomes_alunos = [aluno["nome"] for aluno in lista_alunos]
nome_escolhido = st.selectbox("Qual perfil você deseja usar?", nomes_alunos)

aluno = next(a for a in lista_alunos if a["nome"] == nome_escolhido)

# informações sobre o perfil
with st.container(border=True):
    st.markdown(f"**🎓 Especificações de {aluno['nome']}**")
    st.markdown(
        f"**Idade:** {aluno['idade']} anos &nbsp;&nbsp;|&nbsp;&nbsp; "
        f"**Nível:** {aluno['nivel'].title()} &nbsp;&nbsp;|&nbsp;&nbsp; "
        f"**Estilo de aprendizado:** {aluno['estilo_aprendizado'].title()}"
    )

# conteudo
conteudo = st.text_input("Qual tópico posso te ensinar hoje?", placeholder="Ex: Revolução Francesa, Python Básico...")

# main.py
if st.button("Gerar explicações ✏️", type="primary"):
    if not conteudo:
        st.error("Por favor, digite o tópico que deseja aprender hoje!")
    else:
        chave_busca = f"{aluno['nome']}_{conteudo}".lower().replace(" ", "_")
        
        # caso resposta existente
        if chave_busca in registro_cache:
            st.info(f"⚡Esse conteúdo já foi explicado para {aluno['nome']} antes! Dá uma olhada :D")
            with open(registro_cache[chave_busca], "r", encoding="utf-8") as arquivo_existente:
                respostas = json.load(arquivo_existente)
            
            explicacao = respostas["ensino_gerado"]["explicacao_conceitual"]
            exemplos = respostas["ensino_gerado"]["exemplos_praticos"]
            perguntas = respostas["ensino_gerado"]["perguntas_reflexao"]
            resumo = respostas["ensino_gerado"]["resumo_visual"]
            
        # caso resposta ainda não exista
        else:
            try:
                # animação de carregamento
                with st.spinner('Só um momento... Estou gerando seu conteúdo educativo...'):
                    explicacao = gerar_explicacao_conceitual(aluno, conteudo)
                    time.sleep(2)
                    exemplos = gerar_exemplos(aluno, conteudo)
                    time.sleep(2)
                    perguntas = gerar_perguntas(aluno, conteudo)
                    time.sleep(2)
                    resumo = gerar_resumo(aluno, conteudo)
                    
                    ensino_final = {
                        "aluno": aluno["nome"],
                        "idade": aluno["idade"],
                        "nivel": aluno["nivel"],
                        "estilo_aprendizado": aluno["estilo_aprendizado"],
                        "conteudo": conteudo,
                        "ensino_gerado": {
                            "explicacao_conceitual": explicacao,
                            "exemplos_praticos": exemplos,
                            "perguntas_reflexao": perguntas,
                            "resumo_visual": resumo
                        }
                    }

                    timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
                    nome_arquivo = f"samples/{timestamp}_{aluno['nome'].lower()}.json"

                    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
                        json.dump(ensino_final, arquivo, ensure_ascii=False, indent=4)

                    registro_cache[chave_busca] = nome_arquivo
                    with open("data/cache_registro.json", "w", encoding="utf-8") as arquivo_cache_escrita:
                        json.dump(registro_cache, arquivo_cache_escrita, ensure_ascii=False, indent=4)
                        
                st.success("Seu conteúdo acabou de ser gerado e está pronto para você :)")

            except errors.APIError as e:
                st.error(f"[ERRO] Falha na comunicação com a API. Detalhes: {e}. Por favor, tente novamente")
                st.stop() 
            except Exception as e:
                st.error(f"[ERRO] Ocorreu um problema inesperado: {e}")
                st.stop()

        # respostas em blocos 
        st.divider()
        st.subheader(f"📖 Material para {aluno['nome']}: {conteudo}")
        
        with st.expander("1️⃣ Explicação Conceitual", expanded=True):
            st.markdown(explicacao)
            
        with st.expander("2️⃣ Exemplos Práticos"):
            st.markdown(exemplos)
            
        with st.expander("3️⃣ Perguntas de Reflexão"):
            st.markdown(perguntas)
            
        with st.expander("4️⃣ Resumo Visual"):
            st.code(resumo, language="text")

        # feature: download externo
        st.divider()
        
        # para saber se vem da cache (respostas) ou da API (ensino_final)
        if 'respostas' in locals():
            json_baixar = json.dumps(respostas, ensure_ascii=False, indent=4)
        else:
            json_baixar = json.dumps(ensino_final, ensure_ascii=False, indent=4)
            
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2: 
            st.download_button(
                label="📥 Baixar Material Completo (.JSON)",
                data=json_baixar,
                file_name=f"conteudo{aluno['nome'].lower()}_{conteudo.lower().replace(' ', '_')}.json",
                mime="application/json"
            )
