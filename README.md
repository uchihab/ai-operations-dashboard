# AI Operations Dashboard

AI-powered operations analytics dashboard for monitoring KPIs, costs, productivity, customer experience, and business-unit performance.

## Overview

This project combines Business Operations, Data Analytics, and Artificial Intelligence to support management decision-making.

The dashboard analyzes operational data across multiple business units, identifies performance gaps, highlights management attention points, and allows users to ask AI-assisted questions about the selected data.

## Features

- Executive KPI monitoring
- Revenue, cost, profit, and margin analysis
- Productivity and customer satisfaction tracking
- Business unit comparison
- Revenue vs. operating cost trends
- Automated operational insights
- Management attention alerts
- Management summary
- AI Business Analyst
- Dynamic filtering by business unit

## AI Business Analyst

The AI Business Analyst uses the operational data currently selected in the dashboard to answer management questions such as:

- Which business unit should management investigate first?
- Which unit has the weakest overall performance?
- Where should management focus to reduce costs?
- Which unit has the best operational efficiency?
- Why is a specific business unit underperforming?

The AI is instructed to analyze only the data provided by the dashboard and to support recommendations with operational metrics.

## Technologies

- Python
- Streamlit
- Plotly
- OpenAI API
- CSV Data Processing
- Git & GitHub

## Business Metrics

The dashboard currently monitors:

- Revenue
- Operating Cost
- Profit
- Profit Margin
- Orders
- Productivity
- Customer Satisfaction
- Customer Complaints
- Revenue per Employee
- Operating Cost Ratio

## Project Structure

```text
ai-operations-dashboard/
│
├── data/
│   └── operations_data.csv
│
├── src/
│   ├── __init__.py
│   └── generate_data.py
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
