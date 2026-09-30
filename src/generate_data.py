import csv
import random
from datetime import date, timedelta
from pathlib import Path


random.seed(42)

business_units = [
    "Unit 01",
    "Unit 02",
    "Unit 03",
    "Unit 04",
    "Unit 05",
    "Unit 06",
    "Unit 07",
]

start_date = date(2026, 1, 1)
end_date = date(2026, 6, 30)

output_path = Path("data/operations_data.csv")

fieldnames = [
    "date",
    "business_unit",
    "revenue",
    "operational_cost",
    "orders",
    "employees",
    "customer_complaints",
    "average_service_time",
    "productivity",
    "customer_satisfaction",
]

rows = []

current_date = start_date

while current_date <= end_date:

    for unit in business_units:

        employees = random.randint(8, 17)
        orders = random.randint(60, 179)

        average_ticket = random.uniform(35, 80)
        revenue = orders * average_ticket

        operational_cost = revenue * random.uniform(0.55, 0.82)

        complaints = random.randint(0, 11)
        service_time = random.uniform(8, 25)
        productivity = random.uniform(70, 98)
        customer_satisfaction = random.uniform(75, 99)

        rows.append(
            {
                "date": current_date.isoformat(),
                "business_unit": unit,
                "revenue": round(revenue, 2),
                "operational_cost": round(operational_cost, 2),
                "orders": orders,
                "employees": employees,
                "customer_complaints": complaints,
                "average_service_time": round(service_time, 2),
                "productivity": round(productivity, 2),
                "customer_satisfaction": round(
                    customer_satisfaction,
                    2,
                ),
            }
        )

    current_date += timedelta(days=1)


with output_path.open(
    "w",
    newline="",
    encoding="utf-8",
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames,
    )

    writer.writeheader()
    writer.writerows(rows)


print(
    f"Dataset created successfully: {output_path}"
)

print(
    f"Rows generated: {len(rows)}"
)