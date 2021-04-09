from fastapi import APIRouter, UploadFile, File
from typing import Optional
import pandas as pd

from .db import Database

database = Database()

api = APIRouter()


@api.get('/member', description='Returns members, only use ONE parameter at a time')
async def members(
    user_id: Optional[str] = None,
    phone_number: Optional[str] = None,
    client_member_id: Optional[int] = None,
    account_id: Optional[int] = None,
):
    data = database.get_user(
        user_id=user_id,
        phone_number=phone_number,
        client_member_id=client_member_id,
        account_id=account_id,
    )

    return data


@api.delete('/member', description='Deletes a user')
async def delete_member(client_member_id: int = 0):
    if database.delete_user(client_member_id=client_member_id):
        return {'status': 'user was deleted'}
    return {'status': 'something went wrong'}


@api.put('/member', description='Updates user information, client_member_id is required')
async def update_member(
    first_name: str = "",
    last_name: str = "",
    phone_number: str = "",
    client_member_id: int = 0,
    account_id: int = 0,
):
    data = database.update_user(
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        client_member_id=client_member_id,
        account_id=account_id,
    )

    return data


@api.post('/member', description='Adds a user, all fields required')
async def add_member(
    first_name: str = "",
    last_name: str = "",
    phone_number: str = "",
    client_member_id: int = 0,
    account_id: int = 0,
):
    added_user = database.add_user(
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        client_member_id=client_member_id,
        account_id=account_id,
    )
    return added_user


@api.post('/upload')
async def upload_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    if database.load_data(df):
        return {'status': 'data loaded sucessfully'}
    else:
        return {'status': 'something went wrong'}
