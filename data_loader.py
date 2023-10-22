import json
import time
from concurrent.futures import as_completed

from prefect import task, flow, get_run_logger
from requests_futures.sessions import FuturesSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from schema import TableName

with open("conf.json", "r") as config_file:
    config = json.load(config_file)
    db_config = config["database_access"]
    api_config = config["api_access"]

engine = create_engine(
    f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/"
    f"{db_config['database_name']}")

SessionFactory = sessionmaker(bind=engine)


@task
def fetch_all_data():
    logger = get_run_logger()
    base_url = api_config["base_url"]
    headers = {
        'accept': '*/*',
        'Authorization': api_config["Authorization"]
    }

    session = FuturesSession(max_workers=10)  # you can change max_workers
    all_data = []
    start_time = time.time()  # Record the start time
    response = session.get(base_url, headers=headers)
    response = response.result()
    primary_data = response.json()
    total_records = primary_data['total'] if type(primary_data) == dict and primary_data['total'] else 1  # ** if in API returns the total number of records, you can get in this line

    records_per_page = api_config[
        "records_per_page"]  # Adjust this to match the actual records per page in the API response
    total_pages = (total_records + records_per_page - 1) // records_per_page

    futures = [session.get(f'{base_url}?page={i}&size={records_per_page}', headers=headers) for i in
               range(1, total_pages + 1)]
    for future in as_completed(futures):
        resp = future.result()
        data = resp.json()
        if type(data) == dict:
            logger.info(f"Fetched data from page {data['pageNumber']}")
            if len(data['result']) >= 1:
                all_data.extend(data['result'])
        else:
            all_data.extend(data)
    end_time = time.time()

    elapsed_time = end_time - start_time
    logger.info(f"Total execution time: {elapsed_time} seconds")

    return all_data


@task
def insert_data_into_db(data):
    logger = get_run_logger()
    start_time = time.time()
    users = data
    if users:
        # Create a new session
        session = SessionFactory()

        try:
            # Prepare and insert users into the database
            user_objects = [TableName(firstName=user['firstName'], lastName=user['lastName']) for user in
                            users]
            session.add_all(user_objects)
            session.commit()
            logger.info(f"Inserted {len(users)} users into the database")
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

        end_time = time.time()  # Record the end time

        execution_time = end_time - start_time
        return f"Inserted {len(users)} users into the database in {execution_time} seconds."
    else:
        return "No users to insert."


@flow(name="Fetch Customers ver2", log_prints=True)
def fetch_customers():
    data = fetch_all_data()
    insert_data_into_db(data)


if __name__ == "__main__":
    fetch_customers.serve(name="get_users_data")
