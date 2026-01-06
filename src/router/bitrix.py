
import pytz

from datetime import datetime, timedelta 
from fastapi import APIRouter
from src.bitrix_DTO.deals import Response
from src.csv.save_deal import save_deal_csv
from src.bitrix.client import bitrixClient



router = APIRouter(prefix="/bitrix", tags=["Bitrix"])


@router.get("/deal", response_model=Response)
async def get_deals() -> Response:
    '''Получить список сделок
    - сумма больше 100 000
    - за последние 30 дней
    '''

    arr: list[Response] = []

    thirty_days_ago = (datetime.now(pytz.timezone('Europe/Moscow')) - timedelta(days=30)).strftime('%Y-%m-%d')
    deals = bitrixClient.get_deal(["ID","TITLE","OPPORTUNITY", 'STAGE_ID', 'DATE_CREATE', 'CONTACT_IDS'], {
                '!STAGE_ID': 'WON',
                '>OPPORTUNITY': 100000,
                '>=DATE_CREATE': thirty_days_ago
            })

    for d in deals:
        contactsDeal = bitrixClient.get_contacts_deal(d['ID'])

       
        contacts = []
        for c in contactsDeal:
            contact = bitrixClient.get_contact_deal(c['CONTACT_ID'])
            if 'NAME' not in contact:
                continue;

            emails = []
            
  
            if 'EMAIL' in contact:
                # 3. Проходим по всем email-адресам
                for email_item in contact['EMAIL']:
                    # 4. Проверяем наличие VALUE и что это непустая строка
                    if (
                        isinstance(email_item, dict) 
                        and 'VALUE' in email_item
                        and email_item['VALUE']
                        and isinstance(email_item['VALUE'], str)
                    ):
                        emails.append(email_item['VALUE'].strip())

            contacts.append({'Имя': contact.get('NAME', 'Неизвестно'), 'Email':emails })

        arr.append({'#': d['ID'], "Название": d['TITLE'], 'Сумма': d['OPPORTUNITY'], 'Контакты': contacts })

    save_deal_csv(arr)

    return {"status": "ok", 'deals': arr}
