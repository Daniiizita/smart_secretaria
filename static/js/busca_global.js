document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('busca-rapida');
    const searchResultsContainer = document.getElementById('resultados-busca-rapida');
    const minChars = 3;
    let searchTimeout;
    
    // Função para fazer busca AJAX
    function realizarBuscaRapida() {
        const query = searchInput.value.trim();
        
        // Limpar resultados se a busca for muito curta
        if (query.length < minChars) {
            searchResultsContainer.innerHTML = '';
            searchResultsContainer.style.display = 'none';
            return;
        }
        
        // Mostrar indicador de carregamento
        searchResultsContainer.innerHTML = '<div class="loading-indicator">Buscando...</div>';
        searchResultsContainer.style.display = 'block';
        
        // Fazer requisição AJAX
        fetch(`/api/busca-rapida/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                // Processar e exibir resultados
                exibirResultadosRapidos(data, query);
            })
            .catch(error => {
                console.error('Erro na busca:', error);
                searchResultsContainer.innerHTML = '<div class="error-message">Erro ao realizar a busca</div>';
            });
    }
    
    // Função para exibir resultados da busca
    function exibirResultadosRapidos(data, query) {
        // Se não houver resultados
        if (Object.values(data).every(arr => arr.length === 0)) {
            searchResultsContainer.innerHTML = `<div class="no-results">Nenhum resultado para "${query}"</div>`;
            return;
        }
        
        // Construir HTML com resultados
        let html = '<div class="search-quick-results">';
        
        // Alunos
        if (data.alunos && data.alunos.length > 0) {
            html += '<div class="search-category"><h4>Alunos</h4>';
            data.alunos.forEach(aluno => {
                html += `<div class="search-item">
                            <a href="/aluno/${aluno.id}/">
                                ${aluno.nome_completo}
                            </a>
                        </div>`;
            });
            html += '</div>';
        }
        
        // Professores
        if (data.professores && data.professores.length > 0) {
            html += '<div class="search-category"><h4>Professores</h4>';
            data.professores.forEach(professor => {
                html += `<div class="search-item">
                            <a href="/professor/${professor.id}/">
                                ${professor.nome}
                            </a>
                        </div>`;
            });
            html += '</div>';
        }
        
        // Turmas
        if (data.turmas && data.turmas.length > 0) {
            html += '<div class="search-category"><h4>Turmas</h4>';
            data.turmas.forEach(turma => {
                html += `<div class="search-item">
                            <a href="/turma/${turma.id}/">
                                ${turma.nome}
                            </a>
                        </div>`;
            });
            html += '</div>';
        }
        
        // Link para ver todos os resultados
        html += `<div class="see-all">
                    <a href="/busca/?q=${encodeURIComponent(query)}">
                        Ver todos os resultados
                    </a>
                </div>`;
        
        html += '</div>';
        
        searchResultsContainer.innerHTML = html;
    }
    
    // Eventos de teclado no campo de busca
    searchInput.addEventListener('keyup', function() {
        // Limpar timeout anterior para evitar múltiplas requisições
        clearTimeout(searchTimeout);
        
        // Definir novo timeout para busca (300ms após parar de digitar)
        searchTimeout = setTimeout(realizarBuscaRapida, 300);
    });
    
    // Esconder resultados ao clicar fora
    document.addEventListener('click', function(event) {
        if (!searchInput.contains(event.target) && !searchResultsContainer.contains(event.target)) {
            searchResultsContainer.style.display = 'none';
        }
    });
    
    // Mostrar resultados ao clicar no campo de busca
    searchInput.addEventListener('click', function() {
        if (searchInput.value.trim().length >= minChars) {
            searchResultsContainer.style.display = 'block';
        }
    });
});