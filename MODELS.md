# Modelos do Smart_Secretaria

Este documento detalha os modelos (models) do projeto Smart Secretaria, suas relações, limitações e informações importantes para manutenção e desenvolvimento.

## Visão Geral do Sistema

O Smart Secretaria é um sistema de gestão escolar composto por vários módulos (apps Django):

1. **Aluno**: Gerenciamento de estudantes
2. **Turma**: Gerenciamento de turmas
3. **Professor**: Gerenciamento de professores e disciplinas
4. **Matricula**: Registro de matrículas dos alunos
5. **Calendario**: Gestão de eventos e datas importantes
6. **Documentos**: Gerenciamento de documentação escolar
7. **Usuarios**: Sistema de autenticação e autorização
8. **Logs**: Registro de atividades do sistema
9. **Core**: Funcionalidades centrais e páginas base do sistema

## Modelos e Relacionamentos

### 1. Módulo Turma

#### `Turma`

- **Atributos**:
  - `nome`: CharField - Nome da turma
  - `serie`: IntegerField - Série/ano escolar
  - `professor_responsavel`: ForeignKey para Professor - Regente da turma
  - `horario_aulas`: CharField - Horários das aulas

### 2. Módulo Aluno

#### `Aluno`

- **Atributos**:
  - `nome_completo`: CharField - Nome completo do aluno
  - `data_nascimento`: DateField - Data de nascimento
  - `nome_pai`, `nome_mae`: CharField (opcionais) - Nome dos pais
  - `cpf`, `rg`: CharField (opcionais) - Documentos de identificação
  - `endereco`: CharField - Endereço residencial
  - `telefone_contato`: CharField - Telefone de contato
  - `email`: EmailField (opcional) - Email do aluno
  - `nome_responsavel`: CharField (opcional) - Nome do responsável
  - turma: ForeignKey para Turma - Turma do aluno
  - `foto`: ImageField (opcional) - Foto do aluno

- **Validações**:
  - A turma atribuída precisa existir no banco de dados

### 3. Módulo Professor

#### `Disciplina`

- **Atributos**:
  - `nome`: CharField - Nome da disciplina

#### `Professor`

- **Atributos**:
  - `nome`: CharField - Nome completo do professor
  - `cpf`, `rg`: CharField (opcionais) - Documentos de identificação
  - `endereco`: CharField - Endereço residencial
  - `telefone_contato`: CharField - Telefone de contato
  - `email`: EmailField - Email do professor
  - `data_admissao`: DateField - Data de admissão
  - `disciplinas`: ManyToManyField para Disciplina - Disciplinas lecionadas
  - `foto`: ImageField (opcional) - Foto do professor

### 4. Módulo Matricula

#### `Matricula`

- **Atributos**:
  - aluno: ForeignKey para Aluno - Aluno matriculado
  - `data_matricula`: DateField - Data da matrícula
  - `ano_letivo`: IntegerField - Ano letivo
  - turma: ForeignKey para Turma - Turma em que o aluno está matriculado
  - `status`: CharField (choices) - Status da matrícula (ativo, pendente, cancelado, transferido)

### 5. Módulo Calendario

#### `Evento`

- **Atributos**:
  - `titulo`: CharField - Título do evento
  - `descricao`: TextField (opcional) - Descrição detalhada
  - `data_inicio`: DateTimeField - Data e hora de início
  - `data_fim`: DateTimeField - Data e hora de término
  - `tipo`: CharField (choices) - Tipo de evento (feriado, evento escolar, reunião)

### 6. Módulo Documentos

#### `Documento`

- **Atributos**:
  - aluno: ForeignKey para Aluno - Aluno relacionado ao documento
  - `tipo`: CharField (choices) - Tipo do documento (histórico, declaração, boletim, etc.)
  - `data_emissao`: DateField - Data de emissão
  - `conteudo`: TextField - Conteúdo do documento

### 7. Módulo Usuarios

#### `CustomUser` (Estende AbstractUser do Django)

