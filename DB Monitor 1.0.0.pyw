import os
import pyaudio
import numpy as np
import dearpygui.dearpygui as dpg
import time,threading
import win32con
import win32gui
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from base64 import b64encode, b64decode
import psutil
import sys
import win32process
import os
import pystray
from PIL import Image
for i in psutil.process_iter():
    if i.pid==os.getpid():
        continue
    if i.name()=="DB Monitor.exe":
        hwnd_list = []
        win32gui.EnumWindows(lambda _hwnd, _hwnd_list: _hwnd_list.append(_hwnd), hwnd_list)
        for j in hwnd_list:
            app_pid= win32process.GetWindowThreadProcessId(j)[-1]
            if app_pid==i.pid:
                win32gui.ShowWindow(j, win32con.SW_SHOW)
                break
        sys.exit()
priv_key = b'-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEAkxLbXQryGLFWpSEfOMYjdXOOXZ3paHGzWPcKEZXwq2BKDQ9A\nWZ7aYrLX+oG+fOhv8sgwWFK3pM+gABzf4nSBOPkG3e8gOlsTLL3ACZoqgj/RszVx\nDCxOo4UGIaxVfQZ7ufVvtvVVG8DadMjSK101Ne8DEQlEGl+SF2OSFpy07XwN1qdP\n9QWeFgDitj2CO7CPnymm94ZZSD7l0MV1oHK87tI9IT+45dcWJwtrKv3csxvpM5L1\n3p9k2itU8+G65/uv6Cu7n77l9SdRs+5lj3u1hqY5bXDw+pPKy5t1BMyvROYMyHYE\naKUE3zZEs0TWJc0VY8dwlWKwd5Hk2VznB9mJvQIDAQABAoIBAD5QXYhJBHVo4ey6\nIWflL43qhZXtu8DId/RIS0hTLrL167onzZyLPT1XSEI36bUzqIcFwdISTgPzAng5\nw7RHp56ziHDNCesfvnqU9QI8gylHj/ptuLWvKiyHRqdKxLfh4NdUAd7TiJlnN0gG\n9GFyLwLof3Se5++CsbveML4K7G+4HNEFWobA5OajWuJu2ZuzsI527Oo8DH/dY73o\nD+CzxF2yoipB7sxjDXOwBNIbZEW5ZMB9rQQeqjatzfvx+xQaVW5eLpJP6DQP4gCn\nChghhwrt8I1adlP4iC1s00zvL0ekeD7V1nZnfzXVhUI5U2tRBvnVlsTEVHmqCI4/\nDOWKHqMCgYEAtvtp+qNrw1X+Rw1RYa14zyeS832VH96nqw19bgDIqyBD3cWt+nwa\n0xmAiP0+tuce7NwYCPIPV2sAAdUTF6eqSDycC93LmfIHdesbxpvedNyRJfZLSRsL\nbJk686IwX8catsJoSgQuYkEkKO+512ohi9zM37djpyb8bZfwz6e21B8CgYEAzcM1\nJo6R12YDNjKUcONuF9/9TOeAYZGDBjNB7bNswCj66fRARqUztJsuO6NaJT9I3vOI\ngEG63nQdgzOuJMdRkhKvF9Ex4yosJurwVAPBnx9MT0hp7H+cUUDM+8jI69hQEaUj\nbrVDQR+uANO7QLOGdDx+mvfm4RmKDgb4XjGQRqMCgYAMjNvs++51PF2vY+N0DqDd\nnHpAxxlGUVAwtEEpHVamHhVpjZhsOLziQ7qEKtJ1Ww7M8h+X5XpV5ZnfhkzD75UH\nVVjim3jOe0I1vUVvbttoKoSuFOF/ByLWdQANG8+zkgVsCZN7mCPSS2N+h0q40qew\nXxmSMpLcMRlZLvWuWHN6wwKBgQCVUwpajfLHOBAyn+hcOKDoELTZv9PKevh0YnSB\nFcphdhwJ9ylCW5e3hTq7KyQ7jb7Llj9EnO8Ji4jzc2j45fGLqaWKClZC/pMGN0/s\nGMHGQcd2bh349O8zhGx+eUte5R/OfmLFcCR7uYrkrMPjA6Ya6uAShL/4MjmfTm2m\nph+HMwKBgEU0Uf9aSVR8blQbCKj3F1fFcPcMAPFxwzSfgFzXqD/y+uVNw3njfL1c\nVUkGsCkk+QfeYQf/GJRbJ2+Hz7jiTPDTVY7yErtnYRXdANMIuIvtPse0rq8tQAXu\npoyBHPqfhFTk+M1DxwPxmJHWBSKkbZa0XYuvcjwPeh32Drf5x993\n-----END RSA PRIVATE KEY-----'
pub_key = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkxLbXQryGLFWpSEfOMYj\ndXOOXZ3paHGzWPcKEZXwq2BKDQ9AWZ7aYrLX+oG+fOhv8sgwWFK3pM+gABzf4nSB\nOPkG3e8gOlsTLL3ACZoqgj/RszVxDCxOo4UGIaxVfQZ7ufVvtvVVG8DadMjSK101\nNe8DEQlEGl+SF2OSFpy07XwN1qdP9QWeFgDitj2CO7CPnymm94ZZSD7l0MV1oHK8\n7tI9IT+45dcWJwtrKv3csxvpM5L13p9k2itU8+G65/uv6Cu7n77l9SdRs+5lj3u1\nhqY5bXDw+pPKy5t1BMyvROYMyHYEaKUE3zZEs0TWJc0VY8dwlWKwd5Hk2VznB9mJ\nvQIDAQAB\n-----END PUBLIC KEY-----'
import pystray
import tkinter as tk
from PIL import Image,ImageTk
import time
win=tk.Tk()
screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()
try:
    try:
        image = Image.open("launch.png")
    except:
        try:
            image = Image.open("launch.png")
        except:
            image = Image.open("launch.gif")
    image=image.resize((960,round(960/image.size[0]*image.size[1])))
    if image.size[1]<540:
        image=image.resize((round(540/image.size[1]*image.size[0]),540))
    x,y=(image.size[0]-960)//2,(image.size[1]-540)//2
    image=image.crop(box=(x,y,x+960,y+540))
    win.attributes("-alpha", 0.0)
    win.overrideredirect(True)
    width=960
    height=540
    size = '{}x{}+{}+{}'.format(width, height, int(screen_width / 2 - width / 2), int(screen_height / 2 - height / 2))
    win.geometry(size)
    p=ImageTk.PhotoImage(image)
    tk.Label(win,image=p).pack(side="left", ipadx=0,ipady=0,padx=-1,pady=-1)
    t=20000
    for i in range(t+1):
        win.attributes("-alpha", i/t)
        win.update()
    time.sleep(1.5)
    for i in range(t+1):
        win.attributes("-alpha", 1-i/t)
        win.update()
