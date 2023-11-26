from link_extractor import LinkExtractor
from video_downloader import VideoDownloader  
import subprocess


base_url = "https://cursos.devtalles.com" 


def main():

    kill_edge_processes()

    # Solicita al usuario que introduzca un enlace
    print(" ")
    url = input("Por favor, introduzca el enlace del curso: ")
    # Pide al usuario más información necesaria para la descarga
    print(" ")
    course_name = input("Por favor, introduzca el nombre del curso: ")
    print(" ")
    destination_folder = input("Por favor, introduzca la carpeta de destino para los videos: ")
    print(" ")
    # Crea una instancia de la clase LinkExtractor y obtiene los enlaces
    
    extractor = LinkExtractor()
    links = extractor.get_links(url)

    full_links = [base_url + link for link in links]
    
    # Crea una instancia de VideoDownloader y descarga los videos de los enlaces
    downloader = VideoDownloader()
    downloader.download_from_links(full_links, course_name, destination_folder)

def kill_edge_processes():
    try:
        print(" ")
        subprocess.run(["taskkill", "/F", "/IM", "msedge.exe", "/T"], check=True)
        print(" ")
    except subprocess.CalledProcessError:
        print(" ")
        print("No se encontraron procesos de Microsoft Edge en ejecución.")
        print(" ")
if __name__ == "__main__":
    main()
