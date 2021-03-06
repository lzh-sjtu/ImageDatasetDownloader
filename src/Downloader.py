import tkinter
import tkinter.font as ft
from tkinter.filedialog import askdirectory
import tkinter.messagebox
from threading import Thread
import time
import os

from myImageCrawler import myImageCrawler

# 窗口
mainWin = tkinter.Tk()
mainWin.title('Image Dataset Downloader')
mainWin.geometry('380x500')
mainWin.resizable(0, 0)

# 标题
titleFont = ft.Font(family='Helvetica', size=17, weight=ft.BOLD, slant=ft.ROMAN)
labelTitle = tkinter.Label(mainWin, text='Image Dataset Downloader', fg='#1296db', font=titleFont)
labelTitle.place(x=28, y=40)

# 关键词
textFont = ft.Font(family='Helvetica', size=12, weight=ft.BOLD, slant=ft.ROMAN)
inputFont = ft.Font(family='Helvetica', size=10, weight=ft.NORMAL, slant=ft.ROMAN)
labelKeyWord = tkinter.Label(mainWin, text='Keyword', font=textFont)
labelKeyWord.place(x=145, y=130)
entryKeyWord = tkinter.Entry(mainWin, width=80, font=inputFont)
entryKeyWord.place(x=110, y=170, width=150, height=30)

# 下载数量
textFont = ft.Font(family='Helvetica', size=12, weight=ft.BOLD, slant=ft.ROMAN)
inputFont = ft.Font(family='Helvetica', size=10, weight=ft.NORMAL, slant=ft.ROMAN)
labelNumber = tkinter.Label(mainWin, text='Number', font=textFont)
labelNumber.place(x=148, y=210)
entryNumber = tkinter.Entry(mainWin, width=80, font=inputFont)
entryNumber.place(x=110, y=250, width=150, height=30)

# 保存路径
textFont = ft.Font(family='Helvetica', size=12, weight=ft.BOLD, slant=ft.ROMAN)
inputFont = ft.Font(family='Helvetica', size=10, weight=ft.NORMAL, slant=ft.ROMAN)
labelPath = tkinter.Label(mainWin, text='Path', font=textFont)
labelPath.place(x=163, y=290)
path = tkinter.StringVar()
entryPath = tkinter.Entry(mainWin, width=80, textvariable=path, font=inputFont)
entryPath.place(x=110, y=330, width=150, height=30)

# 选择路径
def selectPath():
  path.set(askdirectory())
selectButtonFont = ft.Font(family='Helvetica', size=10, weight=ft.BOLD, slant=ft.ROMAN)
selectButton = tkinter.Button(mainWin, text='Save as', command=selectPath, bg='#838b8b', fg='white', font=inputFont)
selectButton.place(x=270, y=330, width=80, height=30)

# 更新进度条函数
def change_schedule(now_schedule, all_schedule):
    canvas.coords(fill_rec, (5, 5, 6 + (now_schedule / all_schedule) * 200, 30))
    mainWin.update()
    progress.set(str(int(now_schedule / all_schedule * 100)) + ' %')
    if round(now_schedule / all_schedule * 100, 2) == 100.00:
        progress.set("Finished")

# 下载图片（子线程任务）
def downloadImages():
    crawler.download()

# 下载
def download(*args):
    global downloadButton, crawler, number, canvas, fill_rec, progress

    keyword = entryKeyWord.get()
    number = entryNumber.get()
    path = entryPath.get().replace('\\','/')

    if not keyword:
        tkinter.messagebox.showerror('ERROR', message='Empty Keyword!')
    elif not number:
        tkinter.messagebox.showerror('ERROR', message='Empty Number!')
    elif not path:
        tkinter.messagebox.showerror('ERROR', message='Empty Path!')
    elif not os.path.exists(path):
        tkinter.messagebox.showerror('ERROR', message='Illegal Path!')
    else:
        try:
            number = int(number)

            downloadButton.place_forget()
            selectButton.place_forget()
            mainWin.update()

            crawler = myImageCrawler(keyword=keyword, number=number, path=path)

            pb = Thread(target=downloadImages)
            pb.setDaemon(True) # 设置为守护进程
            pb.start()

            # 显示进度条（主线程任务）
            canvas = tkinter.Canvas(mainWin, width=380, height=500)
            canvas.place(x=65, y=400)
            progress = tkinter.StringVar()

            out_rec = canvas.create_rectangle(5, 5, 205, 30, outline = "#1296db", width = 2)
            fill_rec = canvas.create_rectangle(5, 5, 5, 30, outline = "", width = 0, fill = "#1296db")

            labelPro = tkinter.Label(mainWin, textvariable=progress, fg='#1296db', font=textFont)
            labelPro.place(x=290, y=402)

            while crawler.progress < number:
                change_schedule(crawler.progress, number)
                time.sleep(0.1)

            pb.join()

            downloadButton.place(x=125, y=400, width=120, height=40)
            selectButton.place(x=270, y=330, width=80, height=30)
            canvas.place_forget()
            labelPro.place_forget()

            mainWin.update()

        except ValueError:
            tkinter.messagebox.showerror('ERROR', message='Illegal Number!')
        except:
            exit(1)


# 回车绑定
mainWin.bind('<Return>', download)
# 按钮绑定
downloadButton = tkinter.Button(mainWin, text='Download', command=download, bg='#1296db', fg='white', font=textFont)
downloadButton.place(x=125, y=400, width=120, height=40)

mainWin.mainloop()
