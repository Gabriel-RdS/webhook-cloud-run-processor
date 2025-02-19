from google.cloud import secretmanager

def get_secret(secret_id: str, project_id: str, version_id: str = "latest") -> str:
    """Obtém segredos do Google Secret Manager de forma segura.
    
    Args:
        secret_id: Nome do segredo no Secret Manager
        project_id: ID do projeto GCP
        version_id: Versão do segredo (padrão 'latest')
    
    Returns:
        Valor do segredo como string
    """
    client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(name=secret_name)
    return response.payload.data.decode("UTF-8")
