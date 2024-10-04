import csv
from datetime import datetime, timedelta
from telethon.sync import TelegramClient
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, Radiobutton

api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
phone_number = 'YOUR_PHONE_NUMBER'
chat_username = 'YOUR_CHAT_USERNAME'

client = TelegramClient('session_name', api_id, api_hash)

def export_chat_history(start_date, end_date, export_path, include_usernames=True):
    client.start(phone=phone_number)
    with client:
        messages = client.get_messages(chat_username, limit=None)

        with open(export_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if include_usernames:
                writer.writerow(['Date', 'Sender', 'Message'])
            else:
                writer.writerow(['Date', 'Message'])

            for message in messages:
                if start_date <= message.date.date() <= end_date:
                    if include_usernames:
                        writer.writerow([message.date, message.sender_id, message.message])
                    else:
                        writer.writerow([message.date, message.message])

    print(f'Chat history exported to {export_path} from {start_date} to {end_date}.')

def calculate_date_range(option, start_date_str=None, end_date_str=None):
    end_date = datetime.today().date()
    if option == 1:
        start_date = end_date - timedelta(days=7)
    elif option == 2:
        start_date = end_date - timedelta(days=30)
    elif option == 3:
        start_date = end_date - timedelta(days=365)
    elif option == 4:
        start_date = datetime.min.date()
    elif option == 5:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    else:
        start_date = end_date
    return start_date, end_date

def on_export_click():
    export_path = export_path_var.get()
    include_usernames = include_usernames_var.get().lower() == 'yes'
    date_option = int(date_option_var.get())

    if date_option == 5:
        start_date_str = start_date_var.get()
        end_date_str = end_date_var.get()
        start_date, end_date = calculate_date_range(date_option, start_date_str, end_date_str)
    else:
        start_date, end_date = calculate_date_range(date_option)
    
    export_chat_history(start_date, end_date, export_path, include_usernames)

# Tkinter UI Setup
root = Tk()
root.title("Telegram Chat Exporter")

Label(root, text="Export File Path:").grid(row=0, column=0)
Label(root, text="Include Usernames? (yes/no):").grid(row=1, column=0)
Label(root, text="Date Range:").grid(row=2, column=0)

export_path_var = StringVar()
include_usernames_var = StringVar()
date_option_var = StringVar(value="1")
start_date_var = StringVar()
end_date_var = StringVar()

Entry(root, textvariable=export_path_var).grid(row=0, column=1)
Entry(root, textvariable=include_usernames_var).grid(row=1, column=1)

date_options = [
    ("1. Last 7 Days", "1"),
    ("2. Last 1 Month", "2"),
    ("3. Last 1 Year", "3"),
    ("4. All Time", "4"),
    ("5. Custom", "5")
]

for text, value in date_options:
    Radiobutton(root, text=text, variable=date_option_var, value=value).grid(sticky="w")

Label(root, text="Custom Start Date (YYYY-MM-DD):").grid(row=6, column=0)
Entry(root, textvariable=start_date_var).grid(row=6, column=1)
Label(root, text="Custom End Date (YYYY-MM-DD):").grid(row=7, column=0)
Entry(root, textvariable=end_date_var).grid(row=7, column=1)

Button(root, text="Export", command=on_export_click).grid(row=8, column=0, columnspan=2)

root.mainloop()
