import pytest
from sqlalchemy import select
from pfsw_gestao.models.models import Todo, User


def to_dict(obj, exclude=None):
    exclude = exclude or []
    return {
        k: v for k, v in vars(obj).items()
        if not k.startswith('_') and k not in exclude
    }


class TestDb:
    @pytest.mark.asyncio
    async def test_create_todo(self, session, user):
        todo = Todo(
            title='Test Todo',
            description='Test Desc',
            state='draft',
            user_id=user.id,
        )

        session.add(todo)
        await session.commit()

        todo = await session.scalar(select(Todo))

        assert to_dict(todo) == {
            'description': 'Test Desc',
            'id': todo.id,
            'state': 'draft',
            'title': 'Test Todo',
            'user_id': user.id,
        }

    @pytest.mark.asyncio
    async def test_create_user(self, session, mock_db_time):
        # Arrange
        with mock_db_time(model=User) as time:
            new_user = User(
                username="RodrigoGomes",
                first_name="Rodrigo",
                last_name="Gomes",
                email="rodrigogomes@example.com",
                password="password@example",
                phone_number="0",
                address=""
            )

            session.add(new_user)
            await session.commit()

        # act
        user = await session.scalar(select(User).where(
            User.username == "RodrigoGomes"
            )
        )

        # Assert
        assert user is not None
        user_dict = to_dict(user)
        assert user_dict == {
            "id": user.id,
            "username": "RodrigoGomes",
            "first_name": "Rodrigo",
            "last_name": "Gomes",
            "password": "password@example",
            "email": "rodrigogomes@example.com",
            "phone_number": "0",
            "address": "",
            "created_at": time,
            "todos": []
        }
        assert user.todos == []

    @pytest.mark.asyncio
    async def test_user_todo_relationship(self, session, user: User):
        todo = Todo(
            title='Test Todo',
            description='Test Desc',
            state='draft',
            user_id=user.id,
        )

        session.add(todo)
        await session.commit()
        await session.refresh(user)

        user = await session.scalar(
            select(User).where(User.id == user.id)
        )

        assert user.todos == [todo]
