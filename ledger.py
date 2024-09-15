import pandas as pd
import tkinter as tk
import customtkinter as ctk


def process_string(data_str):
  losers = {"person": [], "balance": []}
  winners = {"person": [], "balance": []}
  lines = data_str.split('\n')
  for line in lines:
    if len(line[-11:].split('+'))>1:
      player = line.split('@')[0].strip()
      balance = line[-11:].split('+')[1]
      winners["person"].append(player)
      winners["balance"].append(int(balance))
    elif len(line[-11:].split('-'))>1:
      player = line.split()[0]
      balance = line[-11:].split('-')[1]
      losers["person"].append(player)
      losers["balance"].append(int(balance))
  losers = pd.DataFrame(losers)
  winners = pd.DataFrame(winners)
  losers = losers.sort_values(by="balance", ascending=False).reset_index(drop=True)
  winners = winners.sort_values(by="balance", ascending=False).reset_index(drop=True)
  return losers, winners


def calculate_ledger(losers, winners):
  count_los = 0
  count_win = 0
  los_balance = losers["balance"][count_los]
  win_balance = winners["balance"][count_win]
  end_ledger = []
  while count_los<len(losers) and count_win<len(winners):
    result = los_balance - win_balance
    if result < 0:
      end_ledger.append(losers["person"][count_los] + ", " + str(los_balance/100) + " -> " + winners["person"][count_win])
      win_balance = win_balance - los_balance
      count_los += 1
      if(count_los<len(losers)):
        los_balance = losers["balance"][count_los]
    elif result > 0:
      end_ledger.append(losers["person"][count_los] + ", " + str(win_balance/100) + " -> " + winners["person"][count_win])
      los_balance = los_balance - win_balance
      count_win += 1
      if(count_win<len(winners)):
        win_balance = winners["balance"][count_win]
    else:
      end_ledger.append(losers["person"][count_los] + ", " + str(win_balance/100) + " -> " + winners["person"][count_win])
      count_los += 1
      count_win += 1
      if(count_los<len(losers) and count_win<len(winners)):
        los_balance = losers["balance"][count_los]
        win_balance = winners["balance"][count_win]
  if count_los != len(losers) or count_win != len(winners):
    end_ledger.append("ledger doesn't check out")

  return end_ledger

def submit_text():
  input_text = txt_input.get('1.0', tk.END).strip()
  losers, winners = process_string(input_text)
  ledger = calculate_ledger(losers, winners)
  result_label.configure(text="\n".join(ledger))
  
def clear():
  result_label.configure(text="")
  txt_input.delete("1.0", tk.END)

def copy_text():
  text = result_label.cget("text")
  window.clipboard_clear()
  window.clipboard_append(text)

window = ctk.CTk()
window.title("PokerNow Ledger Calculator")
window.geometry('400x500')
window.minsize(400,500)

txt_input = ctk.CTkTextbox(window, width=370)
txt_input.pack(pady=20)

frame = ctk.CTkFrame(window, bg_color='transparent')
frame.pack()

submit_btn = ctk.CTkButton(frame, text="Submit", command=submit_text, fg_color="gray", hover_color="gray30")
clear_btn = ctk.CTkButton(frame, text="Clear", command=clear, fg_color="gray", hover_color="gray30")
submit_btn.grid(row=0, column=1, padx=10)
clear_btn.grid(row=0, column=2, padx=10)

result_label = ctk.CTkLabel(window, text="")
result_label.pack(pady=10)

copy_btn = ctk.CTkButton(window, text="Copy to clipboard", command=copy_text, fg_color="gray", hover_color="gray30")
copy_btn.pack(pady=10)

window.mainloop()


