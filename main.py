import csv
from datetime import datetime, timedelta
from telethon.sync import TelegramClient
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Static, Input, RadioSet, RadioButton, Button, Label

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

def calculate_date_range(option, start_date_str=None, end_date_str=None):
    end_date = datetime.today().date()
    if option == "1":
        start_date = end_date - timedelta(days=7)
    elif option == "2":
        start_date = end_date - timedelta(days=30)
    elif option == "3":
        start_date = end_date - timedelta(days=365)
    elif option == "4":
        start_date = datetime.min.date()
    elif option == "5":
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    else:
        start_date = end_date
    return start_date, end_date

class ExportApp(App):

    def compose(self) -> ComposeResult:
        yield Container(
            Static("Telegram Chat Exporter", classes="title"),
            Label("Export File Path:"),
            Input(placeholder="Enter export file path", id="export_path"),
            Label("Include Usernames? (yes/no):"),
            Input(placeholder="yes or no", id="include_usernames"),
            Label("Select Date Range:"),
            RadioSet(
                RadioButton("Last 7 Days", id="1"),
                RadioButton("Last 1 Month", id="2"),
                RadioButton("Last 1 Year", id="3"),
                RadioButton("All Time", id="4"),
                RadioButton("Custom", id="5")
            ),
            Container(
                Label("Custom Start Date (YYYY-MM-DD):"),
                Input(placeholder="YYYY-MM-DD", id="start_date"),
                Label("Custom End Date (YYYY-MM-DD):"),
                Input(placeholder="YYYY-MM-DD", id="end_date"),
            ),
            Button(label="Export", id="export_button"),
            classes="content"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        export_path = self.query_one("#export_path").value
        include_usernames = self.query_one("#include_usernames").value.lower() == 'yes'
        date_option = self.query_one(RadioSet).value

        if date_option == "5":
            start_date_str = self.query_one("#start_date").value
            end_date_str = self.query_one("#end_date").value
            start_date, end_date = calculate_date_range(date_option, start_date_str, end_date_str)
        else:
            start_date, end_date = calculate_date_range(date_option)

        export_chat_history(start_date, end_date, export_path, include_usernames)
        self.query_one("#export_button").label = "Export Complete!"

if __name__ == "__main__":
    ExportApp().run()
