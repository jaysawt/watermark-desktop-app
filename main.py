from tkinter import *
from PIL import Image, ImageTk, ImageGrab
from tkinter import filedialog, messagebox, colorchooser

# -----Window initialization------#
window = Tk()
window.title('Watermark app')
window.config(pady=50, padx=150, bg='#FFF4F4')
window.maxsize(1000, 1000)
x = window.winfo_x()
y = window.winfo_y()


# ------Uploading an image to the app------------------#
def open_pic():
    global canvas_img  # this is done so that the image also exist in the main program rather than in the function
    filetypes = [('image type', ('.png', '.jpg', '.jpeg'))]
    pic = filedialog.askopenfilename(title='Load a Photo', initialdir='C:/Users/jayes/Downloads', filetypes=filetypes)
    if not pic:
        return messagebox.showinfo(title='Something went wrong', message='No photos were selected')

    # Load the image, resize and add to the canvas
    img = Image.open(pic)
    reshape = img.resize((720, 500), Image.LANCZOS)
    canvas_img = ImageTk.PhotoImage(reshape)
    canvas.itemconfig(default_img, image=canvas_img)


def canvas_text(event):
    text = watermark_text.get()
    canvas.itemconfig(can_txt, text=f'{text}')


def text_size(value):
    current_font = canvas.itemcget(can_txt, 'font')
    size = current_font.split(' ')[1]  # --> gives a default string 'Arial 20'
    new_font = current_font.replace(size, value)  # ---> replaces 20 with scale value
    canvas.itemconfig(can_txt, font=new_font)


def change_font(default_font):
    current_font = canvas.itemcget(can_txt, 'font')
    text = current_font.split(' ')[0]
    changed_font = current_font.replace(text, default_font)
    canvas.itemconfig(can_txt, font=changed_font)


def make_bold_itallic():
    if radio_state.get() == 1:
        current_font = canvas.itemcget(can_txt, 'font')
        text = current_font.split(' ')[2]
        changed_font = current_font.replace(text, 'bold')
        canvas.itemconfig(can_txt, font=changed_font)
    else:
        current_font = canvas.itemcget(can_txt, 'font')
        text = current_font.split(' ')[2]
        changed_font = current_font.replace(text, 'italic')
        canvas.itemconfig(can_txt, font=changed_font)


def pick_color():
    color = colorchooser.askcolor(title='Pick a color')
    if color[1]:
        canvas.itemconfig(can_txt, fill=color[1])


# ------------------ the below 3 methods are used to drag the watermark text to desired position-----------------#
def on_mouse_press(event):
    # Record the initial mouse position when the mouse is pressed
    canvas.tag_bind(can_txt, '<B1-Motion>', on_mouse_drag)
    canvas.tag_bind(can_txt, '<ButtonRelease-1>', on_mouse_release)


def on_mouse_drag(event):
    global start_x, start_y
    # Calculate the distance the mouse has moved
    dx = event.x - start_x
    dy = event.y - start_y

    # Move the canvas text item by the calculated distance
    canvas.move(can_txt, dx, dy)

    # Update the start_x and start_y for the next drag
    start_x, start_y = event.x, event.y


def on_mouse_release(event):
    # Unbind the mouse drag and release events
    canvas.tag_unbind(can_txt, '<B1-Motion>')
    canvas.tag_unbind(can_txt, '<ButtonRelease-1>')
# ------------------------------------------------------------------------------------------------#


def reset_text():
    canvas.itemconfig(can_txt, text='')
    watermark_text.delete(0, END)
    default_font.set(fonts[0])
    size_entry.set(20)
    radio_state.set(0)


def save_image():
    filetype = [('PNG file', '.png'), ('JPG file', '.jpg'), ('JPEG file', '.jpeg')]
    saved_image = filedialog.asksaveasfile(defaultextension='.jpg', filetypes=filetype,
                                           initialdir="C:/Users/jayes/PycharmProjects/Day 84 watermarking desktop",
                                           mode='wb')

    if saved_image:
    # Had to tweak coordinates because 4k resolution
        xc = window.winfo_rootx() + canvas.winfo_x() + 46
        yc = window.winfo_rooty() + canvas.winfo_y() + 62
        xd = xc + canvas.winfo_width() + 150
        yd = yc + canvas.winfo_height() + 110
        img = ImageGrab.grab().crop((xc, yc, xd, yd))
        img.show()
        img.save(saved_image)


