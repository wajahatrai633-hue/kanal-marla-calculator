import json
import os

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView


class KanalMarlaCalculator(App):

    def build(self):
        self.title = "Kanal Marla Calculator"

        self.rate_rabi = 850
        self.rate_kharif = 1650

        main = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(8)
        )

        # Header
        title = Label(
            text="KANAL MARLA CALCULATOR",
            font_size=dp(22),
            bold=True,
            size_hint_y=None,
            height=dp(45)
        )
        main.add_widget(title)

        subtitle = Label(
            text="Live Land Measurement Calculator",
            font_size=dp(13),
            size_hint_y=None,
            height=dp(28)
        )
        main.add_widget(subtitle)

        # Season section
        season_box = BoxLayout(
            size_hint_y=None,
            height=dp(48),
            spacing=dp(8)
        )

        season_box.add_widget(
            Label(
                text="Season:",
                size_hint_x=0.35,
                font_size=dp(16),
                bold=True
            )
        )

        self.season = Spinner(
            text="Rabi",
            values=("Rabi", "Kharif"),
            font_size=dp(16)
        )

        self.season.bind(text=self.update_rate)

        season_box.add_widget(self.season)
        main.add_widget(season_box)

        # Rate display
        self.rate_label = Label(
            text="Rabi Rate: Rs. 850 / 8 Kanal",
            font_size=dp(15),
            bold=True,
            size_hint_y=None,
            height=dp(32)
        )
        main.add_widget(self.rate_label)

        # Scroll area
        scroll = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False
        )

        self.rows = []

        grid = GridLayout(
            cols=3,
            spacing=dp(5),
            padding=dp(3),
            size_hint_y=None
        )

        grid.bind(minimum_height=grid.setter("height"))

        # Headings
        grid.add_widget(
            Label(
                text="No.",
                bold=True,
                size_hint_y=None,
                height=dp(32)
            )
        )

        grid.add_widget(
            Label(
                text="Kanal",
                bold=True,
                size_hint_y=None,
                height=dp(32)
            )
        )

        grid.add_widget(
            Label(
                text="Marla",
                bold=True,
                size_hint_y=None,
                height=dp(32)
            )
        )

        # 20 rows
        for i in range(1, 21):
            number = Label(
                text=str(i),
                size_hint_y=None,
                height=dp(42)
            )

            kanal = TextInput(
                hint_text="0",
                input_filter="float",
                multiline=False,
                size_hint_y=None,
                height=dp(42),
                font_size=dp(16)
            )

            marla = TextInput(
                hint_text="0",
                input_filter="float",
                multiline=False,
                size_hint_y=None,
                height=dp(42),
                font_size=dp(16)
            )

            kanal.bind(text=self.calculate)
            marla.bind(text=self.calculate)

            self.rows.append((kanal, marla))

            grid.add_widget(number)
            grid.add_widget(kanal)
            grid.add_widget(marla)

        scroll.add_widget(grid)
        main.add_widget(scroll)

        # Total area
        self.total_label = Label(
            text="Total: 0 Kanal 0 Marla",
            font_size=dp(17),
            bold=True,
            size_hint_y=None,
            height=dp(32)
        )
        main.add_widget(self.total_label)

        self.acre_label = Label(
            text="Acre: 0.00",
            font_size=dp(15),
            size_hint_y=None,
            height=dp(28)
        )
        main.add_widget(self.acre_label)

        self.amount_label = Label(
            text="Total Rate: Rs. 0",
            font_size=dp(17),
            bold=True,
            size_hint_y=None,
            height=dp(34)
        )
        main.add_widget(self.amount_label)

        # Buttons
        buttons = BoxLayout(
            size_hint_y=None,
            height=dp(48),
            spacing=dp(6)
        )

        save_btn = Button(
            text="SAVE",
            font_size=dp(15),
            bold=True
        )
        save_btn.bind(on_press=self.save_data)

        load_btn = Button(
            text="LOAD",
            font_size=dp(15),
            bold=True
        )
        load_btn.bind(on_press=self.load_data)

        clear_btn = Button(
            text="CLEAR ALL",
            font_size=dp(15),
            bold=True
        )
        clear_btn.bind(on_press=self.clear_all)

        buttons.add_widget(save_btn)
        buttons.add_widget(load_btn)
        buttons.add_widget(clear_btn)

        main.add_widget(buttons)

        return main

    def update_rate(self, spinner, text):
        if text == "Rabi":
            self.rate_label.text = "Rabi Rate: Rs. 850 / 8 Kanal"
        else:
            self.rate_label.text = "Kharif Rate: Rs. 1650 / 8 Kanal"

        self.calculate()

    def calculate(self, *args):
        total_marla = 0.0

        for kanal, marla in self.rows:
            try:
                k = float(kanal.text or 0)
            except ValueError:
                k = 0

            try:
                m = float(marla.text or 0)
            except ValueError:
                m = 0

            total_marla += (k * 20) + m

        total_kanal = int(total_marla // 20)
        remaining_marla = total_marla % 20

        acres = total_marla / 160.0

        if self.season.text == "Rabi":
            rate = self.rate_rabi
        else:
            rate = self.rate_kharif

        total_rate = (total_marla / 160.0) * rate

        self.total_label.text = (
            f"Total: {total_kanal} Kanal "
            f"{remaining_marla:.2f} Marla"
        )

        self.acre_label.text = f"Acre: {acres:.2f}"

        self.amount_label.text = (
            f"Total Rate: Rs. {total_rate:,.2f}"
        )

    def save_data(self, *args):
        data = {
            "season": self.season.text,
            "rows": [
                {
                    "kanal": kanal.text,
                    "marla": marla.text
                }
                for kanal, marla in self.rows
            ]
        }

        path = os.path.join(
            self.user_data_dir,
            "kanal_marla_project.json"
        )

        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

    def load_data(self, *args):
        path = os.path.join(
            self.user_data_dir,
            "kanal_marla_project.json"
        )

        if not os.path.exists(path):
            return

        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.season.text = data.get("season", "Rabi")

        saved_rows = data.get("rows", [])

        for i, (kanal, marla) in enumerate(self.rows):
            if i < len(saved_rows):
                kanal.text = saved_rows[i].get("kanal", "")
                marla.text = saved_rows[i].get("marla", "")

        self.calculate()

    def clear_all(self, *args):
        for kanal, marla in self.rows:
            kanal.text = ""
            marla.text = ""

        self.calculate()


if __name__ == "__main__":
    KanalMarlaCalculator().run()
