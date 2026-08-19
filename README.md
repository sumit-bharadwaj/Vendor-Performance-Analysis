Vendor Performance Analysis:-

This is a small end-to-end data analysis project I built to understand vendor and sales performance for a retail/inventory dataset — from raw CSV files all the way to a Power BI dashboard.

Basically I wanted to answer a simple question: are we buying from the right vendors, at the right price, in the right quantity? Turns out the answer was "not really" for a bunch of vendors, and this project is how I found that out.

What I did
Took raw CSV files (purchases, sales, purchase prices, vendor invoices, inventory) and loaded them into a MySQL database using Python — wrote a small ingestion script that also logs everything (so if something fails halfway, I don't have to guess what happened).
Set up the database in MySQL Workbench.
Wrote SQL joins in Jupyter Notebook to combine all the raw tables into one clean summary table — vendor_sales_summary — with calculated columns like Gross Profit, Profit Margin, Stock Turnover, etc.
Did EDA on that summary table — checked distributions, outliers, correlations, cleaned up bad data (negative margins, zero sales, etc.)
Dug into some actual business questions with stats (t-test, confidence intervals) — not just eyeballing charts.
Connected MySQL to Power BI (using MySQL Connector/NET) and built a dashboard on top of the same summary table.
Wrote up everything in a report with the final recommendations.
Tools used
Python (pandas, numpy, matplotlib, seaborn, scipy) — for cleaning, EDA, and stats
MySQL / MySQL Workbench — database
SQLAlchemy + PyMySQL — connecting Python to MySQL
Power BI — dashboard
Jupyter Notebook — where all the actual work happened
Python's logging module — instead of just using print() everywhere

Folder structure
vendor-performance-analysis/
├── data/                      → raw CSVs go here (not uploaded, add your own)
├── logs/
│   └── ingestion_db.log       → logs from the ingestion run
├── notebooks/
│   ├── Logging.ipynb                      → ingestion + logging setup
│   ├── Exploratory_Data_Analysis.ipynb    → builds vendor_sales_summary
│   └── Vendor_Performance_Analysis.ipynb  → the actual analysis + stats
├── dashboard/                 → Power BI file goes here
├── ingestion_db.py            → same ingestion logic as a standalone script
├── Report.docx                → written report with charts
└── README.md
The main tables

Raw tables (from CSV → MySQL):

purchases — what was bought, from whom, when, how much
purchase_prices — vendor + brand wise pricing
vendor_invoice — purchase invoices, includes freight cost
sales — sales transactions
begin_inventory - stock at start
end_inventory — stock at end

The table I actually built the analysis on — vendor_sales_summary: made by joining the above with a CTE-based SQL query, then adding these columns in pandas:

GrossProfit = Total Sales $ − Total Purchase $
ProfitMargin = Gross Profit / Total Sales $ × 100
StockTurnOver = Sales Qty / Purchase Qty
SalesPurchaseRatio = Sales $ / Purchase $
What I found

Some of this genuinely surprised me while I was doing the analysis:

198 brands are selling low volume but have really high profit margins — these are probably underpriced or under-marketed. Good targets for a price bump or a promo push.
Just 10 vendors make up 65.7% of total purchases. That's a lot of dependency on very few suppliers — risky if even one of them has a supply issue.
Buying in bulk actually works — large orders get 72% lower unit cost than small orders (~$10.78/unit vs a lot more for small orders).
Around $2.71M worth of inventory is just sitting unsold. A few vendors account for most of it — that's dead capital.
Ran a t-test comparing profit margins of top vs low performing vendors — the difference (30.7-31.6% vs 40.5-42.6%) is statistically significant, not just random noise. So low-performing vendors are protecting margin but not driving volume, which is its own kind of problem.

Full write-up with charts is in Report.docx.

How to run this yourself

You'll need Python 3.10+, MySQL, MySQL Workbench, and Power BI Desktop installed.

Add your DB credentials in a .env file (don't hardcode them like I initially did in the notebook — learned that the hard way):

DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=inventory

Drop your CSVs into data/, then run:

bash
python ingestion_db.py

After that, just run the two notebooks in order:

Exploratory_Data_Analysis.ipynb
Vendor_Performance_Analysis.ipynb

For Power BI — install MySQL Connector/NET, then in Power BI Desktop go to Get Data → MySQL Database, connect to the same DB, and pull in vendor_sales_summary.

Things I'd still like to improve
Get the DB password out of the code completely (currently half-done)
Automate the whole pipeline so it refreshes on a schedule instead of running notebooks manually
Add some basic tests for the ingestion function
Stop hardcoding thresholds (like the 15th/85th percentile cutoffs) — make them configurable
