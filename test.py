service_list = ['Service 1' , 'Service 2', 'Service 3', 'Service 4' , 'Service 5']
kb = []

for i in range(0 , len(service_list) , 2):
    kb.append(service_list[i: i+2])
print(kb)