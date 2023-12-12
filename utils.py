# utils.py
import re
import subprocess
from pathlib import Path


class AuxMetodos:
    def clean_file_name(self, file_name: str) -> str:
        """Limpia el nombre de archivo eliminando caracteres no deseados."""
        cleaned_name = ''.join(char for char in file_name if char.isalnum() or char in [' ', '-'])
        cleaned_name = ' '.join(cleaned_name.split())
        return cleaned_name[:200]  # Limitar a 200 caracteres

    def get_class_name(self, page) -> str:
        """Extrae el nombre de la clase basándose en un selector CSS específico."""
        try:
            class_name_element = page.query_selector(".content-item__title")
            if class_name_element:
                return class_name_element.text_content().strip()
        except Exception as e:
            print(f"Error al obtener el nombre de la clase: {e}")
        return "unknown_class"


def download_with_ffmpeg(url, destination):
    """Download video using ffmpeg with compression."""
    cmd = ['ffmpeg', '-i', url, '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-c:a', 'aac', '-strict',
           'experimental', destination]

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

                print(f"\rProgress: {progress:.2f}%", end="")

        process.communicate()
        print(" ")
        print("\nVideo downloaded successfully at", destination)
        print(" ")

    except Exception as e:
        print(f"\nError downloading video: {e}")

        """Download video using ffmpeg."""
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
