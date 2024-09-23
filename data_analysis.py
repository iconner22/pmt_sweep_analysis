import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk
from PIL import Image
import os
import pandas as pd
from scipy.optimize import curve_fit
# Define the main application class
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.title("PMT Calibration - Sweep Analysis")
        self.geometry("1051x600")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1) 

        self.base_frame = ctk.CTkFrame(self, fg_color="#5D707F")
        self.base_frame.grid(row = 0, column = 0, sticky = "nsew")

        self.base_frame.columnconfigure(0, weight=1)
        self.base_frame.rowconfigure(0, weight=1)
        self.base_frame.rowconfigure(1, weight=10)

        self.top_frame = ctk.CTkFrame(self.base_frame, fg_color="#5D707F")
        self.top_frame.grid(row = 0, column = 0, sticky = "nsew")
        self.top_frame.columnconfigure((0,1,2,3), weight=1)
        self.top_frame.rowconfigure(0, weight=1)

        self.bottom_frame = ctk.CTkFrame(self.base_frame, fg_color="#5D707F")
        self.bottom_frame.grid(row = 1, column = 0, sticky = "nsew")
        self.bottom_frame.columnconfigure(0, weight=4)
        self.bottom_frame.columnconfigure(1, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)

        self.graph_tabs = ctk.CTkTabview(self.bottom_frame, fg_color="#E5E5E5", segmented_button_selected_color= "#bf1131", segmented_button_selected_hover_color="#da796e")
        self.graph_tabs.grid(row = 0, column = 0, sticky = "nsew", padx = 20, pady = 10)
        self.graph_tabs.add("HV - Gain")
        self.graph_tabs.add("LED - Gain")

        self.led_fig = Figure()
        self.led_canvas = FigureCanvasTkAgg(self.led_fig, master = self.graph_tabs.tab("LED - Gain"))
        self.led_canvas.get_tk_widget().pack(fill = "both", expand = True, padx = 5, pady = 5 )

        self.hv_fig = Figure()
        self.hv_canvas = FigureCanvasTkAgg(self.hv_fig, master = self.graph_tabs.tab("HV - Gain"))
        self.hv_canvas.get_tk_widget().pack(fill = "both", expand = True, padx = 5, pady = 5 )



        self.jlab_logo =  ctk.CTkImage(light_image= Image.open(os.path.join("Img", "jlab_logo.png")), size = (200,65))
        self.logo_button = ctk.CTkLabel(self.top_frame, image=self.jlab_logo, text= "")
        self.logo_button.grid(row = 0, column = 0, sticky = "w", padx = (20,10), pady = (10,5))

        self.help_button = ctk.CTkButton(self.top_frame, text="Help", fg_color="#bf1131",hover_color="#da796e", height=64, command = self.help_pop)
        self.help_button.grid(row = 0, column = 1, sticky = "ew", padx = 10, pady = (10,5))

        self.about_button = ctk.CTkButton(self.top_frame, text="About", fg_color="#bf1131",hover_color="#da796e",height=64, command = self.about_pop)
        self.about_button.grid(row = 0, column = 2, sticky = "ew", padx = 10, pady = (10,5))

        self.open_file_button = ctk.CTkButton(self.top_frame, text="Open File...", fg_color="#bf1131",hover_color="#da796e", command = self.open_file, height   = 64)
        self.open_file_button.grid(row = 0, column = 3, sticky = "ew", padx = (10,20), pady = (10,5))

        self.stability_frame = ctk.CTkFrame(self.bottom_frame, fg_color="#bf1131")
        self.stability_frame.grid(row = 0, column = 1, sticky = "nsew", padx = 20, pady = (25,10))

        self.stability_frame.columnconfigure(0, weight=1)
        self.stability_frame.rowconfigure(0, weight=2)
        self.stability_frame.rowconfigure(1, weight=1)

        self.stability_top_frame = ctk.CTkFrame(self.stability_frame, fg_color="#da796e")
        self.stability_top_frame.grid(row = 0, column = 0, sticky = "nsew", padx = 5, pady = 5)

        self.stability_top_frame.columnconfigure(0, weight = 1)
        self.stability_top_frame.rowconfigure((0,1,2,3), weight = 1)

        self.stability_equation_label = ctk.CTkLabel(self.stability_top_frame, text= "Equation: Q1(Voltage)", fg_color="#bf1131", corner_radius= 5)
        self.stability_equation_label.grid(sticky = "nsew", row = 0, column = 0, padx = 10, pady = 10)

        self.equation_label = ctk.CTkLabel(self.stability_top_frame, text = "")
        self.equation_label.grid(row = 1, column = 0)

        self.stability_label = ctk.CTkLabel(self.stability_top_frame, text= "Q1 Stability",  fg_color="#bf1131", corner_radius=  5)
        self.stability_label.grid(sticky = "nsew", row = 2, column = 0, padx = 10, pady = 10)

        self.q1_stability_label = ctk.CTkLabel(self.stability_top_frame, text="")
        self.q1_stability_label.grid(row=3, column=0)

        self.stability_bottom_frame = ctk.CTkFrame(self.stability_frame, fg_color="#da796e")
        self.stability_bottom_frame.grid(row = 1, column = 0, sticky = "nsew", padx = 5, pady = 5)
        self.stability_bottom_frame.columnconfigure((0,1), weight=1)
        self.stability_bottom_frame.rowconfigure((0,1), weight=1)

        self.ideal_gain_label = ctk.CTkLabel(self.stability_bottom_frame, text="Ideal Gain", fg_color="#bf1131", corner_radius=5)
        self.ideal_gain_label.grid(row = 0, column = 0, sticky = "ew", padx = 5, pady = 5)
        self.ideal_gain_entry = ctk.CTkEntry(self.stability_bottom_frame, fg_color="#E5E5E5" ,text_color="#5D707F")
        self.ideal_gain_entry.grid(row = 0, column = 1, sticky = "ew", padx = 5, pady = 5)
        self.ideal_gain_entry.bind("<Return>", self.on_entry_click)

        self.ideal_voltage_label = ctk.CTkLabel(self.stability_bottom_frame, text = "",fg_color="#bf1131", corner_radius= 5 )
        self.ideal_voltage_label.grid(row = 1, column = 0, columnspan = 2, sticky = "nswe", padx = 5, pady = 5)


        self.stability_percent = 0
        self.params = None


    def about_pop(self, *event):

        popup = ctk.CTkToplevel()  # Create a new Toplevel window
        popup.geometry("500x100")  # Set size of popup window
        popup.title("About Window")
        popup.configure(fg_color="#5D707F")
        # Add a label in the popup window
        label = ctk.CTkLabel(popup, text=f"GUI used to analyze single LED and HV sweeps.\nFor use in PMT Calibration.\nAuthor:Ian Conner", anchor="w")
        label.pack(pady=20)


    def help_pop(self, *events):
        popup = ctk.CTkToplevel()  # Create a new Toplevel window
        popup.geometry("900x200")  # Set size of popup window
        popup.title("Help Window")
        popup.configure(fg_color="#5D707F")
        # Add a label in the popup window
        label = ctk.CTkLabel(popup,
                             text=f"This GUI uses the data read in from the file chosen with the Open File Button.\nThe file should be comma seperated and have both High Voltage and LED Sweep Data and follow the following structure:\nHigh_Voltage,Q_1,LED,mu_1,HV\n" +
                                  f"1520,46,0.6,0.6,True\n1400,28,2.68,0.3,False\nThe boolean value determines if it is a HV Sweep (True) or LED Sweep (False).\nHigh Voltage Sweeps occur at a stable LED value and HV increments.\nLED Sweeps occur at a stable high voltage and LED increments.")
        label.pack(pady=20)

    def on_entry_click(self, event):
        if self.params is not None:
            gain = float(self.ideal_gain_entry.get())
            a = self.params[0]
            b = self.params[1]
            c = self.params[2] - gain

            pos_q = (-b + np.sqrt(b**2 - 4*a*c))/(2*a)
            neg_q = (-b - np.sqrt(b**2 - 4*a*c))/(2*a)
            ideal_voltage = max(pos_q, neg_q)
            self.ideal_voltage_label.configure(text = f"Ideal Voltage {ideal_voltage:.2f}")

    def open_file(self):

        file_path = tk.filedialog.askopenfilename(title="Select a File", filetypes=[("All Files", "*.*"), ("Text Files", "*.txt")])
        data_frame = pd.read_csv(file_path)
        hv_sweep = data_frame[data_frame["HV"] == True]
        led_sweep = data_frame[data_frame["HV"] == False]
        self.hv_graph(hv_sweep)
        self.led_graph(led_sweep)

    def hv_graph(self, df):
        def poly_fit(x, a, b, c):
            return a*x**2 + b*x + c

        x_vals = df["High_Voltage"]
        y_vals = df["Q_1"]
        params, cov_matrix = curve_fit(poly_fit, x_vals, y_vals)
        self.params = params
        x_fit = np.linspace(x_vals.min(), x_vals.max(),100)
        y_fit = poly_fit(x_fit, *params)
        self.hv_fig.clear()
        hv_fig_plot = self.hv_fig.gca()
        hv_fig_plot.scatter(x_vals, y_vals, color = "#5D707F", label = "Experimental Data")
        hv_fig_plot.plot(x_fit, y_fit, alpha=0.5, color="r", linewidth=5, label="Fitted Data")
        hv_fig_plot.set_xlabel("High Voltage (V)")
        hv_fig_plot.set_ylabel("rGain ($Q_1$)")
        hv_fig_plot.legend(frameon = False)
        self.hv_fig.tight_layout()
        self.hv_canvas.draw()

        self.equation_label.configure(text = f"Q1 = {params[0]:.4g}*V^2+{params[1]:.4g}*V+{params[2]:.4g}")



    def led_graph(self, df):
        x_vals = df["mu_1"]
        y_vals = df["Q_1"]
        avg = y_vals.mean()
        ten_p = 0.1 * y_vals.mean()
        five_p = 0.05 * y_vals.mean()
        self.led_fig.clear()
        led_fig_plot = self.led_fig.gca()
        led_fig_plot.scatter(x_vals, y_vals,color = "#5D707F")
        led_fig_plot.set_xlabel(r"$\mu$ photoelectrons")
        led_fig_plot.set_ylabel(r"Gain ($Q_1$) - 5% Increments")

        led_fig_plot.axhline(y = avg, linestyle = "--", color = 'r', alpha = 0.5)
        led_fig_plot.axhline(y = avg + five_p, linestyle = "--", color = 'r', alpha = 0.5)
        led_fig_plot.axhline(y = avg - five_p, linestyle = "--", color = 'r', alpha = 0.5)
        led_fig_plot.axhline(y = avg + ten_p, linestyle = "--", color = 'r', alpha = 0.5)
        led_fig_plot.axhline(y = avg - ten_p, linestyle = "--", color = 'r', alpha = 0.5)

        max_stability = (y_vals.max() - y_vals.mean())/y_vals.mean()
        min_stability = (y_vals.min() - y_vals.mean())/y_vals.mean()
        stability = max(abs(max_stability), abs(min_stability))
        self.q1_stability_label.configure(text = f"All Q1 within {stability * 100:.2f} % of avg.")
        self.led_fig.tight_layout()
        self.led_canvas.draw()


# Main entry point
if __name__ == "__main__":
    # Set the appearance mode and color theme (optional)
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Create and run the application
    app = App()
    app.mainloop()