- **Atributos**:
  - `tipo`: CharField (choices) - Tipo de usuário (admin, secretário, professor, aluno, responsável)
  - `groups`: ManyToManyField com related_name personalizado
  - `user_permissions`: ManyToManyField com related_name personalizado

### 8. Módulo Logs

#### `LogAtividade`

- **Atributos**:
  - `usuario`: ForeignKey para User - Usuário que realizou a ação
  - `acao`: CharField - Ação realizada
  - `data_hora`: DateTimeField (auto_now_add) - Data e hora do registro
  - `descricao_detalhada`: TextField - Descrição detalhada da ação

## Relações entre os Modelos

1. **Aluno ⟷ Turma**: Cada aluno pertence a uma turma (1:N)
2. **Turma ⟷ Professor**: Cada turma tem um professor responsável (1:N)
3. **Professor ⟷ Disciplina**: Professores podem lecionar múltiplas disciplinas (N:M)
4. **Aluno ⟷ Matricula**: Um aluno pode ter múltiplas matrículas (1:N)
5. **Turma ⟷ Matricula**: Uma matrícula está vinculada a uma turma (1:N)
6. **Aluno ⟷ Documento**: Um aluno pode ter vários documentos (1:N)

## Inconsistências no Código Atual

1. **Definição da Turma**:
   - Há inconsistência na estrutura do modelo `Turma` entre os apps turma e aluno
   - No arquivo turmas.json, os campos são `turma_nome`, `turma_ano` e `turma_periodo`
   - No modelo models.py, os campos são `nome`, `serie`, `professor_responsavel` e `horario_aulas`
   - No modelo models.py, há referências à `Turma` de outro app

2. **Estrutura do Professor**:
   - O modelo `Turma` depende de `Professor`, mas não há sincronização entre apps

## Limitações e Pontos de Atenção

1. **Validação de Dados**:
   - Implementada apenas no modelo `Aluno` para verificar se a turma existe

2. **Campos de Imagem**:
   - `foto` em Aluno e Professor requer o Pillow instalado (já está nas dependências)
   - Armazenamento configurado para pasta local, considerar usar armazenamento em nuvem para produção

3. **Autenticação e Autorização**:
   - Sistema de usuários personalizado com `CustomUser`
   - Pendente implementação de permissões específicas por tipo de usuário

4. **Logs**:
   - Sistema básico de logs, pendente automatização do registro de atividades

5. **Inconsistências de Modelos**:
   - Resolver as inconsistências entre a definição de `Turma` nos diferentes apps
   - Atualizar as referências cruzadas entre modelos para garantir consistência

## Migrações e Banco de Dados

- Usando SQLite para desenvolvimento local
- Preparado para migração para MySQL (comentado no settings.py)
- Arquivo de fixtures para turmas disponível: turmas.json (precisa ser atualizado conforme a nova estrutura)

## Recomendações para Desenvolvimento

1. **Resolver Inconsistências**:
   - Padronizar o modelo `Turma` entre todos os apps
   - Atualizar fixtures e referências existentes

2. **Implementar Validação Consistente**:
   - Adicionar validações em todos os modelos
   - Considerar usar Django Validators para regras complexas

3. **Sistema de Autenticação**:
   - Completar o sistema de login e registro
   - Implementar permissões por tipo de usuário

4. **Documentação Avançada**:
   - Considerar implementar documentação automática com Swagger/OpenAPI

5. **Testes**:
   - Ampliar cobertura de testes unitários e de integração

6. **Refatoração**:
   - Considerar refatorar para uma arquitetura API (DRF) + Frontend (React) conforme indicado no TODO.md

## Próximos Passos

1. Resolver inconsistências no modelo `Turma`
2. Implementar views para todos os módulos
3. Completar o sistema de autenticação
4. Desenvolver templates para as operações CRUD
5. Implementar validações de negócio
6. Criar dashboard para administração

---

Este documento deve ser atualizado conforme o desenvolvimento do projeto avança.
