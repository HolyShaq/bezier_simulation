from tkinter import *
from tkinter import colorchooser


class ControlPanel:
    master = Tk()
    master.geometry("285x200")
    master.title("Control Panel")

    global_t = 0
    interp_speed = 5  # Interpolation goes from 0 to 1000, interp_speed is added every frame
    d = 1

    def __init__(self):
        # Animation Toggle
        self.frm_anim_mode = Frame(self.master, bd=1, relief=SOLID)
        self.lbl_anim_mode = Label(self.master, text="Interpolation")

        self.frm_radios = Frame(self.frm_anim_mode)
        self.interp_mode = IntVar()
        self.radio_auto = Radiobutton(self.frm_radios, text="Automatic", variable=self.interp_mode, value=0,
                                      command=self.change_anim_mode)
        self.radio_manual = Radiobutton(self.frm_radios, text="Manual", variable=self.interp_mode, value=1,
                                        command=self.change_anim_mode)
        self.radio_auto.grid(column=0, row=0)
        self.radio_manual.grid(column=1, row=0)

        self.frm_interp_speed = Frame(self.frm_anim_mode)
        self.lbl_interp_speed = DynamicLabel(self.frm_interp_speed, "Speed:", 5)
        self.slider_interp_speed = Scale(self.frm_interp_speed, from_=0, to=30, showvalue=False, orient=HORIZONTAL,
                                         command=self.update_slider_labels)
        self.lbl_interp_speed.pack()
        self.slider_interp_speed.pack()

        self.frm_tval = Frame(self.frm_anim_mode)
        self.lbl_tval = DynamicLabel(self.frm_tval, "T-Value:", 0)
        self.slider_tval = Scale(self.frm_tval, from_=0, to=1000, showvalue=False, orient=HORIZONTAL,
                                 command=self.update_slider_labels)
        self.lbl_tval.pack()
        self.slider_tval.pack()

        self.lbl_anim_mode.pack()
        self.frm_radios.pack()
        self.change_anim_mode()

        self.lbl_anim_mode.grid(column=0, row=0)
        self.frm_anim_mode.grid(column=0, row=1, padx=10, sticky="n")

        # Level Controls
        self.frm_levels = Frame(self.master, bd=1, relief=SOLID)
        self.lbl_levels = Label(self.master, text="Levels")
        self.levels = []

        self.lbl_levels.grid(column=1, row=0)
        self.frm_levels.grid(column=1, row=1, sticky="n")

    def change_anim_mode(self):
        if self.interp_mode.get() == 0:
            self.frm_tval.pack_forget()
            self.frm_interp_speed.pack()
        else:
            self.frm_interp_speed.pack_forget()
            self.slider_tval.set(self.global_t * 1000)
            self.update_slider_labels(self.global_t * 1000)
            self.frm_tval.pack()

    def update_slider_labels(self, val):
        if self.interp_mode.get() == 0:
            self.lbl_interp_speed.update(val)
            self.interp_speed = int(val)
        else:
            self.lbl_tval.update(val)
            self.global_t = float(val) / 1000

    def update_levels(self, color_depth_dict, point_len):
        for level in self.levels:
            level.pack_forget()

        self.levels = []
        for key, val in color_depth_dict.items():
            level = Level(self.frm_levels, key, val)
            self.levels.append(level)

        for level in self.levels[:point_len - 1]:
            level.pack()


class Level:
    def __init__(self, master, depth, color):
        self.master = master
        self.depth = depth
        self.color = color

        _lbl_text = f"Level {self.depth}" if self.depth != 0 else "Curve"
        self.lbl_level = Label(self.master, text=_lbl_text)
        self.toggle = IntVar()
        self.chk_toggle = Checkbutton(self.master, variable=self.toggle)
        self.chk_toggle.select()

        self.btn_color = Button(self.master, background=_from_rgb(self.color), width=2, command=self.choose_color)

    def pack(self):
        self.btn_color.grid(column=0, row=self.depth, padx=1, pady=1, sticky="w")
        self.lbl_level.grid(column=1, row=self.depth)
        self.chk_toggle.grid(column=2, row=self.depth)

    def pack_forget(self):
        self.btn_color.grid_forget()
        self.lbl_level.grid_forget()
        self.chk_toggle.grid_forget()

    def choose_color(self):
        self.color, _ = colorchooser.askcolor(_from_rgb(self.color))
        self.btn_color.configure(background=_from_rgb(self.color))


class DynamicLabel:
    def __init__(self, master, text, val):
        self.master = master
        self.text = text
        self.val = val

        self.frame = Frame(self.master)
        self.staticLabel = Label(self.frame, text=self.text)
        self.dynamicLabel = Label(self.frame, text=self.val)
        self.staticLabel.grid(row=0, column=0)
        self.dynamicLabel.grid(row=0, column=1)

    def pack(self):
        self.frame.pack()

    def update(self, new_val):
        self.val = new_val
        self.dynamicLabel.configure(text=self.val)

        self.frame.pack()


def _from_rgb(rgb):
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'


if __name__ == "__main__":
    control_panel = ControlPanel()
    control_panel.master.mainloop()
