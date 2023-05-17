# def login(username: str , password: str ):
#     assistente = AssistentesRepository.find_by_login(database, login=username)
#     if not assistente or not verify_password(password, assistente.senha):
#         raise HTTPException(
#           status_code=403,
#           detail="Email ou nome de usuário incorretos"
#         )