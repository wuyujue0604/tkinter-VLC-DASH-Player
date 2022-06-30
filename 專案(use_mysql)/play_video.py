import os, platform , time , add_information , cmd_process
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

import platform

if platform.system() == 'Windows':
    import ctypes
    myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string(任意字符串)
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)#在工作列顯是我的icon

# 設置VLC庫路徑，需在import vlc之前
os.environ['PYTHON_VLC_MODULE_PATH'] = "./vlc/"

import vlc
mypath="http://180.218.7.38/1.mpd"
old_mypath = "http://180.218.7.38/1.mpd"
vol = 100
mode = 0
loop = False
search_result=[]

class Player:
    '''
        args:設置 options
    '''

    def __init__(self, *args):
        if args:
            instance = vlc.Instance(*args)
            self.media = instance.media_player_new()
        else:
            self.media = vlc.MediaPlayer()

    # 設置待播放的url地址或本地文件路徑，每次調用都會重新加載資源
    def set_uri(self, uri):
        self.media.set_mrl(uri)

    # 播放 成功返回0，失敗返回-1
    def play(self, path=None):
        if path:
            self.set_uri(path)
            return self.media.play()
        else:
            return self.media.play()

    # 暫停
    def pause(self):
        self.media.pause()

    # 恢復
    def resume(self):
        self.media.set_pause(0)

    # 停止
    def stop(self):
        self.media.stop()

    # 釋放資源
    def release(self):
        return self.media.release()

    # 是否正在播放
    def is_playing(self):
        return self.media.is_playing()

    # 已播放時間，返回毫秒值
    def get_time(self):
        return self.media.get_time()

    # 拖動指定的毫秒值處播放。成功返回0，失敗返回-1 (需要注意，只有當前多媒體格式或流媒體協議支持纔會生效)
    def set_time(self, ms):
        return self.media.set_time(ms)

    # 音視頻總長度，返回毫秒值
    def get_length(self):
        return self.media.get_length()

    # 獲取當前音量（0~100）
    def get_volume(self):
        return self.media.audio_get_volume()

    # 設置音量（0~100）
    def set_volume(self, volume):
        return self.media.audio_set_volume(volume)

    # 返回當前狀態：正在播放；暫停中；其他
    def get_state(self):
        state = self.media.get_state()
        if state == vlc.State.Playing:
            return 1
        elif state == vlc.State.Paused:
            return 0
        else:
            return -1

    # 當前播放進度情況。返回0.0~1.0之間的浮點數
    def get_position(self):
        return self.media.get_position()

    # 拖動當前進度，傳入0.0~1.0之間的浮點數(需要注意，只有當前多媒體格式或流媒體協議支持纔會生效)
    def set_position(self, float_val):
        return self.media.set_position(float_val)

    # 獲取當前文件播放速率
    def get_rate(self):
        return self.media.get_rate()

    # 設置播放速率（如：1.2，表示加速1.2倍播放）
    def set_rate(self, rate):
        return self.media.set_rate(rate)

    # 設置寬高比率（如"16:9","4:3"）
    def set_ratio(self, ratio):
        self.media.video_set_scale(0.6)  # 必須設置爲0，否則無法修改屏幕寬高
        self.media.video_set_aspect_ratio(ratio)

    # 設置窗口句柄
    def set_window(self, wm_id):
        if platform.system() == 'Windows':
            self.media.set_hwnd(wm_id)
        else:
            self.media.set_xwindow(wm_id)

    # 註冊監聽器
    def add_callback(self, event_type, callback):
        self.media.event_manager().event_attach(event_type, callback)

    # 移除監聽器
    def remove_callback(self, event_type, callback):
        self.media.event_manager().event_detach(event_type, callback)


