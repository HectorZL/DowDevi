from link_extractor import LinkExtractor
from video_downloader import VideoDownloader  
import subprocess
import asyncio
from playwright.async_api import async_playwright

base_url_dev = "https://cursos.devtalles.com" 
base_url_skill = "https://www.skillshare.com"

async def main():

    kill_edge_processes()

    # Solicita al usuario que introduzca un enlace
    print(" ")
    #url = input("Por favor, introduzca el enlace del curso: ")
    url='https://www.skillshare.com/es/classes/inteligencia-artificial-para-principiantes-como-funciona-chatgpt/360552099'
    # Pide al usuario más información necesaria para la descarga
    print(" ")
    course_name = input("Por favor, introduzca el nombre del curso: ").strip()
    print(" ")
    #destination_folder = input("Por favor, introduzca la carpeta de destino para los videos: ").strip().strip('"')
    destination_folder = "C:\\Users\\Sky\\Documents\\prueba"
    print(" ")
    # Crea una instancia de la clase LinkExtractor y obtiene los enlaces
    
    validador = input('''
                      
    (Desea retomar la descarga desde un video en especifico)
    (--- Si )
    (--- No )
                      ''')
    if(validador=='1'or validador=='Si'or validador=='si' or validador=='SI'or validador== 1):
        start_index = int(input('''
                      
    (Introduzca el numero del video desde el cual desea retomar la descarga:
                                
                      '''))
    else:
        start_index=0
        
    extractor = LinkExtractor()
    try:
     links = await extractor.get_links(url)
    except Exception as e:
     print(f"Ocurrió un error: {e}")
     links = []  # Asigna un valor vacío a links en caso de error

    if 'devtalles' in url:
        base_url = base_url_dev
        full_links = [base_url + link for link in links]
    else:
        full_links = links  # Asigna el valor de links a full_links# Asigna el primer elemento de la tupla a full_links
    
    
    downloader = VideoDownloader()
    downloader.download_from_links(full_links, course_name, destination_folder, start_index)

def kill_edge_processes():
    try:
        subprocess.run(["tasklist", "/FI", "IMAGENAME eq msedge.exe"], check=True)
        subprocess.run(["taskkill", "/F", "/IM", "msedge.exe", "/T"], check=True)
    except subprocess.CalledProcessError:
        print()

        
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())