from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from permissoes.models import PerfilAcesso

class Command(BaseCommand):
    help = 'Configura os grupos de permissões do sistema'

    def handle(self, *args, **options):
        # Criar/obter grupos
        admin_group, _ = Group.objects.get_or_create(name='Administrador')
        secretaria_group, _ = Group.objects.get_or_create(name='Secretaria')
        professor_group, _ = Group.objects.get_or_create(name='Professor')
        aluno_group, _ = Group.objects.get_or_create(name='Aluno')
        responsavel_group, _ = Group.objects.get_or_create(name='Responsavel')
        
        # Limpar permissões existentes
        admin_group.permissions.clear()
        secretaria_group.permissions.clear()
        professor_group.permissions.clear()
        aluno_group.permissions.clear()
        responsavel_group.permissions.clear()
        
        # Obter todas as permissões
        all_permissions = Permission.objects.all()
        
        # Administrador tem todas as permissões
        admin_group.permissions.add(*all_permissions)
        
        # Permissões da Secretaria
        secretaria_permissions = Permission.objects.filter(
            content_type__app_label__in=['aluno', 'professor', 'turma', 'documento', 'matricula', 'calendario']
        ).exclude(codename__startswith='delete_')
        secretaria_group.permissions.add(*secretaria_permissions)
        
        # Permissões do Professor
        professor_permissions = Permission.objects.filter(
            content_type__app_label__in=['aluno', 'turma', 'calendario', 'documentos'],
            codename__startswith='view_'
        )
        professor_group.permissions.add(*professor_permissions)
        
        # Adicionar permissões específicas para professor
        calendario_ct = ContentType.objects.get(app_label='calendario', model='evento')
        professor_group.permissions.add(
            Permission.objects.get(content_type=calendario_ct, codename='add_evento'),
            Permission.objects.get(content_type=calendario_ct, codename='change_evento')
        )
        
        # Permissões do Aluno (somente visualização de conteúdos específicos)
        aluno_permissions = Permission.objects.filter(
            content_type__app_label__in=['aluno', 'turma', 'calendario', 'documentos'],
            codename__startswith='view_'
        )
        aluno_group.permissions.add(*aluno_permissions)
        
        # Criar ou atualizar perfis de acesso
        perfis = [
            {'nome': 'Administrador do Sistema', 'tipo': 'admin', 'grupo': admin_group, 
             'descricao': 'Acesso completo ao sistema'},
            {'nome': 'Secretaria Escolar', 'tipo': 'secretaria', 'grupo': secretaria_group, 
             'descricao': 'Gerencia alunos, professores, turmas e documentos'},
            {'nome': 'Professor', 'tipo': 'professor', 'grupo': professor_group, 
             'descricao': 'Visualiza alunos e turmas, gerencia eventos'},
            {'nome': 'Aluno', 'tipo': 'aluno', 'grupo': aluno_group, 
             'descricao': 'Visualiza informações pessoais e calendário'},
            {'nome': 'Responsável', 'tipo': 'responsavel', 'grupo': responsavel_group, 
             'descricao': 'Visualiza informações de alunos associados'}
        ]
        
        for perfil_data in perfis:
            PerfilAcesso.objects.update_or_create(
                grupo=perfil_data['grupo'],
                defaults={
                    'nome': perfil_data['nome'],
                    'tipo': perfil_data['tipo'],
                    'descricao': perfil_data['descricao']
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Permissões configuradas com sucesso!'))