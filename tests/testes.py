import unittest
import json
import os

class TestSistema(unittest.TestCase):

    def test_arquivo_alunos_existe(self):
        self.assertTrue(os.path.exists("data/alunos.json"))
    
    def test_chaves_alunos(self):
        with open("data/alunos.json", "r", encoding="utf-8") as arquivo:
            alunos = json.load(arquivo)

            chaves = ["nome", "idade", "nivel", "estilo_aprendizado"]

            for aluno in alunos: 
                for chave in chaves:
                    self.assertIn(chave, aluno)
    def test_valores_validos_nivel(self):
        with open("data/alunos.json", "r", encoding="utf-8") as arquivo:
            alunos = json.load(arquivo)
        niveis_validos = ["iniciante", "intermediário", "avançado"]
        for aluno in alunos:
            self.assertIn(aluno["nivel"], niveis_validos)

    def test_valores_validos_estilo(self):
        with open("data/alunos.json", "r", encoding="utf-8") as arquivo:
            alunos = json.load(arquivo)
        estilos_validos = ["visual", "auditivo", "cinestésico", "leitura-escrita", "leitura/escrita"]
        for aluno in alunos:
            self.assertIn(aluno["estilo_aprendizado"], estilos_validos)

    def test_chave_cache_formato(self):
        nome = "Ana"
        conteudo = "fotossíntese"
        chave = f"{nome}_{conteudo}".lower().replace(" ", "_")
        self.assertNotIn(" ", chave)
        self.assertEqual(chave, "ana_fotossíntese")

if __name__ == "__main__":
    unittest.main()