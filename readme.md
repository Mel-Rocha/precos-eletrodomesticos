## Funcionalidade v.2.0.0
- Fazer upload da planilha de lista de desejos (WishList);
- Visualização páginada da lista de desejos;
- Extração de informações relevantes (preço) de determinado produto com base em sua url;
- Criar novos produtos com base na lista de desejos;
- Informar um produto e um site opcional e extrair suas informações relevantes.

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
uvicorn main:app --port 5001
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