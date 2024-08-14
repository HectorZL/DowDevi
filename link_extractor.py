from playwright.sync_api import sync_playwright
import random
import asyncio
from playwright.async_api import async_playwright

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0"
]

user_agent = random.choice(user_agents)
class LinkExtractor:
    def __init__(self):
        self.user_data = r'C:\Users\Sky\AppData\Local\Microsoft\Edge\User Data'
        self.chrome_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
        self.selectors = {
            'devtalles': 'a.course-player__content-item__link',
         'skillshare': 'li.session-item'
        }
    
    async def get_links(self, url_curso: str) -> list:
        found_links = []
        m3u8_links = []
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch_persistent_context(user_data_dir=self.user_data, executable_path=self.chrome_path, headless=False, user_agent=user_agent)
                page = await browser.new_page()
                        
                await page.keyboard.press('Enter')  # Presiona la tecla Enter
                print("__"*50)
                print("")
                print("Navegando a la página...")
                await page.goto(url_curso)
                await page.wait_for_timeout(10000)  # Espera 30 segundos
                print("")
                print("Buscando enlaces en la página...")
                print("")
                print("__"*50)
                
                # Establece el evento de solicitud solo una vez
                page.on("request", lambda request: self.capture_netflow_event(request, m3u8_links))
            
                
                # Determina el selector a utilizar dependiendo de la página
                selector = self.get_selector(url_curso)
                                
                # Selector para la página
                link_elements = await page.query_selector_all(selector)
                for link_element in link_elements:
                    if 'devtalles' in url_curso:
                        found_links.append(link_element.get_attribute('href'))
                    elif'skillshare' in url_curso:
                        # Hacer clic en el enlace y esperar a que se cargue el contenido
                        await link_element.click()
                        await page.wait_for_timeout(2000)  # Espera 2 segundos
                
                        
                        # Espera a que se capture el evento
                        await page.wait_for_timeout(2000)  # Espera 1 segundo
                        
                        # Espera un segundo antes de continuar con el siguiente link
                        await page.wait_for_timeout(2000)  # Espera 1 segundo  

            if'skillshare' in url_curso:
                found_links = m3u8_links
        except Exception as e:
            print("Ocurrió un error al obtener los enlaces:", str(e))
        
        return found_links
    
    def get_selector(self, url_curso: str) -> str:
        for plataforma, selector in self.selectors.items():
            if plataforma in url_curso:
                return selector
        return None
    
    def capture_netflow_event(self, request, m3u8_links):
     # Verificar si el evento es un request a un archivo M3U8
     if request.url.endswith(".m3u8") and "manifest" in request.url:
         # Extraer el link del archivo M3U8 de la URL del evento
         m3u8_link = request.url + "?useVODOTFE=false"
         # Agregar el link a la lista de links M3U8
         m3u8_links.append(m3u8_link)
        