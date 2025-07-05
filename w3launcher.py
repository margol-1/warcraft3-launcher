import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QDialog, QLineEdit, QHBoxLayout, QFrame, QComboBox, QGroupBox
from PySide6.QtCore import Qt, QSettings, QTranslator
from PySide6.QtGui import QPixmap, QFont, QColor, QPainter, QLinearGradient
class WButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(40)
        self.setCursor(Qt.PointingHandCursor)
        font = QFont()
        font.setBold(True)
        font.setPointSize(10)
        self.setFont(font)
        self.update_style()

    def update_style(self, theme="dark"):
        styles = {
            "dark": """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #c0a062, stop:0.5 #937341, stop:1 #6d4f27);
                    color: #ffdf94;
                    border: 2px solid #000000;
                    border-radius: 4px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #d0b072, stop:0.5 #a38351, stop:1 #7d5f37);
                    color: #ffffa4;
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #6d4f27, stop:0.5 #937341, stop:1 #c0a062);
                    padding: 6px 4px 4px 6px;
                }
            """,
            "light": """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #e0c082, stop:0.5 #b39361, stop:1 #8d6f47);
                    color: #2c2213;
                    border: 2px solid #6d4f27;
                    border-radius: 4px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #f0d092, stop:0.5 #c3a371, stop:1 #9d7f57);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #8d6f47, stop:0.5 #b39361, stop:1 #e0c082);
                    padding: 6px 4px 4px 6px;
                }
            """,
            "aqua": """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #6bb9f0, stop:0.5 #3498db, stop:1 #2980b9);
                    color: #ffffff;
                    border: 2px solid #1a5276;
                    border-radius: 6px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #7dc5f5, stop:0.5 #4aa3df, stop:1 #3d8fc7);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #2980b9, stop:0.5 #3498db, stop:1 #6bb9f0);
                    padding: 6px 4px 4px 6px;
                }
            """
        }
        self.setStyleSheet(styles.get(theme, styles["dark"]))

