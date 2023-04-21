import tkinter
import tkinter.messagebox
import customtkinter
import os
from time import sleep
from os import system
import time
from guizero import App, Text, PushButton, Slider, ListBox, Picture
from PIL import Image
import cv2
from picamera2 import Picamera2, Preview
from tkinter import Spinbox
from libcamera import Transform
import sys
from smbus import SMBus
import board
from adafruit_seesaw.seesaw import Seesaw
from adafruit_extended_bus import ExtendedI2C as I2C
import pickle 




customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


i2c_bus = I2C(22)
addr = 0x38 # bus address
bus = SMBus(22) # indicates /dev/ic2-22
ss1 = Seesaw(i2c_bus, addr=0x36)
ss2 = Seesaw(i2c_bus, addr=0x37)

def manuell_motor1():
    bus.write_byte(addr, 0x1)
    sleep(0.1)
    bus.write_byte(addr, 0x0)

def manuell_motor2():
  bus.write_byte(addr, 0x2)
  sleep(0.1)
  bus.write_byte(addr, 0x0)
  
def vekstlys_pa():
  bus.write_byte(addr, 0x4)
  sleep(0.3)
  bus.write_byte(addr, 0x0)
  
def vekstlys_av():
  bus.write_byte(addr, 0x5)
  sleep(0.3)
  bus.write_byte(addr, 0x0)
    
