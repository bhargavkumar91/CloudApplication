from passlib.hash import pbkdf2_sha256
import pymongo

# Establishing the connection
username = "tezindia"
password = "tezos"

srv = "mongodb+srv://{}:{}@supplychain-u6nhl.mongodb.net/test?retryWrites=true&w=majority".format(
    username, password)
client = pymongo.MongoClient(srv)

print("MongoDB Connected")

db = client['Authenication']

LoginCollection = db['Login']
RequestCollection = db['Request']
SupplierCollection = db['Supplier']

def Register(email, name, password, category, hashc):
    q1 = {"email": email}
    p = LoginCollection.find(q1)
    check = False

    for i in p:
        if email == i['email']:
            check = True

    if check:
        print("email adress already in database")
        return False
    else:
        password = pbkdf2_sha256.hash(password)
        q2 = {"name": name, "email": email,
              "password": password, 'hash': hashc}
        q2['category'] = category

        # print(q2)
        r = LoginCollection.insert_one(q2)
        return True

def Login(email, password):
    l1 = {"email": email}
    res = LoginCollection.find(l1)

    data = {}
    data['check'] = False
    for i in res:
        if pbkdf2_sha256.verify(password, i['password']):
            data['name'] = i['name']
            data['category'] = i['category']
            data['check'] = True
            data['hash'] = i['hash']
    print(data)
    return data

def AddSupplierRequest(CompanyHash,code,CompanyName):
    l1 = {'hash':code}
    check = False
    res = LoginCollection.find(l1)
    for i in res:
        if i['category'] == "Supplier/Buyer":
            check = True 
            
    l2 = {'company':CompanyHash}
    tes = RequestCollection.find(l2)
    
    for i in tes:
        if i['Supplier'] == code:
            check = False
    
    if check:
        l3 = {'company':CompanyName,'Buyer':code,'companyhash':CompanyHash}
        r = RequestCollection.insert_one(l3)
        return True
    return False

def ApprovalStatus(hash):
    l1  =  {'Buyer':hash}
    result = RequestCollection.find(l1)
    data = {}
    for i in result:
        data[i['companyhash']] = i['company']
    print(data)
    return data

def RequestProces(SupplierName,SupplierHash,CompanyHash,check):
    l1  =  {'Buyer':CompanyHash,'companyhash':SupplierHash}
    print(l1)
    result = RequestCollection.delete_one(l1)
    
    if check == 'true':
        l2 = {'CompanyHash':CompanyHash,'SupplierName':SupplierName,'SupplierHash':SupplierHash}
        SupplierCollection.insert_one(l2)
