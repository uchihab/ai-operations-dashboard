import csv
from collections import defaultdict

import streamlit as st
import plotly.graph_objects as go


st.set_page_config(
    page_title="AI Operations Dashboard",
    page_icon="📊",
    layout="wide",
)


# ------------------------------------
# LOAD DATA
# ------------------------------------

def load_data():

    rows = []

    with open(
        "data/operations_data.csv",
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            row["revenue"] = float(row["revenue"])

            row["operational_cost"] = float(
                row["operational_cost"]
            )

            row["orders"] = int(row["orders"])

            row["employees"] = int(row["employees"])

            row["customer_complaints"] = int(
                row["customer_complaints"]
            )

            row["productivity"] = float(
                row["productivity"]
            )

            row["customer_satisfaction"] = float(
                row["customer_satisfaction"]
            )

            row["profit"] = (
                row["revenue"]
                - row["operational_cost"]
            )

            rows.append(row)

    return rows


data = load_data()


# ------------------------------------
# HEADER
# ------------------------------------

st.title("AI Operations Dashboard")

st.caption(
    "Business Performance & Operational Intelligence"
)

st.write(
    "Monitor operational performance across business units "
    "using financial, productivity and customer experience KPIs."
)


# ------------------------------------
# SIDEBAR
# ------------------------------------

business_units = sorted(
    set(
        row["business_unit"]
        for row in data
    )
)


st.sidebar.header("Filters")

selected_units = st.sidebar.multiselect(
    "Business Units",
    business_units,
    default=business_units,
)


filtered_data = [
    row
    for row in data
    if row["business_unit"] in selected_units
]


if not filtered_data:

    st.warning(
        "Select at least one business unit."
    )

    st.stop()


# ------------------------------------
# KPIs
# ------------------------------------

total_revenue = sum(
    row["revenue"]
    for row in filtered_data
)

total_cost = sum(
    row["operational_cost"]
    for row in filtered_data
)

total_profit = sum(
    row["profit"]
    for row in filtered_data
)

total_orders = sum(
    row["orders"]
    for row in filtered_data
)

profit_margin = (
    total_profit / total_revenue * 100
)

average_productivity = (
    sum(
        row["productivity"]
        for row in filtered_data
    )
    / len(filtered_data)
)

average_satisfaction = (
    sum(
        row["customer_satisfaction"]
        for row in filtered_data
    )
    / len(filtered_data)
)


st.subheader("Executive KPIs")


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Revenue",
    f"${total_revenue:,.0f}",
)

col2.metric(
    "Operating Cost",
    f"${total_cost:,.0f}",
)

col3.metric(
    "Profit",
    f"${total_profit:,.0f}",
)

col4.metric(
    "Profit Margin",
    f"{profit_margin:.1f}%",
)


col5, col6, col7 = st.columns(3)

col5.metric(
    "Orders",
    f"{total_orders:,}",
)

col6.metric(
    "Productivity",
    f"{average_productivity:.1f}%",
)

col7.metric(
    "Customer Satisfaction",
    f"{average_satisfaction:.1f}%",
)


st.divider()


# ------------------------------------
# DAILY PERFORMANCE
# ------------------------------------

daily_data = defaultdict(
    lambda: {
        "revenue": 0,
        "cost": 0,
    }
)


for row in filtered_data:

    current_date = row["date"]

    daily_data[current_date]["revenue"] += (
        row["revenue"]
    )

    daily_data[current_date]["cost"] += (
        row["operational_cost"]
    )


dates = sorted(daily_data.keys())

revenues = [
    daily_data[d]["revenue"]
    for d in dates
]

costs = [
    daily_data[d]["cost"]
    for d in dates
]


fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=dates,
        y=revenues,
        name="Revenue",
        mode="lines",
    )
)

fig.add_trace(
    go.Scatter(
        x=dates,
        y=costs,
        name="Operating Cost",
        mode="lines",
    )
)

fig.update_layout(
    title="Revenue vs Operating Cost",
    xaxis_title="Date",
    yaxis_title="Value",
)


st.plotly_chart(
    fig,
    use_container_width=True,
)


# ------------------------------------
# UNIT PERFORMANCE
# ------------------------------------

unit_profit = defaultdict(float)


for row in filtered_data:

    unit_profit[
        row["business_unit"]
    ] += row["profit"]


units = sorted(unit_profit.keys())

profits = [
    unit_profit[unit]
    for unit in units
]


fig_units = go.Figure(
    data=[
        go.Bar(
            x=units,
            y=profits,
        )
    ]
)


