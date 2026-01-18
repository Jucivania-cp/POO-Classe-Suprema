# TEMA 3 – BIBLIOTECA PESSOAL DIGITAL
# Equipe: Classe Suprema
Projeto para disciplina de Programação Orientada a Objetos: desenvolver um sistema para gerenciar uma biblioteca pessoal, permitindo o cadastro de publicações, o registro de leituras, o controle de status (lido/não lido/em leitura) e a geração de relatórios sobre o acervo.

## Integrantes da Equipe

### Jucivânia Cordeiro Pinheiro:
- Criar Classes
- Implementar herança, encapsulamento, métodos especiais.
- Garantir que validações estejam corretas (ano ≥ 1500, nota 0–10, etc.).
- Implementar lógica de status (NÃO LIDO, LENDO, LIDO).
- Validar transições (não pode marcar como LIDO sem data de início).
- Regras de avaliação (só após status = LIDO).
- Implementar dados.py (JSON/SQLite).
- Funções de salvar/carregar.
- Relatórios: total de publicações, percentuais de status, média de avaliações, top 5.
- Criar CLI com subcomandos (cadastrar, listar, anotar, relatorio.)
- Garantir usabilidade (--help, exemplos).
- Escrever README.md com instruções, diagrama simples, guia de execução.
- Coordenar testes básicos com pytest.

## Principais Classes do Projeto

Class: Publicacao
- Atributos: titulo, autor, ano, genero, paginas, status, avaliacao, data_inclusao, data_inicio, data_fim  
- Métodos:  iniciarleitura(), concluirleitura(), avaliar(), adicionaranotacao()

Class: Livro (Classe filha de Publicacao)
- Atributos: isbn
- Métodos: str(), repr(), to_dict(), from_dict()

Class: Revista (Classe filha de Publicacao)
- Atributos: edicao
- Métodos: str(), repr(), to_dict(), from_dict()

Class: Anotacao
- Atributos: texto, data, trecho
- Métodos: str(), to_dict(), from_dict()

Class: Colecao
- Atributos: repositorio[]
- Métodos: adicionar(), listar(), remover(), total_publicacoes(), estatisticas_leitura(), media_avaliacoes(), top5_avaliadas()

Class: RepositorioJSON
- Métodos: salvar(publicacoes), carregar_publicacoes()
  
## Instruções 

1. **Clonar o Repositório**
   ```bash
   git clone https://github.com/Jucivania-cp/POO-Classe-Suprema.git
   cd POO-Classe-Suprema

2. **Instalar Dependências**
    ```bash
    pip install -r requirements.txt

o arquivo requirements.txt contem as dependencias para os testes com pytest 

3. **Execução**
O sistema deve ser acessado via CLI (linha de comando):

**Exemplos de uso:**

*Cadastrar uma publicação*
    ```bash
    python main.py cadastrar --tipo livro --titulo "Alice no País das Maravilhas" --autor "Lewis Carroll" --ano 1865 --genero "Fantasia" --paginas 144

*Listar Publicações*
    ```bash
    python main.py listar

*Iniciar leitura*
    ```bash
    python main.py iniciar --index 10

Esse comando serve para ser executado após o comando cadastrar sugerido acima, pois o arquivo biblioteca.json tem atualmente 10 publicações com indices de 0 a 9.

*Concluir Leitura*
    ```bash
    python main.py concluir --index 10

*Avaliar Publicação"
    ```bash
    python main.py avaliar --index 10 --nota 8

*Adicionar anotação*
    ```bash
    python main.py anotar --index 0 --texto "Minha anotação de exemplo"

*Gerar Relatórios*
    ```bash
    python main.py relatorios


4. **Testes**
Os testes foram implentados com pytest, para executar todos os testes use:
    ```bash
    pytest -q