class App(tk.Tk): 
    
    def __init__(self):
        super().__init__()
        self.player = Player()
        self.title("10366073-吳智偉-網際網路技術期末專案")
        self.iconphoto(False, tk.PhotoImage(file='./icon.png'))
        self.geometry("1440x768+0+0")
        self.Tree_view()
        self.search_view()
        self.create_video_view()
        self.timer()
        self.create_control_view()

    def create_video_view(self):  
        self._canvas = tk.Canvas(self, bg="black")
        self._canvas.pack(fill = "both", expand = 1)
        self.player.set_window(self._canvas.winfo_id())

    def search_view(self):
        global myentry
        
        search_frame = tk.Frame(self)
        
        myentry=tk.Entry(search_frame , width=80)
        myentry.pack(side=tk.LEFT, ipadx=20, padx=10, expand = 1)
        
        tk.Button(search_frame, text="搜尋" , command=self.get_search_word).pack(side=tk.LEFT, ipadx=20, padx=10, expand = 0)
        
        tk.Button(search_frame, text="影片上傳" , command=lambda: self.click(4)).pack(side=tk.LEFT, expand = 0)
        
        search_frame.pack(fill='both', expand = 0)
        
    def Tree_view(self):
        global tree
    
        area=('影片名稱','歌手')
        ac=('影片名稱','歌手')
        tree = ttk.Treeview(self,columns=ac,show='headings')
        for i in range(2):
            tree.column(ac[i],width=110,anchor='e')
            tree.heading(ac[i],text=area[i])

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT , fill = 'both', expand = 0)
        tree.pack(side=tk.RIGHT , fill = 'both', expand = 0)
        
        tree.bind('<<TreeviewSelect>>',self.select)
        
    def select(self , *args):
        global tree , mypath
        selected_iid = tree.selection()[0]
        current_idx = tree.index(selected_iid)
        mypath = web_name[current_idx]

    def timer(self):
        global timeSliderUpdate , timeVar , timeSliderLast , timeSlider , timers_frame
        timers_frame = tk.Frame(self)
        timeVar = tk.DoubleVar()
        timeSliderLast = 0
        timeSlider = tk.Scale(timers_frame, variable=timeVar,command=self.OnTime,
                                   from_=0, to=1000, orient=tk.HORIZONTAL, length=500,
                                   showvalue=0)  # label='Time',
        timeSlider.pack(fill=tk.X, expand=1)
        timeSliderUpdate = time.time()
        timers_frame.pack(fill='both', expand = 0)
        
        self.OnTick()  # set the timer up
    def create_control_view(self):
        global vol , text , play_pause_text , var_tk , vol_scale , total_time , now_time , Total_time , Show_Vol, loop_text , RE10_btn , Pre10_btn
        self.player.set_volume(vol)
        frame = tk.Frame(self)

        RE10_btn = tk.Button(frame, text="倒退10秒" , command=lambda: self.click(6))
        
        play_pause_text = tk.StringVar()
        play_pause_text.set("播放")
        
        play_pause_btn = tk.Button(frame, textvariable=play_pause_text , command=lambda: self.click(0)) 
        
        pause_btn = tk.Button(frame, text="暫停", command=lambda: self.click(1))

        Pre10_btn = tk.Button(frame, text="快轉10秒" , command=lambda: self.click(5))

        stop_btn = tk.Button(frame, text="停止", command=lambda: self.click(2))

        text = tk.StringVar()
        text.set("靜音")
        mute_btn = tk.Button(frame, textvariable=text, command=lambda: self.click(3))
   
        vol = tk.StringVar()
        vol.set(100)        
        Show_Vol = tk.Label(frame, textvariable=vol)  
        
        var_tk=tk.IntVar()
        var_tk.set(100)       
        vol_scale = tk.Scale(frame , variable=var_tk , orient=tk.HORIZONTAL, command = self.change_vol , showvalue=False)

        now_time = tk.StringVar()
        now_time.set("00:00:00") 
        Now_time = tk.Label(frame, textvariable=now_time)   
        
        s = tk.Label(frame, text="/")
        
        total_time = tk.StringVar()
        total_time.set("00:00:00") 
        Total_time = tk.Label(frame, textvariable=total_time)

    #---------------------------------create_control_view 按鍵位置配置----------------------------------------------#

        RE10_btn.pack(side=tk.LEFT, ipadx=10, padx=10,fill='x', expand = 0)   #倒退10秒     
        play_pause_btn.pack(side=tk.LEFT, ipadx=10, padx=10,fill='x', expand = 0)#播放
        pause_btn.pack(side=tk.LEFT, ipadx=10, padx=10,fill='x', expand = 0)#暫停
        Pre10_btn.pack(side=tk.LEFT, ipadx=10, padx=10,fill='x', expand = 0) #快轉10秒       
        stop_btn.pack(side=tk.LEFT, ipadx=10, padx=10,fill='x', expand = 0)#停止
        mute_btn.pack(side=tk.LEFT, ipadx=10, padx=10,fill='both', expand = 0)#靜音
        vol_scale.pack(side=tk.LEFT, ipadx=10, padx=10,fill='x', expand = 0)#音量控制
        Show_Vol.pack(side=tk.LEFT, fill='x', expand = 0)#顯示現在進度
        Now_time.pack(side=tk.RIGHT, fill='x', expand = 0)#顯示現在進度
        s.pack(side=tk.RIGHT, fill='x')#/圖示
        Total_time.pack(side=tk.RIGHT, fill='x', expand = 0) #顯示影片總長度   
        frame.pack(fill='both', expand = 0)

