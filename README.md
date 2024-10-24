# LINKHUB

## Sobre o projeto
LinkHub é um projeto desenvolvido para um trabalaho da faculdade para a matéria "Sistemas distribuidos" e foi pensado juntamente com o grupo para ser uma aplicação simples e intuitiva, que facilitasse as pessoas a compartilharem links que consideram importantes ou produtivos 

## Requisitos para o projeto:
- Python

## Como rodar o projeto?
```bash
# Cria o ambiente virtual
python -m venv venv

# Ativa o ambiente virtual
source venv/bin/activate

# Instala as dependencias
pip install -r requirements.txt

# Realiza as migrações no banco de dados
python manage.py makemigrations
python manage.py migrate

# Cria um super usuário
python manage.py createsuperuser

#Roda a aplicação
python manage.py runserver
```

