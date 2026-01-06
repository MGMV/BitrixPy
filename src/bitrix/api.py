"""
Простой клиент Bitrix24 на вебхуке.
Настройте переменные окружения:
  BITRIX_BASE_URL=https://example.bitrix24.ru/rest/1/<webhook>/
"""

from typing import Any, Dict, Optional


import requests
from pydantic_settings import BaseSettings
from pydantic import HttpUrl
from dotenv import load_dotenv


load_dotenv()

class BitrixSettings(BaseSettings):
    base_url: HttpUrl
    base_webhook: str

    class Config:
        env_prefix = "BITRIX_"
        case_sensitive = False
        


class BitrixAPI:
    def __init__(self, base_url: str, base_webhook: str, session: Optional[requests.Session] = None) -> None:
        self._base_url = base_url+ '/' + base_webhook + '/'
        self._session = session or requests.Session()

    def call(self, method: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Выполняет POST к Bitrix REST (метод без ведущего '/').
        Поднимет HTTPError при 4xx/5xx и RuntimeError при ошибке Bitrix в теле.
        """
        url = f"{self._base_url}{method.lstrip('/')}"
        resp = self._session.post(url, json=payload or {}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, dict) and data.get("error"):
            # Bitrix может вернуть error при 200 OK
            raise RuntimeError(f"Bitrix error: {data}")
        return data

    def get_deal(self, select: list[str], filter: dict[str,any]):
        ''' Получить сделки
        - select - массив с полями выборки
        - filter - словарь с полями филтра
        '''

        deals = self.call('crm.deal.list', 
        {
                'select': select, 
                'filter': filter
        })
        if deals and 'result' in deals and deals['result']:
            return deals['result']
        else:
            return {'error': 'Bitrix error 500'}

    def get_contacts_deal(self, id):
        ''' Получить контактов по ID сделки
        - id - ID сделки
        '''
        contacts = self.call('crm.deal.contact.items.get', {'id': id})

        if contacts and 'result' in contacts and contacts['result']:
            return contacts['result']
        else:
            return {'error': 'Bitrix error 500'}

    def get_contact_deal(self, id):
        ''' Получить контакт по ID контакта
        - id - ID контакта
        '''
        contact = self.call('crm.contact.get', {'id': id})
        
        if contact and 'result' in contact and contact['result']:
            return contact['result']
        else:
            return {'error': 'Bitrix error 500'}

def get_bitrix_api() -> BitrixAPI:
   
    settings = BitrixSettings()
    return BitrixAPI(str(settings.base_url), settings.base_webhook)
