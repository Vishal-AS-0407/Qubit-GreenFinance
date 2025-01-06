import tkinter as tk
from tkinter import ttk
import numpy as np
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpStatus

# Function to perform optimization and generate results
def run_optimization():
    # Larger Dataset
    projects = [f'Project{i+1}' for i in range(20)]  # 20 projects
    ESG_scores = np.random.uniform(0.6, 0.9, size=20).tolist()  # Random ESG scores between 0.6 and 0.9
    risk_scores = np.random.randint(4, 8, size=20).tolist()  # Random risk scores between 4 and 7
    min_budgets = np.random.randint(100, 200, size=20).tolist()  # Random min budgets between 100 and 200
    max_budgets = np.random.randint(300, 500, size=20).tolist()  # Random max budgets between 300 and 500
    total_budget = 1000  # Total budget for the optimization
    diversification_factor = 0.4  # No more than 40% of the total budget in a single project

    # Number of projects
    n = len(projects)

    # Initialize the optimization problem
    problem = LpProblem("Green_Finance_Optimization", LpMaximize)

    # Decision Variables: Investment amounts in each project
    investment = {i: LpVariable(f"investment_{i}", lowBound=0) for i in range(n)}

    # Strategies
    min_investment_threshold = 50  # Minimum threshold for investment in a project
    penalty_factor = 0.1  # Penalty for allocating very small amounts
    min_esg_threshold = 0.7  # Minimum ESG score threshold
    risk_penalty = 0.05  # Penalty weight for risk score

    # Objective Function: Maximize ESG Impact with Penalty for Small Allocations and Risk
    problem += lpSum(ESG_scores[i] * investment[i] for i in range(n)) \
               - penalty_factor * lpSum(investment[i] for i in range(n)) \
               - risk_penalty * lpSum(risk_scores[i] * investment[i] for i in range(n)), "Total_ESG_Impact_with_Risk_Penalty"

    # Constraints

    # 1. Total Budget Constraint
    problem += lpSum(investment[i] for i in range(n)) <= total_budget, "Total_Budget"

    # 2. Investment Limits per Project
    for i in range(n):
        problem += investment[i] >= max(min_budgets[i], min_investment_threshold), f"Min_Budget_{i}"
        problem += investment[i] <= max_budgets[i], f"Max_Budget_{i}"

    # 3. Diversification Constraint
    max_investment_per_project = diversification_factor * total_budget
    for i in range(n):
        problem += investment[i] <= max_investment_per_project, f"Diversification_{i}"

    # 4. Minimum ESG Impact per Project
    for i in range(n):
        if ESG_scores[i] < min_esg_threshold:
            problem += investment[i] == 0, f"Min_ESG_Impact_{i}"

    # Solve the problem
    problem.solve()

    # Results
    status = LpStatus[problem.status]
    total_investment = 0

    # Collecting the data for display
    project_data = []
    for i in range(n):
        allocated = investment[i].varValue
        total_investment += allocated
        project_data.append({
            'Project': projects[i],
            'Risk Score': risk_scores[i],
            'ESG Score': ESG_scores[i],
            'Min Budget': min_budgets[i],
            'Max Budget': max_budgets[i],
            'Allocated Budget': allocated
        })

    # Sorting the data by Allocated Budget in descending order
    project_data_sorted = sorted(project_data, key=lambda x: x['Allocated Budget'], reverse=True)

    # Clear previous entries
    for item in tree.get_children():
        tree.delete(item)

    # Inserting the new results into the table
    for data in project_data_sorted:
        tree.insert("", "end", values=(data['Project'], data['Risk Score'], f"{data['ESG Score']:.2f}", data['Min Budget'], data['Max Budget'], f"{data['Allocated Budget']:.2f}"))

    # Display total investment
    total_investment_label.config(text=f"Total Investment: {total_investment:.2f}")
    status_label.config(text=f"Status: {status}")

# Create main window
root = tk.Tk()
root.title("Green Finance Optimization")

# Set window size
root.geometry("800x600")
root.config(bg="#f7f7f7")

# Title label
title_label = tk.Label(root, text="Green Finance Investment Optimization", font=("Helvetica", 16, "bold"), bg="#f7f7f7")
title_label.pack(pady=10)

# Run optimization button
run_button = tk.Button(root, text="Run Optimization", command=run_optimization, font=("Helvetica", 12), bg="#4CAF50", fg="white", relief="flat", width=20)
run_button.pack(pady=10)

# Status label
status_label = tk.Label(root, text="Status: Not Started", font=("Helvetica", 12), bg="#f7f7f7")
status_label.pack(pady=5)

# Total investment label
total_investment_label = tk.Label(root, text="Total Investment: 0.00", font=("Helvetica", 12), bg="#f7f7f7")
total_investment_label.pack(pady=5)

# Treeview (table) for displaying project data
columns = ("Project", "Risk Score", "ESG Score", "Min Budget", "Max Budget", "Allocated Budget")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)

# Define column headings
for col in columns:
    tree.heading(col, text=col)

tree.pack(pady=20, padx=20)

# Run the Tkinter event loop
root.mainloop()
