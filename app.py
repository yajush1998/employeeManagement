from neo4j import GraphDatabase 
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
NEO4J_URI = "neo4j+s://d9e9f838.databases.neo4j.io"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "V85PJ0iYv_Yq1Z94o21QFWFmswT1ekruUxjgelX7mRA"

# Neo4j connection
try:
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    st.success("✅ Connected to Neo4j!")
except Exception as e:
    st.error(f"❌ Connection failed: {e}")
    driver = None

# Function to run queries
def run_query(query, parameters={}):
    if driver:
        with driver.session() as session:
            return session.run(query, **parameters).data()
    return []

# Function to check if an employee already exists
def employee_exists(name):
    query = """
    MATCH (e:Employee) 
    WHERE toLower(e.name) = toLower($name) 
    RETURN COUNT(e) AS count
    """
    result = run_query(query, {"name": name})
    return result[0]['count'] > 0 if result else False

# Streamlit UI
st.title("Employee Management")

# Add employee section
st.header("Add New Employee")
new_name = st.text_input("Employee Name *")
new_manager = st.text_input("Manager Name *")
new_project = st.text_input("Project Name *")

if st.button("Add Employee") and driver:
    if not new_name.strip() or not new_manager.strip() or not new_project.strip():
        st.warning("⚠ All fields are required!")
    elif employee_exists(new_name.strip()):
        st.warning(f"⚠ Employee '{new_name}' already exists. Please use a unique name!")
    else:
        query = "CREATE (:Employee {name: $name, manager: $manager, project: $project})"
        run_query(query, {"name": new_name.strip(), "manager": new_manager.strip(), "project": new_project.strip()})
        st.success(f"✅ Employee '{new_name}' added successfully!")

# Search employee section
st.header("Search Employee")
search_name = st.text_input("Enter Employee Name")

if st.button("Search") and driver:
    if search_name.strip():
        query = """
        MATCH (e:Employee) 
        WHERE toLower(e.name) = toLower($name) 
        RETURN e.name AS Employee, e.manager AS Manager, e.project AS Project
        """
        results = run_query(query, {"name": search_name.strip()})

        if results:
            for record in results:
                st.write(f"**Employee:** {record['Employee']}")
                st.write(f"**Manager:** {record['Manager']}")
                st.write(f"**Project:** {record['Project']}")
        else:
            st.warning("⚠ No such employee found in the database.")
    else:
        st.warning("⚠ Please enter a valid employee name.")
