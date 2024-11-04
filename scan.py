import cv2
import tkinter as tk
from tkinter import Label, messagebox
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode


class QRCodeReader:
    def __init__(self, master):
        self.master = master
        self.master.title("QR Code Reader")

        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)

        self.label = Label(master)
        self.label.pack()

        self.update()
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            cv2.putText(
                frame_rgb,
                "Put your QR here",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )
            # Decode QR codes
            decoded_objects = decode(frame_rgb)
            if decoded_objects:
                for obj in decoded_objects:
                    cv2.rectangle(
                        frame_rgb,
                        (obj.rect.left, obj.rect.top),
                        (
                            obj.rect.left + obj.rect.width,
                            obj.rect.top + obj.rect.height,
                        ),
                        (0, 255, 0),
                        2,
                    )
                    qr_data = obj.data.decode("utf-8")
                    print("QR Code Data:", qr_data)

                    messagebox.showinfo(
                        "QR Code Scanned", f"Successfully scanned:\n{qr_data}"
                    )
                    break

            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

        self.label.after(10, self.update)

    def on_closing(self):
        self.vid.release()
        self.master.quit()


if __name__ == "__main__":
    root = tk.Tk()
    qr_reader = QRCodeReader(root)
    root.mainloop()
