class TestUpdateTotalUserEndpoint:
    def setup_method(self):
        global database
        database = []

    def test_update_total_user_sucess(self, client):
        # Arrange
        user_data = {
            "username": "RodrigoGomes",
            "first_name": "Rodrigo",
            "last_name": "Gomes",
            "email": "rodrigogomes@example.com",
            "password": "password@example",
            "phone_number": 1234,
        }

        client.post("/user", json=user_data)
        user_update_data = {
            "username": "RoGomes",
            "first_name": "Rodrigo",
            "last_name": "Gomes",
            "email": "rogomes@example.com",
            "password": "password@example2",
            "phone_number": 11123456789,
            "address": "Rua Teste Update",
        }

        # Act
        response = client.put("/user/1", json=user_update_data)

        # Assert
        assert response.json()["new_item"]["username"] == "RoGomes"
        assert response.json()["new_item"]["email"] == "rogomes@example.com"
        assert response.json()["new_item"]["password"] == "password@example2"
        assert response.json()["new_item"]["phone_number"] == 11123456789
        assert response.json()["new_item"]["address"] == "Rua Teste Update"
        assert response.json()["message"] == "Usuário Atualizado com sucesso"

    def test_update_total_user_fail(self, client):
        # Arrange
        user_update_data = {
            "username": "RoGomes",
            "first_name": "Rodrigo",
            "last_name": "Gomes",
            "email": "rogomes@example.com",
            "password": "password@example2",
            "phone_number": 11123456789,
            "address": "Rua Teste Update",
        }

        # Act
        response = client.put("/user/2", json=user_update_data)

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Usuário não existe na base de dados."

    def test_update_total_user_bad_request(self, client):
        # Arrange
        user_update_data = {
            "username": "RoGomes",
            "first_name": "Rodrigo",
            "last_name": "Gomes",
            "phone_number": 11123456789,
            "address": "Rua Teste Update",
        }

        # Act
        response = client.put("/user/2", json=user_update_data)

        # Assert
        assert response.status_code == 422
