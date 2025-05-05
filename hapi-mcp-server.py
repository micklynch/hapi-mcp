from mcp.server.fastmcp import FastMCP
import requests

FHIR_SERVER_URL = "https://hapi.fhir.org/baseR4"


# Initialize the MCP server with a friendly name
mcp = FastMCP("HAPI-MCP")

@mcp.tool()
def find_patient(patient_id: str) -> dict:

    """
    Find a patient by their ID.
    """

    url = f"{FHIR_SERVER_URL}/Patient/{patient_id}"
    response = requests.get(url)
    patient = response.json()

    return patient

@mcp.tool()
def find_medication_requests_by_patient_id(patient_id: str) -> dict:
    """
    Find medication requests for a patient by their ID.
    """
    url = f"{FHIR_SERVER_URL}/MedicationRequest?patient={patient_id}"
    response = requests.get(url)
    medication_requests = response.json()
    return medication_requests

@mcp.tool()
def find_observations_by_patient_id(patient_id: str) -> dict:
    """
    Find observations for a patient by their ID.
    """
    url = f"{FHIR_SERVER_URL}/Observation?patient={patient_id}"
    response = requests.get(url)
    observations = response.json()
    return observations

@mcp.tool()
def find_patient_by_name(first_name: str, last_name: str) -> dict:
    """
    Find patients by first and last name.
    """
    url = f"{FHIR_SERVER_URL}/Patient?given={first_name}&family={last_name}"
    response = requests.get(url)
    patients_bundle = response.json()
    return patients_bundle


if __name__ == "__main__":
    mcp.run(transport="stdio")
