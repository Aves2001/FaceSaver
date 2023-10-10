import dlib
import cv2
import os
import sys
import numpy as np

# Ініціалізація детектора облич та предиктора ключових точок

detector = dlib.get_frontal_face_detector()


def find_faces(image_path):
    img = cv2.imread(image_path)
    faces = detector(img)
    return faces


def get_landmarks(image, face, predictor):
    landmarks = predictor(image, face)
    return landmarks


def show(image_input, landmarks):
    landmarks_array = np.array([[p.x, p.y] for p in landmarks.parts()])
    for (x, y) in landmarks_array:
        cv2.circle(image_input, (x, y), 2, (0, 255, 0), -1)  # Малюємо круги на точках


def align_face(face, image, landmarks, output_size=(449, 361)):
    offset_y = 40
    image_shifted = np.roll(image, offset_y, axis=0)
    face_chip = dlib.get_face_chip(image_shifted, landmarks, size=600, padding=1.20)
    # return face_chip
    # Отримуємо чіп обличчя з врахуванням оригінального масштабу та розміру 449x449
    # face_chip = dlib.get_face_chip(image, landmarks, size=449, padding=0.60)

    # Розширюємо границі чіпа обличчя до розміру 361x449
    target_size = (361, 449)
    extended_face_chip = cv2.getRectSubPix(face_chip, target_size, (face_chip.shape[1] / 2, face_chip.shape[0] / 2))

    return extended_face_chip


def process_image(input_image_path, output_directory, predictor):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    image = cv2.imread(input_image_path)

    if image is None:
        print("\n\nНе вдалось відкрити файл")
        print(f"Будь ласка перейменуйте файл {output_directory}. Наприклад в: 001\n")
        exit()

    faces = find_faces(input_image_path)

    if len(faces) == 0:
        print(f"Не знайдено обличч на цьому фото {input_image_path}")
        return
    ########################
    sorted_faces = sorted(faces, key=lambda rect: (rect.top(), rect.left()))



    count_image = 0
    for face in sorted_faces:
        if face is not None:
            count_image += 1
            landmarks = get_landmarks(image, face, predictor)
            # show(image, landmarks)
            align = align_face(face, image, landmarks)

            filename = f"foto_{count_image}.jpg"
            output_path = os.path.join(output_directory, filename)

            # Запис зображення
            success = cv2.imwrite(output_path, align, [int(cv2.IMWRITE_JPEG_QUALITY), 95])

            if success:
                print(f"Зображення {filename} успішно збереженно.")
            else:
                print(f"Помилка: Не вдалося збереженно зображення {filename}.")

    print(f"\nВсі фото збереженно в папці \"{output_directory}\", їх загальна кількість: {count_image}\n")
##########

    


if __name__ == "__main__":
    print("-------------------------------------------------")
    print("Зачекайте буль ласка, програма завантажується...")
    output_faces_path = sys.argv[1].split("\\")[-1].split(".")[0]
    predictor = dlib.shape_predictor(f'{sys.argv[2]}\\shape_predictor_68_face_landmarks.dat')
    process_image(sys.argv[1], output_faces_path, predictor)

