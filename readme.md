## Rodando o projeto
## Dependências do projeto

```bash
python -m venv venv
```

```bash
pip install -r requirements.txt
```

## Variaveis de ambiente necessárias
configure o banco de dados e as demais váriaveis do .evn
- DATABASE_URL
- SECRET_KEY
- AUTH_TOKEN


## Inicializando o projeto
```bash
uvicorn main:app --port 3001
```

inicialização do tortoise ORM
````bash
aerich init -t settings.TORTOISE_ORM
````

## Migrações no banco de dados
Se o projeto não possuir a pasta migrations ou essa pasta estiver vazia, executar o comando a seguir:
```bash
aerich init-db
```

sempre que um modelo for alterado (campos foram acrescentados, alterados ou removidos), executar os comando a seguir 
para aplicar as mudanças no seu banco de dados.

Comando para gerar os arquivos de migração
```bash
aerich migrate
```

Aplica as migrações no banco de dados
````bash
aerich upgrade
````

## Testes e Segurança
O coverage executa todos os testes unitários do projeto usando o módulo unittest, e mede a cobertura do código, ou seja, 
ele verifica quais partes do código foram cobertas pelos testes durante a execução.
````bash
coverage run -m unittest discover
````
Geração de relatório de corbertura de testes.
````bash
coverage report -m
````
## Bibliotecas Vulneráveis
Aferição das bibliotecas vulneráveis no projeto.
````bash
pip-audit 
````