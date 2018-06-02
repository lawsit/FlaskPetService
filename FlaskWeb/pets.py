
from datetime import datetime
from flask import render_template
from FlaskWeb import app
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

from flask import request,redirect, redirect,url_for, jsonify

title = "Labs on using Python/Flask"
 
client = MongoClient(os.environ["db_url"])
db = client.admin    
db.authenticate(name=os.environ["db_user"],password=os.environ["db_password"] )

pets = db.pets

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

@app.route('/')
@app.route('/pets', methods=['GET'])
def get_all_pets():
    
    output = [] 
    heading = "Pet List"

    for s in pets.find(): 
       output.append({'_id' : s['_id'],
                      'origin' : s['origin'], 'name' : s['name'], 
                      'categoryName' : s['categoryName'],
                      'status' : s['status'] , 'age' : s['age'] })
    return render_template('home.html',pets=output,t=title,h=heading)    

@app.route('/update/<petId>')
def update (petId):
    
    heading = "Update Pet Record" 
    s= pets.find_one({'_id': ObjectId(petId)})
    output = []
    output.append({'_id' : s['_id'],
                      'origin' : s['origin'], 'name' : s['name'], 
                      'categoryName' : s['categoryName'],
                      'status' : s['status'] , 'age' : s['age'] })   
    return render_template('update.html',pets=output,h=heading,t=title)

@app.route("/remove")
def remove (): 
	key=request.values.get("_id")
	pets.remove({"_id":ObjectId(key)})
	return redirect("/pets")

@app.route('/pets/<petId>',methods=['GET'])
def get_one_pet(petId):
     
    s = pets.find_one({'_id': ObjectId(petId)}) 
    
    if s:
       output = {'origin' : s['origin'], 'name' : s['name'], 'status' : s['status'] , 'age' : s['age'] }
    else:
       output = "No record returned"
                
    return jsonify({'result' : output}) 


@app.route('/searchByStat/<_stat>',methods=['GET'])
def get_pets(_stat): 
    output = []
    
    for s in pets.find({'status' : _stat}):
       output.append({'origin' : s['origin'], 'name' : s['name'], 'status' : s['status'] , 'age' : s['age'] })
    return jsonify({'result' : output})  
                 

    
@app.route("/pets", methods=['POST'])
def action ():
    content = request.json
    print (content['name'])
    name=content['name']
    status=content["status"]
    categoryName=content["categoryName"]
    origin=content["origin"]
    age=content["age"]
    pets.insert({ "name":name, "status":status, "categoryName":categoryName, "origin":origin, "age":age})
    return redirect("/pets")
    
      
@app.route("/updateRecord", methods=['POST'])
def updateRecord ():
	 
    id=request.values.get("_id")
    name=request.values.get("name")
    categoryName=request.values.get("categoryName")
    status=request.values.get("status")
    origin=request.values.get("origin")
    age=request.values.get("age")

    pets.update({"_id":ObjectId(id)}, {'$set':{ "name":name, "status":status, "categoryName":categoryName, "origin":origin, "age":age}})
    return redirect("/pets")
 