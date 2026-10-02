from tkinter import *
import datetime
import subprocess

root = Tk()
root.geometry("400x380")
root.title("Alarm Clock")

alarm_target = None   # the exact datetime the alarm will ring
ringing = False       # True while the chime is repeating

SOUNDS = ["Glass", "Ping", "Hero", "Funk", "Submarine", "Tink"]

def play_sound():
    subprocess.Popen(["afplay", f"/System/Library/Sounds/{sound.get()}.aiff"])

def ring():
    # Play the chime, then repeat every 2 seconds until stopped
    if ringing:
        play_sound()
        root.after(2000, ring)

def set_alarm():
    global alarm_target, ringing
    ringing = False
    now = datetime.datetime.now()
    target = now.replace(hour=int(hour.get()), minute=int(minute.get()),
                         second=int(second.get()), microsecond=0)
    if target <= now:                     # time already passed today -> tomorrow
        target += datetime.timedelta(days=1)
    alarm_target = target

def stop_alarm():
    global alarm_target, ringing
    ringing = False
    alarm_target = None
    status.config(text="Alarm stopped", fg="gray")

def update_clock():
    global alarm_target, ringing
    now = datetime.datetime.now()

    clock.config(text=now.strftime("%H:%M:%S"))
    date_label.config(text=now.strftime("%A, %d %B %Y"))

    if alarm_target:
        if now >= alarm_target:           # reached or passed -> ring
            alarm_target = None
            ringing = True
            status.config(text="Time to wake up!", fg="red")
            ring()
        else:
            left = str(alarm_target - now).split(".")[0]
            status.config(text=f"Alarm at {alarm_target.strftime('%H:%M:%S')}  (rings in {left})", fg="green")

    root.after(200, update_clock)

Label(root, text="Alarm Clock", font=("Helvetica 20 bold"), fg="red").pack(pady=(10, 0))

clock = Label(root, text="", font=("Helvetica 32 bold"))
clock.pack()
date_label = Label(root, text="", font=("Helvetica 12"))
date_label.pack()

Label(root, text="Set Time", font=("Helvetica 15 bold")).pack(pady=(10, 0))

frame = Frame(root)
frame.pack()

hours = [f"{i:02d}" for i in range(24)]
minutes = [f"{i:02d}" for i in range(60)]
seconds = [f"{i:02d}" for i in range(60)]

now = datetime.datetime.now()
hour = StringVar(root, now.strftime("%H"))
minute = StringVar(root, now.strftime("%M"))
second = StringVar(root, "00")

OptionMenu(frame, hour, *hours).pack(side=LEFT)
OptionMenu(frame, minute, *minutes).pack(side=LEFT)
OptionMenu(frame, second, *seconds).pack(side=LEFT)

Label(root, text="Chime sound", font=("Helvetica 12 bold")).pack(pady=(10, 0))
sound_frame = Frame(root)
sound_frame.pack()
sound = StringVar(root, "Glass")
OptionMenu(sound_frame, sound, *SOUNDS).pack(side=LEFT)
Button(sound_frame, text="Test", command=play_sound).pack(side=LEFT, padx=5)

buttons = Frame(root)
buttons.pack(pady=10)
Button(buttons, text="Set Alarm", command=set_alarm).pack(side=LEFT, padx=5)
Button(buttons, text="Stop", command=stop_alarm).pack(side=LEFT, padx=5)

status = Label(root, text="No alarm set", font=("Helvetica 12"))
status.pack()

update_clock()
root.mainloop()