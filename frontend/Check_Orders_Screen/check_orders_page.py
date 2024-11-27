from flet import Column, MainAxisAlignment, Divider, ElevatedButton, Row, Page, ScrollMode, ButtonStyle, padding, Container, Text, CircleBorder, BorderSide
from shared import shared_vars

class Check_Orders_Page(Column):
    '''
    Column that displays all the orders a user has made
    '''



    #Button texts
    __page = Page
    __data = dict

    FILTER_BUTTON_TEXT: tuple = ("Por aprovar", "Aprovado", "Por entregar", "Entregue") #Qual a diferença entre aprovado e por entregar?

    __days_row: Row = Row(alignment = MainAxisAlignment.START, scroll = ScrollMode.ADAPTIVE)

    __filters_row: Row = Row(alignment = MainAxisAlignment.CENTER, scroll = ScrollMode.ADAPTIVE)

    __order_row: Row = Row(alignment = MainAxisAlignment.CENTER)
    
    #Constructor
    def __init__(self, page: Page):
        super().__init__(alignment = MainAxisAlignment.SPACE_BETWEEN, expand = True)

        self.__page = page

        self.__fill_days_row()
        self.__create_filters_row()

        # Creating a column that joins order, filters and pages menu rows
        order_row_and_pages_menu_row = Column(
            controls=[
                self.__order_row,
                Column(
                    controls=[
                        Divider(),
                        shared_vars["bottom_menu"]
                    ],
                    alignment=MainAxisAlignment.START,
                    spacing=4
                )
            ],
            alignment=MainAxisAlignment.START,
            spacing=40
        )

        # Updating controls of the screen
        self.controls = [
            Column(
                controls=[
                    self.__days_row,
                    Divider(),
                    self.__filters_row
                ],
                alignment=MainAxisAlignment.START,
                expand=True
            ),
            order_row_and_pages_menu_row
        ]
        

        



    def __create_filters_row(self):
        
        for i in self.FILTER_BUTTON_TEXT:
            self.__filters_row.controls.append(
                ElevatedButton(
                    text = i,
                    adaptive = True,
                    on_click = self.__change_filter_orders_list,
                    data = i
                )
            )



    def __fill_days_row(self):
        '''
        Clears the days row and refill it with new data from DB.
        '''        
        self.__days_row.controls.clear()
            
        self.__create_date_button("11/11")        
        self.__create_date_button("12/11")
        self.__create_date_button("13/11")
        self.__create_date_button("14/11")
        self.__create_date_button("15/11")
        # Add the new days buttons to controls according to data from DB


    def __create_date_button(self, date: str):
        '''
        Creates buttons for a date
        '''
        self.__days_row.controls.append(
            ElevatedButton(
                text = date,
                adaptive = True,
                on_click = self.__change_date_orders_list,
                data = date
            )
        )
    
    def __change_date_orders_list(self, e):
        '''
        Changes shown order according to the date chosen
        '''
        pass
        
    def __change_filter_orders_list(self, e):
        '''
        Change shown orders according to order status
        '''
        pass