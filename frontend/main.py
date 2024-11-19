from flet import (
    app,
    Page,
    SnackBar,
    Text,
    TextThemeStyle,
    FilePickerResultEvent,
    TextField,
    ElevatedButton,
    Row,
    Column,
    Icon,
    icons,
    MainAxisAlignment,
    FontWeight,
    Divider,
    DatePicker,
    Container,
    Checkbox,
    ProgressRing,
    FilePicker,
    NavigationRail,
    NavigationRailLabelType,
    NavigationRailDestination,
    padding,
    VerticalDivider,
    Dropdown,
    dropdown,
    ScrollMode,
    PagePlatform,
)
from main_container import Main_Container
from Login_Screen.login_screen import Login_Screen
from Order_Screen.order_screen import Order_Screen
from bottom_menu import Bottom_Menu
from shared import shared_vars

# Program Function
def main(page: Page):
    """
    Program Function
    """

    shared_vars["main_container"] = Main_Container(page)
    shared_vars["bottom_menu"] = Bottom_Menu()
    login_screen = Login_Screen(page)
    order_screen = Order_Screen(page)
    

    shared_vars["main_container"].add_screen_to_list(login_screen, "login_screen")
    shared_vars["main_container"].add_screen_to_list(order_screen, "order_screen")
    shared_vars["main_container"].change_screen("login_screen")

    # Test Values
    page.window.width = 360
    page.window.height = 800

    page.add(shared_vars["main_container"])
    

if __name__ == "__main__":
    # Program initialization
    app(target=main)
