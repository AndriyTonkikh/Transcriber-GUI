import sys
import os
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from pydub import AudioSegment
import wave
import speech_recognition as sr

class MediaSelector(QWidget):
    def __init__(self, parent=None):
        super(MediaSelector, self).__init__(parent)

        # Встановлення розміру та заголовку вікна
        self.setGeometry(100, 100, 600, 450)
        self.setWindowTitle('TRANSCRIBER')
        
        # Встановлення стилів
        self.setStyleSheet("""
            QWidget {
                font-family: "Playfair Display";
                background-color: #333333;
                color: #ffff00;
            }
            QPushButton {
                background-color: #ffff00;
                color: #333333;
            }
            QPushButton:hover {
                background-color: #dddd00;
            }
            QTextEdit {
                background-color: #666666;
                color: #ffffff;
            }
            QProgressBar {
                background-color: #666666;
                color: #ffffff;
            }
            QComboBox {
                background-color: #ffff00;
                color: #333333;
            }
        """)

        # Встановлення кнопок для вибору та збереження файлу
        self.button_open = QPushButton('Open file', self)
        self.button_open.move(20, 20)
        self.button_open.clicked.connect(self.select_file)

        self.button_savetxt = QPushButton('Save txt', self)
        self.button_savetxt.move(440, 20)
        self.button_savetxt.clicked.connect(self.save_to_file)

        # Встановлення віджета для виведення результата функції
        self.result = QTextEdit(self)
        self.result.setReadOnly(True)
        self.result.setText("""Кнопка Open file:
        Відкриття діалогового вікна для вибору медіа-файлу (формат *.mp3, *.mp4, *.avi, *.wmv).
        
    Кнопка Save txt:
        Збереження транскрибованого тексту в текстовий файл.
        
    Кнопка Transcribe:
        Активація функції транскрибування медіа-файлу.
        
    Кнопка Save wav:
        Збереження аудіо-файлу у форматі *.wav.
        
    Кнопка Clear:
        Очищення вікна для виведення результату функції.
        
    Кнопка вибору мови:
        Вибір мови для транскрибування медіа-файлу. Доступні мови: UA - українська, ENG - англійська, ru - російська.
        
                            """)
        self.result.setGeometry(20, 50, 550, 310)
        
        # Встановлення кнопок для активації функції транскрибування
        self.button_transcribe = QPushButton('Transcribe', self)
        self.button_transcribe.move(150, 20)
        self.button_transcribe.clicked.connect(self.transcribe_file)
        
        # Встановлення кнопки збереження файлу
        self.button_savewav = QPushButton('Save wav', self)
        self.button_savewav.move(295, 20)
        self.button_savewav.clicked.connect(self.save_to_wav)
        
        # Встановлення кнопки очищення поля виводу
        self.button_clear = QPushButton('Clear', self)
        self.button_clear.move(20, 380)
        self.button_clear.clicked.connect(self.clear_window)
        
        # Встановлення прогресбару
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(20, 414, 550, 20)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        
        # Встановлення кнопки вибору мови для транскрибування
        self.comboBox = QComboBox(self)
        self.comboBox.move(150, 380)
        self.comboBox.addItem("UA")
        self.comboBox.addItem("ENG")
        self.comboBox.addItem("ru")
        self.comboBox.currentIndexChanged.connect(self.set_selected_param)


        # Ініціалізація змінних
        self.filename = ''
        self.filepath = ''
        
        

   
    def select_file(self):
        self.result.setText("")
        """Обробка натиснення кнопки для вибору файлу"""
        self.filename, self.filetype = QFileDialog.getOpenFileName(self, 'Виберіть медіа-файл', os.getenv('HOME'), 'Media files (*.mp3 *.mp4 *.avi *.wmv)')
        print(self.filename)
        self.pathtofile = self.filename
        
        self.filepath, self.filename = os.path.split(self.filename)
        try:
                audio = AudioSegment.from_file(self.pathtofile)
                duration = len(audio) / 1000  # duration in seconds
                size = os.path.getsize(self.pathtofile)
                bit_rate = audio.frame_rate
                self.media_info =  f"'duration': {duration} sec, 'size': {size}bytes, 'bit_rate': {bit_rate}"
        except Exception as e:
                self.result.append(f"Error getting media info: {e}")
            
        if self.filepath:
            if self.media_info:
                self.result.append(f"Обраний файл:\n{self.pathtofile} \n\nМедіаінфо:\n\n{self.media_info}")
            else:
                self.result.append('Не вдалося отримати інформацію про медіа-файл.\n' + self.result.toPlainText())
        else:
                self.result.append('Спочатку виберіть медіа-файл.\n' + self.result.toPlainText())
    
    def set_selected_param(self, option):
        lang = "uk-UA"
        if option == 1:
            lang = "en-GB"
        elif option == 2:
            lang = "ru-Ru"

        self.lang = lang
        return lang
            
    def save_to_file(self):
        """Обробка натиснення кнопки для збереження даних у файл"""
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'Text Files (*.txt)')
        if file_name:
            with open(file_name, 'w') as f:
                f.write(self.result.toPlainText())
                
        self.result.clear()
        self.result.append(f"File is saved like {file_name}.txt")
            
    def save_to_wav(self):
        
        if self.pathtofile:
            sound = AudioSegment.from_file(self.pathtofile)
            output_file, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'Wav Files (*.wav)')
            sound.export(output_file, format="wav")
            self.result.append(f"\nFile is saved like {output_file}.wav")
        else:
            self.result.append(f"You need to choose file to transfer before ")
        
        
       

    def transcribe_file(self):
        
        self.result.clear()
        self.result.append("Starting ...\n\nChoose language ")
        if self.pathtofile == '':
            # QMessageBox.warning(self, 'Warning', 'No file selected!')
            return
        if not self.pathtofile.lower().endswith(('.mp3', '.mp4', '.avi', '.wmv')):
            # QMessageBox.warning(self, 'Warning', 'Invalid file format!')
            return
        
        audio = AudioSegment.from_file(self.pathtofile)
        output_file_path = 'output'
        audio.export(output_file_path, format='wav')
        
        with wave.open(output_file_path, 'rb') as input_file:
            # Отримання параметрів аудіофайлу
            sample_width = input_file.getsampwidth()
            frame_rate = input_file.getframerate()
            n_channels = input_file.getnchannels()
            n_frames = input_file.getnframes()

            # Обрахунок кількості частин, на які буде розбито аудіофайл
            segment_length = 59 * frame_rate
            n_segments = n_frames // segment_length
            self.result.append(f"\n\nNumbers of chunks : {n_segments}")

            # Ітерування по всіх частинах і запис кожної в окремий файл
            for i in range(n_segments):
                # Відкриття вихідного файлу
                output_file_path = f"_{i}"
                with wave.open(output_file_path, 'wb') as output_file:
                    output_file.setparams((n_channels, sample_width, frame_rate, segment_length, 'NONE', 'not compressed'))

                    # Копіювання відповідної частини аудіофайлу в вихідний файл
                    input_file.setpos(i * segment_length)
                    output_file.writeframes(input_file.readframes(segment_length))

                    # recognize speech in chunk
                    try:
                        r = sr.Recognizer()
                        with sr.AudioFile(output_file_path) as source:
                            audio_data_chunk = r.record(source)
                            text = r.recognize_google(audio_data_chunk, language=self.lang, show_all=False)
                            self.result.append(f"Segment {i+1}/{n_segments}: \n{text}")
                            # тут оновлюється прогресбар
                            self.progress_bar.setValue((i+1) * 100 // n_segments)
                            
                    except Exception as e:
                        self.result.append(f"Error {e}")
                    

            

    

   


    def closeEvent(self, event):
            """Обробка закриття вікна"""
            
            reply = QMessageBox.question(self, 'Message', 'Sure to quit?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                event.accept()
            else:
                event.ignore()
                
    def clear_window(self):
            self.result.setText(" ")
            for file in os.listdir('.'):
                if file.endswith('.wav'):
                    os.remove(file)
            
            
                
    
        



app = QApplication(sys.argv)
selector = MediaSelector()
selector.show()

sys.exit(app.exec())