#-----------------------------------------------------影片上傳視窗----------------------------------------------------------------#

    def upload_video_information(self):
        self.top_level = tk.Toplevel()
        self.top_level.title("影片上傳")
        self.top_level.geometry("600x200+0+0")  
        self.top_level.resizable(0, 0)
        self.upload_video_input_view()
        return self.top_level
        
    def upload_video_input_view(self):
        global myentryname1 , myentryname2 , myentryname3
        
        upload_video_input_frame1 = tk.Frame(self.top_level)
        
        self.name1 = tk.Label(upload_video_input_frame1, text="影片名稱 ： ").pack(side=tk.LEFT, fill='x')
        
        myentryname1=tk.Entry(upload_video_input_frame1 , width=75)
        
        #-----------------------------------------------------------------------------------------------------#
        
        upload_video_input_frame2 = tk.Frame(self.top_level)
        self.name2 = tk.Label(upload_video_input_frame2, text="影片路徑 ： ").pack(side=tk.LEFT, fill='x')
        
        myentryname2=tk.Entry(upload_video_input_frame2 , width=75)
        
        #-----------------------------------------------------------------------------------------------------#
        
        upload_video_input_frame3 = tk.Frame(self.top_level)
        self.name2 = tk.Label(upload_video_input_frame3, text="歌手資訊 ： ").pack(side=tk.LEFT, fill='x')
        
        myentryname3=tk.Entry(upload_video_input_frame3 , width=75)
        
        #-----------------------------------------------------------------------------------------------------#

        upload_video_input_frame4 = tk.Frame(self.top_level)
        
        check_btn=tk.Button(upload_video_input_frame4, text="確認輸入" , command=self.upload_video_process)
        
        #login=tk.Button(upload_video_input_frame4, text="註冊IP" )
        
        
        #---------------------------------upload_video_input_view 按鍵位置配置----------------------------------------------#
        myentryname1.pack(side=tk.LEFT, ipadx=20, padx=10, pady=10)
        myentryname2.pack(side=tk.LEFT, ipadx=20, padx=10, pady=10)
        myentryname3.pack(side=tk.LEFT, ipadx=20, padx=10, pady=10)
        check_btn.pack(side=tk.LEFT, ipadx=30, padx=20, pady=20)
        #login.pack(side=tk.RIGHT, ipadx=30, padx=20, pady=20)
        
        upload_video_input_frame1.pack(fill='x')
        upload_video_input_frame2.pack(fill='x')
        upload_video_input_frame3.pack(fill='x')
        upload_video_input_frame4.pack(fill='x')
        
    def upload_video_process(self):
        title = myentryname1.get()
        data_path = myentryname2.get()
        Author = myentryname3.get()
        if data_path != "" and Author !="" and title !="":
            cmd_process.upload(data_path , Author , title)
            messagebox.showinfo('上傳完成', "影片名稱:{0}\n歌手:{1}".format(title , Author))
        else:
            messagebox.showerror('上傳錯誤', '欄位有空白，請檢查後再送一次!')
        
        
