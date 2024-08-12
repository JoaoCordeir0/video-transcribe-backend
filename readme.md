# Manual de uso

Para executar local rode os seguintes comandos:

```shell
# Instala a lib para criar o ambiente virtual
$ python -m pip install virtualenv

# Cria o ambiente virtual chamado "venv"
$ python -m virtualenv venv

# Ativa o ambiente virtual
$ source venv/bin/activate

# Instala as dependências do projeto
$ python -m pip install -r requirements.txt

# Comando para rodar o projeto
$ uvicorn main:app

# Comando para rodar no modo debug
$ uvicorn main:app --reload

# Comando alternativo para rodar o projeto
$ python main.py
```

#
Documentação swagger:

> URL: http://127.0.0.1:8000/docs/

É possível realizar todos os teste na API pela própria documentação
