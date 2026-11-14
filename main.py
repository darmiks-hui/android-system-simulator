from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.button import Button
from kivy.uix.widget import Widget


class SystemSimulator(App):

    def build(self):
        Window.fullscreen = "auto"
        Window.clearcolor = (0.015, 0.015, 0.02, 1)

        self.progress = 0
        self.stage = 0

        self.root = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20
        )

        self.title_label = Label(
            text="[b]ANDROID SYSTEM v4.0[/b]",
            markup=True,
            font_size="25sp",
            color=(0.2, 0.8, 1, 1),
            size_hint_y=0.25
        )

        self.status = Label(
            text="SYSTEM DIAGNOSTICS",
            font_size="18sp",
            color=(1, 0.2, 0.2, 1)
        )

        self.details = Label(
            text="Initializing system...",
            font_size="14sp",
            color=(0.7, 0.7, 0.7, 1)
        )

        self.bar = ProgressBar(
            max=100,
            value=0,
            size_hint_y=None,
            height=15
        )

        self.exit_button = Button(
            text="ВЫЙТИ",
            size_hint=(1, None),
            height=45,
            background_color=(0.25, 0.25, 0.3, 1)
        )
        self.exit_button.bind(on_press=self.close_app)

        self.root.add_widget(self.title_label)
        self.root.add_widget(self.status)
        self.root.add_widget(self.details)
        self.root.add_widget(self.bar)
        self.root.add_widget(Widget())
        self.root.add_widget(self.exit_button)

        Clock.schedule_interval(self.update_system, 0.12)

        return self.root

    def update_system(self, dt):
        self.progress += 1
        self.bar.value = self.progress

        if self.progress == 20:
            self.details.text = "Checking system files..."
        elif self.progress == 45:
            self.details.text = "Loading system modules..."
        elif self.progress == 70:
            self.details.text = "Preparing restart..."
        elif self.progress >= 100:
            self.status.text = "SYSTEM RESTART"
            self.details.text = "Simulation complete."
            Clock.schedule_once(self.reset_system, 2)
            return False

    def reset_system(self, dt):
        self.progress = 0
        self.bar.value = 0
        self.status.text = "SYSTEM DIAGNOSTICS"
        self.details.text = "Initializing system..."
        Clock.schedule_interval(self.update_system, 0.12)

    def close_app(self, instance):
        App.get_running_app().stop()


if __name__ == "__main__":
    SystemSimulator().run()
