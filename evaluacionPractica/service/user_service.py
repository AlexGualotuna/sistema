from ..repository.user_repository import select_all, selec_user_by_email, create_user, delete_user, update_user
from ..model.user_model import User

def select_all_user_service():
    users = select_all()
    #print(users)
    return users

def select_user_by_email_service(email: str):
    if(len(email)!= 0):
        return selec_user_by_email(email)
    else:
        return select_all()
    
def create_user_service(username:str, password: str, phone: str, name: str):
    user = selec_user_by_email(username)#valido que no se guarde usuarios con el mismo email
    if(len(user)==0):
        user_save = User(username=username, password=password, phone=phone, name=name)
        return create_user(user_save)
    else:
        print('El usuario ya existe')
        raise BaseException('El usuario ya existe')
    
def delete_user_service(email:str):
    return delete_user(email=email)

#----------------------
def update_user_service(email: str, username: str, password: str, phone: str, name: str):
    # Buscar el usuario por su email
    user = selec_user_by_email(email)
    if user:
        existing_user = user[0]  # Asumimos que solo hay un usuario con ese email

        # Actualizar los campos del usuario existente
        existing_user.username = username
        existing_user.password = password
        existing_user.phone = phone
        existing_user.name = name

        # Llamar a la función del repositorio para actualizar el usuario
        return update_user(existing_user)
    else:
        print('El usuario con el email proporcionado no existe')
        raise BaseException('El usuario con el email proporcionado no existe')