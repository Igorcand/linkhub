# LINKHUB

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


python3 manage.py startapp room_app ./src/django_project/room_app