def lukk():
    bus.write_byte(addr, 0x3)
    sys.exit()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
   
        
        self.after(100, self.avlesing)
        # configure window
        self.title("Embedded systems")
        self.attributes('-fullscreen',True) #fullskjerm
        self.geometry(f"{800}x{480}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(0, weight=0)
        self.sidebar_frame.grid_rowconfigure(1, weight=0)
        self.sidebar_frame.grid_rowconfigure(2, weight=1)
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label1 = customtkinter.CTkLabel(self.sidebar_frame, text="Plantevanner", font=customtkinter.CTkFont(size=27, weight="bold"))
        self.logo_label1.grid(row=0, column=0, padx=10, pady=(10, 10))
        self.logo_label2 = customtkinter.CTkLabel(self.sidebar_frame, text="Simen og Tobias", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label2.grid(row=1, column=0, padx=10, pady=(10, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event, text="Test Kamera")
        self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)
        
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, command=self.plot, text="Plot")
        self.sidebar_button_4.grid(row=3, column=0, padx=20, pady=10)
        
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=lukk)
        self.sidebar_button_3.grid(row=4, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Tema:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))


        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=200, height=300)
        self.tabview.grid(row=0, column=1, padx=(20, 0), pady=(10, 0), sticky="nsew")
        self.tabview.add("Status")
        self.tabview.add("Plante 1")
        self.tabview.add("Plante 2")
        self.tabview.add("Manuell")
        self.tabview.tab("Status").grid_columnconfigure((0,1,2,3,4), weight=1)  # configure grid of individual tabs
        self.tabview.tab("Status").grid_rowconfigure((0,1), weight=1)  # configure grid of individual tabs
        self.tabview.tab("Plante 1").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Plante 2").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Manuell").grid_columnconfigure(0, weight=1)

        ################# Status TAB ##########
        
        #Grafisk visning plante 1
        self.progressbar_1 = customtkinter.CTkProgressBar(self.tabview.tab("Status"), orientation="vertical",
                                                           width=30, height=140)
        self.progressbar_1.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="w")


        #Overskrift fra valg plante 1
        self.label1_tab_status = customtkinter.CTkLabel(self.tabview.tab("Status"), text="Velg type", height=10,
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label1_tab_status.grid(row=0, column=0, padx=(0,20), pady=(5,0))
        
        #Prosent plante 1
        self.label3_tab_status = customtkinter.CTkLabel(self.tabview.tab("Status"), text="",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label3_tab_status.grid(row=1, column=0, padx=(30,0), pady=0)
       
        #Grafisk visning plante 2
        self.progressbar_2 = customtkinter.CTkProgressBar(self.tabview.tab("Status"), orientation="vertical",
                                                          width=30, height=140)
        self.progressbar_2.grid(row=1, column=4, padx=(20, 10), pady=(10, 10), sticky="e")
        #overskrift fra valg plante 2
        self.label2_tab_status = customtkinter.CTkLabel(self.tabview.tab("Status"), text="Velg type", height=10,
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label2_tab_status.grid(row=0, column=4, padx=(20,0), pady=(5,0))

        #Prosent plante 2
        self.label4_tab_status = customtkinter.CTkLabel(self.tabview.tab("Status"), text="",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label4_tab_status.grid(row=1, column=4, padx=(0,20), pady=0)
        
        #Temp
        self.label5_tab_status = customtkinter.CTkLabel(self.tabview.tab("Status"), text="",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label5_tab_status.grid(row=1, column=2, padx=(0,0), pady=(80,0))

        ############### Plante 1 TAB ##############

        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Plante 1"), text="Instillinger for plante 1", 
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_tab_2.grid(row=0, column=0, padx=2, pady=2)
        
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Plante 1"), dynamic_resizing=False,
                                                        values=["Koriander", "Basilikum", "Gressløk"],
                                                        command=self.valg_av_plante1,
                                                        width=300,
                                                        height=30)
        self.optionmenu_1.grid(row=1, column=0, padx=20, pady=(20, 10))
        
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("Plante 1"), text="Mengde vanning (ml)",
                                                           command=self.open_input_dialog_event,
                                                           width=300,
                                                           height=30)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))

         ############### Plante 2 TAB ##############

        self.label_tab_3 = customtkinter.CTkLabel(self.tabview.tab("Plante 2"), text="Instillinger for plante 2", 
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_tab_3.grid(row=0, column=0, padx=2, pady=2)

        self.optionmenu_2 = customtkinter.CTkOptionMenu(self.tabview.tab("Plante 2"), dynamic_resizing=False,
                                                        values=["Koriander", "Basilikum", "Gressløk"],
                                                        command=self.valg_av_plante2,
                                                        width=300,
                                                        height=30)
        self.optionmenu_2.grid(row=1, column=0, padx=20, pady=(20, 10))
        
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("Plante 2"), text="Mengde vanning (ml)",
                                                           command=self.open_input_dialog_event,
                                                           width=300,
                                                           height=30)
                                                        
        self.string_input_button.grid(row=3, column=0, padx=20, pady=(10, 10))

        ############# Manuell tab #############

        self.manuell_button_motor1= customtkinter.CTkButton(self.tabview.tab("Manuell"), command=manuell_motor1, text="Motor 1")
        self.manuell_button_motor1.grid(row=0, column=0, padx=20, pady=10)

        self.manuell_button_motor2= customtkinter.CTkButton(self.tabview.tab("Manuell"), command=manuell_motor2, text="Motor 2")
        self.manuell_button_motor2.grid(row=1, column=0, padx=20, pady=10)

        self.manuell_button_light= customtkinter.CTkButton(self.tabview.tab("Manuell"), command=vekstlys_pa, text="Vekstlys På")
        self.manuell_button_light.grid(row=2, column=0, padx=20, pady=10)
        
        self.manuell_button_light2= customtkinter.CTkButton(self.tabview.tab("Manuell"), command=vekstlys_av, text="Vekstlys Av")
        self.manuell_button_light2.grid(row=3, column=0, padx=20, pady=10)


        # create slider and progressbar frame
        self.slider_frame = customtkinter.CTkFrame(self, width=50, height=400)
        self.slider_frame.grid(row=0, column=2, padx=(20, 20), pady=(28, 12), sticky="nsew", rowspan=4)
        self.slider_frame.grid_columnconfigure(5, weight=1)
        self.slider_frame.grid_rowconfigure(4, weight=1)


        ### Slidere for å sette prosent fuktighet grense ####

        #venste slider
        self.slider_2 = customtkinter.CTkSlider(self.slider_frame, orientation="vertical", command=self.terskel_plante1,
                                                from_=0,
                                                to=100,
                                                width=20, height=420)
        self.slider_2.grid(row=0, column=0, rowspan=4, padx=(10, 10), pady=(10, 10), sticky="w",)
        self.slider_2_label = customtkinter.CTkLabel(self.slider_frame, text="50", 
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.slider_2_label.grid(row=1, column=1, padx=0, pady=0)
        
        #høyre slider
        self.slider_3 = customtkinter.CTkSlider(self.slider_frame, orientation="vertical", command=self.terskel_plante2,
                                                from_=0,
                                                to=100,
                                                width=20, height=420)
        self.slider_3.grid(row=0, column=5, rowspan=4, padx=(10, 10), pady=(10, 10), sticky="e")
        self.slider_2_label2 = customtkinter.CTkLabel(self.slider_frame, text="50", 
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.slider_2_label2.grid(row=1, column=3, padx=2, pady=2)

        #overskrift
        self.slider_frame.overskrift = customtkinter.CTkLabel(self.slider_frame, text="Terskel fukt [%]", anchor="n",
                                                   font=customtkinter.CTkFont(size=14, weight="bold"),
                                                   width=90)
        self.slider_frame.overskrift.grid(row=0, column=2, padx=0, pady=(0, 60))


        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Planter på plass")
        self.scrollable_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 10), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []

        #knapper av/på
        self.switch1 = customtkinter.CTkSwitch(master=self.scrollable_frame, text="Plante 1", command=self.plante1_aktivert, switch_width=80, switch_height=30)
        self.switch1.grid(row=0, column=0, padx=10, pady=(0, 20))
        self.scrollable_frame_switches.append(self.switch1)
        self.switch2 = customtkinter.CTkSwitch(master=self.scrollable_frame, text="Plante 2", command=self.plante2_aktivert, switch_width=80, switch_height=30)
        self.switch2.grid(row=1, column=0, padx=10, pady=(0, 20))
        self.scrollable_frame_switches.append(self.switch2)
        self.switch3 = customtkinter.CTkSwitch(master=self.scrollable_frame,state="disabled", text="Plante 3", switch_width=80, switch_height=30)
        self.switch3.grid(row=3, column=0, padx=10, pady=(0, 20))
        self.scrollable_frame_switches.append(self.switch3)


        # set default values
        self.sidebar_button_3.configure( text="Lukk")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("Type plante")
        self.optionmenu_2.set("Type plante")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        
     
    def plante1_aktivert(self):
        status1 = self.switch1.get()
        print("plante 1:",status1)
        
        file = open('bryter1', 'wb')
        pickle.dump(int(status1), file)
        file.close()
        
        
        

    def plante2_aktivert(self):
        status2 = self.switch2.get()
        print("plante 2:", status2)
        file = open('bryter2', 'wb')
        pickle.dump(int(status2), file)
        file.close()

    def prosent_plante1(self, value):
        value = self.progressbar_2.get()
        print(value)
        self.label3_tab_status.configure(text=value)


    def valg_av_plante1(self, valg: str):
        self.label1_tab_status.configure(text=valg)
    
    def valg_av_plante2(self, valg: str):
        self.label2_tab_status.configure(text=valg)
    
    def terskel_plante1(self, terskel1:int):
        #print(terskel1)
        self.slider_2_label.configure(text=int(terskel1))
        file = open('data1', 'wb')
        pickle.dump(int(terskel1), file)
        file.close()



    def terskel_plante2(self, terskel2:int):
        print(terskel2)
        self.slider_2_label2.configure(text=int(terskel2))
        file = open('data2', 'wb')
        pickle.dump(int(terskel2), file)
        file.close()
        
    
    def avlesing(self):
        #sensor 1
        touch1 = ss1.moisture_read()
        temp1 = ss1.get_temp()
        #sensor 2
        touch2 = ss2.moisture_read()
        #oppdatering av status side
        self.label3_tab_status.configure(text=(int(((touch1-320)/(1015-320)*100)),"%"))
        self.label4_tab_status.configure(text=(int(((touch2-320)/(1015-320)*100)),"%"))
        self.label5_tab_status.configure(text=(int(temp1),"°C"))
        self.progressbar_1.set(((touch1-320)/(1015-320)))
        self.progressbar_2.set(((touch2-320)/(1015-320)))
        self.after(2000, self.avlesing)
        

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("Kameratest")
        system('libcamera-hello -t 8000')
        
    def plot(self):
        system('python3 PLOTTING.py')
        
  

if __name__ == "__main__":
    app = App()
    app.mainloop()