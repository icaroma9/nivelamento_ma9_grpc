# nivelamento_ma9_grpc

## Descrição
Projeto de aprendizado utilizando a tecnologia GRPC. 
O projeto usa um arquivo csv como fonte de dados sobre países no ano de 1960.
O servidor está implementado em server.py e em client.py há um helper que facilita a conexão.

### Funcionalidades

1) Partial countries (page_number): retorna uma lista paginada de países

2) Search country (name): retorna o primeiro país que possui a string de busca no nome. Caso não exista, apresenta um resultado vazio.

3) Get all countries (empty): retorna uma stream com os dados dos países

## Testes
1) Instale as dependências: `pip install -r requirements`
1) Execute `pytest`
