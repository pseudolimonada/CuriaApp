from flet import Page, SnackBar, Text, TextThemeStyle

# Presents a snack bark in the page object.
def present_snack_bar(
    page: Page,
    str_to_log: str = "",
    bgcolor: str = 'Red'
):
    '''
    Presents a snack bar in page object with the given string as text.
    '''
    
    # Snack Bar creation
    snack_bar = SnackBar(
                    Text(str_to_log, theme_style=TextThemeStyle.BODY_LARGE),
                    bgcolor=bgcolor,
                    open=True
                )
    
    page.overlay.append(snack_bar)
    page.update()
    