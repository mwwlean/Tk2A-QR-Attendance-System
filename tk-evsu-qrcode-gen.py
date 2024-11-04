import tkinter as tk
from tkinter import messagebox, filedialog
import qrcode
from PIL import Image, ImageTk

def generate_qr():
    global qr_image  
    data = entry.get()  
    if not data:
        messagebox.showerror("Error", "Please enter some data!")
        return
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill="black", back_color="white").convert("RGB")

    logo_path = "images/evsu.png" 
    try:
        logo = Image.open(logo_path)
        logo_size = 100 
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)  

        qr_center = ((qr_image.size[0] - logo_size) // 2, (qr_image.size[1] - logo_size) // 2)
        qr_image.paste(logo, qr_center, logo)  
    except FileNotFoundError:
        messagebox.showerror("Error", "Logo image not found. Please make sure 'images/evsu.png' exists.")

    
    img_resized = qr_image.resize((150, 150))  
    img_tk = ImageTk.PhotoImage(img_resized)
    qr_label.config(image=img_tk)
    qr_label.image = img_tk  
    
    save_button.pack(pady=10)

def save_qr():
    if not qr_image:
        messagebox.showerror("Error", "No QR code to save. Please generate one first.")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        qr_image.save(file_path)
        messagebox.showinfo("Success", "QR code saved successfully!")

root = tk.Tk()
root.title("QR Code Generator")
root.geometry("300x450")

label = tk.Label(root, text="Enter text to generate QR code:")
label.pack(pady=10)

entry = tk.Entry(root, width=30)
entry.pack(pady=5)

generate_button = tk.Button(root, text="Generate QR Code", command=generate_qr)
generate_button.pack(pady=10)

qr_label = tk.Label(root)
qr_label.pack(pady=10)

save_button = tk.Button(root, text="Save QR Code", command=save_qr)
save_button.pack_forget()  

qr_image = None  

root.mainloop()