fig_units.update_layout(
    title="Profit by Business Unit",
    xaxis_title="Business Unit",
    yaxis_title="Profit",
)


st.plotly_chart(
    fig_units,
    use_container_width=True,
)

# ------------------------------------
# OPERATIONAL INSIGHTS
# ------------------------------------

st.divider()

st.subheader("Operational Insights")

st.caption(
    "Automated analysis of financial, productivity "
    "and customer experience indicators."
)


unit_metrics = {}


for unit in selected_units:

    unit_rows = [
        row
        for row in filtered_data
        if row["business_unit"] == unit
    ]

    if not unit_rows:
        continue

    unit_revenue = sum(
        row["revenue"]
        for row in unit_rows
    )

    unit_cost = sum(
        row["operational_cost"]
        for row in unit_rows
    )

    unit_total_profit = sum(
        row["profit"]
        for row in unit_rows
    )

    unit_margin = (
        unit_total_profit / unit_revenue * 100
        if unit_revenue
        else 0
    )

    unit_productivity = (
        sum(
            row["productivity"]
            for row in unit_rows
        )
        / len(unit_rows)
    )

    unit_satisfaction = (
        sum(
            row["customer_satisfaction"]
            for row in unit_rows
        )
        / len(unit_rows)
    )

    unit_complaints = sum(
        row["customer_complaints"]
        for row in unit_rows
    )

    average_employees = (
        sum(
            row["employees"]
            for row in unit_rows
        )
        / len(unit_rows)
    )

    revenue_per_employee = (
        unit_revenue / average_employees
        if average_employees
        else 0
    )

    cost_ratio = (
        unit_cost / unit_revenue * 100
        if unit_revenue
        else 0
    )

    unit_metrics[unit] = {
        "revenue": unit_revenue,
        "cost": unit_cost,
        "profit": unit_total_profit,
        "margin": unit_margin,
        "productivity": unit_productivity,
        "satisfaction": unit_satisfaction,
        "complaints": unit_complaints,
        "revenue_per_employee": revenue_per_employee,
        "cost_ratio": cost_ratio,
    }


if unit_metrics:

    highest_profit_unit = max(
        unit_metrics,
        key=lambda unit: unit_metrics[unit]["profit"],
    )

    lowest_margin_unit = min(
        unit_metrics,
        key=lambda unit: unit_metrics[unit]["margin"],
    )

    lowest_productivity_unit = min(
        unit_metrics,
        key=lambda unit: unit_metrics[unit]["productivity"],
    )

    lowest_satisfaction_unit = min(
        unit_metrics,
        key=lambda unit: unit_metrics[unit]["satisfaction"],
    )

    highest_cost_ratio_unit = max(
        unit_metrics,
        key=lambda unit: unit_metrics[unit]["cost_ratio"],
    )

    highest_complaints_unit = max(
        unit_metrics,
        key=lambda unit: unit_metrics[unit]["complaints"],
    )

    best_efficiency_unit = max(
        unit_metrics,
        key=lambda unit: unit_metrics[unit][
            "revenue_per_employee"
        ],
    )


    # ------------------------------------
# PERFORMANCE CARDS
# ------------------------------------

insight_col1, insight_col2, insight_col3 = st.columns(3)

insight_col1.metric(
    "Top Profit Unit",
    highest_profit_unit,
    f"${unit_metrics[highest_profit_unit]['profit']:,.0f}",
)

insight_col2.metric(
    "Best Revenue / Employee",
    best_efficiency_unit,
    f"${unit_metrics[best_efficiency_unit]['revenue_per_employee']:,.0f}",
)

insight_col3.metric(
    "Highest Cost Ratio",
    highest_cost_ratio_unit,
    f"{unit_metrics[highest_cost_ratio_unit]['cost_ratio']:.1f}%",
)

st.markdown("### Management Attention Points")


# ------------------------------------
# MANAGEMENT SUMMARY
# ------------------------------------

st.divider()

st.subheader("Management Summary")


if unit_metrics:

    management_priority = min(
        unit_metrics,
        key=lambda unit: (
            unit_metrics[unit]["margin"]
            + unit_metrics[unit]["productivity"]
            + unit_metrics[unit]["satisfaction"]
        ),
    )

    st.write(
        f"Based on the currently selected data, "
        f"**{management_priority}** deserves additional "
        "management attention because its combined financial, "
        "productivity and customer experience indicators are "
        "weaker relative to the other selected business units."
    )

    st.write(
        f"Meanwhile, **{highest_profit_unit}** currently leads "
        "in total profitability and can be used as a reference "
        "point when investigating operational practices that "
        "could be replicated across other units."
    )