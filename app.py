from database.database import initialize_db, create_session
from models.table_model import EmailData, JiraData
from services.db_services import insert_data, prevent_duplicate_data
from services.email_service import get_email
from services.graph import start_graph
from services.jiara_helper import get_case_id
from datetime import datetime
from utils.logger_config import init_logging
import logging
from services.bot import send

init_logging('app.log')
log = logging.getLogger(__name__)
engine = initialize_db()
session = create_session(engine)
token = start_graph()
email_data = get_email(token)
jira_case_id_data = get_case_id()
loop_count = 0
for email_item, jira_case_id_item in zip(email_data, jira_case_id_data):
    loop_count += 1
    timestamp = datetime.strptime(email_item["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
    email_duplicate = prevent_duplicate_data(session, EmailData, email_item["case_id"])
    jira_case_id_duplicate = prevent_duplicate_data(session, JiraData, jira_case_id_item["case_id"])
    if not email_duplicate:
        try:
            log.info(f"Inserting [EMAIL] {email_item['case_id']} — new email found")
            insert_data(session, EmailData, timestamp=timestamp, case_id=email_item["case_id"], content=email_item["content"])
        except Exception as e:
            send(f"Error inputing email to db {e}")
            log.error(f"❌ Failed to insert email {email_item['case_id']}: {e}")

    if not jira_case_id_duplicate:
        try:
            log.info(f"Inserting [JIRA] {jira_case_id_item['case_id']} — recommendation provided")
            insert_data(session, JiraData, case_id=jira_case_id_item["case_id"])
        except Exception as e:
            log.error(f"❌ Failed to insert JIRA case {jira_case_id_item['case_id']}: {e}")
            send(f"Error inputing jira case id to db {e}")
    if loop_count % 10 == 0:
        try:
            session.commit()
        except Exception as e:
            log.error(f"❌ Failed to commit at loop {loop_count}: {e}")
            send(f"Error commiting to db {e}")

session.commit()
session.close()
