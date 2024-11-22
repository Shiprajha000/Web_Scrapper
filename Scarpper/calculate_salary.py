import numpy as np
from pymongo import MongoClient

def calculate_average_salary():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['job_data']
    collection = db['python_jobs']
    
    salaries = []
    
    for job in collection.find():
        salary = job['salary']
        
        # Clean salary data
        if salary != "Not listed":
            salary = salary.replace('$', '').replace(',', '')
            try:
                salary_value = float(salary)
                salaries.append(salary_value)
            except ValueError:
                pass
    
    if salaries:
        average_salary = np.mean(salaries)
        print(f"Average Salary for Python Developers: ${average_salary:.2f}")
    else:
        print("No salary data available.")

if __name__ == "__main__":
    calculate_average_salary()
