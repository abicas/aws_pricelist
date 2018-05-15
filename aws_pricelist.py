import boto3
import json
import argparse

parser = argparse.ArgumentParser(description='Instance Details')
parser.add_argument('instance', help='instance type (i.e. m4.4xlarge)')
parser.add_argument('--region', help='region (i.e. us-east-1)', default='us-east-1')
parser.add_argument('--format', help='default: text, optional table', default='text')
args = parser.parse_args()

regions = {
'us-east-2' : 'US East (Ohio)',
'us-east-1' : 'US East (N. Virginia)',
'us-west-1' : 'US West (N. California)',
'us-west-2' : 'US West (Oregon)',
'ap-northeast-1' : 'Asia Pacific (Tokyo)',
'ap-northeast-2' : 'Asia Pacific (Seoul)',
'ap-northeast-3' : 'Asia Pacific (Osaka-Local)',
'ap-south-1' : 'Asia Pacific (Mumbai)',
'ap-southeast-1' : 'Asia Pacific (Singapore)',
'ap-southeast-2' : 'Asia Pacific (Sydney)',
'ca-central-1' : 'Canada (Central)',
'cn-north-1' : 'China (Beijing)',
'cn-northwest-1' : 'China (Ningxia)',
'eu-central-1' : 'EU (Frankfurt)',
'eu-west-1' : 'EU (Ireland)',
'eu-west-2' : 'EU (London)',
'eu-west-3' : 'EU (Paris)',
'sa-east-1' : 'South America (Sao Paulo)',
'us-gov-west-1' : 'AWS GovCloud (US)'}

pricing = boto3.client('pricing')

print ("Querying for ")
print (" - instance type: "+ args.instance)
print (" - region:        "+ regions[args.region])


#print("All Services")
#print("============")
#response = pricing.describe_services()
#for service in response['Services']:
#    print(service['ServiceCode'] + ": " + ", ".join(service['AttributeNames']))
#print()


response = pricing.get_products(
     ServiceCode='AmazonEC2',
     Filters = [
#        {'Type' :'TERM_MATCH', 'Field':'instanceType',    'Value':args.instance},
        {'Type' :'TERM_MATCH', 'Field':'tenancy',    'Value':'shared'},
		{'Type' :'TERM_MATCH', 'Field':'operatingSystem', 'Value':'Linux'},
		{'Type' :'TERM_MATCH', 'Field':'preInstalledSw', 'Value':'NA'},
        {'Type' :'TERM_MATCH', 'Field':'location',        'Value':regions[args.region]}
        
     ],
     MaxResults=100
)
if args.format == 'table':
	print ("Instance	vCPUs	Memory		USD/Hour OD")
for product in response['PriceList']:
	pp = json.loads(product)
	qq = json.loads(json.dumps(pp['product']['attributes']))
	rr = json.loads(json.dumps(pp['terms']['OnDemand']))
	ss = rr[list(rr.keys())[0]]['priceDimensions']
	tt = ss[list(ss.keys())[0]]['pricePerUnit']['USD']

	if args.instance in qq['instanceType']: 
		if args.format == 'text': 
			print ("Instance Type: "+qq['instanceType'])
			print ("       Config: "+qq['vcpu']+" vCPUs - "+ qq['memory'])
			print ("  USD/Hour OD: "+ '{:02.3f}'.format(float(tt)))
			print ("")
		else: 
			print (qq['instanceType']+"	"+qq['vcpu']+"	"+ qq['memory']+"		"+'{:02.3f}'.format(float(tt)))
