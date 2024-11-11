import pytest 
from src.core.user.domain.user import User
from src.django_project.user_app.repository import DjangoORMUserRepository
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from uuid import UUID


@pytest.fixture
def user():
    return User(
        name= "Jorge",
        username="jorginho22",
        email="jorge@ulife.com.br",
        password="jj223467"
    )

@pytest.fixture
def user_repository() -> DjangoORMUserRepository:
    return DjangoORMUserRepository()

@pytest.mark.django_db
@pytest.mark.web_service
class TestRegisterAPI():
    def test_register_user(self) -> None:
        url = "/api/register/"
        response = APIClient().post(
            url,
            data={
                "name": "Jorge",
                "username":"jorginho22",
                "email":"jorge@ulife.com.br",
                "password":"jj223467"
            }
            )

        assert response.status_code == HTTP_201_CREATED

@pytest.mark.django_db
@pytest.mark.web_service
class TestLoginAPI():
    def test_login_user(self, user: User, user_repository: DjangoORMUserRepository) -> None:
        user_repository.create(user)
        url = "/api/token/"
        response = APIClient().post(
            url,
            data={
                "email":"jorge@ulife.com.br",
                "password":"jj223467"
            }
            )

        assert response.status_code == HTTP_200_OK

#@pytest.mark.django_db
#@pytest.mark.web_service
#class TestDeleteAPI():
#    def test_delete_user(self, user: User, user_repository: DjangoORMUserRepository) -> None:
#        user_repository.create(user)
#        url = f"/api/user/{user.id}/"
#        response = APIClient().delete(url)
#
#        assert response.status_code == HTTP_204_NO_CONTENT
#
#@pytest.mark.django_db
#@pytest.mark.web_service
#class TestPartialUpdateAPI():
#    def test_update_user(self, user: User, user_repository: DjangoORMUserRepository) -> None:
#        user_repository.create(user)
#        url = f"/api/user/{user.id}/"
#        response = APIClient().patch(
#            url, 
#            data={
#                "username":"jorginho"
#            }, 
#            format="json"
#            )
#        assert response.status_code == HTTP_204_NO_CONTENT