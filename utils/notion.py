from notion_client import Client
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Notion client
notion = Client(auth="secret_99DQNMJstSnTQUWdIjUrOpAAQ25WUlXJRxX8zNIRko3")

def create_database(parent_id, name, properties):
    try:
        logger.info(f"Creating database: {name}")
        return notion.databases.create(
            parent={"page_id": parent_id},
            title=[{"type": "text", "text": {"content": name}}],
            properties=properties
        )
    except Exception as e:
        logger.error(f"Error creating database {name}: {str(e)}")
        raise

def create_page(parent_id, properties):
    try:
        logger.info(f"Creating page in database: {parent_id}")
        return notion.pages.create(
            parent={"database_id": parent_id},
            properties=properties
        )
    except Exception as e:
        logger.error(f"Error creating page: {str(e)}")
        raise

# Create main Vedam database
try:
    vedam_db = create_database(
        "109170fddeed80b98d8dfce6167357e7",  # This is your parent page ID
        "Vedam",
        {
            "Name": {"title": {}},
            "Status": {
                "select": {
                    "options": [
                        {"name": "Not Started", "color": "red"},
                        {"name": "In Progress", "color": "yellow"},
                        {"name": "Completed", "color": "green"}
                    ]
                }
            },
            "Type": {
                "select": {
                    "options": [
                        {"name": "Project", "color": "blue"},
                        {"name": "Component", "color": "purple"}
                    ]
                }
            }
        }
    )
    logger.info(f"Vedam database created successfully. ID: {vedam_db['id']}")

    # Create Rig Veda project
    rig_veda = create_page(
        vedam_db["id"],
        {
            "Name": {"title": [{"text": {"content": "Rig Veda"}}]},
            "Status": {"select": {"name": "In Progress"}},
            "Type": {"select": {"name": "Project"}}
        }
    )
    logger.info(f"Rig Veda project created successfully. ID: {rig_veda['id']}")

    # Create Frontend component
    frontend_db = create_database(
        rig_veda["id"],
        "Rig Veda - Frontend",
        {
            "Name": {"title": {}},
            "Status": {
                "select": {
                    "options": [
                        {"name": "Not Started", "color": "red"},
                        {"name": "In Progress", "color": "yellow"},
                        {"name": "Review", "color": "blue"},
                        {"name": "Completed", "color": "green"}
                    ]
                }
            },
            "Priority": {
                "select": {
                    "options": [
                        {"name": "Low", "color": "blue"},
                        {"name": "Medium", "color": "yellow"},
                        {"name": "High", "color": "red"}
                    ]
                }
            },
            "Estimated Hours": {"number": {}}
        }
    )
    logger.info(f"Frontend database created successfully. ID: {frontend_db['id']}")

    print("Vedam project structure created successfully!")
except Exception as e:
    logger.error(f"An error occurred: {str(e)}")