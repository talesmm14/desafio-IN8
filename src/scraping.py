from playwright.async_api import async_playwright


URLS_PRODUCTS = (
    ('computers', 'computers'),
    ('laptops', 'computers/laptops'),
    ('tablets', 'computers/tablets'),
    ('phones', 'phones'),
    ('touch', 'phones/touch')
)


async def get_products(url: str = '') -> list:
    """ Returns a list of products from the site https://webscraper.io/test-sites/e-commerce/allinone/ 
    
        To access other products, query the constant URLS_PRODUCTS
        
        URLS_PRODUCTS = (
            
            ('computers', 'computers'),
            ('laptops', 'computers/laptops'),
            ('tablets', 'computers/tablets'),
            ('phones', 'phones'),
            ('touch', 'phones/touch')
            
        )
        
        Ex: 
            menu = dict(URLS_PRODUCTS)
            
            print(menu['laptops'])
            >>> computers/laptops
    
    """
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        context = await browser.new_context(
            base_url='https://webscraper.io/test-sites/e-commerce/allinone/'
        )
        page = await context.new_page()
        await page.goto(url)
        cards = await page.query_selector_all('div.thumbnail')
        
        products = []
        
        for card in cards:
            price = await (await card.query_selector('.price')).text_content()
            reviews = await (await (await card.query_selector('.ratings')).query_selector('.pull-right')).text_content()
            products.append({
                'thumbnail': await (await card.query_selector('.img-responsive')).get_attribute('src'),
                'name': await (await card.query_selector('.title')).get_attribute('title'),
                'price': price.replace('$', ''),
                'description': await (await card.query_selector('.description')).text_content(),
                'p_range': await (await (await card.query_selector('.ratings')).query_selector('p:nth-child(2)')).get_attribute('data-rating'),
                'reviews': reviews.replace(' reviews', '')
            })
        await browser.close()
    return products