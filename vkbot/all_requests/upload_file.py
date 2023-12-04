import requests
import io


def upload_file(url, file_path, max_chunk_size):
    with open(file_path, 'rb') as file:
        file_size = len(file.read())
        file.seek(0)  # Вернем указатель на начало файла

        chunk_number = 1
        returning_value = 0
        while True:
            chunk_data = file.read(max_chunk_size)
            if not chunk_data:
                break  # Если файл закончился, прекращаем цикл

            response = requests.post(url, data=chunk_data)

            if response.json().get('next_url'):
                url = response.json().get('next_url')
                print(f"Часть {chunk_number} загружена успешно.")
            else:
                returning_value = response.text
                print(response.text)
            chunk_number += len(chunk_data)
        if returning_value:
            return returning_value
            
def upload_file_without_download(url, file_content, max_chunk_size):
    file_size = len(file_content)

    chunk_number = 1
    offset = 0
    while offset < file_size:
        end_byte = offset + max_chunk_size
        chunk_data = file_content[offset:end_byte]
        
        response = requests.post(url, data=chunk_data)

        if response.json().get('next_url'):
            url = response.json().get('next_url')
            print(f"Часть {chunk_number} успешно загружена.")
        else:
            print(response.text)

        chunk_number += 1
        offset += max_chunk_size


upload_url = "https://drive-b.amocrm.ru/v1.0/sessions/upload/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODk5NjEyNDYsImlhdCI6MTY4OTg3NDg0NiwibmJmIjoxNjg5ODc0ODQ2LCJhY2NvdW50X2lkIjoyODg2MTU3MCwic2Vzc2lvbl9pZCI6ODQ3NTE2NjEsImNvbnRlbnRfaWQiOiIxYmNhN2QzZC00MjJkLTQ2OTYtYTJjMS05MGY4YTg5OTY5NDciLCJjb250ZW50X3NpemUiOjYzMTE1NzYsIm5vZGVfaWQiOiIyNWE5YWM1MC0xZTUzLTQ2MjEtOGNiYS04MjkxZmFjMjU0OGYiLCJ1c2VyX2lkIjoxMTQwNDIzLCJ1c2VyX3R5cGUiOiJpbnRlcm5hbCIsInBhcnRfbnVtIjoxfQ.8U0Ov2OJdVOBlc7xy0ecvnFeBdJaH5Vgqg8aQ68ZPcY"
file_path_to_upload = "aaa1.txt"  # Замените на путь к вашему текстовому файлу

