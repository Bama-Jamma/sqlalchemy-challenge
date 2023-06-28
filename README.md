# sqlalchemy-challenge

# Hawaii Climate Analysis API

The Hawaii Climate Analysis API is a web service that provides climate analysis for the beautiful islands of Hawaii. It offers various routes to access climate data, including precipitation, temperature observations, and station information. The API leverages the OpenWeatherMap API to fetch current weather data for Hawaii.

## Installation

1. Clone the repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Create a file named `config.py` and store your OpenWeatherMap API key as `api_key = "<your-api-key>"`.
4. Run the application using `python app.py`.
5. Access the API at `http://localhost:5000/`.

## Usage

The API provides the following routes:

- `/api/v1.0/precipitation`: Returns a JSON list of precipitation data for the dates between 8/23/2016 and 8/23/2017.
- `/api/v1.0/stations`: Returns a JSON list of stations from the dataset.
- `/api/v1.0/tobs`: Returns a JSON list of temperature observations (TOBS) for the dates between 8/23/2016 and 8/23/2017.
- `/api/v1.0/<start>`: Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for all dates greater than and equal to the start date. Replace `<start>` in the URL with a valid date in the format YYYY-MM-DD.
- `/api/v1.0/<start>/<end>`: Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for the dates between the start and end dates (inclusive). Replace `<start>` and `<end>` in the URL with valid dates in the format YYYY-MM-DD.

## Example

To retrieve the current weather data for Hawaii, you can access the root endpoint:

- `http://localhost:5000/`

The response will include the current temperature in Celsius and Fahrenheit, as well as the weather condition.

## Dependencies

The project uses the following dependencies:

- Flask: A lightweight web framework used to create the API endpoints.
- Requests: A library used to make HTTP requests to the OpenWeatherMap API.

## Analysis

The Hawaii Climate Analysis API provides valuable climate data for the beautiful islands of Hawaii. With this API, users can access information such as precipitation, temperature observations, and station details. This data can be used for various purposes, including research, planning outdoor activities, or gaining insights into the climate patterns of Hawaii.

The API leverages the OpenWeatherMap API to fetch the current weather data for Hawaii. By integrating this external service, the API ensures accurate and up-to-date weather information. The API key is securely stored in a separate configuration file to maintain privacy and prevent unauthorized access.

The API's endpoints follow a consistent naming convention and provide a user-friendly way to access different types of climate data. The `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>` endpoints allow users to retrieve temperature statistics for specific date ranges. This feature is particularly useful for researchers or analysts who want to study temperature patterns over time.

The code is implemented using Python and Flask, making it lightweight and easy to understand. The project is well-structured, with separate functions for fetching weather data, converting temperature units, and generating the HTML response. The use of Markdown for the README file ensures readability and proper formatting.

Overall, the Hawaii Climate Analysis API is a valuable tool for anyone interested in exploring the climate of Hawaii. Its simple interface, well-defined endpoints, and integration with the OpenWeatherMap API make it a reliable source of climate data. Whether it's for scientific research or planning a vacation, this API provides the necessary information to understand and analyze the climate of Hawaii.

### This project is brought to you by:
Insomnia and caffine.

Music: Breakance
Podcast: Lex Friendman