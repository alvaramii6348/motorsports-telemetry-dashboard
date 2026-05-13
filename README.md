# Motorsports Telemetry Dashboard

A Python-based telemetry dashboard for analyzing and comparing racing laps using Garage61/iRacing-style CSV data.

## Features

- Upload telemetry CSV files
- Compare two laps side-by-side
- Visualize speed, brake, and throttle traces
- Calculate lap summary statistics
- Analyze sector and mini-sector performance
- Identify where time is gained or lost across a lap

## Tech Stack

- Python
- pandas
- Streamlit
- Plotly
- NumPy

## Motivation

This project was built to strengthen my software engineering and data analysis skills while applying them to motorsports performance analysis.

## Project Structure

```text
src/
  data_loader.py
  preprocessing.py
  lap_analysis.py
  sector_analysis.py
  plotting.py
app.py