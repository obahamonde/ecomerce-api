from bs4 import BeautifulSoup
from requests import get
from package.services.fauna import Q
from pydantic import BaseModel
from typing import Optional

css_classes = {
    'img': 'attachment-woocommerce_thumbnail',
    'p': 'no-text-overflow',
    'a': 'woocommerce-loop-product__link',
    'span': 'woocommerce-Price-amount'
}

BASE_URL = "https://senseirecords.net/tienda/page/"

class Vinyl(BaseModel):
    img: Optional[str]
    title: Optional[str]
    price: Optional[str]
    category: Optional[str]
    url: Optional[str]

def scrap():
    for i in range(18):
        url = BASE_URL + str(i + 1)
        response = get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        img = soup.find_all('img', class_='attachment-woocommerce_thumbnail')
        p = soup.find_all('p', class_='no-text-overflow')
        a = soup.find_all('a', class_='woocommerce-loop-product__link')
        span = soup.find_all('span', class_='woocommerce-Price-amount')
        z = zip(img, p, a, span)
        for i, j, k, l in z:
            vinyl = Vinyl(
                img=i.get('src'),
                title=j.get_text(),
                price=l.get_text(),
                category=k.get_text(),
                url=k.get('href')
            )
            print(vinyl)
            Q.create(vinyl)
            print('\n')