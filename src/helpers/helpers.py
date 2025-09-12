import os


def return_image(game_id):
    image_path = f'src/static/images/{game_id}.jpg'
    if os.path.isfile(image_path):
        return f'{game_id}.jpg'
    return 'capa_padrao.jpg'


def remove_image(game_id):
    image_path = f'src/static/images/{game_id}.jpg'
    if os.path.isfile(image_path):
        os.remove(image_path)
