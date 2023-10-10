# coding=utf-8

import os
import codecs
import subprocess

# Отримання повного шляху до теки, з якої був запущений скрипт
bat_folder = os.path.dirname(os.path.abspath(__file__)).split("\\")
bat_folder_sl = "\\\\".join(bat_folder)

bat_folder.append('FaceSaver.bat')

save_face_path = "\\\\".join(bat_folder)


reg_file_name = 'save_face_context_menu.reg'

print(save_face_path, bat_folder_sl)

# Створення вмісту файлу .reg в кодуванні UTF-16LE з BOM
reg_content = f"""Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\*\shell\FaceSaver]
@="Зберегти обличчя"

[HKEY_CLASSES_ROOT\*\shell\FaceSaver\command]
@="\\"{save_face_path}\\" \\"%1\\" \\"{bat_folder_sl}\\""
"""

# Збереження файлу .reg в кодуванні UTF-16LE з BOM
with codecs.open(reg_file_name, 'w', encoding='utf-16-le') as reg_file:
    reg_file.write(u'\ufeff')
    reg_file.write(reg_content)

print(f"Файл {reg_file_name} успішно створений в кодуванні UTF-16LE з BOM.")


# Запустити файл .reg
subprocess.run(['regedit.exe', '/s', reg_file_name])

print(f"Файл {reg_file_name} був успішно запущений.")