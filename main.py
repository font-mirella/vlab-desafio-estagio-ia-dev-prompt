import json 
import time
from datetime import datetime
from google.genai import errors
from motor_prompts import gerar_explicacao_conceitual
from motor_prompts import gerar_exemplos
from motor_prompts import gerar_perguntas 
from motor_prompts import gerar_resumo

# open and read
with open("data/alunos.json", "r", encoding="utf-8") as arquivo_alunos:
    lista_alunos = json.load(arquivo_alunos)

print("Qual perfil de aluno você deseja?\n")
for i in range(len(lista_alunos)):
    print(f"Nome: {lista_alunos[i]['nome']}\nIdade: {lista_alunos[i]['idade']}\nNível: {lista_alunos[i]['nivel']}\nEstilo de aprendizado: {lista_alunos[i]['estilo_aprendizado']}")
    print("-" * 30)

aluno = None

while not aluno:
    entrada = input("Digite o nome do perfil desejado ou 'novo' para cadastrar um perfil: ")

    if entrada.lower().strip() == "novo":
        print("\n" + "-"*40)
        print("➕ Deseja criar um perfil novo? Escreva aqui!")
        print("-"*40 + "\n")
        
        novo_nome = input("Nome do estudante: ").strip()
        novo_idade = int(input("Idade: "))
        novo_nivel = input("Nível de conhecimento (iniciante, intermediário, avançado): ").strip().lower()
        novo_estilo = input("Estilo de aprendizado (visual, auditivo, cinestésico, leitura/escrita): ").strip().lower()
        
        novo_perfil = {
            "nome": novo_nome,
            "idade": novo_idade,
            "nivel": novo_nivel,
            "estilo_aprendizado": novo_estilo
        }
        
        # add na lista e att
        lista_alunos.append(novo_perfil)
        with open("data/alunos.json", "w", encoding="utf-8") as arquivo_aluno_novo:
            json.dump(lista_alunos, arquivo_aluno_novo, ensure_ascii=False, indent=4)
            
        print(f"\n✅ O perfil de {novo_nome} foi salvo.")
        
        # define o aluno novo como o escolhido para continuar
        aluno = novo_perfil
    else: 

        for i in range(len(lista_alunos)):
            if entrada.lower() == lista_alunos[i]['nome'].lower():
                aluno = lista_alunos[i]
            
        if not aluno:
            print("Aluno não encontrado. Por favor, digite novamente.")

conteudo = ""

print("\nQual conteúdo você deseja estudar?")
conteudo = input("Digite o conteúdo desejado: ")

# registro de respostas existentes
try:
    with open("data/cache_registro.json", "r", encoding="utf-8") as arquivo_cache:
        registro_cache = json.load(arquivo_cache)
except (FileNotFoundError, json.JSONDecodeError): 
    # primeira execução
    registro_cache = {}

# buscar em respostas existentes
chave_busca = f"{aluno['nome']}_{conteudo}".lower().replace(" ", "_")

if chave_busca in registro_cache:
    print(f"Esse conteúdo já foi explicado para {aluno['nome']}!\nAqui estão suas explicações:\n \n")
    with open (registro_cache[chave_busca], "r", encoding="utf-8") as arquivo_existente:
        respostas_existentes = json.load(arquivo_existente)

    print("-" * 50)
    print(respostas_existentes["ensino_gerado"]["explicacao_conceitual"])
    print("-" * 50)
    print(respostas_existentes["ensino_gerado"]["exemplos_praticos"])
    print("-" * 50)
    print(respostas_existentes["ensino_gerado"]["perguntas_reflexao"])
    print("-" * 50)
    print(respostas_existentes["ensino_gerado"]["resumo_visual"])
    print("-" * 50)

else: 
    try:
        print(f"--------- Explicação conceitual sobre {conteudo} para {aluno['nome']} ---------\n")
        print("-" * 50)
        explicacao = gerar_explicacao_conceitual(aluno, conteudo)
        print(explicacao)
        print("-" * 50)
        time.sleep(4)


        print(f"--------- Exemplos práticos sobre {conteudo} para {aluno['nome']} ---------\n")
        print("-" * 50)
        exemplos = gerar_exemplos(aluno, conteudo)
        print(exemplos)
        print("-" * 50)
        time.sleep(4)

        print(f"--------- Perguntas de reflexão sobre {conteudo} para {aluno['nome']} ---------\n")
        print("-" * 50)
        perguntas = gerar_perguntas(aluno, conteudo)
        print(perguntas)
        print("-" * 50)
        time.sleep(4)

        print(f"--------- Resumo visual sobre {conteudo} para {aluno['nome']} ---------\n")
        print("-" * 50)
        resumo = gerar_resumo(aluno, conteudo)
        print(resumo)
        print("-" * 50)
        time.sleep(4)

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

        # arquivo com Timestamp
        timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
        nome_arquivo = f"samples/{timestamp}_{aluno['nome'].lower()}.json"

        # salva arquivo JSON de respostas
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(ensino_final, arquivo, ensure_ascii=False, indent=4)

        # atualiza dic com a novas respostas
        registro_cache[chave_busca] = nome_arquivo
        
        # salva o dic atualizado no arquivo de cache
        with open("data/cache_registro.json", "w", encoding="utf-8") as arquivo_cache_escrita:
            json.dump(registro_cache, arquivo_cache_escrita, ensure_ascii=False, indent=4)

    except errors.APIError as e:
        print(f"\n[ERRO] Falha na comunicação com a API. Detalhes: {e}\nPor favor, tente novamente")
        exit()
    except Exception as e:
        print(f"\n[ERRO] Ocorreu um problema inesperado: {e}")
        exit()