# -----------Editing Window---------------------#
def editing_window():
    global watermark_text
    global size_entry
    global radio_state
    global default_font
    global fonts

    new_window = Toplevel()
    new_window.title('Editing window')
    new_window.config(pady=50, padx=50, bg='#FFF4F4')
    new_window.geometry("+%d+%d" % (x + 1050, y + 200))

    # --------------WATERMARK TEXT----------------------#
    watermark_label = Label(new_window, text='Watermark text', pady=5, bg='#FFF4F4')
    watermark_label.grid(row=0, column=0)
    watermark_text = Entry(new_window)
    watermark_text.focus()
    watermark_text.bind('<KeyRelease>', canvas_text)  # event binder to display text on canvas in real time
    watermark_text.grid(row=0, column=1)

    # drop down menu in tkinter for fonts
    font_label = Label(new_window, text='Font', pady=5, bg='#FFF4F4')
    font_label.grid(row=1, column=0)
    fonts = ["Arial", "Calibri", 'Cambria', 'Ebrima']
    default_font = StringVar()
    default_font.set(fonts[0])
    font_entry = OptionMenu(new_window, default_font, *fonts, command=change_font)
    font_entry.grid(row=1, column=1)

    # bold or italic text of watermark
    radio_state = IntVar()
    radiobutton1 = Radiobutton(new_window, text="Bold", value=1, variable=radio_state, command=make_bold_itallic)
    radiobutton1.grid(row=2, column=1)
    radiobutton2 = Radiobutton(new_window, text="Itallic", value=2, variable=radio_state, command=make_bold_itallic)
    radiobutton2.grid(row=2, column=0)

    # Colour for the watermark text
    color_label = Label(new_window, text='Color', pady=5, bg='#FFF4F4')
    color_label.grid(row=3, column=0)
    color_entry = Button(new_window, text='Pick a color', command=pick_color)
    color_entry.grid(row=3, column=1)

    # Adjust size for the watermark text
    size_label = Label(new_window, text='Size', pady=5, bg='#FFF4F4')
    size_label.grid(row=4, column=0)
    size_entry = Scale(new_window, from_=1, to=100, orient=HORIZONTAL, bg='#FFF4F4', command=text_size)
    size_entry.grid(row=4, column=1)
    size_entry.set(20)  # slider will be on default 20 value

    position_label = Label(new_window, text='Use Mouse pointer to move the watermark to the desired position', pady=5,
                           bg='#FFF4F4')
    position_label.grid(row=5, column=0, columnspan=2)

    # clear changes  of watermark
    reset = Button(new_window, text='Reset Changes', pady=5, padx=5, command=reset_text)
    reset.grid(row=6, column=1)

    save = Button(new_window, text='Apply and Save image', pady=5, command=save_image)
    save.grid(row=6, column=0)


# -----GUI home------#
watermark = Label(text='Watermark App🖌️', font=("Arial Black", 30), pady=20, fg='#3F2305', bg='#FFF4F4')
watermark.grid(column=0, row=0, columnspan=2)
image = Image.open('A Hotel.png')
photo = ImageTk.PhotoImage(image)
canvas = Canvas(width=720, height=500)
canvas.grid(column=0, row=1, columnspan=2, pady=20)
default_img = canvas.create_image(360, 250, image=photo)
can_txt = canvas.create_text(360, 250, text='', font=('Arial', 20, ''))
start_x, start_y = canvas.coords(can_txt)

# Bind the mouse press event to start dragging the text
canvas.tag_bind(can_txt, '<ButtonPress-1>', lambda event: on_mouse_press(event))

upload_button = Button(text='Upload Image', font=5, fg='#0E2954', bg='#EF6262', command=open_pic)
upload_button.grid(column=0, row=2)

edit_button = Button(text='Edit Image', font=5, fg='#0E2954', bg='#EF6262', command=editing_window)
edit_button.grid(column=1, row=2)

window.mainloop()
