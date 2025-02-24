import os
import requests
import logging

# Obtenha as URLs dos webhooks a partir de variáveis de ambiente
SUCCESS_WEBHOOK_URL = os.getenv("GOOGLE_CHAT_SUCCESS")
FAILURE_WEBHOOK_URL = os.getenv("GOOGLE_CHAT_FAILURE")

# Também, se necessário, pode obter algum URL base para logs ou para Insider
#INSIDER_URL = os.getenv("INSIDER_URL", "")

class Monitoring:
    def __init__(self, success_webhook_url=SUCCESS_WEBHOOK_URL, failure_webhook_url=FAILURE_WEBHOOK_URL):
        self.success_webhook_url = success_webhook_url
        self.failure_webhook_url = failure_webhook_url

    def send_chat_message(self, message_text, webhook_url):
        message = {"text": message_text}
        try:
            response = requests.post(webhook_url, json=message)
            response.raise_for_status()
            logging.info("Mensagem enviada para o Google Chat com sucesso.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Falha ao enviar mensagem para o Google Chat: {e}")

    def format_success_message(self, file_uuid, arquivo_nome):
        return (f"✅ WEBHOOK INSIDER: Processamento concluído\n"
                f"Logs: https://console.cloud.google.com/run/detail/us-central1/insider-webhook/logs?hl=pt-br&project=prd-data-transient.\n"
                f"ID: {file_uuid}\n"
                f"Arquivo: {arquivo_nome}")

    def format_failure_message(self, file_uuid, arquivo_nome, error):
        return (f"⚠️ WEBHOOK INSIDER: Processamento com Falha\n"
                f"Logs: https://console.cloud.google.com/run/detail/us-central1/insider-webhook/logs?hl=pt-br&project=prd-data-transient.\n"
                f"ID: {file_uuid}\n"
                f"Arquivo: {arquivo_nome}\n"
                f"Erro: {error}")

    def send_success_message(self, file_uuid, arquivo_nome):
        if self.success_webhook_url:
            message = self.format_success_message(file_uuid, arquivo_nome)
            self.send_chat_message(message, self.success_webhook_url)
        else:
            logging.warning("SUCCESS_WEBHOOK_URL não configurado.")

    def send_failure_message(self, file_uuid, arquivo_nome, error):
        if self.failure_webhook_url:
            message = self.format_failure_message(file_uuid, arquivo_nome, error)
            self.send_chat_message(message, self.failure_webhook_url)
        else:
            logging.warning("FAILURE_WEBHOOK_URL não configurado.")