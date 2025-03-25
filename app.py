from neo4j import GraphDatabase
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Neo4j connection credentials
NEO4J_URI = "neo4j+s://d9e9f838.databases.neo4j.io"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "V85PJ0iYv_Yq1Z94o21QFWFmswT1ekruUxjgelX7mRA"

# Connect to Neo4j
try:
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    st.success("✅ Connected to Neo4j!")
except Exception as e:
    st.error(f"❌ Connection failed: {e}")
    driver = None

# Function to execute queries
def run_query(query, parameters={}):
    with driver.session() as session:
        return session.run(query, **parameters).data() if driver else []

# Streamlit UI
st.title("Employee Management System")

# ---------------------- ADD EMPLOYEE SECTION ----------------------
st.header("Add New Employee")

with st.form(key="add_employee_form"):
    new_name = st.text_input("Employee Name")  # Employee name input
    new_manager = st.text_input("Manager Name (Enter 'NA' if none)")  # Manager name
    new_project = st.text_input("Project Name")  # Project name
    submit_button = st.form_submit_button("Add Employee")  # Submit button

if submit_button and driver:
    new_name, new_manager, new_project = new_name.strip(), new_manager.strip(), new_project.strip()

    if not new_name or not new_manager or not new_project:
        st.error("⚠ All fields are required!")
    else:
        # Check if employee name already exists
        check_query = "MATCH (e:Employee {name: $name}) RETURN e"
        existing_employee = run_query(check_query, {"name": new_name})

        if existing_employee:
            st.error("⚠ Employee with this name already exists! Use a different name.")
        else:
            query = "CREATE (:Employee {name: $name, manager: $manager, project: $project})"
            run_query(query, {"name": new_name, "manager": new_manager, "project": new_project})
            st.success(f"✅ Employee {new_name} added successfully!")

# ---------------------- SEARCH EMPLOYEE SECTION ----------------------
st.header("Search Employee")

with st.form(key="search_employee_form"):
    search_name = st.text_input("Enter Employee Name to Search")
    search_button = st.form_submit_button("Search")

if search_button and driver:
    search_name = search_name.strip()

    if not search_name:
        st.warning("⚠ Please enter an employee name to search.")
    else:
        # Case-insensitive search
        query = """
        MATCH (e:Employee) 
        WHERE LOWER(e.name) = LOWER($name) 
        RETURN e.name AS Employee, e.manager AS Manager, e.project AS Project
        """
        results = run_query(query, {"name": search_name})

        if results:
            for record in results:
                st.write(f"**Employee:** {record['Employee']}")
                st.write(f"**Manager:** {record['Manager']}")
                st.write(f"**Project:** {record['Project']}")
                st.markdown("---")
        else:
            st.warning("⚠ No employee found with this name.")
