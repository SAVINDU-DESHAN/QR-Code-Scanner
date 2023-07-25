import cv2
from pyzbar.pyzbar import decode
import webbrowser
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.colorpicker import ColorPicker
from kivy.config import ConfigParser


class QRCodeScannerApp(App):
    def build(self):
        self.video_source = 0
        self.cap = cv2.VideoCapture(self.video_source)

        # Main layout containing the camera interface
        main_layout = BoxLayout(orientation='vertical')

        # Camera interface
        self.label = Image()

        # Small button layout for actions
        small_button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        main_layout.add_widget(self.label)
        main_layout.add_widget(small_button_layout)

        # Buttons for actions
        self.upload_button = Button(text="Upload QR Code Image", on_press=self.upload_qr_code, size_hint=(0.3, 1))
        self.set_browser_button = Button(text="Set Default Browser", on_press=self.set_default_browser, size_hint=(0.3, 1))
        self.dark_theme_button = Button(text="Dark Theme", on_press=self.toggle_dark_theme, size_hint=(0.3, 1))
        self.settings_button = Button(text="Settings", on_press=self.open_settings_popup, size_hint=(0.1, 1))

        small_button_layout.add_widget(self.upload_button)
        small_button_layout.add_widget(self.set_browser_button)
        small_button_layout.add_widget(self.dark_theme_button)
        small_button_layout.add_widget(self.settings_button)

        # Load user preferences from config file
        self.config = ConfigParser()
        self.load_preferences()

        Clock.schedule_interval(self.decode_qr, 1.0 / 30.0)

        return main_layout

    def upload_qr_code(self, *args):
        # Implement the QR code image upload logic here
        # You may use a FileChooserListView to allow the user to select an image file.
        pass

    def set_default_browser(self, *args):
        # Implement the default browser setting logic here
        # You may use a FileChooserListView to allow the user to select a browser executable.
        pass

    def toggle_dark_theme(self, *args):
        if not hasattr(self, 'is_dark_theme'):
            self.is_dark_theme = False

        if self.is_dark_theme:
            # Apply default theme (light theme)
            Window.clearcolor = (1, 1, 1, 1)
        else:
            # Apply dark theme
            Window.clearcolor = (0.133, 0.133, 0.133, 1)

        self.is_dark_theme = not self.is_dark_theme

    def decode_qr(self, *args):
        ret, frame = self.cap.read()

        if ret:
            # Decode QR codes
            decoded_objects = decode(frame)

            for obj in decoded_objects:
                data = obj.data.decode('utf-8')
                print(f"QR Code Data: {data}")

                # Draw a rectangle around the QR code
                rect_points = obj.polygon
                for i in range(4):
                    cv2.line(frame, rect_points[i], rect_points[(i + 1) % 4], (0, 255, 0), 3)

                # Open the decoded data in the default browser
                webbrowser.open(data)

        # Convert the frame to a Kivy texture
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')

        # Update the label with the new texture
        self.label.texture = texture

    def open_settings_popup(self, *args):
        settings_popup = Popup(title="Settings", size_hint=(0.8, 0.6))
        layout = BoxLayout(orientation='vertical')

        color_picker = ColorPicker(color=self.get_color(), size_hint=(1, 0.7))
        save_button = Button(text="Save Settings", on_press=lambda x: self.save_settings(color_picker.color))
        layout.add_widget(color_picker)
        layout.add_widget(save_button)

        settings_popup.content = layout
        settings_popup.open()

    def set_color(self, color):
        r, g, b, a = color
        Window.clearcolor = (r, g, b, 1)

    def get_color(self):
        return Window.clearcolor

    def load_preferences(self):
        if os.path.exists('preferences.ini'):
            self.config.read('preferences.ini')
            color = list(map(float, self.config.get('Settings', 'color').split(',')))
            self.set_color(color)

    def save_settings(self, color):
        self.set_color(color)
        self.config.set('Settings', 'color', ','.join(map(str, color)))
        self.save_preferences()
        self.toggle_dark_theme()

    def save_preferences(self):
        with open('preferences.ini', 'w') as config_file:
            self.config.write(config_file)

    def on_stop(self):
        self.cap.release()


if __name__ == '__main__':
    QRCodeScannerApp().run()
