from flet import app, Page, SnackBar, Text, TextThemeStyle, FilePickerResultEvent, TextField, ElevatedButton, Row, Column, Icon, icons, MainAxisAlignment, FontWeight, Divider, DatePicker, Container, Checkbox, ProgressRing, FilePicker, NavigationRail, NavigationRailLabelType, NavigationRailDestination, padding, VerticalDivider, Dropdown, dropdown, ScrollMode, PagePlatform
from main_container import Main_Container
from login_screen import Login_Screen


# Program Function
def main(page: Page):
    '''
    Program Function
    '''
    
    main_container = Main_Container()
    login_screen = Login_Screen()
    
    main_container.content = login_screen
    main_container.selected_screen_name = "login_screen"
    
    page.add(main_container)

if __name__ == "__main__":
    # Program initialization
    app(target=main)


            