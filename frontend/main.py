from flet import (
    app,
    Page,
    Theme,
    ColorScheme,
    TextTheme,
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
from shared import shared_vars, PRIM_COLOR, SEC_COLOR

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
    
    page.padding = 0
    page.theme = Theme(
        color_scheme=ColorScheme(
            ###primary="",      # Buttons Text, TextBox Outline, Icons Color
            #on_primary="",
            #primary_container="",
            #on_primary_container="",
            #secondary="",
            #on_secondary="",
            #secondary_container="",
            #tertiary="",
            #on_tertiary="",
            #tertiary_container="",
            #on_tertiary_container="",
            #background="",
            #on_background="",
            #surface="",
            ###on_surface="",       # Disabled Button Color
            #surface_variant="",
            ###on_surface_variant="",   # Textbox Text Color
            #outline="",
            ###outline_variant="",        # Dividers Color
            #shadow="",
            #scrim="",
            #inverse_surface="",
            #on_inverse_surface="",
            #inverse_primary="",
            #surface_tint=""
        )
    )

    page.add(shared_vars["main_container"])
    

if __name__ == "__main__":
    # Program initialization
    app(target=main)
