import Tkinter as Tk
from PIL import Image, ImageTk
import tkMessageBox as tkMeg
import tkFileDialog
import stitched
import cv2

class MainPage(object):
    def __init__(self, master=None):
        self.root = master
        self.root.geometry('%dx%d' % (800, 700))
        self.route_first = 'Unknown.jpg'
        self.route_second = 'Unknown.jpg'
        self.route_stitch = 'Unknown.jpg'
        self.stitcher = stitched.Stitcher()
        img_open = Image.open('Unknown.jpg')
        self.fname = 'Click Me ^-^ ~'
        self.img_png_first = ImageTk.PhotoImage(img_open)
        self.img_png_second = ImageTk.PhotoImage(img_open)
        self.img_png_stitch = ImageTk.PhotoImage(img_open)
        self.h_box = 260
        self.w_box = 260
        self.createPage()

    def createPage(self):
        self.page = Tk.Frame(self.root)
        self.page.pack()
        Tk.Label(self.page).grid(row=0, stick='n')
        # Tk.Button(self.page, text='Quit', command=self.page.quit).grid(row=0, stick='n')
        self.label_img1 = Tk.Label(self.page, image=self.img_png_first).grid(row=1, column=0, sticky='N')
        Tk.Label(self.page, text='        ').grid(row=1, column=1, stick='n')
        self.label_img2 = Tk.Label(self.page, image=self.img_png_second).grid(row=1, column=2, stick='n')
        Tk.Label(self.page, text=self.fname).grid(stick='n', row=2,column =0)
        Tk.Label(self.page, text=self.fname).grid(stick='n', row=2, column=2)
        Tk.Button(self.page, text='First Image', command=self.GetFirstImage).grid(row=3, column=0, stick='n')
        Tk.Button(self.page, text='Second Image', command=self.GetSecondImage).grid(row=3,column = 2, stick='n')
        self.img_stitch = self.label_img3 = Tk.Label(self.page,image = self.img_png_stitch).grid(row= 4, column = 0, sticky = 'N', columnspan= 3)
        Tk.Button(self.page, text = 'Please! Please! Please Click Me~',command = self.stitching).grid(row = 5, column = 0, stick = 'n')
        Tk.Button(self.page, text = 'Want Save the Image?',command = self.save).grid(row = 5,column = 2, stick = 'n')
        # try:
        #     self.label_img1.pack()
        #     # self.label_img2.pack()
        #     # self.label_img3.pack()
        # except:
        #     a = 1

    def GetFirstImage(self):
        self.on_click()
        self.route_first = self.fname
        img_open = Image.open(self.route_first)
        w,h = img_open.size
        width, height = self.find_factor(w,h)
        img_open = img_open.resize((width,height),Image.ANTIALIAS)
        self.img_png_first = ImageTk.PhotoImage(img_open)
        Tk.Label(self.page, text=self.fname).grid(row=2, column=0, stick='n')
        try:
            Tk.Label(self.page, image=self.img_png_first).grid(row=1, column=0, stick='n').pack()
        except:
            a=1

    def GetSecondImage(self):
        self.on_click()
        self.route_second = self.fname
        img_open = Image.open(self.route_second)
        w, h = img_open.size
        width, height = self.find_factor(w, h)
        img_open = img_open.resize((width, height), Image.ANTIALIAS)
        self.img_png_second = ImageTk.PhotoImage(img_open)
        Tk.Label(self.page, text=self.fname).grid(row=2, column=2, stick='n')
        try:
            Tk.Label(self.page, image=self.img_png_second).grid(row=1, column=2, stick='n').pack()
        except:
            a = 1

    def on_click(self):
        self.fname = tkFileDialog.askopenfilename(initialdir="/Users", title="Select file")

    # def createPage_tem(self,master_tem):
    #     self.root_tem = master_tem
    #     self.page_tem = Tk.Frame(self.root_tem)
    #     self.page_tem.pack()
    #     Tk.Label(self.page_tem,text = 'Click Me ~').grid(stick='n', row=0)
    #     Tk.Button(self.page_tem,text = 'Please select an image ^_^',command = self.on_click).grid(row=1,stick = 'n')

    def find_factor(self,w,h):
        f1 = 1.0 * self.w_box / w  # 1.0 forces float division in Python2
        f2 = 1.0 * self.h_box / h
        factor = max([f1, f2])
        width = int(w * factor)
        height = int(h * factor)
        return width,height

    def stitching(self):
        imageA = cv2.imread(self.route_first)
        imageB = cv2.imread(self.route_second)
        [result,via] = self.stitcher.stitch([imageA,imageB],showMatches=True)
        cv2.imwrite('tem.jpg',result)
        self.img_open_original = Image.open('tem.jpg')
        w, h = self.img_open_original.size
        f1 = 1.0 * self.w_box / w  # 1.0 forces float division in Python2
        f2 = 1.0 * self.h_box / h
        factor = max([f1, f2])
        width = int(w * factor)
        height = int(h * factor)
        img_open = self.img_open_original.resize([width,height], Image.ANTIALIAS)
        image_tem = ImageTk.PhotoImage(img_open)
        # self.stitch.comgif(image = image_tem)
        Tk.Label(self.page,image = image_tem).grid(row= 4, column = 0, sticky = 'N', columnspan= 3).pack()

    def save(self):
        save_address = "stitched.jpg"
        save_img = cv2.imread('tem.jpg')
        cv2.imwrite(str(save_address), save_img)
        tkMeg.showinfo('Save picture', 'We are already named in ' + save_address)

class LoginPage(object):
    def __init__(self, master):
        self.root = master
        self.root.geometry('%dx%d' % (300,180))
        self.username = Tk.StringVar()
        self.password = Tk.StringVar()
        self.createPage()

    def createPage(self):
        self.page = Tk.Frame(self.root)
        self.page.pack()
        Tk.Label(self.page).grid(row=0, stick='w')
        Tk.Label(self.page, text = 'Username: ').grid(row=1, stick='w', pady=10)
        Tk.Entry(self.page, textvariable=self.username).grid(row=1, column=1, stick='e')
        Tk.Label(self.page, text = 'Password: ').grid(row=2, stick='w', pady=10)
        Tk.Entry(self.page, textvariable=self.password, show='*').grid(row=2, column=1, stick='e')
        Tk.Button(self.page, text='Login', command=self.loginCheck).grid(row=3, stick='w', pady=10)
        Tk.Button(self.page, text='Quit', command=self.page.quit).grid(row=3, column=1, stick='e')

    def loginCheck(self):
        name = self.username.get()
        secret = self.password.get()
        # if 1==1:
        if name=='admin' and secret=='admin':
            self.page.destroy()
            MainPage(self.root)
        else:
            tkMeg.showinfo(title='Wrong!', message='That password is incorrect. Please check that you entered the right one.')

if __name__ == "__main__":
    root = Tk.Tk()
    root.title('Image Stitch Program')
    LoginPage(root)
    root.mainloop()