```bash
uvicorn main:app --port 5001
```


````bash
aerich init -t settings.TORTOISE_ORM
````

```bash
aerich init-db
```

```bash
aerich migrate
```

````bash
aerich upgrade
````