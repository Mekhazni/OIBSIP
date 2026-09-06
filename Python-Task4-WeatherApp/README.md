# Basic Weather App

> Oasis Infobyte — Python Programming Internship | Task 4

A command-line weather application built with Python that retrieves and displays real-time weather information for a user-specified location using the OpenWeatherMap API.

## Project Overview

This project was developed as part of the Oasis Infobyte Python Programming Internship.

The application connects to the OpenWeatherMap API, retrieves the current weather information, processes the JSON response, and displays the relevant weather details in the terminal.

This implementation covers the Beginner Tier requirements of Task 4.

## Features

- Prompt the user to enter a city name or ZIP code
- Retrieve real-time weather data from the OpenWeatherMap API
- Parse the API response in JSON format
- Display the current temperature in Celsius and Fahrenheit
- Display humidity percentage
- Display weather condition
- Display wind speed
- Handle common API and network errors
- Validate user input and reject empty input

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Requests | Sending HTTP requests to the weather API |
| JSON | Processing API responses |
| python-dotenv | Loading the API key from an environment variable |
| OpenWeatherMap API | Providing real-time weather data |

## Project Structure

    Python-Task4-WeatherApp/
    ├── weather_api.py
    └── README.md

The `.env` file is stored locally and is not included in the repository because it contains the API key.

## How It Works

1. The user is prompted to enter a city name or ZIP code.
2. The input is checked to make sure it is not empty.
3. The application sends a request to the OpenWeatherMap API.
4. The API returns the current weather information as JSON.
5. The application extracts the required weather values.
6. The temperature is converted from Celsius to Fahrenheit.
7. The weather information is displayed in the terminal.
8. If an error occurs, an appropriate message is displayed.
9. Recoverable errors allow the user to try another location.

## API Configuration

An OpenWeatherMap API key is required to run the application.

Create a `.env` file in the project directory:

    OPENWEATHER_API_KEY=your_api_key_here

Replace `your_api_key_here` with your actual API key.

The key is loaded using `python-dotenv`:

    from dotenv import load_dotenv
    import os

    load_dotenv()

    API_KEY = os.getenv("OPENWEATHER_API_KEY")

The API key is not hard-coded into the source code.

## Installation

Make sure Python is installed on your computer.

Install the required dependencies:

    pip install requests python-dotenv

## Running the Application

Navigate to the project directory:

    cd Python-Task4-WeatherApp

Run the application:

    python weather_api.py

The application will prompt you to enter a location:

    Enter a city name or ZIP code: Algiers

## Example Output

    Weather Information
    -------------------
    City: Algiers
    Temperature: 30.9 °C
    Temperature: 87.6 °F
    Humidity: 66 %
    Condition: Clear Sky
    Wind Speed: 6.17 m/s

The displayed weather values depend on the current weather conditions and the selected location.

## Error Handling

The application handles the following situations:

| Situation | Behavior |
|---|---|
| Empty input | Asks the user to enter a location again |
| City not found | Displays an error message and asks again |
| Invalid API key | Displays an error message and stops the program |
| Network timeout | Displays a timeout message and allows another attempt |
| Other request errors | Displays an appropriate error message |

## Testing

The application was tested with:

- Valid city input
- Empty input
- Invalid or non-existent city
- Invalid API key
- Successful API request
- Weather information display
- Celsius to Fahrenheit conversion
- Network and API error handling

## What I Learned

Through this project, I practiced:

- Working with REST APIs
- Sending HTTP requests using `requests`
- Parsing JSON responses
- Managing API keys using environment variables
- Handling exceptions with `try` and `except`
- Validating user input
- Converting temperature units
- Organizing Python code using functions

## Outcome

The application successfully retrieves and displays real-time weather information from the OpenWeatherMap API.

The project fulfills the Beginner Tier requirements for Oasis Infobyte Python Programming Internship — Task 4: Basic Weather App.

## Author

**Nihad Mekhazni**

Python Programming Intern  
Oasis Infobyte — OIB-SIP

## Internship Details

| Field | Details |
|---|---|
| Organization | Oasis Infobyte |
| Program | OIB-SIP |
| Domain | Python Programming |
| Task | Task 4 — Basic Weather App |
| Level | Beginner |

## Security

The OpenWeatherMap API key is stored locally in a `.env` file and is not committed to GitHub.

This prevents the API key and unnecessary Python-generated files from being uploaded to the repository.
