# TEMA 3 – BIBLIOTECA PESSOAL DIGITAL
# Equipe: Classe Suprema
Projeto para disciplina de Programação Orientada a Objetos: desenvolver um sistema para gerenciar uma biblioteca pessoal, permitindo o cadastro de publicações, o registro de leituras, o controle de status (lido/não lido/em leitura) e a geração de relatórios sobre o acervo.

## Integrantes da Equipe

### Aluno 1 -- Modelagem das classes bases:
- Criar Classes
- Implementar herança, encapsulamento, métodos especiais.
- Garantir que validações estejam corretas (ano ≥ 1500, nota 0–10, etc.).

### Aluno 2 -- Regras de negócio e estados:
- Implementar lógica de status (NÃO LIDO, LENDO, LIDO).
- Validar transições (não pode marcar como LIDO sem data de início).
- Regras de avaliação (só após status = LIDO).

### Aluno 3 -- Persistência e relatórios:
- Implementar dados.py (JSON/SQLite).
- Funções de salvar/carregar.
- Relatórios: total de publicações, percentuais de status, média de avaliações, top 5.

### Aluno 4 -- Interface e documentação:
- Criar subcomandos (cadastrar, listar, anotar, relatorio.)
- Garantir usabilidade (--help, exemplos).
- Escrever README.md com instruções, diagrama simples, guia de execução.
- Coordenar testes básicos com pytest.


