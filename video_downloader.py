# video_downloader.py
import os
from pathlib import Path
from threading import Event
from utils import AuxMetodos, download_with_ffmpeg
from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError
from concurrent.futures import ThreadPoolExecutor

class VideoDownloader:
    def __init__(self):
        self.user_data = r'C:\Users\sky\AppData\Local\Microsoft\Edge\User Data'
        self.chrome_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
        self.video_links = []
        self.aux = AuxMetodos()  # Instancia de la clase auxiliar
        self.video_found = False
        self.video_found_event = Event()

    def download_from_links(self, links, course_name, destination_folder, start_index):
        course_path = Path(destination_folder) / course_name.lower().replace(':', '-')
        course_path.mkdir(parents=True, exist_ok=True)

        with ThreadPoolExecutor(max_workers=2) as executor:
            for link_index, link in enumerate(links[start_index:], start=start_index):
                if link.endswith('.m3u8'):
                    executor.submit(self.download_m3u8, link, course_path, link_index)
                else:
                    full_link = 'https://cursos.devtalles.com' + link
                    executor.submit(self.download_video, full_link, course_path, link_index, len(links))
                self.video_found_event.wait()  # Esperar a que el video actual se descargue completamente
        course_url_prefix = 'https://cursos.devtalles.com'
        course_path = Path(destination_folder) / course_name.lower().replace(':', '-')
        course_path.mkdir(parents=True, exist_ok=True)

        with ThreadPoolExecutor(max_workers=2) as executor:
            for link_index, link in enumerate(links[start_index:], start=start_index):
                full_link = course_url_prefix + link
                self.video_found = False
                self.video_found_event.clear()

                executor.submit(self.download_video, full_link, course_path, link_index, len(links))
                self.video_found_event.wait()  # Esperar a que el video actual se descargue completamente
    def download_m3u8(self, link, course_path, link_index):
        file_name_from_url = link.split("/")[-1]
        valid_file_name = self.aux.clean_file_name("-".join(file_name_from_url.split("-")[1:]))

        destination = course_path / f"{link_index} {valid_file_name}.mp4"

        if os.path.exists(str(destination)):
            print(f"El archivo {destination} ya existe. Saltando descarga.")
            return

        print("Enlace de video encontrado:", link)
        download_with_ffmpeg(link, str(destination))
    def _handle_requests(self, page, request, course_path, link_index, course_url):
        if self.video_found:
            return

        if request.url.startswith('https://fast.wistia.com/embed/medias') and request.url.endswith('.m3u8'):
            self.video_links.append(request.url)

            file_name_from_url = course_url.split("/")[-1]
            valid_file_name = self.aux.clean_file_name("-".join(file_name_from_url.split("-")[1:]))

            destination = course_path / f"{link_index} {valid_file_name}.mp4"

            if os.path.exists(str(destination)):
                print(f"El archivo {destination} ya existe. Saltando descarga.")
                self.video_found = True
                self.video_found_event.set()
                return

            print("Enlace de video encontrado:", request.url)
            self.video_found = True
            download_with_ffmpeg(request.url, str(destination))
            self.video_found_event.set()

    def download_video(self, link, course_path, link_index, total_links):
        with sync_playwright() as p:
            context = p.chromium.launch_persistent_context(
                user_data_dir=self.user_data, executable_path=self.chrome_path, headless=True)

            try:
                print(f"\nProcesando enlace {link_index+1}/{total_links}: {link}")

                self.video_found = False
                self.video_found_event.clear()

                page = context.new_page()
                self._get_iframe_src_and_download(link, course_path, page, link_index+1, total_links)

                # Esperar a que el video actual se descargue completamente o se detecte que no hay video
                self.video_found_event.wait()

            except Exception as e:
                print(f"Error procesando {link}: {e}")

            finally:
                context.close()

    def _get_iframe_src_and_download(self, course_url, course_path, page, link_index, total_links):
        try:
            print(f"\nProcesando enlace {link_index+1}/{total_links}: {course_url}")

            self.video_found = False
            self.video_found_event.clear()

            request_handler = lambda request: self._handle_requests(
                page, request, course_path, link_index, course_url)
            page.on("request", request_handler)

            max_attempts = 3 if 'lesson' in course_url else 1

            for attempt in range(max_attempts):
                page.goto(course_url, timeout=30000)

                if self.video_found:
                    break

                if attempt < max_attempts - 1:
                    page.wait_for_timeout(6000)

            if not self.video_found:
                print(f"La clase en {course_url} no tiene video. Continuando con el siguiente enlace.")

        except TimeoutError:
            if not self.video_found:
                print(f"Error de tiempo de espera procesando {course_url} pero no se encontró ningún video.")

        except Exception as e:
            print(f"Error procesando {course_url}: {e}")

        finally:
            page.close()
            # Señalar que el video actual se ha manejado completamente
            self.video_found_event.set()
