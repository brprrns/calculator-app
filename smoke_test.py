import json
import os
import urllib.request

import boto3

region = os.environ.get("AWS_DEFAULT_REGION", "ap-south-1")
cf = boto3.client("cloudformation", region_name=region)
outputs = cf.describe_stacks(StackName="calculator-app")["Stacks"][0]["Outputs"]
url = next(o["OutputValue"] for o in outputs if o["OutputKey"] == "ApiUrl")
print("Live URL:", url)

with urllib.request.urlopen(url + "?op=add&a=2&b=3", timeout=20) as resp:
    body = json.loads(resp.read().decode())
print("Response:", body)
assert body["result"] == 5, "Smoke test failed"
print("Smoke test passed")
