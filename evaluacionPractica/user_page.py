import reflex as rx
from .model.user_model import User
from .service.user_service import select_all_user_service, select_user_by_email_service, create_user_service, delete_user_service
from .notify import notify_component
import asyncio

class UserState(rx.State):
    #states
    users:list[User]
    user_buscar: str
    user_edit: User = None
    error: str = ''

    @rx.background
    async def get_all_user(self):
        async with self:
            self.users = select_all_user_service()

    @rx.background
    async def get_user_by_email(self):
        async with self:
            self.users = select_user_by_email_service(self.user_buscar)

    async def handleNotify(self):
        async with self:
            await asyncio.sleep(2)#tiempo para que se oculte
            self.error = ''

    @rx.background
    async def create_user(self, data: dict):
        async with self:
            try:
                self.users = create_user_service(username= data['username'], password=data['password'], phone=data['phone'], name= data['name'])                
            except BaseException as be:
                print(be.args)
                self.error = be.args
        await self.handleNotify()

    def buscar_on_change(self,value: str):
        self.user_buscar = value

    @rx.background
    async def delete_user_by_email(self, email):
        async with self:
            self.users = delete_user_service(email)


    @rx.background
    async def load_user_to_edit(self, email: str):
        async with self:
            user = select_user_by_email_service(email)
            if user:
                self.user_edit = user[0]  # Asumimos que solo hay un usuario con ese email



@rx.page(route='/', title='user', on_load=UserState.get_all_user)
def user_page() -> rx.Component:
    return rx.flex(
        rx.heading('Usuarios', align='center'),
        rx.hstack(
            buscar_user_component(),
            create_user_dialog_component(),
            justify='center',
            style={'margin-top':'30px'}
        ),
        #table_user(UserState.users),
        rx.flex(  # Añadir un contenedor flex para centrar la tabla
            table_user(UserState.users),
            justify='center',  # Centrar horizontalmente
            align='center',    # Centrar verticalmente (si es necesario)
            style={"width": "100%", "margin": "20px auto"}
        ),
        rx.cond(
            UserState.error != '',
            notify_component(UserState.error, 'shield-alert', 'yellow')
        ),
        direction='column',
        style={"width": "1000px", "margin": "auto"}
    )

def table_user(list_user: list[User]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(                
                rx.table.column_header_cell('Nombre'),
                rx.table.column_header_cell('Email'),
                rx.table.column_header_cell('Teléfono'),
                rx.table.column_header_cell('Acción')
            )
        ),
        rx.table.body(
            rx.foreach(list_user, row_table)
        )
    )

def row_table(user: User) -> rx.Component:    
    return rx.table.row(
        rx.table.cell(user.name),
        rx.table.cell(user.username),
        rx.table.cell(user.phone),
        rx.table.cell(rx.hstack(
            edit_user_dialog_component(user.username),
            delete_user_dialog_component(user.username)
        ))
    )

def buscar_user_component()-> rx.Component:
    return rx.hstack(
        rx.input(placeholder='Ingrese email', on_change=UserState.buscar_on_change),
        rx.button('Buscar usuario', on_click=UserState.get_user_by_email)
    )

def create_user_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(
                placeholder='Nombre',
                name="name"                       
            ),
            rx.input(
                placeholder='Email',
                name="username"
            ),
            rx.input(
                placeholder='Contraseña',
                name="password",
                type='password'
            ),
            rx.input(
                placeholder='Teléfono',
                name="phone"
            ),
            
        ),
        on_submit=UserState.create_user,
    )

def create_user_dialog_component() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button('Crear usuario')),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title('Crear usuario'),
                create_user_form(),
                justify='center',
                align='center',
                direction='column',
            ),
            rx.flex(
                rx.dialog.close(
                rx.button('Guardar', type='submit')
                ),
                rx.dialog.close(
                    rx.button('Cancelar', color_scheme='gray', variant='soft')
                ),                
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            style={'width':'300px'}
        ),
    )

def delete_user_dialog_component(username:str) ->rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.icon('trash-2'))),
        rx.dialog.content(
            rx.dialog.description('Está seguro de querer eliminar el usuario '+ username),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        'Cancelar',
                        color_scheme='gray',
                        variant='soft'
                    ),
                ),
                rx.dialog.close(
                    rx.button('Confirmar', on_click=UserState.delete_user_by_email(username)),
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            )
        )
    )

def edit_user_dialog_component(email: str) -> rx.Component:
    # Cambiar el on_click a solo abrir el diálogo, sin cargar datos
    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.icon('pencil'), on_click=UserState.load_user_to_edit(email))),  # Cambiar a una función lambda
        rx.dialog.content(
            rx.flex(
                rx.dialog.title('Editar usuario '+email),
                create_user_form(),  # Utiliza el mismo formulario
                justify='center',
                align='center',
                direction='column',
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button('Cancelar', color_scheme='gray', variant='soft')
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            style={'width': '300px'}
        ),
    )
