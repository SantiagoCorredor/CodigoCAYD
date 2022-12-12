import tkinter
import customtkinter
import random

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

menu = customtkinter.CTk()
menu.geometry("360x400")
menu.title("Parcial rescate")


def linea(): 
    print("Hola mundo 1")
    
def canal():
    print("Hola mundo 2")
    
def b_base():
    print("hola mundo 3")
    
def qam_32():
    print("hola mundo 4")
    
def tdm():
    print("hola mundo 5")
    
def tdma():
    print("hola mundo 6")



frame_1 = customtkinter.CTkFrame(master=menu)
frame_1.pack(pady=20, padx=40, fill="both", expand=True)

label_1 = customtkinter.CTkLabel(master=frame_1, text="Parcial Rescate", font=("Roboto Medium", -16) ,justify=tkinter.LEFT)
label_1.pack(pady=12, padx=10)

label_2 = customtkinter.CTkLabel(master=frame_1, text="Hecho por Andrés Corredor", font=("Roboto Medium", -12) ,justify=tkinter.LEFT)
label_2.place(x=75, y=70)
label_3 = customtkinter.CTkLabel(master=frame_1, text="Menu principal", font=("Roboto Medium", -12) ,justify=tkinter.LEFT)
label_3.place(x=108, y=90)

button_1 = customtkinter.CTkButton(master=frame_1, text="Cod. Línea", font=("Roboto Medium", -16) , command=linea)
button_1.place(x=75, y=125)

button_2 = customtkinter.CTkButton(master=frame_1, text="Cod. Canal", font=("Roboto Medium", -16) , command=canal)
button_2.place(x=75, y=155)

button_3 = customtkinter.CTkButton(master=frame_1, text="Banda Base", font=("Roboto Medium", -16) , command=b_base)
button_3.place(x=75, y=185)

button_4 = customtkinter.CTkButton(master=frame_1, text="32 - QAM", font=("Roboto Medium", -16) , command=qam_32)
button_4.place(x=75, y=215)

button_5 = customtkinter.CTkButton(master=frame_1, text="Mult - TDM", font=("Roboto Medium", -16) , command=tdm)
button_5.place(x=75, y=245)

button_6 = customtkinter.CTkButton(master=frame_1, text="Acces - TDMA", font=("Roboto Medium", -16) , command=tdma)
button_6.place(x=75, y=275)

menu.mainloop()