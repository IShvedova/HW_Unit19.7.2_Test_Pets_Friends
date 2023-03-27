from api import PetFriends
from settings import valid_email, valid_password, invalid_password, invalid_email
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
#Получение ключа с валидными данными. Базовый положительный сценарий

    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_api_key_for_invalid_user_psw(email=valid_email, password=invalid_password):
# Получение ключа с не валидным паролем. Негативный сценарий

    status, result = pf.get_api_key(email, password)
    print(result)
    assert status == 403


def test_get_api_key_for_invalid_user_email(email=invalid_email, password=valid_password):
# Получение ключа с не валидным email. Негативный сценарий

    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_all_pets_with_valid_key(filter=''):
#Получение списка питомцев с валидным ключом. Базовый позитивный сценарий.

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Тузик', animal_type='Дворняга', age='2', pet_photo='images/photo_dog.jpeg'):
# Добавление питомца с валидными данными. Базовый позитивный сценарий.

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_invalid_photo_txt(name='Тузик', animal_type='Дворняга', age='2', pet_photo='images/photo_dog_invalid.txt'):
# Добавление питомца с не валидным фото. Негативный сценарий.

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_successful_delete_pet():
# Удаление питомца. Базовый позитивный сценарий.
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Супердог", "Дог", "3", "images/photo_dog.jpeg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_delete_of_deleted_pet():
# Удаление уже удаленного питомца. Негативный сценарий
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Супердог", "Дог", "3", "images/photo_dog.jpeg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Tuzik', animal_type='Жевастик', age=1):
#Обновление данных. Позитивный сценарий.

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.get_update_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_add_new_pet_without_photo(name='Барсик', animal_type='Тузямба', age='2'):
#Добавление питомца без фото. Базовый позитивный сценарий.

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_long_name(animal_type='Тузямба', age='2'):
# Добавление питомца с длинным именем. Базовый позитивный сценарий.

    name = """Тузик вышел погулять и поймал лягушку 
    вобщем Тузик молодец но нафиг мне лягушка
    лучше б Тузик притащил толстую курицу"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_special_characters_in_name(name='DoG_doG123!@#5647.,?#', animal_type='Тузямба', age='2'):
#Добавление питомца со спецсимволами в имени. Позитивный сценарий.

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_only_numbers_in_name(name='12345678', animal_type='Тузямба', age='2'):
#Добавление питомца с целыми числами в имени. Негативный сценарий.

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 400
    assert result['name'] != name


def test_add_new_pet_with_age_not_number(name='Барсик', animal_type='Тузямба', age='twelve'):
#Добавление питомца с возрастом не числовые значения. Негативный сценарий.
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 400
    assert result['age'] == age


def test_successful_add_photo_of_pet(pet_photo='images/photo_dog.jpeg'):
#Добавление фото. Позитивный сценарий.
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200
        assert 'pet_photo' in result
    else:
        raise Exception("There is no my pets")