#-----------------------------------------------------處理程序----------------------------------------------------------------#
    def OnTick(self):
        """Timer tick, update the time slider to the video time.
        """
        global timeSliderLast , timeSliderUpdate , timeVar
        if self.player:
            # 由於 self.player.get_length 可能會在播放時發生變化，請將 timeSlider 重新設置為正確的範圍
            t = self.player.get_length() * 1e-3  # to seconds
            if t > 0:
                timeSlider.config(to=t)
                t = self.player.get_time() * 1e-3  # to seconds
                # don't change slider while user is messing with it
                if t > 0 and time.time() > (timeSliderUpdate + 2):
                    timeSlider.set(t)
                    timeSliderLast = int(timeVar.get())
        # start the 1 second timer again
        timers_frame.after(1000, self.OnTick)
    
    def OnTime(self, *unused):
        global timeSliderLast , timeSliderUpdate , timeVar
        if self.player:
            t = int(timeVar.get())
            if timeSliderLast != int(t):
                self.player.set_time(int(t * 1e3))  # milliseconds
                timeSliderUpdate = time.time()
                time.sleep(0.1)
                
    def Video_End_process(self,event):#處理影片播到結尾
        global  play_pause_text
        play_pause_text.set("播放")   

    def get_search_word(self):#取得搜尋文字
        global myentry , mypath , tree , video_name , web_name , Author_name
        tree.delete(*tree.get_children())
        if myentry.get() != '':
            search_word = myentry.get()
            x = add_information.search_video(search_word)
            if x == "NULL":
                messagebox.showwarning('搜尋錯誤', '找不到')
            else:
                #print(x)
                video_name = x[0] 
                web_name = x[1]
                Author_name = x[2]  
                for i in range(len(video_name)):
                    contacts = ( video_name[i] , Author_name[i])
                    tree.insert('', tk.END,  values=contacts)

    def t2s(self,sec):#將毫秒轉乘hh:mm:ss
        m, s = divmod(sec, 60)
        h, m = divmod(m, 60)
        return ("%02d:%02d:%02d" % (h, m, s))

    def get_now_time_call_back(self,event):#處理取得影片現在播放秒數
        global now_time
        N = int(self.player.get_time()) 
        N=self.t2s(N/1000) 
        now_time.set(N)    

    def get_now_time(self,):#取得影片現在播放秒數
        self.player.add_callback(vlc.EventType.MediaPlayerTimeChanged, self.get_now_time_call_back)

    def get_total_time(self):#取得影片總長度
        global total_time , T , Total
        T = self.player.get_length()
        Total=self.t2s(T/1000)
        total_time.set(Total) 

    def change_vol(self,volume):#改變滑竿音量
        global vol , var_tk , mode , text
        volume = var_tk.get()
        self.player.set_volume(volume) 
        vol_text = volume
        if volume == 0 and mode == 0:#音量0但滑竿狀態仍在非0狀態(音量>0)
            mode = 1#表示滑竿設為0
            text.set("解除靜音") #按鈕從靜音，變成解除靜音
            
        elif volume != 0 and mode == 1:#音量非0但滑竿狀態仍在0狀態(音量=0)
            mode = 0#表示滑竿沒有設為0
            text.set("靜音") #按鈕從解除靜音，變成靜音
            
        vol_text = str(volume)
        vol.set(vol_text)#改變音量文字顯示的值為vol_text
             
    def on_closing(self):#關閉
        self.click(2)#處理點擊停止鍵事件
        self.destroy()#釋放資源
        
    def play_new(self):      
        global var_tk , volume
        self.player.play(mypath)#讀取網址
        v = self.player.get_volume()
        self.change_vol(v)
        #self.player.set_volume(v)
        #var_tk.set(v)
        
        time.sleep(0.5)#暫停0.5sec讀取
        self.get_total_time()#得到影片總長度
        self.get_now_time()#得到現在影片播放時間
        self.player.add_callback(vlc.EventType.MediaPlayerEndReached, self.Video_End_process)
        
 
    def click(self, action):#x處理點擊事件
        global vol , text , var_tk , play_pause_text , volume , old_mypath , mypath , timeSlider

        if action == 0:#播放
                if self.player.get_state() == 0:#如果影片狀態為暫停
                    self.player.resume()#繼續播放         
                elif self.player.get_state() == 1:# 播放新資源
                    if mypath != old_mypath:
                        self.player.stop()
                        self.play_new()
                        old_mypath = mypath
                        
                    else : pass
                else : self.play_new()
                

        elif action == 1:#暫停
            self.player.pause()
                
        elif action == 2:#停止
            self.player.stop()
            
            
        elif action == 3:#靜音
            global Show_Vol
            volume = self.player.get_volume()
            if(volume!=0): #如果音量不為0
                self.player.set_volume(0)
                text.set("解除靜音") 
                vol_text = '0'
                vol.set(vol_text)
                
            else:#如果音量為0
                volume = var_tk.get()#從滑竿得到音量值
                self.player.set_volume(volume) 
                vol_text = volume
                vol_scale.set(vol_text)
                text.set("靜音")  
                vol_text = str(volume)
                vol.set(vol_text)     
                
        elif action == 4:#影片上傳
            self.upload_video_information()
            
        elif action == 5:#快轉10秒
            global Pre10_btn , now_time
            self.player.pause()
            Pre10_btn['state'] = tk.DISABLED
            nt = self.player.get_time() + 10000#取得當前影片播放位置，並加上10秒(10000ms)，VLC給的函數有時會偷走2s
            tt = self.player.get_length() #取得影片總長度
            if nt >= tt : 
                pass
            else : 
                self.player.set_time(nt) 
                now_time.set(self.t2s(nt/1000))
            self.player.resume()#繼續播放 
            Pre10_btn['state'] = tk.NORMAL
        
        elif action == 6:#倒轉10秒
            self.player.pause()
            nt = self.player.get_time() - 10000#取得當前影片播放位置，並減去10秒(10000ms)
            tt = 0#歸零
            if nt >= 0 : self.player.set_time(nt)
            else : self.player.set_time(0) 
            self.player.resume()#繼續播放 
                
app = App()
app.protocol("WM_DELETE_WINDOW", app.on_closing)

app.mainloop()