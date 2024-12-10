from flet import (
    app,
    Page,
    Theme,
    ColorScheme,
    Stack,
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
    IconTheme
)
from main_container import Main_Container
from Login_Screen.login_screen import Login_Screen
from bottom_menu import Bottom_Menu
from shared import MAIN_TEXT_COLOR, shared_vars, user_ids

# Program Function
def main(page: Page):
    """
    Program Function
    """
    user_ids["is_admin"] = False
    shared_vars["current_business"]["name"] = "Farinha e Afeto"
    shared_vars["current_business"]["id"] = "1"
    shared_vars["main_container"] = Main_Container(page)
    shared_vars["bottom_menu"] = Bottom_Menu()
    login_screen = Login_Screen(page)
    
    shared_vars["main_container"].add_screen_to_list(login_screen, "login_screen")
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
            on_surface_variant=MAIN_TEXT_COLOR,   # Textbox Text Color
            #outline="",
            ###outline_variant="#606060",        # Dividers Color
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
