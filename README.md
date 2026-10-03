# Business Sales Data Analysis

## Project Overview
This project is a beginner-friendly data science and analytics project for business sales analysis. It focuses on understanding sales performance, identifying high-value products and categories, evaluating regional performance, and creating a simple professional dashboard.

## Internship Task
This project was created to satisfy a business analytics internship task that includes:
- data cleaning and preparation
- KPI calculation
- revenue trend analysis
- product and category analysis
- regional analysis
- dashboard development
- business insights and recommendations

## Problem Statement
Businesses need a clear understanding of product performance, customer demand, and revenue movement across time and regions. Without this understanding, inventory planning, sales strategy, and marketing decisions become difficult.

## Objectives
- Explore the sales dataset and understand its structure.
- Clean the data and prepare it for business analysis.
- Measure the main sales KPIs.
- Identify top-performing products, categories, and regions.
- Analyze revenue trends over time.
- Build a professional dashboard using Streamlit.
- Present actionable business recommendations based on the data.

## Dataset
This project uses a realistic sample sales dataset stored in `data/sales_data.csv`.

The dataset includes the following fields, if present in the source file:
- Order_ID
- Order_Date
- Product
- Category
- Region
- Quantity
- Unit_Price
- Discount
- Revenue
- Profit

The code is written to inspect the dataset first and adapt to the actual column names. It does not assume a fixed schema.

## Technologies Used
- Python 3
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit
- Jupyter Notebook

## Data Cleaning
The project performs data cleaning by:
- loading the dataset with Pandas
- displaying the first rows and shape
- checking columns and data types
- identifying missing values and duplicates
- converting date columns to datetime
- cleaning numeric values
- filling missing discount values with zero
- creating a Revenue column when needed
- removing invalid rows and standardizing text values
- retaining missing category labels as `Unknown`
- estimating missing profit at 28% of revenue when no profit value is available

The dataset is a generated sample. Profit is illustrative rather than cost-accounted because product costs and returns are not provided; do not use its flat 28% margin to rank categories for investment.

## KPIs
The project calculates important business KPIs when the relevant data is available, including:
- Total Revenue
- Total Orders
- Total Quantity Sold
- Average Order Value
- Number of Products
- Number of Categories
- Number of Regions
- Revenue Growth

If a required column is missing, the project clearly reports that the KPI cannot be calculated.

## Exploratory Data Analysis
The project includes exploratory analysis for:
- revenue trends over time
- top-selling products
- category contribution
- regional performance
- product and category comparison

## Revenue Trends
Revenue is analyzed by month to study growth, decline, and seasonal movement. Trend charts are generated to identify peak and low periods.

## Product Analysis
The project identifies:
- top 10 products by revenue
- top 10 products by quantity sold
- the percentage contribution of the most important products

## Category Analysis
The project compares categories using:
- total revenue
- total quantity sold
- percentage contribution to total revenue

## Regional Analysis
Regional analysis focuses on:
- revenue by region
- quantity sold by region
- average order value by region
- strong and weak-performing regions

## Dashboard
A Streamlit dashboard is included to present the following sections:
- Sales Overview
- Product Performance
- Category Performance
- Category profitability with an illustrative-profit caveat
- Regional Performance
- Business Insights
- Actionable region and inventory recommendations
- Year-bounded date filters, synchronized reset controls, and explicit month-over-month growth
- Downloadable filtered data and an HTML executive report with embedded charts and KPI definitions

## Key Insights
The final insights are generated directly from the dataset. They help answer questions such as:
- Which product generates the most revenue?
- Which category contributes the most?
- Which region is performing best?
- Is there a recurring sales pattern over time?
- Are a small number of products driving a large share of revenue?

## Business Recommendations
Recommendations are tied directly to evidence found in the business data, including:
- inventory planning
- product promotion
- regional strategy
- marketing focus
- seasonal promotions
- category investment decisions

## Project Structure
business-sales-analysis/
├── data/
│   └── sales_data.csv
├── notebooks/
│   └── sales_analysis.ipynb
├── src/
│   └── analysis.py
├── app.py
├── requirements.txt
├── README.md
├── .gitignore

## How to Run
1. Open a terminal in this project folder.
2. Create a virtual environment if needed.
3. Install dependencies:
   pip install -r requirements.txt
4. Run the analysis notebook.
5. Run the dashboard:
   streamlit run app.py

## Results
The results are contained in the generated charts, KPI outputs, and dashboard views. These are based on the actual dataset in `data/sales_data.csv`.

## Future Improvements
Possible improvements include:
- adding customer analysis
- adding profit margin analysis
- integrating a database
- generating an automated PDF report
- deploying the dashboard online
