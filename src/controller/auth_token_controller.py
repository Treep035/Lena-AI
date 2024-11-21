import json
import os

from model.token.auth_token import check_auth_token, generate_tokens, insert_tokens

def check_auth_token_controller():
    logged_in = check_auth_token()
    return logged_in

def generate_tokens_controller():
    auth_token, refresh_token, auth_token_expiration, refresh_token_expiration = generate_tokens()
    return auth_token, refresh_token, auth_token_expiration, refresh_token_expiration

def insert_tokens_controller(id_user, auth_token, refresh_token, auth_token_expiration, refresh_token_expiration):
    insert_tokens(id_user, auth_token, refresh_token, auth_token_expiration, refresh_token_expiration)