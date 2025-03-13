# services/app_token_service.py
# Serviço para buscar o token de serviço, para utilizar em apps.
import requests
import time
from models.app_token import AppToken
from config.api_config import URL_PARTNER


class AppTokenService:
    def __init__(self, app_id, partner_service, wait_time=60, max_retries=3):
        """
        Inicializa o serviço de token do app.

        :param app_id: ID do aplicativo.
        :param partner_service: Instância de PartnerService para autenticação.
        :param wait_time: Tempo de espera em segundos antes de tentar novamente após erro 429.
        :param max_retries: Número máximo de tentativas para renovar o token.
        """
        self.app_id = app_id
        self.partner_service = partner_service
        self.app_token = AppToken()
        self.wait_time = wait_time
        self.max_retries = max_retries

    def fetch_app_token(self):
        """
        Faz uma requisição para obter o TOKEN_APP e armazená-lo.
        """
        url = f"{URL_PARTNER}partner/app/{self.app_id}/token"
        headers = self.partner_service.get_headers()

        retries = 0  # Contador de tentativas
        while retries < self.max_retries:
            print(f"Tentativa {retries + 1} de {self.max_retries}. Enviando requisição para obter TOKEN_APP...")
            response = requests.get(url, headers=headers)

            if response.status_code == 429:
                # Limite de requisições atingido
                print("[TokenService] Limite de requisições atingido. Aguardando para tentar novamente...")
                retries += 1
                time.sleep(self.wait_time)
                continue  # Tenta novamente após o tempo de espera

            if response.status_code == 200:
                # Extrai o token do dicionário JSON aninhado
                token_app = response.json().get('token', {}).get('token')
                if token_app:
                    self.app_token.set_token_app(token_app)
                    print("TOKEN_APP obtido e armazenado com sucesso.")
                    return  # Sai do loop após sucesso
                else:
                    print("Não foi possível obter o TOKEN_APP no corpo da resposta.")
                    break

            # Para outros erros, registra e finaliza
            print(f"[TokenService] Erro ao obter TOKEN_APP: {response.status_code} - {response.text}")
            break

        # Se todas as tentativas falharem
        raise Exception("Não foi possível obter o TOKEN_APP após várias tentativas.")

    def get_app_token(self):
        """
        Retorna o TOKEN_APP armazenado no modelo AppToken.
        """
        return self.app_token.get_token_app()

    def refresh_app_token(self):
        """
        Atualiza o token do app chamando o método fetch_app_token.
        """
        try:
            print("Tentando renovar o TOKEN_APP...")
            self.fetch_app_token()
            print("TOKEN_APP renovado com sucesso.")
        except Exception as e:
            print(f"Erro ao renovar o TOKEN_APP: {e}")
            raise Exception("Não foi possível renovar o TOKEN_APP.")
