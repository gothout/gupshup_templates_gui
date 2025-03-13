# services/partner_service.py
import requests
import time
from models.partner import Partner
from config.api_config import URL_PARTNER

class PartnerService:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.partner = Partner() 
        self.token_expiry = None

    def authenticate(self):
        """Realiza a requisição para autenticar e obter o token."""
        url = f"{URL_PARTNER}partner/account/login"
        data = {
            'email': self.email,
            'password': self.password
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        response = requests.post(url, headers=headers, data=data)
        
        if response.status_code == 200:
            token = response.json().get('token')
            self.partner.set_token(token)  # Armazena o token no modelo Partner
            self.token_expiry = int(time.time()) + 3600  # Define expiração para 1 hora
            print("Autenticação realizada com sucesso. Token atualizado.")
        else:
            print(f"Erro no login: {response.status_code} - {response.json().get('message')}")
            raise Exception("Não foi possível obter o token.")

    def get_token(self):
        """Verifica se o token ainda é válido, caso contrário reautentica."""
        if self.partner.get_token() and time.time() < self.token_expiry:
            return self.partner.get_token()
        else:
            self.authenticate()
            return self.partner.get_token()

    def get_headers(self):
        """Retorna os headers com o token de autenticação."""
        return {
            'Content-Type': 'application/json',
            'Authorization': f'{self.get_token()}'
        }

    def get_templates(self, app_id):
        """Utiliza o token para obter os templates de um app específico."""
        url = f"{URL_PARTNER}partner/app/{app_id}/templates"
        headers = self.get_headers()
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro ao obter templates: {response.status_code} - {response.text}")
            return None
