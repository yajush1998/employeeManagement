from neo4j import GraphDatabase
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
NEO4J_URI = "neo4j+s://d9e9f838.databases.neo4j.io"

NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "V85PJ0iYv_Yq1Z94o21QFWFmswT1ekruUxjgelX7mRA"

# Neo4j connection using neo4j.Driver
try:
    driver = GraphDatabase.driver("neo4j+s://d9e9f838.databases.neo4j.io", auth=("neo4j", "V85PJ0iYv_Yq1Z94o21QFWFmswT1ekruUxjgelX7mRA"))
    st.success("✅ Connected to Neo4j!")
except Exception as e:
    st.error(f"❌ Connection failed: {e}")
    driver = None

# Function to run queries
def run_query(query, parameters={}):
    with driver.session() as session:
        return session.run(query, **parameters).data() if driver else []

# Streamlit UI
st.title("Employee Management")

# Add employee section
st.header("Add New Employee")
new_name = st.text_input("Employee Name")
new_manager = st.text_input("Manager Name (Enter 'NA' if none)")
new_project = st.text_input("Project Name")

if st.button("Add Employee") and driver:
    query = "CREATE (:Employee {name: $name, manager: $manager, project: $project})"
    run_query(query, {"name": new_name, "manager": new_manager, "project": new_project})
    st.success(f"✅ Employee {new_name} added!")

# Search employee section
st.header("Search Employee")
search_name = st.text_input("Enter Employee Name")

if st.button("Search") and driver:
    query = "MATCH (e:Employee) WHERE e.name = $name RETURN e.name AS Employee, e.manager AS Manager, e.project AS Project"
    results = run_query(query, {"name": search_name})

    if results:
        for record in results:
            st.write(f"**Employee:** {record['Employee']}")
            st.write(f"**Manager:** {record['Manager']}")
            st.write(f"**Project:** {record['Project']}")
    else:
        st.warning("⚠ No records found.")