except:
    pass
win.destroy()
def show_app(a=1,b=1):
    global hwnd
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
log=[]
def exit_app(a=1,b=1):
    global log,write_log,tray_icon,hwnd
    tray_icon.stop()
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
    write_log()
    for i in psutil.process_iter():
        if i.name() == "DB Monitor.exe":
            i.kill()
    dpg.destroy_context()
    sys.exit()
class myopen:
    def __init__(self,file,mode):
        self.file=open(file,mode)
    def read(self):
        cipher_text = b64decode(self.file.read())
        decrypter = PKCS1_v1_5.new(RSA.import_key(priv_key))
        result = decrypter.decrypt(cipher_text, None).decode('utf-8')
        return result
    def write(self,s):
        plain_text = s.encode()
        encryptor = PKCS1_v1_5.new(RSA.import_key(pub_key))
        cipher_text = encryptor.encrypt(plain_text)
        res = b64encode(cipher_text).decode('utf-8')
        self.file.write(res)
    def __enter__(self):
        return self
    def __exit__(self,type,value,traceback):
        self.file.close()
if sys.argv[0][-3:]=="pyw":
    da=10
else:
    da=0
def update_fail():
    global fail
    fail=100
def read_log():
    global log_lost,lne
    with myopen("log.txt","a") as a:
        pass
    with myopen("log.txt","r") as a:
        try:
            lne=a.read()
        except:
            log_lost=True
            lne="Terminated."
def write_log():
    with myopen("log.txt", "w") as a:
        a.write("Terminated.")
