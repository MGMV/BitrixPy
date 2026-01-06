import csv
import os
from typing import List
from datetime import datetime

from src.bitrix_DTO.deals import DealItem

def save_deal_csv(deals: List[DealItem], filename: str = None) -> str:
    """
    Сохраняет данные сделок в CSV‑файл.
    
    Args:
        deals: список сделок (объектов DealItem)
        filename: имя файла (если не указано — генерируется автоматически)
    
    
    Returns:
        Путь к сохранённому файлу
    """
    # Генерируем имя файла, если не передано
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"deals_report_{timestamp}.csv"
    

    # Определяем поля для CSV (соответствуют ключам в DealItem и ContactItem)
    fieldnames = [
        'deal_id', 'deal_title', 'amount',
        'contact_emails'
    ]

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Записываем заголовок
            writer.writeheader()

            # Проходим по всем сделкам
            for deal in deals:
                # Проходим по всем контактам в сделке
                for contact in deal['Контакты']:
                    emails = contact.get('Email', [])
                    row = {
                        'deal_id': deal.get('#', ''),
                        'deal_title': deal.get('Название', ''),
                        'amount': deal.get('Сумма', ''),
                        'contact_emails': '; '.join(emails) if len(emails) > 0 else 'null'
                    }
                    writer.writerow(row)

        return os.path.abspath(filename)

    except Exception as e:
        print(f"Ошибка при сохранении в CSV: {e}")
        raise
