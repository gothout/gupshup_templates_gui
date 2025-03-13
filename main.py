# main_test.py

from controllers.apps_controller import AppsController
from controllers.template_controller import TemplateController
from interface.menu import Menu

class App:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.apps_controller = AppsController(email, password)
        self.template_controller = TemplateController(email, password)
        self.current_app_id = None

    def login(self):
        print("Efetuando login...")
        self.apps_controller.list_apps()
        app_ids = [app.get_app_id() for app in self.apps_controller.apps_service.Apps]

        while True:
            app_id_choice = input("Digite o ID do aplicativo desejado: ")
            if app_id_choice in app_ids:
                self.current_app_id = app_id_choice
                print(f"Aplicativo selecionado: {app_id_choice}")
                break
            else:
                print("ID de aplicativo inválido. Por favor, tente novamente.")

    def execute_menu(self):
        menu = Menu(self.template_controller, self.current_app_id)
        menu.show()


def main():
    email = input("Digite seu email: ")
    password = input("Digite sua senha: ")

    app = App(email, password)
    app.login()
    app.execute_menu()


if __name__ == "__main__":
    main()
