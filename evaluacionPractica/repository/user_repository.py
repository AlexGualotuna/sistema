from ..model.user_model import User
from .connect_db import connect
from sqlmodel import Session, select

def select_all():
    engine = connect()
    with Session(engine) as session: #cierra la sesion cuando termina la operacion con la base de datos
        query = select(User)
        return session.exec(query).all() #devuelve una lista de usuarios
    
def selec_user_by_email(email:str):
    engine = connect()
    with Session(engine) as session:
        query = select(User).where(User.username== email)
        return session.exec(query).all()
    
def create_user(user:User):
    engine = connect()
    with Session(engine) as session:
        session.add(user)
        session.commit()
        query = select(User)
        return session.exec(query).all()
    
def delete_user(email:str):
    engine = connect()
    with Session(engine) as session:
        query = select(User).where(User.username==email)
        user_delete= session.exec(query).one()
        session.delete(user_delete)
        session.commit()
        query=select(User)
        return session.exec(query).all()
    
def update_user(email: str, updated_user: User):
    engine = connect()
    with Session(engine) as session:
        # Buscar el usuario existente en la base de datos
        existing_user = session.exec(select(User).where(User.username == email)).one_or_none()
        
        if existing_user:
            # Actualizar los campos necesarios
            existing_user.name = updated_user.name
            existing_user.username = updated_user.username            
            existing_user.password = updated_user.password
            existing_user.phone = updated_user.phone
            # Agrega aquí cualquier otro campo que desees actualizar
            
            session.commit()  # Guardar los cambios en la base de datos
            session.refresh(existing_user)  # Refrescar la instancia del usuario para reflejar los cambios más recientes
            
        query = select(User)  # Devolver la lista de todos los usuarios
        return session.exec(query).all()