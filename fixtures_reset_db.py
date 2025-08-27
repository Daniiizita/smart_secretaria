#!/usr/bin/env python
import os
import django
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smartsecretaria.settings")
django.setup()

from django.core.management import call_command
from django.contrib.auth import get_user_model

User = get_user_model()

def reset_db():
    print("🧹 Limpando o banco de dados...")
    call_command('flush', '--noinput')

def load_fixtures():
    fixtures = [
        'fixtures/disciplinas.json', 
        'fixtures/professores.json',
        'fixtures/turmas.json',
        'fixtures/alunos.json', 
        'fixtures/matriculas.json',
        'fixtures/calendarios.json',
        'fixtures/documentos.json',
        'fixtures/usuarios.json'
    ]
    
    for fixture in fixtures:
        try:
            print(f"📂 Carregando {fixture}...")
            call_command('loaddata', fixture)
            print(f"✅ {fixture} carregado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao carregar {fixture}: {str(e)}")
            print(f"Detalhes: {type(e).__name__}")
            sys.exit(1)

def create_superuser():
    username = "admin"
    password = "admin"
    email = "admin@example.com"

    if not User.objects.filter(username=username).exists():
        print("👤 Criando superusuário padrão (admin/admin)...")
        User.objects.create_superuser(username=username, email=email, password=password)
        print("✅ Superusuário criado com sucesso!")
    else:
        print("ℹ️ Superusuário já existe, não foi recriado.")

if __name__ == "__main__":
    reset_db()
    load_fixtures()
    create_superuser()
    print("\n🎉 Banco de dados resetado e populado com sucesso!")
