import asyncio
import aiohttp
from time import time
import json
from bs4 import BeautifulSoup


async def get_request(session, url): #асинхронный запрос 
    async with session.get(url) as response:
        return await response.text()
    
    
async def ria_news(session):
    url = 'https://ria.ru/'
    try:
        html = await get_request(session, url)
        soup = BeautifulSoup(html, 'html.parser') #парсим html код 
        titles = [h3.text.strip() for h3 in soup.select('h3.gs-c-promo-heading__title')] 
        return {"source": "ria", "titles": titles[:5]} # возвращаем первы 5 заголовков
    except Exception as e:
        print(f"Error parsing BBC: {e}")
        return {"source": "ria", "titles": []}


async def rbc_news(session):
    url = 'https://www.rbc.ru/'
    try:
        html = await get_request(session, url)
        soup = BeautifulSoup(html, 'html.parser')
        titles = [h3.text.strip() for h3 in soup.select('h3.gs-c-promo-heading__title')]
        return {"source": "rbc", "titles": titles[:5]}
    except Exception as e:
        print(f"Error parsing BBC: {e}")
        return {"source": "rbc", "titles": []}
    
    
    
async def save_to_files(data): #сохраняем результат в json файл
    with open('new_title.json', 'w') as file: 
        json.dump(data, file, indent=2)

async def main():
    start = time()
    
    async with aiohttp.ClientSession() as session: #запускаем клиентскую сессию
        tasks = [
            ria_news(session), #список тасков 
            rbc_news(session)
        ]
        
        results = await asyncio.gather(*tasks) #запускаем конкурентно
    
        await save_to_files(results) # сохраняем результат
        
        for result in results:
            print(f"\n--- {result['source']} ---")
            for i, title in enumerate(result['titles'], 1):
                print(f"{i}. {title}")
    
    print(f"\nЗавершено за {time() - start:.2f} секунд")

    
    
    
    
    
if __name__ == '__main__': 
    asyncio.run(main())





