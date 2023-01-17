from playwright.sync_api import sync_playwright


URLS_PRODUCTS = (
    ('computers', 'computers'),
    ('laptops', 'computers/laptops'),
    ('tablets', 'computers/tablets'),
    ('phones', 'phones'),
    ('touch', 'phones/touch')
)


def get_products(url: str = '') -> list:
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
    with sync_playwright() as p:
        browser = p.firefox.launch()
        context = browser.new_context(
            base_url='https://webscraper.io/test-sites/e-commerce/allinone/'
        )
        page = context.new_page()
        page.goto(url)
        cards = page.query_selector_all('div.thumbnail')
        
        products = []
        
        for card in cards:
            products.append({
                'thumbnail': card.query_selector('.img-responsive').get_attribute('src'),
                'name': card.query_selector('.title').get_attribute('title'),
                'price': float(card.query_selector('.price').text_content().replace('$', '')),
                'description': card.query_selector('.description').text_content(),
                'p_range': card.query_selector('.ratings').query_selector('p:nth-child(2)').get_attribute('data-rating'),
                'reviews': card.query_selector('.ratings').query_selector('.pull-right').text_content().replace(' reviews', '')
            })
        browser.close()
    return products