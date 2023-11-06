from flask import *

import ibm_db
import os 

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=3883e7e4-18f5-4afe-be8c-fa31c41761d2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31498;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=vnn69770;PWD=dKgLMEtsEtxRLHuT",'','')
print(conn)


app = Flask(__name__, template_folder='template')

@app.route('/')
def home():
    return render_template("index.html")




@app.route('/help')
def help():
    return render_template("help.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/login')
def login():
    return render_template("login.html")
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/result')
def result():
    return render_template("result.html")



@app.route('/guided')
def guided():
    return render_template("guided.html")

@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route('/register1',methods=['POST'])
def register1():
    x = [x for x in request.form.values()]
    print(x)
    NAME=x[0]
    EMAIL=x[1]
    PASSWORD=x[2]
    sql = "SELECT * FROM REGISTER WHERE EMAIL =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,EMAIL)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print(account)
    if account:
        return render_template('login.html', pred="You are already a member, please login using your details")
    else:
        insert_sql = "INSERT INTO  REGISTER VALUES (?, ?, ?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, NAME)
        ibm_db.bind_param(prep_stmt, 2, EMAIL)
        ibm_db.bind_param(prep_stmt, 3, PASSWORD)
        ibm_db.execute(prep_stmt)
        return render_template('login.html', pred="Registration Successful, please login using your details")
            
@app.route('/login1',methods=['POST'])
def login1():
    NAME = request.form['NAME']
    EMAIL = request.form['EMAIL']
    sql = "SELECT * FROM REGISTER WHERE NAME =? AND EMAIL=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,NAME)
    ibm_db.bind_param(stmt,2,EMAIL)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print (account)
    print(NAME,EMAIL)
    if account:
            return render_template('admin.html', pred="Login successful")
    else:
        return render_template('login.html', pred="Login unsuccessful. Incorrect username/password !")
    
    
    
    
@app.route('/result1',methods = ["POST","GET"])
def result1():
    if request.method=="POST":
        f=request.files['image']
        basepath=os.path.dirname(__file__) #getting the current path i.e where app.py is present
        #print("current path",basepath)
        filepath=os.path.join(basepath,'uploads',f.filename) #from anywhere in the system we can give image but we want that image later  to process so we are saving it to uploads folder for reusing
        #print("upload folder is",filepath)
        f.save(filepath)
        
        return render_template("result.html")
        
        return "Image uploaded successfully"
       
        COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud"
        COS_API_KEY_ID = "UKQDmU0zPDyzGzX_wYao20jqSVo0jNQY_ASt0XM4UxEY"
        COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/8a03f1c86efe4897abd7cd5050702178:6cabfb46-eaaf-4755-a0af-94411770b25d::"
        cos = ibm_boto3.client("s3",ibm_api_key_id=COS_API_KEY_ID,ibm_service_instance_id=COS_INSTANCE_CRN, config=Config(signature_version="oauth"),endpoint_url=COS_ENDPOINT)
        cos.upload_file(Filename= filepath,Bucket='nikhilimages',Key='cadsession.jpg')
      
    return render_template("result.html")
   






if __name__ == "__main__":
    app.run(debug = True,port = 2000,host ='0.0.0.0')






