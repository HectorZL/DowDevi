import os
import re
import subprocess
from pathlib import Path
from aux_metodos import AuxMetodos
from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError
from concurrent.futures import ThreadPoolExecutor

class VideoDownloader:
    def __init__(self):
        self.user_data = r'C:\Users\jesuc\AppData\Local\Microsoft\Edge\User Data'
        self.chrome_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
        self.video_links = []
        self.aux = AuxMetodos()  # Instancia de la clase auxiliar
        self.video_found = False

    def _download_with_ffmpeg(self, url, destination):
        """Descargar video usando ffmpeg."""
        cmd = ['ffmpeg', '-i', url, '-c', 'copy', '-bsf:a', 'aac_adtstoasc', destination]

        duration_pattern = re.compile(r"Duration: (\d{2}:\d{2}:\d{2}\.\d{2})")
        duration = None

        time_pattern = re.compile(r"time=(\d{2}:\d{2}:\d{2}\.\d{2})")

        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

            for line in iter(process.stdout.readline, ""):
                if duration is None:
                    duration_match = duration_pattern.search(line)
                    if duration_match:
                        duration = sum(float(x) * 60 ** i for i, x in enumerate(reversed(duration_match.group(1).split(":"))))

                time_match = time_pattern.search(line)
                if time_match and duration:
                    time = sum(float(x) * 60 ** i for i, x in enumerate(reversed(time_match.group(1).split(":"))))
                    progress = (time / duration) * 100

                    print(f"\rProgreso: {progress:.2f}%", end="")

            process.communicate()
            print(" ")
            print("\nVideo descargado con éxito en", destination)
            print(" ")

        except Exception as e:
            print(f"\nError al descargar video: {e}")

    def download_video(self, link, course_path, link_index, total_links):
        with sync_playwright() as p:
            context = p.chromium.launch_persistent_context(
                user_data_dir=self.user_data, executable_path=self.chrome_path, headless=True)

            try:
                print(" ")
                print(f"Procesando enlace {link_index + 1}/{total_links}: {link}")

                self.video_found = False

                page = context.new_page()
                self._get_iframe_src_and_download(link, course_path, page, link_index, total_links)

            except Exception as e:
                print(f"Error procesando {link}: {e}")

            finally:
                context.close()

    def download_from_links(self, links, course_name, destination_folder):
        course_path = Path(destination_folder) / course_name.lower().replace(':', '-')
        course_path.mkdir(parents=True, exist_ok=True)

        with ThreadPoolExecutor(max_workers=2) as executor:
            for link_index, link in enumerate(links):
                self.video_found = False
                executor.submit(self.download_video, link, course_path, link_index, len(links))
                while not self.video_found:
                    pass  # Esperar a que el video actual se descargue completamente

    def _handle_requests(self, page, request, course_path, link_index, course_url):
        if self.video_found:
            return

        if request.url.startswith('https://fast.wistia.com/embed/medias') and request.url.endswith('.m3u8'):
            self.video_links.append(request.url)

            file_name_from_url = course_url.split("/")[-1]
            valid_file_name = self.aux.clean_file_name("-".join(file_name_from_url.split("-")[1:]))

            destination = course_path / f"{link_index + 1} {valid_file_name}.mp4"

            if os.path.exists(str(destination)):
                print(f"El archivo {destination} ya existe. Saltando descarga.")
                self.video_found = True
                return

            print("Enlace de video encontrado:", request.url)
            self.video_found = True
            self._download_with_ffmpeg(request.url, str(destination))

    def _get_iframe_src_and_download(self, course_url, course_path, page, link_index, total_links):
        try:
            print(" ")
            print(f"Procesando enlace {link_index + 1}/{total_links}: {course_url}")

            self.video_found = False

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

            if self.video_found:
                page.wait_for_timeout(6000)

            if not self.video_found:
                print(f"La clase en {course_url} no tiene video.")

        except TimeoutError:
            if not self.video_found:
                print(
                    f"Error de tiempo de espera procesando {course_url} pero no se encontró ningún video.")

        except Exception as e:
            print(f"Error procesando {course_url}: {e}")

        finally:
            page.close()

