from flet import RoundedRectangleBorder, Animation, AnimationCurve, Column, MainAxisAlignment, Divider, ElevatedButton, Row, Page, ScrollMode, ButtonStyle, padding, Container, Text, AlertDialog, TextButton, TextStyle, Padding, alignment, TextAlign, FontWeight, IconButton, icons, CrossAxisAlignment, VisualDensity, Checkbox
from shared import configs, DIALOG_BG_COLOR, BUTTON_OVERLAY_COLOR, STATUS_CODES, MAIN_TEXT_COLOR, user_data, shared_vars, endpoints_urls, TESTING
from utils import Selected_Gradient, Secondary_ElevatedButton_Container, Smart_TextField, Primary_Gradient, Secondary_Gradient, Third_Gradient, present_snack_bar, get_refreshed_catalog
from datetime import datetime, timedelta
from string import Template
from typing import Optional
import requests

class Order_Screen(Column):
    '''
    Column that represents a screen for the order realization
    '''
    
    
    #############################################
    #              Initializations              #
    #############################################
    
    ###############################
    # Initializing the texts strings

    ORDER_BUTTON_TEXT: dict = {
        "English": "Order",
        "Portuguese": "Encomendar"
    }
    CONFIRM_BUTTON_TEXT: dict = {
        "English": "Confirm",
        "Portuguese": "Confirmar"
    }
    EDIT_BUTTON_TEXT: dict = {
        "English": "Edit",
        "Portuguese": "Editar"
    }
    EDIT_TEXTFIELD_TEXT: dict = {
        "English": "Quantity",
        "Portuguese": "Quantidade"
    }
    EDIT_TEXTFIELD_HINT_TEXT: dict = {
        "English": "e.g.: 23",
        "Portuguese": "ex.: 23"
    }
    EDITING_SUBTITLE_TEXT: dict = {
        "English": "Edit day: ",
        "Portuguese": "Dia em edição: "
    }
    ALERT_DIALOG_TITLE_TEXT: dict = {
        "English": "Alert Confirmation",
        "Portuguese": "Alerta de Confirmação"
    }
    ALERT_DIALOG_CONTENT_TEXT: dict = {
        "English": "By changing the day your current order will be cleared. If you still want to continue, press 'OK', otherwise press CANCEL.",
        "Portuguese": "Ao mudar o dia, a sua encomenda atual será esquecida. Se pretender continuar e mudar o dia, pressione 'OK', caso contrário pressione 'CANCELAR'."
    }
    ALERT_DIALOG_OK_TEXT: dict = {
        "English": "OK",
        "Portuguese": "OK"
    }
    ALERT_DIALOG_CANCEL_TEXT: dict = {
        "English": "CANCEL",
        "Portuguese": "CANCELAR"
    }
    DATE_CATALOG_EDIT_SUCCESS_TEXT: dict = {
        "English": "Current day edited successfully!",
        "Portuguese": "Dia atual editado com sucesso"
    }
    INTERNAL_ERROR_TEXT: dict = {
        "English": "An internal error occurred, please wait and try again...",
        "Portuguese": "Ocorreu um erro interno, por favor, espere e tente novamente..."
    }
    UNRECOGNIZED_ERROR_TEXT: dict = {
        "English": "An unexpected error occurred, please verify if your app is updated...",
        "Portuguese": "Ocorreu um erro inesperado, por favor, verifique se a sua aplicação está atualizada..."
    }
    NETWORK_ERROR_TEXT: dict = {
        "English": "Please verify your internet connection and try again...",
        "Portuguese": "Por favor verifique a sua conexão à internet e tente novamente..."
    }
    PRODUCT_SCARCITY_5_TEXT: dict = {
        "English": "\nOnly 5 or less available!",
        "Portuguese": "\nRestam 5 ou menos!"
    }
    PRODUCT_SCARCITY_1_TEXT: dict = {
        "English": "\nOnly 1 available!",
        "Portuguese": "\nResta apenas 1!"
    }
    PRODUCT_SCARCITY_0_TEXT: dict = {
        "English": "\nOut of stock to order.",
        "Portuguese": "\nEsgotado para encomenda."
    }
    WEEK_DAYS: dict = {
        "Mon": {
            "English": "Mon",
            "Portuguese": "Seg"
        },
        "Tue":{
            "English": "Tue",
            "Portuguese": "Ter"
        },
        "Wed":{
            "English": "Wed",
            "Portuguese": "Qua"
        },
        "Thu":{
            "English": "Thu",
            "Portuguese": "Qui"
        },
        "Fri":{
            "English": "Fri",
            "Portuguese": "Sex"
        },
        "Sat":{
            "English": "Sat",
            "Portuguese": "Sab"
        },
        "Sun":{
            "English": "Sun",
            "Portuguese": "Dom"
        }
    }

    ###############################
    # Initializing the page object
    __page: Page
    
    ###############################
    # Initializing catalogs and order objects
    __catalog: dict = {}
    __current_week_catalog: dict = {}
    __current_order: dict = {
        "date": str,
        "products": dict
    }
    
    ###############################
    # Initializing editing tools variables and objects
    __editing: bool = False
    __current_date_catalog_edit: dict = {}
    
    ###############################
    # Initializing help variables and objects
    __total_amount: int = 0
    __current_date: str
    __current_week_day: str
    __current_week_text: Text = Text(
        size=15,
        width=FontWeight.BOLD,
        color=MAIN_TEXT_COLOR
    )
    
    ###############################
    # Initializing title section
    __business_title: Text = Text(
        size=25,
        text_align=TextAlign.CENTER,
        width=FontWeight.BOLD,
        color=MAIN_TEXT_COLOR
    )
    
    ###############################
    # Initializing pass week section and buttons
    __pass_week_section: Container = Container(
        alignment=alignment.center
    )
    __pass_week_forward_button: IconButton
    __pass_week_backward_button: IconButton
    
    ###############################
    # Initializing days row
    __days_row: Row = Row(
        alignment=MainAxisAlignment.CENTER,
        run_spacing=5,
        wrap=True
        #scroll=ScrollMode.ADAPTIVE
    )
    
    ###############################
    # Initializing products column
    __products_column: Column = Column(
        alignment=MainAxisAlignment.START,
        scroll=ScrollMode.ADAPTIVE,
        expand=True
    )
    
    ###############################
    # Initializing main button section
    __main_button_row: Row = Row(
        alignment=MainAxisAlignment.CENTER
    )
    __order_button: Container = Container(
        opacity=0.4,
        alignment=alignment.center,
        gradient=Primary_Gradient(),
        border_radius=20,
        scale=1.6,
        animate_opacity=Animation(
            duration=200,
            curve=AnimationCurve.EASE_IN_OUT
        )
    )
    __edit_day_button: Container = Container(
        alignment=alignment.center,
        gradient=Primary_Gradient(),
        border_radius=20,
        scale=1.2
    )
    __confirm_button: Container = Container(
        alignment=alignment.center,
        gradient=Primary_Gradient(),
        border_radius=20,
        scale=1.2
    )
    
    ###############################
    # Initializing and setting up the alert dialog
    __alert = AlertDialog(
        modal=True,
        adaptive=True,
        bgcolor=DIALOG_BG_COLOR,
        title=Text(
            color=MAIN_TEXT_COLOR
        ),
        content=Text(
            color=MAIN_TEXT_COLOR
        ),
        actions_alignment=MainAxisAlignment.END
    )
    
    
    #############################################
    #                Constructor                #
    #############################################
    
    # Constructor
    def __init__(
        self,
        page: Page
    ):
        ###############################
        # Setting up the main column
        super().__init__(alignment=MainAxisAlignment.SPACE_BETWEEN, expand=True)
        
        ###############################
        # Saving the page object and setting the business title
        self.__page = page
        self.__business_title.value = "Farinha e Afeto"
        
        ###############################
        # Setting the current date / week day
        today = datetime.today()
        self.__current_date = today.strftime("%d/%m/%Y")
        self.__current_week_day = today.strftime("%A")[:3]
        
        ###############################
        # Setting up the pass week section buttons
        self.__pass_week_forward_button = IconButton(
            icon = icons.ARROW_FORWARD_IOS,
            icon_size = 12,
            icon_color=MAIN_TEXT_COLOR,
            enable_feedback=False,
            adaptive=True,
            on_click=self.__change_current_week,
            data="forward",
            style=ButtonStyle(
                padding=padding.all(0),
                visual_density=VisualDensity.COMPACT
            )
        )
        self.__pass_week_backward_button = IconButton(
            icon = icons.ARROW_BACK_IOS,
            icon_size = 12,
            icon_color=MAIN_TEXT_COLOR,
            enable_feedback=False,
            adaptive=True,
            on_click=self.__change_current_week,
            data="backward",
            style=ButtonStyle(
                padding=padding.all(0),
                visual_density=VisualDensity.COMPACT
            )
        )
        
        ###############################
        # Setting up and building the pass week section
        days_to_monday = today.weekday()
        monday = today - timedelta(days=days_to_monday)
        sunday = monday + timedelta(days=6)
        self.__current_week_text.value = f"{monday.strftime('%d/%m')} - {sunday.strftime('%d/%m')}"
        self.__pass_week_section.content = Column(
            controls=[
                Container(
                    content=self.__current_week_text,
                    padding=Padding(left=1, top=3, right=1, bottom=0),
                    alignment=alignment.center
                ),
                Container(
                    content=Row(
                        controls=[
                            self.__pass_week_backward_button,
                            self.__pass_week_forward_button
                        ],
                        alignment=MainAxisAlignment.CENTER,
                        spacing=5
                    ),
                    padding=Padding(left=1, top=0, right=1, bottom=0),
                    alignment=alignment.center
                )
            ],
            horizontal_alignment=CrossAxisAlignment.CENTER,
            alignment=MainAxisAlignment.CENTER,
            spacing=1
        )
        
        ###############################
        # Refreshing data for the current date
        self.refresh_data(update_days_row=True)
        
        ###############################
        # Setting up the order / confirm & edit button
        if user_data["is_admin"]:
            self.__confirm_button.content = ElevatedButton(
                text=self.CONFIRM_BUTTON_TEXT[configs["LANGUAGE"]],
                adaptive=True,
                on_click=self.__update_current_day,
                bgcolor="transparent",
                color="#606060",
                style=ButtonStyle(
                    padding=padding.symmetric(10, 70),
                    elevation=0,
                    overlay_color=BUTTON_OVERLAY_COLOR
                )
            )
            self.__edit_day_button.content = ElevatedButton(
                text=self.EDIT_BUTTON_TEXT[configs["LANGUAGE"]],
                adaptive=True,
                on_click=self.__edit_current_day,
                bgcolor="transparent",
                color="#606060",
                style=ButtonStyle(
                    padding=padding.symmetric(10, 70),
                    elevation=0,
                    overlay_color=BUTTON_OVERLAY_COLOR
                )
            )
            self.__main_button_row.controls = [self.__edit_day_button]
        else:
            self.__order_button.content = ElevatedButton(
                opacity=0.4,
                text=self.ORDER_BUTTON_TEXT[configs["LANGUAGE"]],
                adaptive=True,
                disabled=True,
                on_click=self.__realize_order,
                bgcolor="transparent",
                color="#606060",
                style=ButtonStyle(
                    padding=padding.symmetric(10, 50),
                    elevation=0,
                    overlay_color=BUTTON_OVERLAY_COLOR
                )
            )
            self.__main_button_row.controls = [self.__order_button]
        
        self.__alert.actions=[
            Container(
                content = ElevatedButton(
                    text=self.ALERT_DIALOG_OK_TEXT[configs["LANGUAGE"]],
                    adaptive=True,
                    on_click=self.__handle_close_dialog,
                    bgcolor="transparent",
                    color="#606060",
                    style=ButtonStyle(
                        elevation=0,
                        overlay_color=BUTTON_OVERLAY_COLOR
                    )
                ),
                gradient=Primary_Gradient(),
                border_radius=20
            ),
            Container(
                content = ElevatedButton(
                    text=self.ALERT_DIALOG_CANCEL_TEXT[configs["LANGUAGE"]],
                    adaptive=True,
                    on_click=self.__handle_close_dialog,
                    bgcolor="transparent",
                    color="#606060",
                    style=ButtonStyle(
                        elevation=0,
                        overlay_color=BUTTON_OVERLAY_COLOR
                    )
                ),
                gradient=Primary_Gradient(),
                border_radius=20
            )
        ]
        self.__alert.title.value=self.ALERT_DIALOG_TITLE_TEXT[configs["LANGUAGE"]]
        self.__alert.content.value=self.ALERT_DIALOG_CONTENT_TEXT[configs["LANGUAGE"]]
        
        ###############################
        # Final setting up the main column controls with everything
        self.__update_controls()
    
    
    #############################################
    #                Main Methods               #
    #############################################
    
    # Refresh data about the days and products by full filling the rows and columns info again
    def refresh_data(
        self,
        update_days_row: bool
    ):
        '''
        Refresh data about the days and products by full filling the rows and columns info again.
        '''
        
        ###############################
        # Calculating monday datetime of the current week
        current_date_datetime = datetime.strptime(self.__current_date, "%d/%m/%Y")
        days_to_monday = current_date_datetime.weekday()
        monday = current_date_datetime - timedelta(days=days_to_monday)
        
        ###########################################################################
        #        ------- REMOVE THIS IF CASE FOR REAL TEST !!!!!!! -------        #
        ###########################################################################
        if TESTING:
            self.__current_order["products"] = {}
            for i in range(20):
                self.__current_order["products"][f"Este é um Pao disto assim {i}"] = {
                    "product_id": f"{i}",
                    "quantity_text": Text(value="0", color=MAIN_TEXT_COLOR, weight=FontWeight.BOLD),
                    "quantity": 0,
                    "cost": 1.50
                }
            self.__current_order["date"] = self.__current_date
            if update_days_row:
                self.__fill_days_row(monday)
            self.__fill_products_column()
            return
        
        ###############################
        # Refreshing catalog then week catalog and finally update objects
        if self.__refresh_catalog():
            if self.__refresh_week_catalog(monday.strftime("%d/%m/%Y")):
                ###############################
                # Initializing/Resetting current order products
                self.__current_order["products"] = {}
                for product_id in self.__catalog.keys():
                    self.__current_order["products"][self.__catalog[product_id]["product_title"]] = {
                        "product_id": product_id,
                        "quantity_text": Text(value="0", color=MAIN_TEXT_COLOR, weight=FontWeight.BOLD),
                        "quantity": 0,
                        "cost": self.__catalog[product_id]["product_price"]
                    }
                
                ###############################
                # Updating days and products objects
                self.__current_order["date"] = self.__current_date
                if update_days_row:
                    self.__fill_days_row(monday)
                self.__fill_products_column()
    
    # Realizes an order when clicked in order_button
    def __realize_order(self, e):
        '''
        Realizes an order when clicked in order_button
        '''
        
        shared_vars["current_order"] = self.__current_order
        shared_vars["main_container"].change_screen("full_order_screen")
    
    # Changes the actual screen to the edit screen
    def __edit_current_day(self, e):
        '''
        Enters in the edit mode for the current day catalog
        '''
        if not TESTING:
            ###############################
            # Refreshing the catalog
            if not self.__refresh_catalog():
                return
        
        ###############################
        # Entering in edit mode
        self.__editing = True
        self.__current_date_catalog_edit = {}
        self.__main_button_row.controls = [self.__confirm_button]
        self.__products_column.controls.clear()
        
        ###########################################################################
        #        ------- REMOVE THIS IF CASE FOR REAL TEST !!!!!!! -------        #
        ###########################################################################

        if TESTING:
            if self.__current_week_day == "Wed" and self.__current_date == "04/12/2024":
                num = 20
            elif self.__current_week_day == "Thu" and self.__current_date == "05/12/2024":
                num = 5
            elif self.__current_week_day == "Fri" and self.__current_date == "06/12/2024":
                num = 2
            elif self.__current_week_day == "Wed":
                num = 10
            elif self.__current_week_day == "Thu":
                num = 1
            elif self.__current_week_day == "Fri":
                num = 8
            else:
                num = 0

            state = False
            for i in range(num):
                new_container = self.__create_new_product_container(f"Este é um Pao disto assim {i}", i, str(i+20), state)
                self.__products_column.controls.append(new_container)
            
            self.__update_controls()
            return
        
        ###############################
        # Creating and adding products containers according to the products in the catalog
        for product_id in self.__catalog.keys():
            quantity = 0
            state = False
            
            if product_id in self.__current_week_catalog[self.__current_week_day].keys():
                quantity = self.__current_week_catalog[self.__current_week_day][product_id]["quantity"]
                state = True
                
            self.__current_date_catalog_edit[product_id] = {
                "quantity": quantity,
                "state": state
            }
            
            new_container = self.__create_new_product_container(self.__catalog[product_id]["product_title"], product_id, str(quantity), state)
            self.__products_column.controls.append(new_container)
        
        ###############################
        # Updating the screen to the new format
        self.__update_controls()
    
    # Updates the current day after the edit
    def __update_current_day(self, e):
        '''
        Updates the current day after the edit
        '''
        
        ###########################################################################
        #        ------- REMOVE THIS IF CASE FOR REAL TEST !!!!!!! -------        #
        ###########################################################################
        if TESTING:
            self.__editing = False
            self.__main_button_row.controls = [self.__edit_day_button]
            
            self.refresh_data(update_days_row=True)
            self.__update_controls()
        
        ###############################
        # Setting up all requirements for the request
        new_date_catalog = {
            "catalog_date": self.__current_date,
            "catalog_products": {}
        }
        for product_id in self.__current_date_catalog_edit.keys():
            if self.__current_date_catalog_edit[product_id]["state"]:
                new_date_catalog[product_id] = self.__current_date_catalog_edit[product_id]["quantity"]
        
        headers = {
            "Authorization": f"{user_data["token"]}"
        }

        url_template = Template(endpoints_urls["EDIT_CURRENT_DAY"])
        get_catalog_url = url_template.safe_substitute(business_id=shared_vars["current_business"]["id"])
        
        ###############################
        # Making and processing the request
        try:
            # Sending request and getting response
            response = requests.post(get_catalog_url, headers=headers, json=new_date_catalog)
            
            # Check the response
            if response.status_code == STATUS_CODES["SUCCESS"]:
                present_snack_bar(self.__page, self.DATE_CATALOG_EDIT_SUCCESS_TEXT[configs["LANGUAGE"]], "Green")
                
            elif response.status_code >= STATUS_CODES["INTERNAL_ERROR"]:
                present_snack_bar(self.__page, self.INTERNAL_ERROR_TEXT[configs["LANGUAGE"]], "Red")
            else:
                present_snack_bar(self.__page, self.UNRECOGNIZED_ERROR_TEXT[configs["LANGUAGE"]], "Red")
        except requests.exceptions.RequestException as e:
            # Handle network-related errors
            present_snack_bar(self.__page, self.NETWORK_ERROR_TEXT[configs["LANGUAGE"]], "Red")
        
        ###############################
        # Exits the edit mode and updates screen
        self.__editing = False
        self.__main_button_row.controls = [self.__edit_day_button]
        self.refresh_data(update_days_row=True)
        self.__update_controls()

    
    #############################################
    #             Refreshing Methods            #
    #############################################
    
    # Refreshes the catalog for the actual business and save it in self.__catalog
    def __refresh_catalog(self):
        '''
        Refreshes the catalog for the actual business and save it in self.__catalog
        If any error occurs return false, otherwise return true
        Catalog Structure:
        {
            "product_id1": {
                "image_url":"(opt)",
                "product_title":"...",
                "product_description":"...",
                "product_price":"...",
            },
            "product_id2": {
                ...
            },
        }
        '''
        catalog = get_refreshed_catalog(self.__page)
        if catalog is not None:
            self.__catalog = catalog
            return True
        
        return False
        
    # Refreshes the week catalog for the actual business and save it in self.__current_week_catalog
    def __refresh_week_catalog(
        self,
        monday_date:str
    ):
        '''
        Refreshes the week catalog for the actual business and save it in self.__current_week_catalog
        If any error occurs return false, otherwise return true
        Week Catalog Structure:  (product_scarcity can be 5, 1, 0 or null, the null is in case there are more then 5)
        FOR CLIENT:
        {
            "Mon": {"product_idX": product_scarcity, "product_idX": product_scarcity, ...},
            "Tue": {"product_idX": product_scarcity, "product_idX": product_scarcity, ...},
            "Wed": {"product_idX": product_scarcity, "product_idX": product_scarcity, ...},
            "Thu": {"product_idX": product_scarcity, "product_idX": product_scarcity, ...},
            "Fri": {"product_idX": product_scarcity, "product_idX": product_scarcity, ...},
            "Sat": {"product_idX": product_scarcity, "product_idX": product_scarcity, ...},
            "Sun": {"product_idX": product_scarcity, "product_idX": product_scarcity, ...}
        }
        FOR ADMIN:
        {
            "Mon": {"product_id":"...", "product_quantity_total": 5, "product_quantity_sold": 5},
            "Tue": {"product_id":"...", "product_quantity_total": 5, "product_quantity_sold": 5},
            "Wed": {"product_id":"...", "product_quantity_total": 5, "product_quantity_sold": 5},
            "Thu": {"product_id":"...", "product_quantity_total": 5, "product_quantity_sold": 5},
            "Fri": {"product_id":"...", "product_quantity_total": 5, "product_quantity_sold": 5},
            "Sat": {"product_id":"...", "product_quantity_total": 5, "product_quantity_sold": 5},
            "Sun": {"product_id":"...", "product_quantity_total": 5, "product_quantity_sold": 5}
        }
        '''
        
        ###############################
        # Setting up all requirements for the request
        headers = {
            "Authorization": f"{user_data["token"]}"
        }
        params = {
            "monday_date": monday_date,
        }
        url_template = Template(endpoints_urls["GET_CATALOG"])
        get_catalog_url = url_template.safe_substitute(business_id=shared_vars["current_business"]["id"])
        
        ###############################
        # Making and processing the request
        try:
            # Sending request and getting response
            response = requests.get(get_catalog_url, headers=headers, params=params)
            
            # Check the response
            if response.status_code == STATUS_CODES["SUCCESS"]:
                # Saving the catalog for each day
                response_data = response.json()
                self.__current_week_catalog["Mon"] = response_data.get("Mon", [])
                self.__current_week_catalog["Tue"] = response_data.get("Tue", [])
                self.__current_week_catalog["Wed"] = response_data.get("Wed", [])
                self.__current_week_catalog["Thu"] = response_data.get("Thu", [])
                self.__current_week_catalog["Fri"] = response_data.get("Fri", [])
                self.__current_week_catalog["Sat"] = response_data.get("Sat", [])
                self.__current_week_catalog["Sun"] = response_data.get("Sun", [])
                return True
                
            elif response.status_code >= STATUS_CODES["INTERNAL_ERROR"]:
                present_snack_bar(self.__page, self.INTERNAL_ERROR_TEXT[configs["LANGUAGE"]], "Red")
            else:
                present_snack_bar(self.__page, self.UNRECOGNIZED_ERROR_TEXT[configs["LANGUAGE"]], "Red")
        except requests.exceptions.RequestException as e:
            # Handle network-related errors
            present_snack_bar(self.__page, self.NETWORK_ERROR_TEXT[configs["LANGUAGE"]], "Red")
        
        return False
    
    # Clears the days row and refill it with new data
    def __fill_days_row(
        self,
        monday: datetime
    ):
        '''
        Clears the days row and refill it with new data from DB.
        '''
        
        self.__days_row.controls.clear()
        
        self.__create_new_date_button("Mon", monday.strftime("%d/%m/%Y"))
        self.__create_new_date_button("Tue", (monday + timedelta(days=1)).strftime("%d/%m/%Y"))
        self.__create_new_date_button("Wed", (monday + timedelta(days=2)).strftime("%d/%m/%Y"))
        self.__create_new_date_button("Thu", (monday + timedelta(days=3)).strftime("%d/%m/%Y"))
        self.__create_new_date_button("Fri", (monday + timedelta(days=4)).strftime("%d/%m/%Y"))
        self.__create_new_date_button("Sat", (monday + timedelta(days=5)).strftime("%d/%m/%Y"))
        self.__create_new_date_button("Sun", (monday + timedelta(days=6)).strftime("%d/%m/%Y"))
        
    # Clears the products column and refill it with new data from DB for a specific date
    def __fill_products_column(self):
        '''
        Clears the products column and refill it with new data from DB for a specific date.
        '''
        
        self.__products_column.controls.clear()
        
        ###########################################################################
        #        ------- REMOVE THIS IF CASE FOR REAL TEST !!!!!!! -------        #
        ###########################################################################
        if TESTING:
            if self.__current_week_day == "Wed" and self.__current_date == "04/12/2024":
                num = 20
                product_scarcity = None
            elif self.__current_week_day == "Thu" and self.__current_date == "05/12/2024":
                num = 5
                product_scarcity = 1
            elif self.__current_week_day == "Fri" and self.__current_date == "06/12/2024":
                num = 2
                product_scarcity = 0
            elif self.__current_week_day == "Wed":
                num = 10
                product_scarcity = 5
            elif self.__current_week_day == "Thu":
                num = 1
                product_scarcity = None
            elif self.__current_week_day == "Fri":
                num = 8
                product_scarcity = 1
            else:
                num = 0
            for i in range(num):
                if user_data["is_admin"]:
                    product_row = self.__create_new_product_row_manager(f"Este é um Pao disto assim {i}", self.__current_order["products"][f"Este é um Pao disto assim {i}"]["cost"], i+10, i+20)
                else:
                    product_row = self.__create_new_product_row_client("1", f"Este é um Pao disto assim {i}", self.__current_order["products"][f"Este é um Pao disto assim {i}"]["cost"], product_scarcity)
                self.__products_column.controls.append(product_row)
            return
        
        ###############################
        # Adding products rows according to the products in the catalog day
        for product_id in self.__current_week_catalog[self.__current_week_day].keys():
            if user_data["is_admin"]:
                product_quantity_sold = self.__current_week_catalog[self.__current_week_day][product_id]["product_quantity_sold"]
                product_quantity_total = self.__current_week_catalog[self.__current_week_day][product_id]["product_quantity_total"]
                product_row = self.__create_new_product_row_manager(self.__catalog[product_id]["product_title"], self.__catalog[product_id]["product_price"], product_quantity_sold, product_quantity_total)
            else:
                product_scarcity = self.__current_week_catalog[self.__current_week_day][product_id]
                product_row = self.__create_new_product_row_client(product_id, self.__catalog[product_id]["product_title"], self.__catalog[product_id]["product_price"], product_scarcity)
            
            self.__products_column.controls.append(product_row)
        
    
    #############################################
    #          Data Management Methods          #
    #############################################

    # Changes the current week
    def __change_current_week(self, e):
        '''
        Changes the current week
        '''
        
        ###############################
        # Checking the current total amount and changing the week or 
        # popping up an alert dialog according to that
        if self.__total_amount > 0:
            self.__alert.actions[0].content.data=e.control.data
            self.__page.open(self.__alert)
        else:        
            current_date_datetime = datetime.strptime(self.__current_date, "%d/%m/%Y")
            if e.control.data == "forward":
                current_date_datetime += timedelta(days=7)
            elif e.control.data == "backward":
                current_date_datetime -= timedelta(days=7)
            
            days_to_monday = current_date_datetime.weekday()
            monday = current_date_datetime - timedelta(days=days_to_monday)
            sunday = monday + timedelta(days=6)
            self.__current_date = current_date_datetime.strftime("%d/%m/%Y")
            self.__current_week_text.value = f"{monday.strftime('%d/%m')} - {sunday.strftime('%d/%m')}"
            self.__current_order["date"] = self.__current_date
            
            self.refresh_data(True)
            self.__page.update()
    
    # Changes the products list according to the date selected
    def __change_date_product_list(self, e):
        '''
        Changes the products list according to the date selected.
        '''
        
        if e.control.data[1] != self.__current_date:
            if self.__total_amount > 0:
                self.__alert.actions[0].content.data=e.control.data
                self.__page.open(self.__alert)
            else:
                current_date_datetime = datetime.strptime(self.__current_date, "%d/%m/%Y")
                days_to_monday = current_date_datetime.weekday()
                self.__days_row.controls[days_to_monday].gradient=Primary_Gradient()
                
                self.__current_date = e.control.data[1]
                self.__current_week_day = e.control.data[0]
                
                new_current_date_datetime = datetime.strptime(self.__current_date, "%d/%m/%Y")
                days_to_monday = new_current_date_datetime.weekday()
                self.__days_row.controls[days_to_monday].gradient=Selected_Gradient()
                
                self.__current_order["date"] = self.__current_date
                self.__fill_products_column()
                self.__page.update()
    
    # Changes the product amount in the current order list.
    def __change_product_amount(self, e):
        '''
        Changes the product amount in the current order list.
        '''
        
        operation = e.control.data[0]
        product_name = e.control.data[1]
        product_id = e.control.data[2]
        
        ###############################
        # Checking if the pressed button was the '+' or '-'
        # and changing quantities according to that
        if operation == "+":
            testing = True
            if testing:
                product_scarcity = None
            else:
                product_scarcity = self.__current_week_catalog[self.__current_week_day][product_id]
            
            increment = True
            if product_scarcity is not None:
                if self.__current_order["products"][product_name]["quantity"] >= product_scarcity:
                    increment = False
            if increment:
                self.__current_order["products"][product_name]["quantity"] += 1
                self.__total_amount += 1
                if self.__total_amount > 0:
                    self.__order_button.content.disabled = False
                    self.__order_button.content.opacity = 1
                    self.__order_button.opacity = 1
        elif operation == "-":
            if self.__current_order["products"][product_name]["quantity"] > 0:
                self.__current_order["products"][product_name]["quantity"] -= 1
                self.__total_amount -= 1
                if self.__total_amount <= 0:
                    self.__order_button.content.disabled = True
                    self.__order_button.content.opacity = 0.4
                    self.__order_button.opacity = 0.4
                    
        self.__current_order["products"][product_name]["quantity_text"].value = f"{self.__current_order["products"][product_name]["quantity"]}"
        self.__page.update()
    
    # Edits the product state by removing or adding it to the current week catalog
    def __edit_product_state(self, e):
        '''
        Edits the product state by removing or adding it to the current week catalog
        '''
        
        state = e.control.value
        product_id = e.control.data
        self.__current_date_catalog_edit[product_id]["state"] = state
        self.__page.update()
        
    # Edits the current week catalog with the new defined product quantity
    def __edit_product_amount(self, e):
        '''
        Edits the current week catalog with the new defined product quantity
        '''
        
        product_id = e.control.data
        if e.control.value == "":
            self.__current_date_catalog_edit[product_id]["quantity"] = 0
        else:
            self.__current_date_catalog_edit[product_id]["quantity"] = int(e.control.value)
    
    # Handles the close of the dialog alert
    def __handle_close_dialog(self, e):
        '''
        Handles the close of the dialog alert.
        '''
        
        ###############################
        # Closing the alert
        self.__page.close(self.__alert)
        
        ###############################
        # Verifying if the OK button got clicked and if it is about
        # to change just the day or the whole week
        if e.control.text == self.ALERT_DIALOG_OK_TEXT[configs["LANGUAGE"]]:
            current_date_datetime = datetime.strptime(self.__current_date, "%d/%m/%Y")
                
            if e.control.data in ["forward", "backward"]:
                if e.control.data == "forward":
                    current_date_datetime += timedelta(days=7)
                elif e.control.data == "backward":
                    current_date_datetime -= timedelta(days=7)
                
                ###############################
                # Updating the current date and week
                days_to_monday = current_date_datetime.weekday()
                monday = current_date_datetime - timedelta(days=days_to_monday)
                sunday = monday + timedelta(days=6)
                self.__current_date = current_date_datetime.strftime("%d/%m/%Y")
                self.__current_week_text.value = f"{monday.strftime('%d/%m')} - {sunday.strftime('%d/%m')}"
                
                ###############################
                # Resetting the current order and refreshing all data
                self.reset_current_order()
                self.__page.update()
                self.refresh_data(True)
            else:
                ###############################
                # Updating the current date and week day
                days_to_monday = current_date_datetime.weekday()
                self.__days_row.controls[days_to_monday].gradient=Primary_Gradient()
                
                self.__current_date = e.control.data[1]
                self.__current_week_day = e.control.data[0]
                
                new_current_date_datetime = datetime.strptime(self.__current_date, "%d/%m/%Y")
                days_to_monday = new_current_date_datetime.weekday()
                self.__days_row.controls[days_to_monday].gradient=Selected_Gradient()
                
                ###############################
                # Resetting the current order and refilling the products column
                self.reset_current_order()
                self.__fill_products_column()
            
        self.__page.update()
    
    
    #############################################
    #                Help Methods               #
    #############################################
    
    # Creates and returns a button for a respective date
    def __create_new_date_button(
        self,
        week_day: str,
        date: str
    ):
        '''
        Creates and appends to the days list a button for a respective date.
        '''
        
        if date == self.__current_date:
            gradient = Selected_Gradient()
        else:
            gradient = Primary_Gradient()
            
        self.__days_row.controls.append(
            Container(
                content=ElevatedButton(
                    text=self.WEEK_DAYS[week_day][configs["LANGUAGE"]],
                    adaptive=True,
                    bgcolor="transparent",
                    color="#606060",
                    on_click=self.__change_date_product_list,
                    data=(week_day, date),
                    width=60,
                    height=30,
                    style=ButtonStyle(
                        elevation=0,
                        overlay_color="#fff791",
                        padding=Padding(left=2, top=1, right=2, bottom=1),
                        text_style=TextStyle(size=14)
                    )
                ),
                width=60,
                height=30,
                gradient=gradient,
                border_radius=20,
                alignment=alignment.center
            )
        )
    
    # Creates and returns a row with the information about the product and two buttons ('+' and '-')
    def __create_new_product_row_client(
        self,
        product_id: str,
        product_name: str,
        product_cost: float,
        product_scarcity: int = None
    ):
        '''
        Creates and returns a row with the information about the product and two buttons ('+' and '-').
        '''
        
        ###############################
        # Checking and setting up the product scarcity
        match product_scarcity:
            case None:
                product_scarcity_text = ""
            case 5:
                product_scarcity_text = self.PRODUCT_SCARCITY_5_TEXT[configs["LANGUAGE"]]
            case 1:
                product_scarcity_text = self.PRODUCT_SCARCITY_1_TEXT[configs["LANGUAGE"]]
            case 0:
                product_scarcity_text = self.PRODUCT_SCARCITY_0_TEXT[configs["LANGUAGE"]]
        
        return Container (
            content=Row(
                controls=[
                    Container(
                        content=Row(
                            controls=[
                                Container(
                                    content=Text(
                                        value= f"{product_name}{product_scarcity_text}",
                                        color=MAIN_TEXT_COLOR
                                    ),
                                    padding=padding.only(left=5, right=5),
                                    expand=True
                                ),
                                Container(
                                    content=Text(
                                        value=f"{product_cost:.2f}€",
                                        color=MAIN_TEXT_COLOR
                                    ),
                                    padding=padding.only(left=5, right=5),
                                )
                            ],
                            alignment=MainAxisAlignment.SPACE_AROUND
                        ),
                        height=80,
                        expand=True,
                        gradient = Third_Gradient(),
                        border_radius=20,
                        alignment=alignment.center
                    ),
                    Row(
                        controls=[
                            Secondary_ElevatedButton_Container(
                                text="-",
                                on_click=self.__change_product_amount,
                                data=("-", product_name, product_id),
                                width=40,
                                height=40
                            ),
                            self.__current_order["products"][product_name]["quantity_text"],
                            Secondary_ElevatedButton_Container(
                                text="+",
                                on_click=self.__change_product_amount,
                                data=("+", product_name, product_id),
                                width=40,
                                height=40
                            ),
                        ],
                        alignment=MainAxisAlignment.START,
                        spacing=10
                    )
                ]
            ),
            alignment=alignment.center,
            padding=padding.only(left=10, right=10)
        )
    
    # Creates and returns a row with the information about the product
    def __create_new_product_row_manager(
        self,
        product_name: str,
        product_cost: float,
        product_quantity_sold: int,
        product_quantity_total: int
    ):
        '''
        Creates and returns a row with the information about the product
        '''
        
        return Container(
            content=Row(
                controls=[
                    Container(
                        content=Row(
                            controls=[
                                Container(
                                    content=Text(
                                        value = f"{product_name}",
                                        color = MAIN_TEXT_COLOR
                                    ),
                                    padding=padding.only(left=5, right=5),
                                    expand=True
                                ),
                                Container(
                                    content=Text(
                                        value = f"{product_quantity_sold}/{product_quantity_total}",
                                        color = MAIN_TEXT_COLOR
                                    ),
                                    padding=padding.only(left=5, right=5),
                                ),
                                Container(
                                    content=Text(
                                        value = f"{product_cost:.2f}€",
                                        color = MAIN_TEXT_COLOR
                                    ),
                                    padding=padding.only(left=5, right=5),
                                )
                            ],
                            alignment=MainAxisAlignment.SPACE_AROUND
                        ),
                        padding=padding.symmetric(0, 10),
                        height=60,
                        expand=True,
                        gradient = Third_Gradient(),
                        border_radius=15,
                        alignment=alignment.center
                    )
                ],
                alignment=MainAxisAlignment.CENTER,
            ),
            padding=padding.symmetric(2.5, 10),
        )
    
    # Creates and returns a container with the product name, a checkbox and a text field for edition
    def __create_new_product_container(
        self,
        product_name: str,
        product_id: str,
        product_quantity: str,
        current_state: bool
    ):
        '''
        Creates and returns a container with the product name, a checkbox and a text field for edition
        '''
        
        return Container(
            content=Container(
                content=Column(
                    controls=[
                        Text(
                            value= f"{product_name}",
                            color=MAIN_TEXT_COLOR
                        ),
                        Row(
                            controls=[
                                Checkbox(
                                    adaptive=True,
                                    value=current_state,
                                    data=product_id,
                                    on_change=self.__edit_product_state,
                                    check_color="#606060",
                                    fill_color="transparent",
                                    overlay_color="#606060",
                                    hover_color="#606060",
                                    shape=RoundedRectangleBorder(radius=5)
                                ),
                                Container(
                                    content=Smart_TextField(
                                        page=self.__page,
                                        label=self.EDIT_TEXTFIELD_TEXT[configs["LANGUAGE"]],
                                        hint_text=self.EDIT_TEXTFIELD_HINT_TEXT[configs["LANGUAGE"]],
                                        init_value = product_quantity,
                                        numeric=True,
                                        data=product_id,
                                        on_blur=self.__edit_product_amount,
                                        expand=True,
                                        label_style=TextStyle(size=15, color="#606060", weight=FontWeight.BOLD),
                                        hint_style=TextStyle(size=15, color="#606060")
                                    ),
                                    width=130,
                                    height=40,
                                    alignment=alignment.center
                                )
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            spacing=3
                        )
                    ],
                    alignment=MainAxisAlignment.SPACE_AROUND,
                    horizontal_alignment=CrossAxisAlignment.CENTER
                ),
                height=80,
                gradient=Third_Gradient(),
                border_radius=12,
                alignment=alignment.center
            ),
            padding=padding.symmetric(2, 25),
            alignment=alignment.center
        )
          
    # Resets the current order
    def reset_current_order(self):
        '''
        Resets the current order and actualize its date
        '''
        
        for product in self.__current_order["products"]:
            self.__current_order["products"][product]["quantity"] = 0
            self.__current_order["products"][product]["quantity_text"].value = "0"
        self.__current_order["date"] = self.__current_date
        self.__order_button.content.disabled = True
        self.__order_button.content.opacity = 0.4
        self.__order_button.opacity = 0.4
        self.__total_amount = 0
    
    # Updates the controls according to if the user is in edit mode or not
    def __update_controls(self):
        '''
        Updates the controls according to if the user is in edit mode or not and updates the page
        '''
        
        if self.__editing:
            self.controls = [
                Column(
                    controls=[
                        Container(
                            content = Column(
                                controls=[
                                    self.__business_title,
                                    Text(
                                        value=f"{self.EDITING_SUBTITLE_TEXT[configs["LANGUAGE"]]}{self.__current_date}",
                                        color=MAIN_TEXT_COLOR
                                    )
                                ],
                                spacing=6,
                                alignment=MainAxisAlignment.CENTER,
                                horizontal_alignment=CrossAxisAlignment.CENTER
                            ),
                            border_radius=12,
                            gradient=Secondary_Gradient(),
                            padding=Padding(left=1, top=5, right=1, bottom=10),
                            alignment=alignment.center
                        ),
                        self.__products_column,
                    ],
                    alignment=MainAxisAlignment.START,
                    expand=True
                ),
                Container(
                    content=self.__main_button_row,
                    border_radius=12,
                    gradient=Secondary_Gradient(),
                    padding=padding.symmetric(20, 0),
                    alignment=alignment.center
                )
            ]
            self.__products_column.spacing = 15
            
        else:
            ###############################
            # Creating a column that makes the union between the main
            # button row and pages menu row
            main_button_row_and_pages_menu_row = Container(
                content=Column(
                    controls=[
                        self.__main_button_row,
                        shared_vars["bottom_menu"],
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=20
                ),
                border_radius=12,
                gradient=Secondary_Gradient(),
                padding=padding.only(top=20, bottom=4),
                alignment=alignment.center
            )
            
            self.controls = [
                Column(
                    controls=[
                        Container(
                            content=Column(
                                controls=[
                                    Container(
                                        content = Row(
                                            controls=[
                                                self.__business_title,
                                                self.__pass_week_section
                                            ],
                                            alignment=MainAxisAlignment.SPACE_AROUND
                                        ),
                                        padding=Padding(left=1, top=5, right=1, bottom=2),
                                        alignment=alignment.center
                                    ),
                                    Container(
                                        content = self.__days_row,
                                        padding=Padding(left=8, top=1, right=8, bottom=10),
                                        alignment=alignment.center
                                    )
                                ],
                                alignment=MainAxisAlignment.CENTER,
                                horizontal_alignment=CrossAxisAlignment.CENTER
                            ),
                            alignment=alignment.center,
                            gradient = Secondary_Gradient(),
                            border_radius=12,
                        ),
                        self.__products_column,
                    ],
                    alignment=MainAxisAlignment.START,
                    expand=True
                ),
                main_button_row_and_pages_menu_row
            ]
            self.__products_column.spacing = 10
    
        self.__page.update()
            
