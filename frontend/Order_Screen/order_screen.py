from flet import Column, MainAxisAlignment, Divider, ElevatedButton, Row, Page, ScrollMode, ButtonStyle, padding, Container, Text, CircleBorder, AlertDialog, TextButton, TextStyle, Padding, alignment, TextAlign, FontWeight, IconButton, icons, CrossAxisAlignment, VisualDensity, Checkbox, ResponsiveRow
from shared import STATUS_CODES, user_ids, shared_vars, endpoints_urls, TESTING
from utils import Smart_TextField, present_snack_bar, get_refreshed_catalog
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
    ORDER_BUTTON_TEXT: str = "Order"
    CONFIRM_BUTTON_TEXT: str = "Confirm"
    EDIT_BUTTON_TEXT: str = "Edit"
    EDIT_TEXTFIELD_TEXT: str = "Quantity"
    EDIT_TEXTFIELD_HINT_TEXT: str = "e.g.: 23"
    EDITING_SUBTITLE_TEXT: str = "Edit day: "
    ALERT_DIALOG_TITLE_TEXT: str = "Alert confirmation"
    ALERT_DIALOG_CONTENT_TEXT: str = "By changing the day your current order will be cleared. If you still want to continue, press 'OK', otherwise press CANCEL."
    ALERT_DIALOG_OK_TEXT: str = "OK"
    ALERT_DIALOG_CANCEL_TEXT: str = "CANCEL"
    INTERNAL_ERROR_TEXT: str = "An internal error occurred, please wait and try again..."
    UNRECOGNIZED_ERROR_TEXT: str = "An unexpected error occurred, please verify if your app is updated..."
    NETWORK_ERROR_TEXT: str = "Please verify your internet connection and try again..."
    PRODUCT_SCARCITY_5_TEXT: str = "\nOnly 5 or less available!"
    PRODUCT_SCARCITY_1_TEXT: str = "\nOnly 1 available!"
    PRODUCT_SCARCITY_0_TEXT: str = "\nOut of stock to order"

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
        width=FontWeight.BOLD
    )
    
    ###############################
    # Initializing title section
    __business_title: Text = Text(
        size=25,
        text_align=TextAlign.CENTER,
        width=FontWeight.BOLD
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
    __order_button: ElevatedButton
    __edit_day_button: ElevatedButton
    __confirm_button: ElevatedButton
    
    ###############################
    # Initializing and setting up the alert dialog
    __alert = AlertDialog(
        modal=True,
        title=Text(ALERT_DIALOG_TITLE_TEXT),
        content=Text(ALERT_DIALOG_CONTENT_TEXT),
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
        self.__current_week_day = today.strftime("%A")
        
        ###############################
        # Setting up the pass week section buttons
        self.__pass_week_forward_button = IconButton(
            icon = icons.ARROW_FORWARD_IOS,
            icon_size = 12,
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
        if user_ids["is_admin"]:
            self.__confirm_button = ElevatedButton(
                text=self.CONFIRM_BUTTON_TEXT,
                adaptive=True,
                on_click=self.__update_current_day,
                style=ButtonStyle(
                    padding=padding.symmetric(10, 70)
                ),
                scale=1.2
            )
            self.__edit_day_button = ElevatedButton(
                text=self.EDIT_BUTTON_TEXT,
                adaptive=True,
                on_click=self.__edit_current_day,
                style=ButtonStyle(
                    padding=padding.symmetric(10, 70)
                ),
                scale=1.2
            )
            self.__main_button_row.controls = [self.__edit_day_button]
        else:
            self.__order_button = ElevatedButton(
                text=self.ORDER_BUTTON_TEXT,
                adaptive=True,
                disabled=True,
                on_click=self.__realize_order,
                style=ButtonStyle(
                    padding=padding.symmetric(10, 70)
                ),
                scale=1.6
            )
            self.__main_button_row.controls = [self.__order_button]
        
        ###############################
        # Final setting up the main column controls with everything
        self.__update_controls()
    
    
    #############################################
    #                Main Methods               #
    #############################################
    
    
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
                    "quantity_text": Text(value="0"),
                    "quantity": 0,
                    "cost": "1.50€"
                }
            self.__current_order["date"] = self.__current_date
            if update_days_row:
                self.__fill_days_row(monday)
            self.__fill_products_column()
            return
        
        ###############################
        # Refreshing catalog then week catalog and finally update objects
        if self.__refresh_catalog(self):
            if self.__refresh_week_catalog(self, monday.strftime("%d/%m/%Y")):
                ###############################
                # Initializing/Resetting current order products
                self.__current_order["products"] = {}
                for product_id in self.__catalog.keys():
                    self.__current_order["products"][self.__catalog[product_id]["product_title"]] = {
                        "product_id": product_id,
                        "quantity_text": Text(value="0"),
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
                new_container = self.__create_new_product_container(f"Este é um Pao disto assim {i}", i, state)
                self.__products_column.controls.append(new_container)
            
            self.__update_controls()
            return
        
        ###############################
        # Creating and adding products containers according to the products in the catalog
        for product_id in self.__catalog.keys():
            if product_id in self.__current_week_catalog[self.__current_week_day].keys():
                state = True
            else:
                state = False
                
            self.__current_date_catalog_edit[product_id] = {
                "quantity": None, #TODO
                "state": state
            }
            
            new_container = self.__create_new_product_container(self.__catalog[product_id]["product_title"], product_id, state)
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
        new_date_catalog = {}
        for product_id in self.__current_date_catalog_edit.keys():
            if self.__current_date_catalog_edit[product_id]["state"]:
                new_date_catalog[product_id] = self.__current_date_catalog_edit[product_id]["quantity"]
        
        headers = {
            "user_id": user_ids["user_id"],
            "manager_business_ids": user_ids["manager_business_ids"]
        }
        payload = {
            "new_date_catalog": new_date_catalog,
        }
        url_template = Template(endpoints_urls[""])
        get_catalog_url = url_template.safe_substitute(business_id=shared_vars["current_business"]["id"])
        
        ###############################
        # Making and processing the request
        try:
            # Sending request and getting response
            response = requests.post(get_catalog_url, headers=headers, json=payload)
            
            # Check the response
            if response.status_code == STATUS_CODES["SUCCESS"]:
                present_snack_bar(self.__page, self.DATE_CATALOG_EDIT_SUCCESS_TEXT, "Green")
                
            elif response.status_code >= STATUS_CODES["INTERNAL_ERROR"]:
                present_snack_bar(self.__page, self.INTERNAL_ERROR_TEXT, "Red")
            else:
                present_snack_bar(self.__page, self.UNRECOGNIZED_ERROR_TEXT, "Red")
        except requests.exceptions.RequestException as e:
            # Handle network-related errors
            present_snack_bar(self.__page, self.NETWORK_ERROR_TEXT, "Red")
        
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
    # If any error occurs return false, otherwise return true
    # Week Catalog Structure:  (product_scarcity can be 5, 1, 0 or null, the null is in case there are more then 5)
    #   {
    #       "Mon": [{"product_id":"...", "product_scarcity": ...}, {"product_id":"...", "product_scarcity": ...}],
    #       "Tue": [{"product_id":"...", "product_scarcity": ...}, {"product_id":"...", "product_scarcity": ...}],
    #       "Wed": [{"product_id":"...", "product_scarcity": ...}, {"product_id":"...", "product_scarcity": ...}],
    #       "Thu": [{"product_id":"...", "product_scarcity": ...}, {"product_id":"...", "product_scarcity": ...}],
    #       "Fri": [{"product_id":"...", "product_scarcity": ...}, {"product_id":"...", "product_scarcity": ...}],
    #       "Sat": [{"product_id":"...", "product_scarcity": ...}, {"product_id":"...", "product_scarcity": ...}],
    #       "Sun": [{"product_id":"...", "product_scarcity": ...}, {"product_id":"...", "product_scarcity": ...}]
    #   }
    #
    def __refresh_week_catalog(
        self,
        monday_date:str
    ):
        '''
        Refreshes the week catalog for the actual business and save it in self.__current_week_catalog
        If any error occurs return false, otherwise return true
        Week Catalog Structure:  (product_scarcity can be 5, 1, 0 or null, the null is in case there are more then 5)
        {
            "Mon": {"product_idX": product_scarcity, "product_idX": product_scarcity, ...},
            "Tue": {"product_idX": product_scarcity, "product_idX": product_scarcity, ...},
            "Wed": {"product_idX": product_scarcity, "product_idX": product_scarcity, ...},
            "Thu": {"product_idX": product_scarcity, "product_idX": product_scarcity, ...},
            "Fri": {"product_idX": product_scarcity, "product_idX": product_scarcity, ...},
            "Sat": {"product_idX": product_scarcity, "product_idX": product_scarcity, ...},
            "Sun": {"product_idX": product_scarcity, "product_idX": product_scarcity, ...}
        }
        '''
        
        ###############################
        # Setting up all requirements for the request
        headers = {
            "user_id": user_ids["user_id"],
            "manager_business_ids": user_ids["manager_business_ids"]
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
                self.__current_week_catalog["Mon"] = response["Mon"]
                self.__current_week_catalog["Tue"] = response["Tue"]
                self.__current_week_catalog["Wed"] = response["Wed"]
                self.__current_week_catalog["Thu"] = response["Thu"]
                self.__current_week_catalog["Fri"] = response["Fri"]
                self.__current_week_catalog["Sat"] = response["Sat"]
                self.__current_week_catalog["Sun"] = response["Sun"]
                return True
                
            elif response.status_code >= STATUS_CODES["INTERNAL_ERROR"]:
                present_snack_bar(self.__page, self.INTERNAL_ERROR_TEXT, "Red")
            else:
                present_snack_bar(self.__page, self.UNRECOGNIZED_ERROR_TEXT, "Red")
        except requests.exceptions.RequestException as e:
            # Handle network-related errors
            present_snack_bar(self.__page, self.NETWORK_ERROR_TEXT, "Red")
        
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
                if user_ids["is_admin"]:
                    product_row = self.__create_new_product_row_manager(f"Este é um Pao disto assim {i}", self.__current_order["products"][f"Este é um Pao disto assim {i}"]["cost"])
                else:
                    product_row = self.__create_new_product_row_client("1", f"Este é um Pao disto assim {i}", self.__current_order["products"][f"Este é um Pao disto assim {i}"]["cost"], product_scarcity)
                self.__products_column.controls.append(product_row)
            return
        
        ###############################
        # Adding products rows according to the products in the catalog day
        for product_id in self.__current_week_catalog[self.__current_week_day].keys():
            if user_ids["is_admin"]:
                product_row = self.__create_new_product_row_manager(self.__catalog[product_id]["product_title"], self.__catalog[product_id]["product_price"])
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
            self.__alert.actions=[
                TextButton(self.ALERT_DIALOG_OK_TEXT, on_click=self.__handle_close_dialog, data=e.control.data),
                TextButton(self.ALERT_DIALOG_CANCEL_TEXT, on_click=self.__handle_close_dialog)
            ]
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
                self.__alert.actions=[
                    TextButton(self.ALERT_DIALOG_OK_TEXT, on_click=self.__handle_close_dialog, data=e.control.data),
                    TextButton(self.ALERT_DIALOG_CANCEL_TEXT, on_click=self.__handle_close_dialog)
                ]
                self.__page.open(self.__alert)
            else:
                self.__current_date = e.control.data[1]
                self.__current_week_day = e.control.data[0]
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
                    self.__order_button.disabled = False
        elif operation == "-":
            if self.__current_order["products"][product_name]["quantity"] > 0:
                self.__current_order["products"][product_name]["quantity"] -= 1
                self.__total_amount -= 1
                if self.__total_amount <= 0:
                    self.__order_button.disabled = True
                    
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
        if e.control.text == self.ALERT_DIALOG_OK_TEXT:
            if e.control.data in ["forward", "backward"]:
                current_date_datetime = datetime.strptime(self.__current_date, "%d/%m/%Y")
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
                self.__current_date = e.control.data[1]
                self.__current_week_day = e.control.data[0]
                
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
        
        self.__days_row.controls.append(
            ElevatedButton(
                text=week_day,
                adaptive=True,
                on_click=self.__change_date_product_list,
                data=(week_day, date),
                width=60,
                height=30,
                style=ButtonStyle(
                    padding=Padding(left=2, top=1, right=2, bottom=1),
                    text_style=TextStyle(size=14)
                )
            )
        )
    
    # Creates and returns a row with the information about the product and two buttons ('+' and '-')
    def __create_new_product_row_client(
        self,
        product_id: str,
        product_name: str,
        product_cost: str,
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
                product_scarcity_text = self.PRODUCT_SCARCITY_5_TEXT
            case 1:
                product_scarcity_text = self.PRODUCT_SCARCITY_1_TEXT
            case 0:
                product_scarcity_text = self.PRODUCT_SCARCITY_0_TEXT
        
        return Row(
            controls=[
                Container(
                    content=Row(
                        controls=[
                            Container(
                                content=Text(
                                    value= f"{product_name}{product_scarcity_text}"
                                ),
                                padding=padding.only(left=10, right=20),
                                expand=True
                            ),
                            Text(product_cost),
                        ],
                        alignment=MainAxisAlignment.SPACE_AROUND
                    ),
                    height=80,
                    expand=True
                ),
                Container(
                    content=Row(
                        controls=[
                            Container(
                                content=ElevatedButton(
                                    text="-",
                                    adaptive=True,
                                    style=ButtonStyle(
                                        shape=CircleBorder(),
                                        padding=padding.all(0)
                                    ),
                                    on_click=self.__change_product_amount,
                                    data=("-", product_name, product_id)
                                ),
                                width=40,
                                height=40
                            ),
                            self.__current_order["products"][product_name]["quantity_text"],
                            Container(
                                content=ElevatedButton(
                                    text="+",
                                    adaptive=True,
                                    style=ButtonStyle(
                                        shape=CircleBorder(),
                                        padding=padding.all(0)
                                    ),
                                    on_click=self.__change_product_amount,
                                    data=("+", product_name, product_id)
                                ),
                                padding=padding.only(right=10),
                                width=50,
                                height=40
                            )
                        ],
                        alignment=MainAxisAlignment.START,
                        spacing=10,
                        expand=True
                    )
                )
            ]
        )
    
    # Creates and returns a row with the information about the product
    def __create_new_product_row_manager(
        self,
        product_name: str,
        product_cost: str,
    ):
        '''
        Creates and returns a row with the information about the product
        '''
        
        return Row(
            controls=[
                Container(
                    content=Row(
                        controls=[
                            Container(
                                content=Text(
                                    value = f"{product_name}"
                                ),
                                padding=padding.only(left=10, right=20),
                                expand=True
                            ),
                            Container(
                                content=Text(
                                    value = product_cost
                                ),
                                padding=padding.only(left=20, right=10),
                            )
                        ],
                        alignment=MainAxisAlignment.SPACE_AROUND
                    ),
                    height=60,
                    expand=True
                )
            ]
        )  
    
    # Creates and returns a container with the product name, a checkbox and a text field for edition
    def __create_new_product_container(
        self,
        product_name: str,
        product_id: str,
        current_state: bool
    ):
        '''
        Creates and returns a container with the product name, a checkbox and a text field for edition
        '''
        
        return Container(
            content=Column(
                controls=[
                    Text(
                        value= f"{product_name}"
                    ),
                    Row(
                        controls=[
                            Checkbox(
                                adaptive=True,
                                value=current_state,
                                data=product_id,
                                on_change=self.__edit_product_state
                            ),
                            Container(
                                content=Smart_TextField(
                                    page=self.__page,
                                    label=self.EDIT_TEXTFIELD_TEXT,
                                    hint_text=self.EDIT_TEXTFIELD_HINT_TEXT,
                                    numeric=True,
                                    data=product_id,
                                    on_blur=self.__edit_product_amount,
                                    expand=True,
                                    label_style=TextStyle(size=10),
                                    hint_style=TextStyle(size=10)
                                ),
                                width=100,
                                height=30,
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
        self.__order_button.disabled = True
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
                                        value=f"{self.EDITING_SUBTITLE_TEXT}{self.__current_date}"
                                    )
                                ],
                                alignment=MainAxisAlignment.CENTER,
                                horizontal_alignment=CrossAxisAlignment.CENTER
                            ),
                            padding=Padding(left=1, top=5, right=1, bottom=5),
                            alignment=alignment.center
                        ),
                        Divider(),
                        self.__products_column,
                    ],
                    alignment=MainAxisAlignment.START,
                    expand=True
                ),
                Container(
                    content=self.__main_button_row,
                    padding=padding.symmetric(20, 0),
                    alignment=alignment.center
                )
            ]
            self.__products_column.spacing = 15
            
        else:
            ###############################
            # Creating a column that makes the union between the main
            # button row and pages menu row
            main_button_row_and_pages_menu_row = Column(
                controls=[
                    Divider(),
                    self.__main_button_row,
                    Column(
                        controls=[
                            Divider(),
                            shared_vars["bottom_menu"],
                            Divider()
                        ],
                        alignment=MainAxisAlignment.START,
                        spacing=1
                    )
                ],
                alignment=MainAxisAlignment.START,
                spacing=20
            )
            
            self.controls = [
                Column(
                    controls=[
                        Container(
                            content = Row(
                                controls=[
                                    self.__business_title,
                                    self.__pass_week_section
                                ],
                                alignment=MainAxisAlignment.SPACE_AROUND
                            ),
                            padding=Padding(left=1, top=5, right=1, bottom=5),
                            alignment=alignment.center
                        ),
                        Container(
                            content = self.__days_row,
                            padding=Padding(left=8, top=2, right=8, bottom=2),
                            alignment=alignment.center
                        ),
                        Divider(),
                        self.__products_column,
                    ],
                    alignment=MainAxisAlignment.START,
                    expand=True
                ),
                main_button_row_and_pages_menu_row
            ]
            self.__products_column.spacing = 10
    
        self.__page.update()
            