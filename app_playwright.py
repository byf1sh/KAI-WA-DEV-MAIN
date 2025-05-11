from playwright.sync_api import sync_playwright
import datetime
import time
import json
from dotenv import load_dotenv
from models.table_model import WaData
from services.data_utils import extract_field
import requests
from services.bot import send
from database.database import initialize_db, create_session
from services.db_services import insert_data
import os
import logging
from utils.logger_config import init_logging

init_logging('playwright.log')

log = logging.getLogger(__name__)

load_dotenv()

class WhatsAppReader:
    def __init__(self, profile_path, target_group,headless):
        self.profile_path = profile_path
        self.target_group = target_group
        self.engine = initialize_db()
        self.browser = None
        self.page = None
        self.headless = headless

    def start_browser(self):
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch_persistent_context(
            user_data_dir=self.profile_path,
            headless=self.headless,
            args=["--start-maximized", "--window-size=1280,1024"],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.94 Safari/537.36"

        )
        self.page = self.browser.pages[0]
        self.page.goto("https://web.whatsapp.com")

    def button_presser(self, count):
        rows = self.page.query_selector_all(f'(//div[@role="row"])[position() > last()-{count}]')
        for row in rows:
            button = row.query_selector('div[role="button"]')
            if button:
                button.click()
                break
    
    def get_unread_messages(self, count):
        bubbles = self.page.query_selector_all(f'(//div[@role="row"])[position() > last()-{count}]')
        messages = []

        for i, bubble in enumerate(bubbles, 1):
            text = bubble.inner_text()
            timestamp = datetime.datetime.now().isoformat()
            messages.append({
                "timestamp": timestamp,
                "message": text
            })

        json_output = json.dumps(messages, indent=4, ensure_ascii=False)
        log.info(json_output)
        return messages
    
    def make_data(self,data):
        session = create_session(self.engine)
        for row in data:
            if "[Automation]" in row["message"]:
                log.info("Automation Detected not sending to xlsx")
            elif "NOC KAI" in row["message"]:
                log.info("Message from noc not sending to xlsx")
            else:
                case_id = extract_field("Case ID", row["message"])
                insert_data(session, WaData, case_id, row["message"])
                log.info(f"{case_id} ..inserting to DB")
                # form_service(row["timestamp"], case_id ,row["message"])
            time.sleep(1)
        session.commit()
        session.close()

    def run(self):
        message_trigger = 0
        try:
            while True:
                try:
                    log.info(f"waiting new message from grup {self.target_group}....")
                    selector = f'//div[@class="x1n2onr6"][.//span[@title="{self.target_group}"]]//div[@class="_ahlk"]'
                    self.page.wait_for_selector(selector, timeout=60000)
                    unread_div = self.page.query_selector(selector)
                    time.sleep(0.5)

                    if unread_div:
                        message_trigger = 0
                        group_selector = f'//div[@class="x1n2onr6"]//span[@title="{self.target_group}"]'
                        self.page.click(group_selector)
                        time.sleep(3)
                        count = int(unread_div.inner_text())
                        self.button_presser(count)
                        message_data = self.get_unread_messages(count)
                        self.page.keyboard.press("Escape")
                        time.sleep(1)
                        self.page.keyboard.press("Escape")
                        self.make_data(message_data)
                        self.page.keyboard.press("Escape")
                        time.sleep(1)
                        self.page.keyboard.press("Escape")
                    else:
                        log.info("Tidak ditemukan unread message")

                except Exception as e:
                    message_trigger += 1
                    log.info(f"masuk ke except : {message_trigger}")
                    if message_trigger >= 140:
                        send(f"Playwright Erorr, cannot click target group / There's no message in last 30 minutes {e}")
                        time.sleep(5)
                    else:
                        log.warning(f"Tidak ditemukan adanya unread message pada {self.target_group} mencoba lagi dalam 10 detik")
                        time.sleep(5)

                time.sleep(5)
        except KeyboardInterrupt:
            log.warning("\n⛔ Dihentikan oleh pengguna. Menutup browser...")
            self.browser.close()

# --- MAIN ---
if __name__ == "__main__":
    reader = WhatsAppReader(
        profile_path=os.getenv('PROFILE_PATH'),
        target_group=os.getenv('TARGET_GROUP'),
        headless=True
    )
    reader.start_browser()
    reader.run()