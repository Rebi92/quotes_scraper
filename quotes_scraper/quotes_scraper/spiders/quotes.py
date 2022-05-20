from email.quoprimime import quote
from gc import callbacks
import scrapy

#Titulo  = //h1/a/text()
#Citas = //span[@class="text" and @itemprop="text"]/text()
#top ten tags = //div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()
#next page= //ul[@class="pager"]//li[@class="next"]/a/@href').get()


class QuotesSpider(scrapy.Spider):
    name= 'quotes'
    start_urls = ['https://quotes.toscrape.com/']
    custom_settings= {
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUESTS': 24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['raulbi_92@hotmail.com'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'PepitoMartinez',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }
    
    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            quotes= kwargs['quotes']
            author= kwargs['author']
        quotes.extend(response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall())
        author.extend(response.xpath('//small[@class="author" and @itemprop="author"]/text()').getall())
        #xpath donde se encuentra el boton
        next_page_button_link= response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        #comprobamos se existe
        if next_page_button_link:
            #sumamos la ruta relativa a la ruta principal y mandamos 
            #a correr nuevamente el metodo para extraer los datos de la pagina
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={
                'quotes': quotes,
                'author': author
            })
        else:
            yield{
                'author':author,
                'quotes': quotes
                
            }
            
            
    def parse(self, response):
        
        title= response.xpath('//h1/a/text()').get()    
        quotes= response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall() 
        author= response.xpath('//small[@class="author" and @itemprop="author"]/text()').getall()
        top_tags = response.xpath('//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()
        
        #getattr sirve para pasar argumentos por consola, si no llega ninigun argumento asigna None
        top= getattr(self, 'top', None)
        #validamos que exista el argumento
        if top:
            #transformamos a entero
            top= int(top)
            #y recortamos el diccionario del inidice 0 al indice top
            top_tags= top_tags[:top]
        
        yield {
            'title': title,
            'top_tags': top_tags
        }
        
        #xpath donde se encuentra el boton
        next_page_button_link= response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        #comprobamos se existe
        if next_page_button_link:
            #sumamos la ruta relativa a la ruta principal y mandamos 
            #a correr nuevamente el metodo para extraer los datos de la pagina
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={
                'quotes': quotes,
                'author': author
            })
        
        
    