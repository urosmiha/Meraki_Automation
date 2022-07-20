import json
from re import TEMPLATE
from textwrap import indent
import requests

import meraki
from env import API_KEY, ORG_ID, SG_HQ, MV2_SERIAL

BASE_URL = "https://api.meraki.com/api/v1/"


def getCameras(dashboard, newtrok_id):
    '''
    Return all the cameras from my network
    '''
    devices = getAllNetworkDevices(dashboard, newtrok_id)
    cameras = []
    # check all devices in the network and return the ones which model starts with MV
    for device in devices:
        if "MV" in device['model'][:2]:
            cameras.append({
                "name" : device['name'],
                "serial" : device['serial']
            }
            )
    return cameras


def requestsCall(method, api_key, base_url, api_id, payload=None):

    url = "{}/{}".format(base_url, api_id)

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key": api_key
    }

    response = requests.request(method, url, headers=headers, data = payload)

    print (json.dumps(response.json(), indent=2))


def downloadTemplateToJson(dashboard, org_id, template_id):
    '''
    Update Template: https://developer.cisco.com/meraki/api-latest/#!update-organization-config-template
    Create Template: https://developer.cisco.com/meraki/api-latest/#!create-organization-config-template
    '''

    response = dashboard.switch.getOrganizationConfigTemplateSwitchProfiles(org_id, template_id)
    # print(json.dumps(response, indent=2))
    JsonToFile(json.dumps(response, indent=2), "hello")


def getSwitchPortTemplate(dashboard, org_id, template_id, switchport_id):
    '''
    https://developer.cisco.com/meraki/api-latest/#!get-organization-config-template-switch-profile-ports

    Update switch profile port: https://developer.cisco.com/meraki/api-latest/#!update-organization-config-template-switch-profile-port
    '''

    response = dashboard.switch.getOrganizationConfigTemplateSwitchProfilePorts(
    org_id, template_id, switchport_id)
    print(json.dumps(response, indent=2))


def JsonToFile(json_string, name):
    print(type(json_string))
    print(json_string)

    with open('ConfigTemplates/json_data.json', 'w') as outfile:
        outfile.write(json_string)


def createAdmin(dashboard, organization_id, email, name, org_access):

    response = dashboard.organizations.createOrganizationAdmin(
        organization_id, email, name, org_access, 
        tags=[{'tag': 'api', 'access': 'full'}]
    )

    print(json.dumps(response), indent=2)


if __name__ == "__main__":
    print("Hello Meraki")
    # requestsCall('GET', API_KEY, BASE_URL, "organizations")

    dashboard = meraki.DashboardAPI(API_KEY)

    # print(json.dumps(dashboard.organizations.getOrganizations(), indent=2))
    # print(json.dumps(dashboard.organizations.getOrganization(ORG_ID), indent=2))
    # print(json.dumps(dashboard.organizations.getOrganizationNetworks(ORG_ID, total_pages='all'), indent=2))

    # print(json.dumps(dashboard.networks.getNetworkDevices(SG_HQ), indent=2))
    # print(json.dumps(getCameras(dashboard, SG_HQ), indent=2))

    # get Org Templates
    # print(json.dumps(dashboard.organizations.getOrganizationConfigTemplates(ORG_ID), indent=2))
    # downloadTemplateToJson(dashboard, ORG_ID, TMP_ACCESS)
    # getSwitchPortTemplate(dashboard, ORG_ID, TMP_ACCESS, SW_PORT)

    # Admin manupulation
    # createAdmin(dashboard, ORG_ID, "", "", "full")

