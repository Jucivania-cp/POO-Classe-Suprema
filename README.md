# TEMA 3 – BIBLIOTECA PESSOAL DIGITAL
# Equipe: Classe Suprema
Projeto para disciplina de Programação Orientada a Objetos: desenvolver um sistema para gerenciar uma biblioteca pessoal, permitindo o cadastro de publicações, o registro de leituras, o controle de status (lido/não lido/em leitura) e a geração de relatórios sobre o acervo.

## Integrantes da Equipe

### Hailton Silva Thé Neto -- Modelagem das classes bases e regras de negócio:
- Criar Classes
- Implementar herança, encapsulamento, métodos especiais.
- Garantir que validações estejam corretas (ano ≥ 1500, nota 0–10, etc.).
- Implementar lógica de status (NÃO LIDO, LENDO, LIDO).
- Validar transições (não pode marcar como LIDO sem data de início).
- Regras de avaliação (só após status = LIDO).

### Jucivânia Cordeiro Pinheiro -- Persistência e relatórios:
- Implementar dados.py (JSON/SQLite).
- Funções de salvar/carregar.
- Relatórios: total de publicações, percentuais de status, média de avaliações, top 5.

### Lucas Geremias dos Santos -- Interface e documentação:
- Criar CLI com subcomandos (cadastrar, listar, anotar, relatorio.)
- Garantir usabilidade (--help, exemplos).
- Escrever README.md com instruções, diagrama simples, guia de execução.
- Coordenar testes básicos com pytest.

## Principais Classes do Projeto

Class: Publicacao
- Atributos: titulo, autor, ano, genero, paginas, status, avaliacao, data_inclusao, data_inicio, data_fim  
- Métodos:  iniciarLeitura(), concluirLeitura(), avaliar(), adicionarAnot(), listarAnot()

Class: Livro (Classe filha de Publicacao)
- Atributos: isbn
- Métodos: str(), repr()

Class: Revista (Classe filha de Publicacao)
- Atributos: edicao
- Métodos: str(), repr()

Class: Anotacao
- Atributos: texto, data, trecho
- Métodos: str(), to_dict(), from_dict()

Class: Colecao
- Atributos: publicacoes[]
- Métodos: adicionar(), remover(), buscar_por(), filtrar_por_periodo(), listar_por_status(), validar_duplicidade(), relatorio_resumo(), relatorio_percentuais_status(), relatorio_media_avaliacoes(), relatorio_top5()

Class: EstadoLeitura (Classe abstrata)
- Métodos: iniciar(publicacao), concluir(publicacao), avaliar(publicacao, nota)
  
  Class: NaoLido (Classe Filha de EstadoLeitura)
  - Métodos: iniciar(publicacao)
  Class: Lendo (Classe Filha de EstadoLeitur)
  - Métodos: concluir(publicacao)
  Class: Lido (Classe Filha de EstadoLeitur)
  - Métodos: avaliar(publicacao, nota)

Class: PoliticasConfig
- Atributos: meta_anual, limite_leituras, genero_favorito
- Métodos: carregar(), get_meta_anual(), get_limite_leituras(), get_genero_favorito()

Class: Repositorio
- Métodos: salvar_publicacoes(publicacoes), carregar_publicacoes()
  Class: RepositorioJSON 
  - Métodos: salvar_publicacoes(), carregar_publicacoes()
  Class: RepositorioSQLite
  - Métodos: salvar_publicacoes(), carregar_publicacoes()



