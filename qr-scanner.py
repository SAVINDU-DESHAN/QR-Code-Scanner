import cv2
from pyzbar.pyzbar import decode
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import webbrowser

class QRCodeScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Scanner")
        self.video_source = 0
        self.cap = cv2.VideoCapture(self.video_source)
        self.label = ttk.Label(root)
        self.label.pack(pady=10)

        # Create a custom style for the interface
        self.custom_style = ttk.Style()
        self.custom_style.theme_use("default")

        # Set background color
        self.custom_style.configure("TFrame", background="#f0f0f0")
        self.custom_style.configure("TLabel", background="#f0f0f0")
        self.custom_style.configure("TButton", background="#007bff", foreground="white", relief="raised", font=("Arial", 12, "bold"))

        # Button for uploading QR code image
        self.upload_button = ttk.Button(root, text="Upload QR Code Image", command=self.upload_qr_code, style="TButton")
        self.upload_button.pack(pady=5)

        # Button for setting the default browser
        self.set_browser_button = ttk.Button(root, text="Set Default Browser", command=self.set_default_browser, style="TButton")
        self.set_browser_button.pack(pady=5)

        # Toggle button for dark theme
        self.dark_theme_button = ttk.Button(root, text="Dark Theme", command=self.toggle_dark_theme, style="TButton")
        self.dark_theme_button.pack(pady=5)

        self.is_dark_theme = False
        self.toggle_dark_theme()

        self.decode_qr()

    def toggle_dark_theme(self):
        if self.is_dark_theme:
            # Apply default theme (light theme)
            self.custom_style.theme_use("default")
            self.root.configure(background="#f0f0f0")  # Set root window background to light color
        else:
            # Apply dark theme
            self.custom_style.theme_use("default")  # You can choose a dark theme here
            self.root.configure(background="#222222")  # Set root window background to dark color

        self.is_dark_theme = not self.is_dark_theme

    def decode_qr(self):
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

        # Convert the frame to a Tkinter image
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img_tk = ImageTk.PhotoImage(image=img)

        # Update the label with the new image
        self.label.img = img_tk
        self.label.config(image=img_tk)

        # Repeat the process after 100 milliseconds
        self.root.after(100, self.decode_qr)

    def upload_qr_code(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])

        if file_path:
            # Read the image file
            image = cv2.imread(file_path)

            # Decode QR codes from the uploaded image
            decoded_objects = decode(image)

            for obj in decoded_objects:
                data = obj.data.decode('utf-8')
                print(f"QR Code Data from Uploaded Image: {data}")

                # Open the decoded data in the default browser
                webbrowser.open(data)

    def set_default_browser(self):
        browser_path = filedialog.askopenfilename(filetypes=[("Application", "*.exe")])

        if browser_path:
            # Save the selected browser path to a file or configuration
            # In this example, we'll simply print it
            print(f"Default browser set to: {browser_path}")

    def close_app(self):
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(background="#f0f0f0")  # Set initial root window background to light color
    app = QRCodeScannerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    root.mainloop()


# All Copyright for ~ Savindu Deshan ~ 
