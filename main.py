from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 1
SHORT_BREAK_MIN = 2
LONG_BREAK_MIN = 3
reps = 0
checkmark_count = 0
timer = None
pause = False
resume = False
time_left = 0


# Function to reset timer
def reset_timer():
    global reps, pause
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text=f"00:00")
    timer_label.config(text="Timer", fg=GREEN)
    checkmark.config(text="")
    reps = 0
    pause_btn.config(text="Pause", command=pause_timer)
    pause = False
    start_btn["state"] = NORMAL


# Function to pause timer
def pause_timer():
    print("pause")
    global pause
    pause = not pause
    pause_btn.config(text="Resume", command=resume)
    print(pause)


# Function to resume
def resume():
    print("resume")
    global pause, time_left
    pause = not pause
    pause_btn.config(text="Pause", command=pause_timer)
    count_down(time_left-1)


# Function to start timer
def start_timer():
    global reps, time_left
    global checkmark_count
    time_left = 0
    reps += 1
    work_sec = WORK_MIN*60
    short_break_sec = SHORT_BREAK_MIN*60
    long_break_sec = LONG_BREAK_MIN*60

    if reps % 8 == 0:
        timer_label.config(text="Break", fg=RED)
        count_down(long_break_sec)

    elif reps % 2 == 0:
        timer_label.config(text="Break", fg=PINK)
        count_down(short_break_sec)

    else:
        timer_label.config(text="Work", fg=GREEN)
        count_down(work_sec)

    start_btn["state"] = DISABLED

# Countdown mechanism
def count_down(count):
    global reps, timer, time_left
    global checkmark_count
    count_min = math.floor(count/60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    if count_min < 10:
        count_min = f"0{count_min}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    if count > 0:
        if not pause:
            timer = window.after(1000, count_down, count-1)
            time_left = count
    else:
        start_timer()
        mark = ""
        work_sessions = math.floor(reps/2)
        for n in range(work_sessions):
            mark += "✔"
        checkmark.config(text=mark)


# User Interface
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

# Canvas
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")

canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text=f"{WORK_MIN}:00", font=(FONT_NAME, 35, "bold"), fill="white")
canvas.grid(column=1, row=1)

# Label
timer_label = Label(text="Timer", font=(FONT_NAME, 45, "bold"), bg=YELLOW, fg=GREEN)
timer_label.grid(column=1, row=0)

checkmark = Label(text="", bg=YELLOW, fg=GREEN, font=("Courier", 15, "bold"))
checkmark.grid(column=1, row=4)
checkmark.config(pady=10)

# Button
start_btn = Button(text="Start", command=start_timer)
start_btn.grid(column=0, row=3)

pause_btn = Button(text="Pause", command=pause_timer)
pause_btn.grid(column=1, row=3)


resume_btn = Button(text="")
reset_btn = Button(text="Reset", command=reset_timer)
reset_btn.grid(column=2, row=3)

window.mainloop()