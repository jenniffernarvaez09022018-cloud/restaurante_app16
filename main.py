from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView

def main():
    servicio = RestauranteServicio()

    def abrir_menu_principal(usuario_autenticado):
        app_principal = MainView(servicio, usuario_autenticado)
        app_principal.mainloop()

    app_login = LoginView(servicio, abrir_menu_principal)
    app_login.mainloop()

if __name__ == "__main__":
    main()