"""
Приложение для запоминания английских слов (Kivy)
Особенности: 
- Карточки слов с переключением направления
- Кнопки "Далее" и "Выход"
- Просмотр всего списка
- Добавление новых пар слово-перевод
- Сохранение в JSON-файл
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
import json
import os

# Начальный список слов (можно заменить своими)
DEFAULT_WORDS = [
    {"en": "apple", "ru": "яблоко"},
    {"en": "cat", "ru": "кот"},
    {"en": "dog", "ru": "собака"},
    {"en": "sun", "ru": "солнце"},
    {"en": "book", "ru": "книга"},
]

# Файл для сохранения
DATA_FILE = "words.json"

class WordCardApp(App):
    def build(self):
        self.load_words()
        self.current_index = 0
        self.show_english = True  # True = показываем английское слово, False = русское

        # Главный вертикальный контейнер
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Верхняя панель: переключатель направления
        top_panel = BoxLayout(size_hint_y=0.15, spacing=10)
        top_panel.add_widget(Label(text="Направление:", size_hint_x=0.4))
        
        self.switch_label = Label(text="EN -> RU", size_hint_x=0.3)
        top_panel.add_widget(self.switch_label)
        
        self.lang_switch = Switch(active=True, size_hint_x=0.3)
        self.lang_switch.bind(active=self.toggle_direction)
        top_panel.add_widget(self.lang_switch)
        
        main_layout.add_widget(top_panel)

        # Карточка слова (центр)
        self.word_label = Label(
            text=self.get_current_word(),
            font_size='40sp',
            halign='center',
            valign='middle',
            size_hint_y=0.5
        )
        self.word_label.bind(size=self.word_label.setter('text_size'))
        main_layout.add_widget(self.word_label)

        # Нижняя панель с кнопками
        bottom_panel = BoxLayout(size_hint_y=0.2, spacing=10)
        
        btn_prev = Button(text="◀ Пред.", size_hint_x=0.25)
        btn_prev.bind(on_press=self.prev_word)
        bottom_panel.add_widget(btn_prev)
        
        btn_next = Button(text="Далее ▶", size_hint_x=0.25)
        btn_next.bind(on_press=self.next_word)
        bottom_panel.add_widget(btn_next)
        
        btn_list = Button(text="📋 Список", size_hint_x=0.25)
        btn_list.bind(on_press=self.show_word_list)
        bottom_panel.add_widget(btn_list)
        
        btn_add = Button(text="➕ Добавить", size_hint_x=0.25)
        btn_add.bind(on_press=self.show_add_word_popup)
        bottom_panel.add_widget(btn_add)
        
        main_layout.add_widget(bottom_panel)

        # Кнопка выхода
        exit_btn = Button(text="Выход", size_hint_y=0.1, background_color=(0.8, 0.2, 0.2, 1))
        exit_btn.bind(on_press=self.exit_app)
        main_layout.add_widget(exit_btn)

        return main_layout

    # ---------- Загрузка / сохранение ----------
    def load_words(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                self.words = json.load(f)
        else:
            self.words = DEFAULT_WORDS.copy()
            self.save_words()

    def save_words(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.words, f, ensure_ascii=False, indent=2)

    # ---------- Логика работы со словами ----------
    def get_current_word(self):
        if not self.words:
            return "Список пуст"
        word = self.words[self.current_index]
        return word['en'] if self.show_english else word['ru']

    def next_word(self, instance):
        if self.words:
            self.current_index = (self.current_index + 1) % len(self.words)
            self.word_label.text = self.get_current_word()

    def prev_word(self, instance):
        if self.words:
            self.current_index = (self.current_index - 1) % len(self.words)
            self.word_label.text = self.get_current_word()

    def toggle_direction(self, switch, value):
        self.show_english = value
        self.switch_label.text = "EN -> RU" if value else "RU -> EN"
        if self.words:
            self.word_label.text = self.get_current_word()

    # ---------- Показать весь список ----------
    def show_word_list(self, instance):
        if not self.words:
            popup = Popup(title="Список пуст", content=Label(text="Нет слов"), size_hint=(0.7, 0.4))
            popup.open()
            return

        # Создаём прокручиваемый список
        grid = GridLayout(cols=2, spacing=5, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        
        for w in self.words:
            grid.add_widget(Label(text=w['en'], size_hint_y=None, height=40))
            grid.add_widget(Label(text=w['ru'], size_hint_y=None, height=40))

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(grid)
        
        popup = Popup(title="Все слова", content=scroll, size_hint=(0.9, 0.8))
        popup.open()

    # ---------- Добавление нового слова ----------
    def show_add_word_popup(self, instance):
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        en_input = TextInput(hint_text="Английское слово", multiline=False)
        ru_input = TextInput(hint_text="Перевод на русский", multiline=False)
        box.add_widget(en_input)
        box.add_widget(ru_input)
        
        btn_layout = BoxLayout(size_hint_y=0.3, spacing=10)
        save_btn = Button(text="Сохранить")
        cancel_btn = Button(text="Отмена")
        btn_layout.add_widget(save_btn)
        btn_layout.add_widget(cancel_btn)
        box.add_widget(btn_layout)
        
        popup = Popup(title="Добавить слово", content=box, size_hint=(0.8, 0.5))
        
        def save_word(btn):
            en = en_input.text.strip()
            ru = ru_input.text.strip()
            if en and ru:
                self.words.append({"en": en, "ru": ru})
                self.save_words()
                # Если список был пуст, обновляем карточку
                if len(self.words) == 1:
                    self.current_index = 0
                    self.word_label.text = self.get_current_word()
                popup.dismiss()
            else:
                # Простое уведомление (можно улучшить)
                en_input.hint_text = "Заполните оба поля!"
                ru_input.hint_text = "Заполните оба поля!"
        
        save_btn.bind(on_press=save_word)
        cancel_btn.bind(on_press=popup.dismiss)
        popup.open()

    # ---------- Выход ----------
    def exit_app(self, instance):
        App.get_running_app().stop()

if __name__ == "__main__":
    WordCardApp().run()