def get_lock():
    with myopen("locked.txt","a") as a:
        pass
    with myopen("locked.txt","r") as a:
        try:
            return eval(a.read())
        except:
            log.append([time.strftime("%Y.%m.%d %H:%M:%S", time.localtime()), "File \"locked\" lost.", (221, 132, 82)])
            with myopen("locked.txt", "w") as a:
                a.write(str(False))
            return False
def unlock():
    global psww
    psww=True
    dpg.hide_item("fail")
    dpg.show_item("ps1")
    dpg.show_item("ps2")
    dpg.show_item("ps3")
def lock():
    global lock_,log
    lock_=True
    with myopen("locked.txt","w") as a:
        a.write(str(lock_))
    dpg.set_item_label("lock","Unlock")
    dpg.set_item_callback("lock",unlock)
    log.append([time.strftime("%Y.%m.%d %H:%M:%S", time.localtime()), "Variables locked.", (255, 255, 255)])
def ul2():
    global lock_, lock,log,psww
    psww = False
    dpg.hide_item("ps1")
    dpg.hide_item("ps2")
    dpg.hide_item("ps3")
    if dpg.get_value("ps2")=="DB2023":
        dpg.hide_item("fail")
        dpg.set_value("ps2","")
        lock_ = False
        with myopen("locked.txt", "w") as a:
            a.write(str(lock_))
        log.append([time.strftime("%Y.%m.%d %H:%M:%S", time.localtime()), "Variables unlocked.",(255, 255, 255)])
        dpg.set_item_label("lock", "Lock")
        dpg.set_item_callback("lock", lock)
    else:
        log.append([time.strftime("%Y.%m.%d %H:%M:%S", time.localtime()), "Failed to unlock.",(221, 132, 82)])
        dpg.set_value("ps2","")
        dpg.set_value("fail", "Fail to unlock.")
        dpg.show_item("fail")
        update_fail()
def get_db():
    global stream
    n=np.frombuffer(stream.read(1024),dtype=np.int16)
    f=np.fft.fft(n)
    fq=np.fft.fftfreq(len(n),1)**2
    p=np.abs(f)**2/len(f)
    return 10*np.log10(max(np.sum(p*fq)/1e-12,1))
def get_dt():
    with myopen("shift.txt","a") as a:
        pass
    with myopen("shift.txt","r") as a:
        try:
            return float(a.read())
        except:
            log.append([time.strftime("%Y.%m.%d %H:%M:%S", time.localtime()), "File \"shift\" lost.", (221, 132, 82)])
            with myopen("shift.txt", "w") as a:
                a.write(str(-get_db()+40))
            return -get_db()+40
def get_limit():
    with myopen("limit.txt","a") as a:
        pass
    with myopen("limit.txt","r") as a:
        try:
            return float(a.read())
        except:
            log.append([time.strftime("%Y.%m.%d %H:%M:%S", time.localtime()), "File \"limit\" lost.", (221, 132, 82)])
            with myopen("limit.txt", "w") as a:
                a.write(str(60))
            return 60.0
def update_data():
    global sec_n,dt,limit,max_,average,time_ax,db_ay,limit_
    sec_n = sec_n + 0.01
    db_val = get_db()
    time_ax.append(sec_n)
    db_ay.append(db_val)
    if sec_n<=5:
        limit_=[0,5]
        dpg.set_axis_limits("x",0,5)
    else:
        time_ax=time_ax[1:]
        limit_ = [time_ax[-1]-5, time_ax[-1]]
        db_ay=db_ay[1:]
        dpg.set_axis_limits("x", sec_n-5,sec_n)
    max_ = round(np.max(np.array(db_ay))+dt)
    average = round(np.average(np.array(db_ay))+dt)
    dpg.set_value('series_tag', [time_ax, np.array(db_ay)+dt])
    dpg.set_value('limit', [limit_, [limit,limit]])
    dpg.set_item_label('series_tag', "Noise DB:"+str(db_val+dt)[:7]+"db")
def time_func():
    global pre,fail
    if not dpg.is_mouse_button_down(0):
        pre=False
    if fail>=0:
        fail-=1
    else:
        dpg.hide_item("fail")
    update_data()
    timer_max_val = 0.01
    timer = threading.Timer(timer_max_val,time_func)
    timer.start()
