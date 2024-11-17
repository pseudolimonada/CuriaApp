from flet import Column, MainAxisAlignment, ElevatedButton, TextField, Row

class Login_Screen(Column):
    '''
    
    '''
    
    name_textfield: TextField = TextField(label="User Name", hint_text="Insert Your User Name Here", max_length=40)
    password_textfield: TextField = TextField(label="Password", hint_text="Insert Your Password Here", max_length=40)
    credentials_column: Column
    
    login_button: ElevatedButton = ElevatedButton(text="LOGIN", scale=1.5)
    register_button: ElevatedButton = ElevatedButton(text="REGISTER", scale=1)
    login_register_column: Column
    
    def __init__(self):
        super().__init__(alignment=MainAxisAlignment.SPACE_EVENLY, expand=True)
        
        self.credentials_column = Column(
            controls=[
                Row(controls=[self.name_textfield], alignment=MainAxisAlignment.CENTER),
                Row(controls=[self.password_textfield], alignment=MainAxisAlignment.CENTER)
            ],
            alignment=MainAxisAlignment.CENTER
        )
        
        self.login_button.on_click = Login_Screen.login
        self.register_button.on_click = Login_Screen.register
        self.login_register_column = Column(
            controls=[
                Row(controls=[self.login_button], alignment=MainAxisAlignment.CENTER),
                Row(controls=[self.register_button], alignment=MainAxisAlignment.CENTER),
            ],
            alignment=MainAxisAlignment.CENTER,
            spacing=20
        )
        
        self.controls = [
            self.credentials_column,
            self.login_register_column
        ]

    def login(e):
        pass

    def register(e):
        pass