class WTitleBar(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(30)
        font = QFont()
        font.setBold(True)
        font.setPointSize(12)
        font.setFamily("Arial")
        self.setFont(font)
        self.update_style()

    def update_style(self, theme="dark"):
        styles = {
            "dark": """
                QLabel {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #2c2213, stop:1 #1a140b);
                    color: #ffdf94;
                    border-top-left-radius: 8px;
                    border-top-right-radius: 8px;
                    border-bottom: 2px solid #000000;
                }
            """,
            "light": """
                QLabel {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #d0c8b0, stop:1 #b0a890);
                    color: #2c2213;
                    border-top-left-radius: 8px;
                    border-top-right-radius: 8px;
                    border-bottom: 2px solid #6d4f27;
                }
            """,
            "aqua": """
                QLabel {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #5dade2, stop:1 #3498db);
                    color: #ffffff;
                    border-top-left-radius: 8px;
                    border-top-right-radius: 8px;
                    border-bottom: 2px solid #1a5276;
                }
            """
        }
        self.setStyleSheet(styles.get(theme, styles["dark"]))

class WFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.update_style()

    def update_style(self, theme="dark"):
        styles = {
            "dark": "QFrame {background-color: #1a140b; border: 2px solid #000000; border-radius: 8px;}",
            "light": "QFrame {background-color: #e0d8c0; border: 2px solid #6d4f27; border-radius: 8px;}",
            "aqua": "QFrame {background-color: #eaf2f8; border: 2px solid #3498db; border-radius: 8px;}"
        }
        self.setStyleSheet(styles.get(theme, styles["dark"]))

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.settings = QSettings("Warcraft3Launcher", "Settings")
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setFixedSize(400, 450)
        
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        self.paths_group = QGroupBox()
        self.settings_group = QGroupBox()
        
        self.roc_label = QLabel()
        self.roc_path_edit = QLineEdit()
        self.roc_btn = WButton()
        self.roc_btn.setFixedSize(70, 30)
        
        self.tft_label = QLabel()
        self.tft_path_edit = QLineEdit()
        self.tft_btn = WButton()
        self.tft_btn.setFixedSize(70, 30)
        
        self.theme_label = QLabel()
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("Dark", "dark")
        self.theme_combo.addItem("Light", "light")
        self.theme_combo.addItem("Aqua", "aqua")
        
        self.language_label = QLabel()
        self.language_combo = QComboBox()
        self.language_combo.addItem("English", "en")
        self.language_combo.addItem("Русский", "ru")
        self.language_combo.addItem("Español", "es")
        self.language_combo.addItem("한국어", "ko")
        self.language_combo.addItem("中文", "zh")
        self.language_combo.addItem("Українська", "uk")
        self.language_combo.addItem("Tiếng Việt", "vi")
        
        self.apply_btn = WButton()
        self.ok_btn = WButton("OK")
        self.cancel_btn = WButton()
        self.apply_btn.setFixedSize(85, 32)
        self.ok_btn.setFixedSize(85, 32)
        self.cancel_btn.setFixedSize(85, 32)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)
        main_layout.addWidget(self.title_label)
        main_layout.addSpacing(5)
        
        paths_layout = QVBoxLayout()
        paths_layout.setContentsMargins(8, 15, 8, 8)
        paths_layout.setSpacing(8)
        
        roc_layout = QHBoxLayout()
        self.roc_label.setFixedWidth(110)
        roc_layout.addWidget(self.roc_label)
        self.roc_path_edit.setMinimumWidth(180)
        roc_layout.addWidget(self.roc_path_edit)
        roc_layout.addWidget(self.roc_btn)
        paths_layout.addLayout(roc_layout)
        
        tft_layout = QHBoxLayout()
        self.tft_label.setFixedWidth(110)
        tft_layout.addWidget(self.tft_label)
        self.tft_path_edit.setMinimumWidth(180)
        tft_layout.addWidget(self.tft_path_edit)
        tft_layout.addWidget(self.tft_btn)
        paths_layout.addLayout(tft_layout)
        
        self.paths_group.setLayout(paths_layout)
        main_layout.addWidget(self.paths_group)
        
        settings_layout = QVBoxLayout()
        settings_layout.setContentsMargins(8, 15, 8, 8)
        settings_layout.setSpacing(10)
        
        theme_layout = QHBoxLayout()
        self.theme_label.setFixedWidth(110)
        theme_layout.addWidget(self.theme_label)
        self.theme_combo.setMinimumWidth(180)
        theme_layout.addWidget(self.theme_combo)
        settings_layout.addLayout(theme_layout)
        
        lang_layout = QHBoxLayout()
        self.language_label.setFixedWidth(110)
        lang_layout.addWidget(self.language_label)
        self.language_combo.setMinimumWidth(180)
        lang_layout.addWidget(self.language_combo)
        settings_layout.addLayout(lang_layout)
        
        self.settings_group.setLayout(settings_layout)
        main_layout.addWidget(self.settings_group)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.apply_btn)
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        main_layout.addLayout(btn_layout)
        
        self.setLayout(main_layout)
        
        self.roc_btn.clicked.connect(lambda: self.browse_path("roc"))
        self.tft_btn.clicked.connect(lambda: self.browse_path("tft"))
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        self.language_combo.currentIndexChanged.connect(self.change_language)
        self.apply_btn.clicked.connect(self.apply_settings)
        self.ok_btn.clicked.connect(self.ok_pressed)
        self.cancel_btn.clicked.connect(self.reject)
        
        self.update_style()
        self.retranslate_ui()

    def retranslate_ui(self):
        lang = self.settings.value("language", "en")
        translations = {
            "en": {
                "window_title": "Warcraft III Settings",
                "title": "Path Settings",
                "paths_group": "Game Paths",
                "settings_group": "Interface Settings",
                "roc_label": "Reign of Chaos:",
                "tft_label": "Frozen Throne:",
                "roc_btn": "Browse",
                "tft_btn": "Browse",
                "theme_label": "Theme:",
                "language_label": "Language:",
                "apply_btn": "Apply",
                "cancel_btn": "Cancel"
            },
            "ru": {
                "window_title": "Настройки Warcraft III",
                "title": "Настройки путей",
                "paths_group": "Пути к играм",
                "settings_group": "Настройки интерфейса",
                "roc_label": "Reign of Chaos:",
                "tft_label": "Frozen Throne:",
                "roc_btn": "Обзор",
                "tft_btn": "Обзор",
                "theme_label": "Тема:",
                "language_label": "Язык:",
                "apply_btn": "Применить",
                "cancel_btn": "Отмена"
            },
            "es": {
                "window_title": "Configuración Warcraft III",
                "title": "Configuración de rutas",
                "paths_group": "Rutas de juegos",
                "settings_group": "Configuración de interfaz",
                "roc_label": "Reign of Chaos:",
                "tft_label": "Frozen Throne:",
                "roc_btn": "Examinar",
                "tft_btn": "Examinar",
                "theme_label": "Tema:",
                "language_label": "Idioma:",
                "apply_btn": "Aplicar",
                "cancel_btn": "Cancelar"
            },
            "ko": {
                "window_title": "워크래프트 III 설정",
                "title": "경로 설정",
                "paths_group": "게임 경로",
                "settings_group": "인터페이스 설정",
                "roc_label": "Reign of Chaos:",
                "tft_label": "Frozen Throne:",
                "roc_btn": "찾아보기",
                "tft_btn": "찾아보기",
                "theme_label": "테마:",
                "language_label": "언어:",
                "apply_btn": "적용",
                "cancel_btn": "취소"
            },
            "zh": {
                "window_title": "魔兽争霸III设置",
                "title": "路径设置",
                "paths_group": "游戏路径",
                "settings_group": "界面设置",
                "roc_label": "混乱之治:",
                "tft_label": "冰封王座:",
                "roc_btn": "浏览",
                "tft_btn": "浏览",
                "theme_label": "主题:",
                "language_label": "语言:",
                "apply_btn": "应用",
                "cancel_btn": "取消"
            },
            "uk": {
                "window_title": "Налаштування Warcraft III",
                "title": "Налаштування шляхів",
                "paths_group": "Шляхи до ігор",
                "settings_group": "Налаштування інтерфейсу",
                "roc_label": "Reign of Chaos:",
                "tft_label": "Frozen Throne:",
                "roc_btn": "Огляд",
                "tft_btn": "Огляд",
                "theme_label": "Тема:",
                "language_label": "Мова:",
                "apply_btn": "Застосувати",
                "cancel_btn": "Скасувати"
            },
            "vi": {
                "window_title": "Cài đặt Warcraft III",
                "title": "Cài đặt đường dẫn",
                "paths_group": "Đường dẫn trò chơi",
                "settings_group": "Cài đặt giao diện",
                "roc_label": "Reign of Chaos:",
                "tft_label": "Frozen Throne:",
                "roc_btn": "Duyệt",
                "tft_btn": "Duyệt",
                "theme_label": "Chủ đề:",
                "language_label": "Ngôn ngữ:",
                "apply_btn": "Áp dụng",
                "cancel_btn": "Hủy"
            }
        }
        
        trans = translations.get(lang, translations["en"])
        self.setWindowTitle(trans["window_title"])
        self.title_label.setText(trans["title"])
        self.paths_group.setTitle(trans["paths_group"])
        self.settings_group.setTitle(trans["settings_group"])
        self.roc_label.setText(trans["roc_label"])
        self.tft_label.setText(trans["tft_label"])
        self.roc_btn.setText(trans["roc_btn"])
        self.tft_btn.setText(trans["tft_btn"])
        self.theme_label.setText(trans["theme_label"])
        self.language_label.setText(trans["language_label"])
        self.apply_btn.setText(trans["apply_btn"])
        self.cancel_btn.setText(trans["cancel_btn"])

    def update_style(self, theme=None):
        theme = theme or self.settings.value("theme", "dark")
        styles = {
            "dark": """
                QDialog {background-color: #1a140b; color: #ffdf94; border: 2px solid #000000;}
                QLabel {color: #ffdf94; font-weight: bold;}
                QLineEdit, QComboBox {background-color: #2c2213; color: #ffdf94; border: 2px solid #000000; padding: 4px;}
                QComboBox QAbstractItemView {background-color: #2c2213; color: #ffdf94;}
                QGroupBox {border: 1px solid #6d4f27; border-radius: 4px; margin-top: 10px; padding-top: 15px;
                          font-weight: bold; color: #ffdf94;}
                QGroupBox::title {subcontrol-origin: margin; left: 10px; padding: 0 3px;}
            """,
            "light": """
                QDialog {background-color: #e8e0c8; color: #2c2213; border: 2px solid #6d4f27;}
                QLabel {color: #2c2213; font-weight: bold;}
                QLineEdit, QComboBox {background-color: #f8f0d8; color: #2c2213; border: 2px solid #6d4f27; padding: 4px;}
                QComboBox QAbstractItemView {background-color: #f8f0d8; color: #2c2213;}
                QGroupBox {border: 1px solid #b39361; border-radius: 4px; margin-top: 10px; padding-top: 15px;
                          font-weight: bold; color: #2c2213;}
                QGroupBox::title {subcontrol-origin: margin; left: 10px; padding: 0 3px;}
            """,
            "aqua": """
                QDialog {background-color: #eaf2f8; color: #154360; border: 2px solid #3498db;}
                QLabel {color: #154360; font-weight: bold;}
                QLineEdit, QComboBox {background-color: #d4e6f1; color: #154360; border: 2px solid #3498db; padding: 4px;}
                QComboBox QAbstractItemView {background-color: #d4e6f1; color: #154360;}
                QGroupBox {border: 1px solid #5dade2; border-radius: 4px; margin-top: 10px; padding-top: 15px;
                          font-weight: bold; color: #154360;}
                QGroupBox::title {subcontrol-origin: margin; left: 10px; padding: 0 3px;}
            """
        }
        self.setStyleSheet(styles.get(theme, styles["dark"]))
        for btn in [self.roc_btn, self.tft_btn, self.apply_btn, self.ok_btn, self.cancel_btn]:
            btn.update_style(theme)

    def load_settings(self):
        self.roc_path_edit.setText(self.settings.value("roc_path", ""))
        self.tft_path_edit.setText(self.settings.value("tft_path", ""))
        self.theme_combo.setCurrentIndex(self.theme_combo.findData(self.settings.value("theme", "dark")))
        self.language_combo.setCurrentIndex(self.language_combo.findData(self.settings.value("language", "en")))

    def browse_path(self, game_type):
        titles = {
            "en": "Select game executable",
            "ru": "Выберите файл игры",
            "es": "Seleccionar ejecutable del juego",
            "ko": "게임 실행 파일 선택",
            "zh": "选择游戏可执行文件",
            "uk": "Виберіть файл гри",
            "vi": "Chọn tệp thực thi trò chơi"
        }
        lang = self.settings.value("language", "en")
        title = titles.get(lang, titles["en"])
        path, _ = QFileDialog.getOpenFileName(self, title, "", "Executable Files (*.exe)")
        if path:
            if game_type == "roc":
                self.roc_path_edit.setText(path)
            else:
                self.tft_path_edit.setText(path)

    def change_theme(self):
        theme = self.theme_combo.currentData()
        self.settings.setValue("theme", theme)
        self.update_style(theme)
        if self.parent:
            self.parent.update_theme(theme)

    def change_language(self):
        lang = self.language_combo.currentData()
        self.settings.setValue("language", lang)
        self.retranslate_ui()
        if self.parent:
            self.parent.update_language(lang)

    def apply_settings(self):
        self.settings.setValue("roc_path", self.roc_path_edit.text())
        self.settings.setValue("tft_path", self.tft_path_edit.text())

    def ok_pressed(self):
        self.apply_settings()
        self.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("Warcraft3Launcher", "Settings")
        self.translator = QTranslator()
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        self.setWindowTitle("Warcraft III Launcher")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(350, 500)

        self.main_frame = WFrame()
        self.setCentralWidget(self.main_frame)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.main_frame.setLayout(main_layout)

        self.title_bar = WTitleBar()
        main_layout.addWidget(self.title_bar)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setPixmap(self.create_logo())
        content_layout.addWidget(self.logo_label)

        self.roc_btn = WButton()
        self.roc_btn.clicked.connect(lambda: self.launch_game("roc"))
        content_layout.addWidget(self.roc_btn)

        self.tft_btn = WButton()
        self.tft_btn.clicked.connect(lambda: self.launch_game("tft"))
        content_layout.addWidget(self.tft_btn)

        self.settings_btn = WButton()
        self.settings_btn.clicked.connect(self.open_settings)
        content_layout.addWidget(self.settings_btn)

        self.exit_btn = WButton()
        self.exit_btn.clicked.connect(self.close)
        content_layout.addWidget(self.exit_btn)

        main_layout.addLayout(content_layout)
        self.old_pos = None

    def create_logo(self):
        pixmap = QPixmap(300, 150)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        theme = self.settings.value("theme", "dark")
        if theme == "dark":
            gradient = QLinearGradient(0, 0, 0, pixmap.height())
            gradient.setColorAt(0, QColor(44, 34, 19))
            gradient.setColorAt(1, QColor(26, 20, 11))
            text_color = QColor(255, 223, 148)
        elif theme == "light":
            gradient = QLinearGradient(0, 0, 0, pixmap.height())
            gradient.setColorAt(0, QColor(220, 210, 180))
            gradient.setColorAt(1, QColor(180, 170, 150))
            text_color = QColor(44, 34, 19)
        else:  # aqua
            gradient = QLinearGradient(0, 0, 0, pixmap.height())
            gradient.setColorAt(0, QColor(93, 173, 226))
            gradient.setColorAt(1, QColor(52, 152, 219))
            text_color = QColor(255, 255, 255)
        
        painter.fillRect(pixmap.rect(), gradient)
        font = QFont()
        font.setBold(True)
        font.setPointSize(24)
        font.setFamily("Arial")
        painter.setFont(font)
        painter.setPen(text_color)
        painter.drawText(pixmap.rect(), Qt.AlignCenter, "Warcraft III")
        painter.end()
        return pixmap

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = None

    def load_settings(self):
        theme = self.settings.value("theme", "dark")
        lang = self.settings.value("language", "en")
        self.update_theme(theme)
        self.update_language(lang)

    def update_theme(self, theme):
        self.main_frame.update_style(theme)
        self.title_bar.update_style(theme)
        for btn in [self.roc_btn, self.tft_btn, self.settings_btn, self.exit_btn]:
            btn.update_style(theme)
        self.logo_label.setPixmap(self.create_logo())

    def update_language(self, lang):
        translations = {
            "en": {
                "title": "Warcraft III Launcher",
                "roc_btn": "Launch The Reign of Chaos",
                "tft_btn": "Launch The Frozen Throne",
                "settings_btn": "Settings",
                "exit_btn": "Exit"
            },
            "ru": {
                "title": "Warcraft III Лаунчер",
                "roc_btn": "Запустить The Reign of Chaos",
                "tft_btn": "Запустить The Frozen Throne",
                "settings_btn": "Настройки",
                "exit_btn": "Выход"
            },
            "es": {
                "title": "Lanzador Warcraft III",
                "roc_btn": "Iniciar The Reign of Chaos",
                "tft_btn": "Iniciar The Frozen Throne",
                "settings_btn": "Configuración",
                "exit_btn": "Salir"
            },
            "ko": {
                "title": "워크래프트 III 실행기",
                "roc_btn": "The Reign of Chaos 실행",
                "tft_btn": "The Frozen Throne 실행",
                "settings_btn": "설정",
                "exit_btn": "종료"
            },
            "zh": {
                "title": "魔兽争霸III启动器",
                "roc_btn": "启动混乱之治",
                "tft_btn": "启动冰封王座",
                "settings_btn": "设置",
                "exit_btn": "退出"
            },
            "uk": {
                "title": "Warcraft III Запускач",
                "roc_btn": "Запустити The Reign of Chaos",
                "tft_btn": "Запустити The Frozen Throne",
                "settings_btn": "Налаштування",
                "exit_btn": "Вийти"
            },
            "vi": {
                "title": "Trình khởi chạy Warcraft III",
                "roc_btn": "Khởi chạy The Reign of Chaos",
                "tft_btn": "Khởi chạy The Frozen Throne",
                "settings_btn": "Cài đặt",
                "exit_btn": "Thoát"
            }
        }
        
        trans = translations.get(lang, translations["en"])
        self.title_bar.setText(trans["title"])
        self.roc_btn.setText(trans["roc_btn"])
        self.tft_btn.setText(trans["tft_btn"])
        self.settings_btn.setText(trans["settings_btn"])
        self.exit_btn.setText(trans["exit_btn"])
        self.logo_label.setPixmap(self.create_logo())

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec()

    def launch_game(self, game_type):
        path = self.settings.value(f"{game_type}_path", "")
        if not path or not os.path.exists(path):
            self.open_settings()
            path = self.settings.value(f"{game_type}_path", "")
            if not path or not os.path.exists(path):
                return
        
        try:
            os.startfile(path)
        except Exception as e:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