def update_dt():
    global dt,lock_,pre,log,psww
    if lock_:
        dpg.set_value("dlt",dt)
        if pre == False:
            log.append([time.strftime("%Y.%m.%d %H:%M:%S", time.localtime()), "Fail to update shift.", (221, 132, 82)])
        pre = dpg.is_mouse_button_down(0)
        dpg.set_value("fail","Fail to update shift.(Variables have been locked)")
        if not psww:
            dpg.show_item("fail")
            update_fail()
        return
    if pre==False:
        log.append([time.strftime("%Y.%m.%d %H:%M:%S", time.localtime()), "DB shift updated.", (255, 255, 255)])
    pre = dpg.is_mouse_button_down(0)
    dt = dpg.get_value("dlt")
    with myopen("shift.txt","w") as a:
        a.write(str(dt))
def update_limit():
    global limit,lock_,pre,log,psww
    if lock_:
        dpg.set_value("lim",limit)
        if pre == False:
            log.append([time.strftime("%Y.%m.%d %H:%M:%S", time.localtime()), "Fail to update limit.", (221, 132, 82)])
        pre = dpg.is_mouse_button_down(0)
        dpg.set_value("fail", "Fail to update limit.(Variables have been locked)")
        if not psww:
            dpg.show_item("fail")
            update_fail()
        return
    if pre==False:
        log.append([time.strftime("%Y.%m.%d %H:%M:%S", time.localtime()), "DB limit updated.", (255, 255, 255)])
    pre = dpg.is_mouse_button_down(0)
    limit = dpg.get_value("lim")
    with myopen("limit.txt","w") as a:
        a.write(str(limit))
