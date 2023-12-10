from django.test import TestCase
from .models import Aluno, Turma

class AlunoTestCase(TestCase):
    fixtures = ['turmas.json']

    def setUp(self):
        self.turma = Turma.objects.get(pk=1)
        self.aluno = Aluno.objects.create(
            nome_completo="João da Silva",
            data_nascimento="2000-01-01",
            endereco="Rua A, 123",
            telefone_contato="999999999",
            turma=self.turma
        )

    def test_aluno_criado_com_sucesso(self):
        self.assertEqual(self.aluno.nome_completo, "João da Silva")
        self.assertEqual(self.aluno.data_nascimento, "2000-01-01")
        self.assertEqual(self.aluno.endereco, "Rua A, 123")
        self.assertEqual(self.aluno.telefone_contato, "999999999")
        self.assertEqual(self.aluno.turma, self.turma)

    def test_aluno_sem_turma(self):
        aluno_sem_turma = Aluno.objects.create(
            nome_completo="Maria Souza",
            data_nascimento="2001-02-02",
            endereco="Rua B, 456",
            telefone_contato="888888888"
        )
        with self.assertRaises(ValueError):
            aluno_sem_turma.save()

    def test_aluno_com_turma_inexistente(self):
        turma_inexistente = Turma.objects.create(turma_nome="Turma B", turma_ano=2023, turma_periodo="Segundo Semestre")
        aluno_com_turma_inexistente = Aluno.objects.create(
            nome_completo="Pedro Santos",
            data_nascimento="2002-03-03",
            endereco="Rua C, 789",
            telefone_contato="777777777",
            turma=turma_inexistente
        )
        with self.assertRaises(ValueError):
            aluno_com_turma_inexistente.save()
