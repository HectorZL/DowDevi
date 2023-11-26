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