def time_func2():
    global ext,pss,psww
    ddpp=get_db()+dt
    dpg.set_value("dbb",str(round(ddpp)))
    move=0
    if ddpp>=100 or ddpp<=-10:
        dpg.set_item_font("dbb", "c")
        move = 50
    else:
        dpg.set_item_font("dbb", "a")
        move = 0
    dpg.set_value("aandm"," Max:{}  Average:{}".format(max_,average))
    dpg.configure_item("dbb", color=(255,255,255) if ddpp<=limit else (221, 132, 82))
    dpg.configure_item("dbb", pos=((321-dpg.get_item_rect_size("dbb")[0])//2-4,-17+move))
    dpg.configure_item("aandm", pos=((321 - dpg.get_item_rect_size("aandm")[0])//2-4, 260))
    if ddpp>limit:
        if not pss:
            if not ext:
                log.append([time.strftime("%Y.%m.%d %H:%M:%S", time.localtime()), "DB exceed the limit.", (221, 132, 82)])
                dpg.set_value("fail", "DB exceed the limit.")
                if not psww:
                    dpg.show_item("fail")
            ext=True
        pss=False
        if not psww:
            update_fail()
    else:
        ext=False
        pss=True
    timer_max_val = 0.2
    timer = threading.Timer(timer_max_val,time_func2)
    timer.start()
def time_func3():
    global log_,log
    for i in range(10000):
        if log_<len(log):
            dpg.add_text("["+log[log_][0]+"]"+log[log_][1],color=log[log_][2],parent="win3")
            log_+=1
    timer_max_val = 0.01
    timer = threading.Timer(timer_max_val,time_func3)
    timer.start()
def close():
    global hwnd
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
def main(sa=0):
    global fail,hwnd,log_,log,ext,pss,psww,limit,lock_,pre,dt,sec_n,max_,average,time_ax,db_ay,limit_,stream,lock,log_lost,lne,screen_width,screen_height
    fail = 0
    dpg.create_context()
    time_ax = []
    db_ay = []
    limit_ = [0]
    max_ = 0
    average = 0
    log_lost = False
    log=[]
    lne="Terminated."
    read_log()
    if lne!="Terminated.":
        log.append([time.strftime("%Y.%m.%d %H:%M:%S", time.localtime()),
                    "Program started after\nan abnormal termination.", (221, 132, 82)])
    else:
        log.append([time.strftime("%Y.%m.%d %H:%M:%S", time.localtime()), "Program started.", (255, 255, 255)])
    with myopen("log.txt","w") as a:
        a.write("Started.")
    if log_lost:
        log.append([time.strftime("%Y.%m.%d %H:%M:%S", time.localtime()), "File \"log\" lost.", (221, 132, 82)])
    log_ = 0
    ext = False
    pre = False
    pss = True
    lock_ = get_lock()
    psww = False
    stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    dt = get_dt()
    limit = get_limit()
    with dpg.font_registry():
        dpg.add_font("simsun.ttc", 300, id="a")
        dpg.add_font("simsun.ttc", 29, id="b")
        dpg.add_font("simsun.ttc", 200, id="c")
    with dpg.window(label="DB Value", tag="win2", pos=(615, 0), width=321, height=310, no_resize=True, no_close=True,
                    no_move=True, no_collapse=True):
        timer_max_val = 0.2
        sec_n = -0.01
        timer = threading.Timer(timer_max_val, time_func2)
        dt = get_dt()
        timer.start()
        dpg.add_text(str(round(get_db() + dt)), tag="dbb", pos=(10, -17))
        dpg.add_text(" Max:{}  Average:{}".format(max_, average), tag="aandm", pos=(10, 260))
        dpg.set_item_font("dbb", "a")
        dpg.set_item_font("aandm", "b")
    with dpg.window(label="Log", tag="win3", pos=(615, 309), width=321, height=391, no_resize=True, no_close=True,
                    no_move=True, no_collapse=True):
        timer_max_val = 0.01
        sec_n = -0.01
        timer = threading.Timer(timer_max_val, time_func3)
        dt = get_dt()
        timer.start()
    with dpg.window(label="DB Line", tag="win", pos=(0, 0), width=616, height=700, no_resize=True, no_close=True,
                    no_move=True, no_collapse=True):
        timer_max_val = 0.01
        sec_n = -0.01
        timer = threading.Timer(timer_max_val, time_func)
        dt = get_dt()
        timer.start()
        dpg.add_button(label="Lock", callback=lock, tag="lock")
        if lock_:
            dpg.set_item_label("lock", "Unlock")
            dpg.set_item_callback("lock", unlock)
        dpg.add_text("Password:", pos=(80, 27), tag="ps1")
        dpg.add_text("Fail to unlock.", pos=(80, 27), tag="fail", color=(221, 132, 82))
        dpg.add_input_text(pos=(149, 27), width=412, tag="ps2", password=True)
        dpg.add_button(label="Enter", tag="ps3", pos=(565, 27), callback=ul2)
        dpg.hide_item("ps1")
        dpg.hide_item("ps2")
        dpg.hide_item("ps3")
        dpg.hide_item("fail")
        with dpg.plot(height=550, width=600):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="", tag="x")
            dpg.set_axis_limits("x", 0, 5)
            dpg.add_plot_axis(dpg.mvYAxis, label="DB", tag="y_axis")
            dpg.set_axis_limits("y_axis", 0, 100)
            dpg.add_line_series(time_ax, db_ay, label="Noise DB", parent="y_axis", tag="series_tag")
            dpg.add_line_series(time_ax, limit_, label="Limit", parent="y_axis", tag="limit")
        dpg.add_text("Shift:")
        dpg.add_slider_float(default_value=dt, min_value=-200, max_value=0, width=600, callback=update_dt, tag="dlt")
        dpg.add_text("Limit:")
        dpg.add_slider_float(default_value=limit, min_value=0, max_value=100, width=600, callback=update_limit,
                             tag="lim")
    dpg.create_viewport(title='DB Monitor', width=942 + da, height=729 + da, resizable=False, always_on_top=True,
                        small_icon="icon.ico", large_icon="icon.ico", max_width=942 + da, max_height=729 + da,
                        disable_close=True,x_pos=int((screen_width-942 - da)/2),y_pos=int((screen_height-729 - da)/2))
    dpg.setup_dearpygui()
    dpg.set_exit_callback(close)
    dpg.show_viewport()
    hwnd=win32gui.FindWindow(None, "DB Monitor")
    dpg.start_dearpygui()
    dpg.destroy_context()
def create_tray_icon():
    global tray_icon
    image = Image.open("icon.ico")
    menu = (pystray.MenuItem("Show",show_app, default=True),pystray.MenuItem("Exit", exit_app))
    tray_icon = pystray.Icon("DB Monitor", image, "DB Monitor", menu)
    tray_icon.tooltip = "DB Monitor"
    tray_icon.run_detached()
    main()
create_tray_icon()


    
