from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import sys


def caesar_encrypt(text, shift):
    encrypted = ""
    for char in text:
        if char.isalpha():
            shift_amount = shift % 26
            new_char = chr((ord(char) - 65 + shift_amount) % 26 + 65) if char.isupper() else chr(
                (ord(char) - 97 + shift_amount) % 26 + 97)
            encrypted += new_char
        else:
            encrypted += char
    return encrypted


def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)


def crack_caesar_cipher(encrypted_text):
    best_shift = None
    best_score = float('-inf')
    english_letter_frequency = "etaoinshrdlu"  # Частые буквы в английском

    for shift in range(1, 26):
        decrypted_text = caesar_decrypt(encrypted_text, shift)
        score = sum(decrypted_text.count(letter) for letter in english_letter_frequency)

        # Находим лучший сдвиг по оценке
        if score > best_score:
            best_score = score
            best_shift = shift

    if best_shift is not None:
        return best_shift, caesar_decrypt(encrypted_text, best_shift)


class CaesarCipherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Caesar Cipher Tool')

        layout = QVBoxLayout()

        self.label_text = QLabel('Введите текст для шифрования (англ.):')
        self.text_input = QLineEdit(self)

        self.label_shift = QLabel('Введите значение сдвига (shift):')
        self.shift_input = QLineEdit(self)

        self.encrypt_button = QPushButton('Зашифровать и проанализировать', self)
        self.encrypt_button.clicked.connect(self.process_text)

        self.result_label = QLabel('Результаты:')

        layout.addWidget(self.label_text)
        layout.addWidget(self.text_input)
        layout.addWidget(self.label_shift)
        layout.addWidget(self.shift_input)
        layout.addWidget(self.encrypt_button)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def process_text(self):
        text = self.text_input.text()
        shift = self.shift_input.text()

        try:
            shift = int(shift)
            encrypted_text = caesar_encrypt(text, shift)
            decrypted_text = caesar_decrypt(encrypted_text, shift)
            cracked_results = crack_caesar_cipher(encrypted_text)

            results = (
                f'Зашифрованный текст: {encrypted_text}\n'
                f'Расшифрованный текст: {decrypted_text}\n'
                f'Лучшее совпадение (shift={cracked_results[0]}): {cracked_results[1]}'
            )
            self.result_label.setText(results)

        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Введите корректное значение для сдвига!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CaesarCipherApp()
    ex.show()
    sys.exit(app.exec_())
