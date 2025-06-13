from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pfsw_gestao.database import get_session
from pfsw_gestao.models.models import User
from pfsw_gestao.schemas import Token
from pfsw_gestao.security import create_access_token, verify_password

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
SessionUser = Annotated[AsyncSession, Depends(get_session)]

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post("/token/{id}", response_model=Token)
async def login_for_access_token(
    id: int,
    form_data: OAuth2Form,
    session: SessionUser,
):
    user = await session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
