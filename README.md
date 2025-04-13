# bagre_bet

Sistema de apostas desenvolvido com Flask
## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)

## Como executar
0. Entre na pasta do arquivo

1. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

2. Execute a aplicação:
   ```
   python app.py
   ```

3. Acesse a aplicação no navegador:
   ```
   http://localhost:5000/login
   ```
   
   Para cadastro de novo usuário:
   ```
   http://localhost:5000/cadastro
   ```

    Para ver a base de dados:
   ```
   http://localhost:5000/dados
   ```

## Observações
- No .gitignore a pasta criada contendo a base de dados está sendo excluída do GitHub, sendo assim os dados estão sendo salvos localmente
- Adicionar customização no app 