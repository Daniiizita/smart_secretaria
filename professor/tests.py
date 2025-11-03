from django.test import TestCase
from .models import Professor, Disciplina

class ProfessorTestCase(TestCase):
    def setUp(self):
        # Crie algumas disciplinas para usar nos testes
        self.disciplina1 = Disciplina.objects.create(nome='Matemática')
        self.disciplina2 = Disciplina.objects.create(nome='História')

    def test_criacao_professor(self):
        professor = Professor.objects.create(
            nome='João Silva',
            cpf='12345678901',
            rg='12345',
            endereco='Rua Exemplo, 123',
            telefone_contato='987654321',
            email='joao@example.com',
            data_admissao='2022-01-01',
            foto=None  # Pode deixar como None ou adicionar um caminho para uma imagem se desejar
        )

        # Adicione disciplinas ao professor
        professor.disciplinas.add(self.disciplina1, self.disciplina2)

        # Teste se o método __str__ está correto
        self.assertEqual(str(professor), 'João Silva')

        # Teste se as disciplinas foram adicionadas corretamente
        self.assertEqual(professor.disciplinas.count(), 2)

    def test_str_disciplina(self):
        disciplina = Disciplina.objects.create(nome='Biologia')
        self.assertEqual(str(disciplina), 'Biologia')

