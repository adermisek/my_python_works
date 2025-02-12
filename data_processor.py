import pandas as pd
import os

class DataProcessor:
    @staticmethod
    def manipulate(df):
        """Dodaje nove kolone i kreira grupisane podatke"""
        df["Start_Date"] = pd.to_datetime(df["Start_Date"])
        df["Year"] = df["Start_Date"].dt.year
        df["New_Salary"] = df["Salary"] + df["Bonus"]
        
        df = df[["ID", "Full_Name", "City", "Job_Title", "Department", "Salary", "Bonus", "New_Salary", "Years_of_Experience", "Start_Date", "Year"]]
        
        grouped_by_year = df.groupby("Year")["ID"].count().reset_index().rename(columns={"ID": "Employee_Count"})
        grouped_by_department_avg_salary = df.groupby("Department")["New_Salary"].mean().reset_index().rename(columns={"New_Salary": "Avg_Salary"})
        
        df_neto = df[['ID', 'Full_Name', 'New_Salary']].copy()
        df_neto['Neto_Salary'] = df_neto['New_Salary'] * 0.62

        return df, grouped_by_year, grouped_by_department_avg_salary, df_neto
    
    @staticmethod
    def save_to_excel(df, grouped_by_year, grouped_by_department_avg_salary, df_neto):
       
        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, "EmployeesFiltered.xlsx")
        
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Employees", index=False)
            grouped_by_year.to_excel(writer, sheet_name="Grouped by Year", index=False)
            grouped_by_department_avg_salary.to_excel(writer, sheet_name="Grouped by Department", index=False)
            df_neto.to_excel(writer, sheet_name="Employees neto", index=False)
        
        return output_path

