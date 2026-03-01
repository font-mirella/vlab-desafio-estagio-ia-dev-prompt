import os
from google import genai
from dotenv import load_dotenv

# load .env val 
load_dotenv()

# api key,  config google bible, model
chave_api = os.getenv("GEMINI_API_KEY")
cliente = genai.Client(api_key=chave_api)

# create
def gerar_explicacao_conceitual(aluno, conteudo):
    # extract info
    idade = aluno["idade"]
    nivel = aluno["nivel"]
    estilo_aprendizado = aluno["estilo_aprendizado"]
    
    # prompt
    prompt = f"""
    Você é um professor experiente em Pedagogia e foca no ensino de qualidade.
    Explique de forma educativa, didática e qualitativa o conteúdo {conteudo} para um aluno de {idade} anos e de nível {nivel}, que tem melhor rendimento de aprendizado com {estilo_aprendizado}.
    Entregue a resposta em um formato que se adeque perfeitamente ao estilo de aprendizado preferido pelo aluno
    (ex: caso seja auditivo, pense em um roteiro de podcast que indica pausas, mudanças de entonação e momentos de recapitulação para clarificar o conteúdo;
    caso seja visual, pense em formas de tornar visual, como indicando filmes, pesquisar imagens, documentários;
    caso seja leitura, foque na explicação, mas também indique obras literárias construtivas para o aluno;
    caso seja cinestésico, sugira atividades práticas, dinâmicas de movimento ou experimentos manuais).
    Pense passo a passo antes de me entregar a sua resposta, para que eu receba com qualidade.
    """

    # call ai
    resposta = cliente.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=prompt)
    
    # texto
    return resposta.text

def gerar_exemplos(aluno, conteudo):
    # extract info
    idade = aluno["idade"]
    nivel = aluno["nivel"]
    estilo_aprendizado = aluno["estilo_aprendizado"]
    
    # prompt
    prompt = f"""
    Você é um professor experiente em Pedagogia e foca no ensino de qualidade.
    Com relação ao conteúdo {conteudo}, dê exemplos práticos contextualizados para a idade {idade} e o nível {nivel},
    que tem melhor rendimento de aprendizado com {estilo_aprendizado} sobre como é possível encaixar esse assunto no cotidiano,
    para que esse aluno possa entender o que aprendeu de forma global e didática.
    Entregue a resposta em um formato que se adeque perfeitamente ao estilo de aprendizado preferido pelo aluno 
    (ex: caso seja auditivo, pense em um roteiro de podcast que indica pausas, mudanças de entonação e momentos de recapitulação para clarificar o conteúdo;
    caso seja visual, pense em formas de tornar visual, como indicando filmes, pesquisar imagens, documentários;
    caso seja leitura, foque na explicação, mas também indique obras literárias construtivas para o aluno;
    caso seja cinestésico, sugira atividades práticas, dinâmicas de movimento ou experimentos manuais).
    """

    # call ai
    resposta = cliente.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=prompt)
        
    # texto
    return resposta.text

def gerar_perguntas(aluno, conteudo):
    # extract info
    idade = aluno["idade"]
    nivel = aluno["nivel"]
    estilo_aprendizado = aluno["estilo_aprendizado"]
    
    # prompt
    prompt = f"""
    Você é um professor experiente em Pedagogia e foca no ensino de qualidade.
    Com relação ao conteúdo {conteudo}, formule perguntas de reflexão contextualizadas para estimular o pensamento crítico do aluno
    com o perfil de idade {idade} e nível {nivel}, que tem melhor rendimento de aprendizado com {estilo_aprendizado},
    de modo que seja possível ele faça suas próprias conexões em pensamento e tenha as próprias ideias e insights inteligentes
    sobre esse assunto no cotidiano.
    Entregue a resposta em um formato que se adeque perfeitamente ao estilo de aprendizado preferido pelo aluno 
    (ex: caso seja auditivo, pense em um roteiro de podcast que indica pausas, mudanças de entonação e momentos de recapitulação para clarificar o conteúdo;
    caso seja visual, pense em formas de tornar visual, como indicando filmes, pesquisar imagens, experiências;
    caso seja leitura, foque na explicação, mas também indique filósofos, pessoas de referência na área, estudiosos;
    caso seja cinestésico, tente fazer com que a pessoa se coloca no lugar da outra por meio de experiências).
    """

    # call ai
    resposta = cliente.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=prompt)
    
    # texto
    return resposta.text

def gerar_resumo(aluno, conteudo):
    # extract info
    idade = aluno["idade"]
    nivel = aluno["nivel"]
    estilo_aprendizado = aluno["estilo_aprendizado"]
    
    # prompt
    prompt = f"""
    Você é um professor experiente em Pedagogia e foca no ensino de qualidade.
    Com relação ao conteúdo {conteudo}, você precisa formular um resumo em formato visual,
    como um diagrama em ASCII para sintetizar e facilitar o aprendizado do aluno com o perfil de idade {idade} e nível {nivel},
    que tem melhor rendimento de aprendizado com {estilo_aprendizado}, para que o aluno compreenda da melhor forma possível o que lhe foi ensinado.
    """

    # call ai
    resposta = cliente.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=prompt)
    
    # texto
    return resposta.text