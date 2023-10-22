# Data Retrieval from API with Pagination

## Overview

This Python script is designed to handle the retrieval of data from a remote API that contains a large number of records and stores it in DB. Consider that We have an API which uses pagination to split the data into manageable chunks, and it requires authorization for access. This code ensures that you can retrieve data efficiently, even when dealing with over 100,000 records.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Considerations](#considerations)
- [Limitations](#limitations)
- [Contributions](#contributions)

## Features

- Efficiently retrieves data from a remote API with pagination.
- Configurable for different APIs by adjusting the base URL and authorization token.
- Handles large datasets by intelligently splitting the retrieval process into manageable chunks.

## Requirements

- Python 3.x
- - The required Python libraries (install them using `pipenv`):
- The `requests_futures` library for asynchronous requests.
- The `prefect` library for task management.
- The `sqlalchemy` for storing the retrieved data.


## Usage

1. **Configure Database and API**:
   - Update the `conf.json` file with your database and API configuration.

2. **Run the Script**:
   - Execute the script by running it in the terminal using Python.

   ```bash
   python your_script.py
   ```
3. **Deploy Your flow on prefect**:
   ```bash
   prefect deployment run 'Fetch And Insert/fetch_and_insert'
   ```
4. **Run prefect server and monitor your flow on prefect UI**:
   ```bash
   prefect server start
   ```
   and you can Check out the dashboard at http://127.0.0.1:4200

5. **View Logs**:
   - The script will log information to the console. You can configure the log output as needed.

6. **Review Data**:
   - After running the script, the data will be fetched and inserted into the database.

## How It Works

This Python script is designed to efficiently retrieve data from web services and APIs that provide data in multiple pages, often referred to as pagination. It handles authorization for secure access and is particularly suitable for dealing with large datasets. Here's how it works:

1. **Configuration**: The script begins by configuring the API details. You need to specify the following information in the `api_access` key in `conf.json`:

   - `base_url`: The base URL of the API you want to access.
   - `Authorization`: If the API requires authorization, you provide the access token or API key in this field.
   - `records_per_page`: You specify the number of records to retrieve per page. This value depends on the API's design.

2. **Total Records Calculation**: If the API provides information about the total number of records (often indicated as the `total` field in the API response), the script calculates the total number of pages required to retrieve the exact number of records specified. It rounds up to the nearest whole page.

3. **Asynchronous Requests**: To enhance efficiency, the script uses asynchronous requests. 

4. **Pagination Handling**: The script iterates through the pages of the API, fetching data from each page and extending the `all_data` list with the data obtained. It logs each page fetched, making it easy to monitor the retrieval process.

5. **Efficiency and Performance**: The script is optimized for performance by minimizing the time required to retrieve large datasets. It keeps track of execution time, providing valuable feedback on the script's efficiency.


## Considerations

- **Total Records**: If the API provides information about the total number of records (e.g., the `total` field in the API response), the script calculates the number of pages required to retrieve the exact number of records specified.Else default for total is 1. you can custom script by your necessity

- **Async Processing**: The script utilizes asynchronous requests and multi-threading for efficiency. Be cautious about the maximum number of concurrent requests to avoid overloading the server or breaching rate limits.

- **Error Handling**: Ensure proper error handling is in place in case the API returns errors. You may want to implement retries or error logging for robustness.


## Limitations

- This code assumes that the API follows standard pagination practices. If the API has unique pagination mechanisms, additional adjustments may be required.

## Contributions

Contributions and improvements to this code are welcome. Please create a pull request or open an issue if you encounter any problems or have suggestions for enhancements.

