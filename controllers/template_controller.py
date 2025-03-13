# controllers/template_controller.py

from services.partner_service import PartnerService
from services.app_token_service import AppTokenService
from services.template_service import TemplateService
import csv

class TemplateController:
    def __init__(self, email, password):
        self.partner_service = PartnerService(email, password)
        self.app_token_service = None  # Inicializado após definir o app_id
        self.template_service = None  # Inicializado após obter o token do app

    def get_templates(self, app_id):
        """
        Obtém e apresenta os templates para um determinado app_id.

        Args:
            app_id (str): O ID da aplicação Gupshup.
        """
        try:
            # 1. Obter token do parceiro (se necessário)
            self.partner_service.get_token()

            # 2. Obter token da aplicação
            self.app_token_service = AppTokenService(app_id, self.partner_service)
            self.app_token_service.fetch_app_token()

            # 3. Obter e apresentar templates
            self.template_service = TemplateService(self.app_token_service)
            self.template_service.fetch_templates(app_id)
            self.template_service.present_templates()

        except Exception as e:
            print(f"Ocorreu um erro ao obter os templates: {e}")

        except Exception as e:
            print(f"Erro ao obter templates: {e}") 

    def backup_templates(self, app_id):
        """
        Realiza o backup dos templates para um determinado app_id em um arquivo CSV.

        Args:
            app_id (str): O ID da aplicação Gupshup.
        """
        try:
            # 1. Obter token do parceiro (se necessário)
            self.partner_service.get_token()

            # 2. Obter token da aplicação
            self.app_token_service = AppTokenService(app_id, self.partner_service)
            self.app_token_service.fetch_app_token()

            # 3. Obter templates usando fetch_templates
            self.template_service = TemplateService(self.app_token_service)
            self.template_service.backup_templates(app_id)

        except Exception as e:
            print(f"Erro ao realizar backup dos templates: {e}")

    def export_html_templates(self, app_id):
        """
        Realiza o backup dos templates para um determinado app_id em um arquivo CSV.

        Args:
            app_id (str): O ID da aplicação Gupshup.
        """
        try:
            # 1. Obter token do parceiro (se necessário)
            self.partner_service.get_token()

            # 2. Obter token da aplicação
            self.app_token_service = AppTokenService(app_id, self.partner_service)
            self.app_token_service.fetch_app_token()

            # 3. Obter templates usando fetch_templates
            self.template_service = TemplateService(self.app_token_service)
            self.template_service.export_templates_html(app_id)

        except Exception as e:
            print(f"Erro ao realizar backup dos templates: {e}")

    def create_template(self, app_id, name, category, language_code, content, example):
            """
                Realiza a criação de template da Meta Library na plataforma Gupshup.

                Args:
                    app_id (str): O ID da aplicação Gupshup.
                    name (str): O nome do template.
                    category (str): A categoria do template.
                    language_code (str): O código do idioma do template.
                    content (str): O conteúdo do template.
            """
            try:
                # 1. Obter token do parceiro (se necessário)
                self.partner_service.get_token()

                # 2. Obter token da aplicação
                self.app_token_service = AppTokenService(app_id, self.partner_service)
                self.app_token_service.fetch_app_token()

                # 3. Instancia o TemplateService
                self.template_service = TemplateService(self.app_token_service) 

                # 4. Cria template
                self.template_service.create_template(app_id, name, category, language_code, content, example)
            except Exception as e:
                print(f"[TemplateController] Erro ao criar template: {e}")

    def remove_template_by_id(self, app_id, template_id):
            """
                Realiza a criação de template da Meta Library na plataforma Gupshup.

                Args:
                    app_id (str): O ID da aplicação Gupshup.
                    name (str): O nome do template.
                    category (str): A categoria do template.
                    language_code (str): O código do idioma do template.
                    content (str): O conteúdo do template.
            """
            try:
                # 1. Obter token do parceiro (se necessário)
                self.partner_service.get_token()

                # 2. Obter token da aplicação
                self.app_token_service = AppTokenService(app_id, self.partner_service)
                self.app_token_service.fetch_app_token()

                # 3. Instancia o TemplateService
                self.template_service = TemplateService(self.app_token_service) 

                # 4. Deleta template
                self.template_service.remove_template_by_id(app_id, template_id)
            except Exception as e:
                print(f"[TemplateController] Erro ao criar template: {e}")

    def remove_templates_from_csv(self, app_id, csv_path):
            """
            Remove templates da plataforma Gupshup com base em uma lista de IDs em um arquivo CSV.

            Args:
                app_id (str): O ID da aplicação Gupshup.
                csv_path (str): O caminho para o arquivo CSV contendo os IDs dos templates.
            """
            try:
                # 1. Obter token do parceiro (se necessário)
                self.partner_service.get_token()

                # 2. Obter token da aplicação
                self.app_token_service = AppTokenService(app_id, self.partner_service)
                self.app_token_service.fetch_app_token()

                # 3. Instancia o TemplateService
                self.template_service = TemplateService(self.app_token_service)

                # 4. Ler os IDs dos templates do arquivo CSV
                with open(csv_path, 'r', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    next(reader)  # Pula o cabeçalho, se houver
                    template_ids = [row[0] for row in reader]  # Obtém o ID da primeira coluna de cada linha

                # 5. Remover cada template pelo ID
                for template_id in template_ids:
                    self.template_service.remove_template_by_id(app_id, template_id)

            except Exception as e:
                print(f"[TemplateController] Erro ao remover templates do CSV: {e}")