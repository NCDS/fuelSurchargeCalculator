#!/usr/bin/env python
from tkcalendar import Calendar, DateEntry
import fuelSurchargeCalculator as fsc
import customtkinter as ctk
import tkinter as tk
import calendar

#Global vars to retain user choices, probably a better way to handle this
tDate = 0
tDest = "0"
DEBUG = True

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Layout
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.geometry("400x450")
        self.title("Fuel Surcharge Calculator")
        self.minsize(400, 300)

        #self.grid_rowconfigure(0, weight=1)
        #self.grid_columnconfigure((0, 1), weight=1)

        # Main Label    
        root_label_font = ("",30,"bold")
        self.label =ctk.CTkLabel(
            master=self,
            font=root_label_font,
            text="Fuel Surcharge Calculator"
        )
        self.label.pack(pady=5, padx=0)

        # Main Conatiner
        self.frame = ctk.CTkFrame(master=self)
        self.frame.pack(pady=5, padx=5, fill="both", expand=True)

        # Second label
        self.secondary_label = ctk.CTkLabel(
            master=self.frame,
            text="Please submit the following criteria:"
        )
        self.secondary_label.pack(pady=0, padx=0)

        # Landfill Option Menu
        def landfillOption_callback(cb):
            global tDest
            tDest = str(cb)
            if DEBUG:
                print("D:landfillOption_callback() tDest = "+tDest)

        landfillOption_var = ctk.StringVar(value="Select Landfill...")
        self.combobox = ctk.CTkOptionMenu(
            master=self.frame,
            values=["Millseat", "High Acres", "Ontario", "Hyland"],
            command=landfillOption_callback,
            variable=landfillOption_var,
        )
        self.combobox.pack(side="top", pady=0, padx=10, anchor="w")

        # Main data handling
        def logData():
            global tDate
            global tDest
            try:
                tDate = str(fsc.roundDate(str(cal.get_date()), "%x"))
                if DEBUG:
                    print("D:logData() tDate = "+tDate)
                    vals = (tDest, tDate)
                    for i in vals:
                        print("D:logData() 'i' in vals = "+str(i))
                    
                fee = round(fsc.calculateSurcharge(tDest, tDate, "%x"),2)
                print("D:logData() fee = "+str(fee))
                if fee < 0:
                    resultText = "Diesel costs do not warrant a surcharge at this level."
                elif fee > 0:
                    resultText = "The Fuel Surcharge is $"+str(fee)+"/load for the week starting "+tDate+"."
                elif fee == 0:
                    resultText = "Failed to calculate data, did you specify a destination in the drop down menu?"
            except (UnboundLocalError, IndexError) as e:
                resultText = "Please double check the date you've selected. \nDespite my best efforts, I can't predict the future."

            # Top layer Results window
            window = ctk.CTkToplevel(self.frame)
            window.geometry("450x100+30+300")
            window.title("EIA Results")
            labelFont = ("",10,"bold")
            tl_main_label = ctk.CTkLabel(window, text="Results based on averages provided by eia.gov", font=labelFont)
            tl_main_label.pack(side="bottom", fill="both", expand=True, padx=5, pady=0)
            tl_label = ctk.CTkLabel(window, text=resultText)
            tl_label.pack(fill="both", expand=True, padx=5, pady=10)
            
        # Confirm Selections Button
        self.button = ctk.CTkButton(self.frame, height=12, corner_radius=12, text="Confirm Selections", command=logData)
        self.button.pack(side="bottom", pady=2, padx=10, anchor="e")

        # Calendar
        cal = Calendar(self.frame, selectmode="day")
        cal.minsize="200x200"
        cal.pack(pady=5, padx=5, fill="both", expand=True)

# Main loop
if __name__ == "__main__":
    app = App()
    app.mainloop()
    







    
