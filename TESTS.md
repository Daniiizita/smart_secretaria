
## Recomendação: Testes primeiro, depois API

Recomendo implementar testes primeiro, por estas razões:

### Por que testes primeiro:

1. **Preserva o comportamento durante refatoração**: 
   - O sistema já está funcionando com SSR (Server-Side Rendering)
   - Os testes garantirão que a funcionalidade existente continue funcionando ao migrar para API

2. **Identificação de gaps**: 
   - Os testes revelarão partes do sistema que precisam de mais atenção antes da refatoração
   - Você identificará casos de uso que podem não estar óbvios na interface atual

3. **Documentação viva do comportamento**: 
   - Os testes servirão como especificação do comportamento esperado para quando desenvolver o frontend React

4. **Facilita integração contínua**: 
   - Com testes automatizados, você poderá configurar CI/CD mais facilmente depois

### Plano de implementação:

1. **Testes unitários para modelos e regras de negócio**:
   - Teste validações, métodos e relações dos modelos
   - Isso solidifica seu domínio antes de expor via API

2. **Testes de integração para os fluxos principais**:
   - Teste os fluxos completos (ex: matrícula de aluno, geração de documento)
   - Isso garante que os processos críticos estão bem definidos

3. **Implementação gradual da API**:
   - Comece convertendo um módulo por vez para DRF
   - Mantenha o sistema híbrido (parte SSR, parte API) durante a transição
   - Use os testes para validar que cada módulo convertido funciona como esperado

4. **Desenvolvimento do frontend**:
   - Com API testada, o desenvolvimento do frontend se torna mais previsível
   - Swagger/OpenAPI facilitará o desenvolvimento do frontend React

## Observações importantes:

- **Seu projeto já tem estrutura bem definida**: os modelos, views e templates existentes formam uma boa base
- **MVP.md indica maturidade do sistema**: já existem muitas funcionalidades implementadas
- **TODO.md já prevê esta transição**: você já tem um roteiro claro para API+frontend

