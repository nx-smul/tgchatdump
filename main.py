import csv
from datetime import datetime
from telethon.sync import TelegramClient
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox

api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
phone_number = 'YOUR_PHONE_NUMBER'
chat_name = 'YOUR_CHAT_NAME'

client = TelegramClient('session_name', api_id, api_hash)

def export_chat_history(start_date, end_date, export_path, include_usernames=True):
    client.start(phone=phone_number)
    with client:
        messages = client.get_messages(chat_name, limit=None)

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

    messagebox.showinfo("Export Complete", f'Chat history exported to {export_path} from {start_date} to {end_date}.')

def on_export_click():
    start_date = datetime.strptime(start_date_var.get(), "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_var.get(), "%Y-%m-%d").date()
    export_path = export_path_var.get()
    include_usernames = include_usernames_var.get().lower() == 'yes'

    export_chat_history(start_date, end_date, export_path, include_usernames)

# Tkinter UI Setup
root = Tk()
root.title("Telegram Chat Exporter")

Label(root, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0)
Label(root, text="End Date (YYYY-MM-DD):").grid(row=1, column=0)
Label(root, text="Export File Path:").grid(row=2, column=0)
Label(root, text="Include Usernames? (yes/no):").grid(row=3, column=0)

start_date_var = StringVar()
end_date_var = StringVar()
export_path_var = StringVar()
include_usernames_var = StringVar()

Entry(root, textvariable=start_date_var).grid(row=0, column=1)
Entry(root, textvariable=end_date_var).grid(row=1, column=1)
Entry(root, textvariable=export_path_var).grid(row=2, column=1)
Entry(root, textvariable=include_usernames_var).grid(row=3, column=1)

Button(root, text="Export", command=on_export_click).grid(row=4, column=0, columnspan=2)

root.mainloop()
