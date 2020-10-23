import http.client
import json


def main(args): 
    # provide user name and api key for ibm cloud account- change it with your credentials       
    name = '{"username": "b.bhattacharyya@zzz.com","key": "atPNebdmMe2fDAk5hLKbcC3a2s3dAcAwO2zBSgYQkUl0","poweraction":"stop"}'
    namejson = json.loads(name)   
    ibmcloud_iaas_user = namejson["username"]
    print("Username: " + ibmcloud_iaas_user)
    ibmcloud_iaas_key = namejson["key"]
    # print("API Key: " + ibmcloud_iaas_key)
    iamv=iamtoken(ibmcloud_iaas_key)
    region = "us-south"

    conn = http.client.HTTPSConnection(f"{region}.iaas.cloud.ibm.com")

    headers = {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json',
        'Authorization': iamv,
        'cache-control': 'no-cache'
    }
    version = "2020-06-22"
    payload = ""

    try:
        # Connect to api endpoint for vpcs
        conn.request("GET", "/v1/instances?generation=2&version=" + version, payload, headers)

        # Get and read response data
        res = conn.getresponse()
        data = res.read()

        # iterate response data and call api with stop action for each instace
        namejson=json.loads(data.decode("utf-8"))
        for item in namejson["instances"]:
            print(item["id"])
            # use start to start the VMs & stop for shutting those down
            payload = f'{{"type": "stop"}}'
            itemid=item["id"]
            # itemid="0737_d239ced2-8a3e-41c1-9677-4a7dd98d6752"
            # print(json.dumps(namejson, indent=2, sort_keys=True))
            # Connect to api endpoint for vpcs
            conn.request("POST", "/v1/instances/"+itemid+"/actions?generation=2&version=" + version, payload, headers)
            
            # Get and read response data
            res = conn.getresponse()
            data = res.read()

            # Print response data
            print(data.decode("utf-8"))            
            

    except Exception as error:
        print(f"Error fetching VPCs. {error}")
        raise    
def iamtoken(apikey):
		# URL for token
		conn = http.client.HTTPSConnection("iam.cloud.ibm.com")

		# Payload for retrieving token. Note: An API key will need to be generated and replaced here
		payload = 'grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey&apikey='+apikey+'&response_type=cloud_iam'

		# Required headers
		headers = {
			'Content-Type': 'application/x-www-form-urlencoded',
			'Accept': 'application/json',
			'Cache-Control': 'no-cache'
		}

		try:
			# Connect to endpoint for retrieving a token
			conn.request("POST", "/identity/token", payload, headers)

			# Get and read response data
			res = conn.getresponse().read()
			data = res.decode("utf-8")

			# Format response in JSON
			json_res = json.loads(data)

			# Concatenate token type and token value
			return json_res['token_type'] + ' ' + json_res['access_token']

		# If an error happens while retrieving token
		except Exception as error:
			print(f"Error getting token. {error}")
			raise
main('')		    
