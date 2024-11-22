import zeep 

wsdl = 'http://172.25.1.177:8080/ClarityServiceManagement-war/ServiceManagementAPIService?wsdl'
client = zeep.Client(wsdl=wsdl)
print(client.service.getActiveServiceOrderID('SI200507232000016551'))