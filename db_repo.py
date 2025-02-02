import mysql.connector
import json
import datetime
import random

su="1234567891" #Superuser


def pingAndReconnect(self):
	try:
		self.conn.ping()
	except self.conn.OperationalError as e:
		print "Caught An Operational Error... #reconnecting"
		self.conn = mysql.connector.connect(
			host="cgdbaws.cv23wjqihuhm.ap-south-1.rds.amazonaws.com",
			port=3306,
			user="root",
			passwd="CGDBAWSsql"
		)
		self.c=self.conn.cursor()
		self.c.execute('USE flaskdb;')
	except:
		print "caught default error, reconnecting"
		self.conn = mysql.connector.connect(
			host="cgdbaws.cv23wjqihuhm.ap-south-1.rds.amazonaws.com",
			port=3306,
			user="root",
			passwd="CGDBAWSsql"
		)
		self.c=self.conn.cursor()
		self.c.execute('USE flaskdb;')

class database_flaskr:

	def __init__(self):
		self.conn = mysql.connector.connect(
			host="cgdbaws.cv23wjqihuhm.ap-south-1.rds.amazonaws.com",
			port=3306,
			user="root",
			passwd="CGDBAWSsql"
		)
		self.c=self.conn.cursor()
		self.c.execute('USE flaskdb;')



#****************************************************************************
	#DBA definitions
	def killProcessList(self):
		'''
		db_response=self.c.execute("SELECT ID FROM INFORMATION_SCHEMA.PROCESSLIST;")
		db_response=self.c.fetchall()
		for row in db_response:
			process_id=row[0]
			if(int(process_id) > 100):
				query="CALL mysql.rds_kill("+str(process_id)+");"
				try:
					self.c.execute(query)
				except:
					continue
		'''
		return 'Done'
#****************************************************************************



#****************************************************************************
	#test definitions
	def yellowtest(self):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT * FROM aws_test;")
		db_response=self.c.fetchall()
		return str(db_response)
#****************************************************************************




#****************************************************************************
	#Learn2Earn Definitions
	def insertLearn2EarnRecordNumberData(self,tid,phoneNumber,datetime):
		pingAndReconnect(self)
		self.c.execute("INSERT INTO learn2earn_pilkha_ksheer_call_actions (tid,phoneNumber,datetime_of_call) VALUES (%s,%s,%s);",(tid,phoneNumber,datetime) )
		self.conn.commit()

	def insertLearn2EarnRecordNumberDataWithChannel(self,tid,phoneNumber,datetime,channel):
		pingAndReconnect(self)
		self.c.execute("INSERT INTO learn2earn_pilkha_ksheer_call_actions (tid,phoneNumber,datetime_of_call,oth_data_2) VALUES (%s,%s,%s,%s);",(tid,phoneNumber,datetime,channel) )
		self.conn.commit()

	def insertLearn2EarnRechargeData(self,tid,recharge_status,datetime,recharge_given):
		pingAndReconnect(self)
		self.c.execute("UPDATE learn2earn_pilkha_ksheer_call_actions SET recharge_status = %s, datetime_of_recharge = %s, recharge_given= %s WHERE tid = %s;",(recharge_status,datetime,recharge_given,tid) )
		self.conn.commit()

	def insertLearn2EarnReferralRechargeData(self,id,recharge_status,recharge_given):
		pingAndReconnect(self)
		self.c.execute("UPDATE l2e_referral_data SET recharge_status = %s, recharge_given= %s WHERE id = %s;",(recharge_status,recharge_given,id) )
		self.conn.commit()

	def insertHLRData(self,phoneNumber,op_code):
		pingAndReconnect(self)
		self.c.execute("INSERT INTO hlr_data (phoneNumber,op_code) VALUES (%s,%s);",(phoneNumber,op_code) )
		self.conn.commit()

	def getHLRData(self,phoneNumber):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT op_code FROM hlr_data WHERE phoneNumber = %s;",(phoneNumber,) )
		db_response=self.c.fetchall()
		if len(db_response) > 0:
			return [True,db_response[0][0]]
		else:
			return [False,""]

	def isRechargeEligible(self,tid):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT response_q1, response_q2, response_q3 FROM learn2earn_pilkha_ksheer_call_actions WHERE tid = %s;",(tid,))
		db_response=self.c.fetchall()
		q=db_response[0]
		if q[0]=='1' and q[1]=='1' and q[2]=='2':
			return True
		else:
			return False

	def learn2earnRedirector(self,tid):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT response_q1, response_q2, response_q3 FROM learn2earn_pilkha_ksheer_call_actions WHERE tid = %s;",(tid,))
		db_response=self.c.fetchall()
		shuffler=[]
		i=0
		for q in db_response[0]:
			i=i+1
			if q == None or not q or q.isspace() or q == '':
				shuffler.append(str(i))

		db_response_1=self.c.execute("SELECT phoneNumber FROM learn2earn_pilkha_ksheer_call_actions WHERE tid = %s;",(tid,))
		db_response_1=self.c.fetchall()
		number=db_response_1[0][0]
		recharge_given="%yes%"
		db_response_1=self.c.execute("SELECT * FROM learn2earn_pilkha_ksheer_call_actions WHERE phoneNumber = %s AND recharge_given LIKE %s;",(number,recharge_given))
		db_response_1=self.c.fetchall()
		if len(db_response_1) > 0 and number != "08527837805" and number != "09717078576" and number != "09930310610":
			return '6'

		if len(shuffler)==0:
			q=db_response[0]
			if q[0]=='1' and q[1]=='1' and q[2]=='2':
				return '4'
			else:
				return '5'

		else:
			random.shuffle(shuffler,random.random)
			return shuffler[0]

	def l2eUpdateQuestionResponse(self,tid,question,response):
		pingAndReconnect(self)
		column="response_"+question
		query="""UPDATE learn2earn_pilkha_ksheer_call_actions SET %s = %%s WHERE tid = %%s;"""
		query = query % (column,)
		self.c.execute(query,(response,tid))
		self.conn.commit()

	def insertLearn2EarnOpCodeData(self,tid,op_code):
		pingAndReconnect(self)
		self.c.execute("UPDATE learn2earn_pilkha_ksheer_call_actions SET oth_data_1 = %s WHERE tid = %s;",(op_code,tid) )
		self.conn.commit()

	def insertL2eReferralData(self,tid,dnis,referred_number,datetime,channel):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT * FROM l2e_referral_data WHERE phone_number = %s;",(referred_number,) )
		if db_response>0:
			return True
		else:
			self.c.execute("INSERT INTO l2e_referral_data (tid,phone_number,referred_by,datetime,oth_data_1) VALUES (%s,%s,%s,%s,%s);",(tid,referred_number,dnis,datetime,channel))
			self.conn.commit()

#****************************************************************************



#****************************************************************************
	#CGSwara Definitions
	def insertCGSwaraRecordNumberData(self,phoneNumber,ref_id,is_synced,datetime):
		pingAndReconnect(self)
		self.c.execute("INSERT INTO CGSwara_IMI_call_log (phoneNumber,ref_id,is_synced,datetime_of_api_call) VALUES (%s,%s,%s,%s);",(phoneNumber,ref_id,is_synced,datetime) )
		self.conn.commit()


#****************************************************************************



#****************************************************************************
	#Mobile Satyagraha app CHAT definitions
	def insertChatData(self,problem_id,sender,message,datetime):
		pingAndReconnect(self)
		id=""+problem_id+":"+sender
		self.c.execute("INSERT INTO app_chat (problem_id,sender,message,datetime) VALUES (%s,%s,%s,%s);",(problem_id,sender,message,datetime) )
		self.conn.commit()

	def loadChat(self,problem_id):
		pingAndReconnect(self)
		db_response=self.c.execute(
			"SELECT * FROM app_chat WHERE problem_id = %s ORDER BY datetime ASC",(problem_id,))
		db_response=self.c.fetchall()
		db_parse=[{"id": str(x[0]),
					"problem_id": x[1],
					"sender": x[2],
					"message": x[3],
					"datetime": str(x[4])} for x in db_response]
		return json.dumps(db_parse)
#****************************************************************************



#****************************************************************************
	#yatra definitions
	def yatraDataExists(self,sender_number,receiver_number):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT * FROM yatra_data_2 WHERE sender_number = %s AND receiver_number = %s;",(sender_number,receiver_number) )
		return db_response>0

	def yatraAnsweredDataExists(self,receiver_number):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT phoneNumber FROM learn2earn_pilkha_ksheer_call_actions WHERE phoneNumber = %s and response_consent > %s;",(receiver_number,"") )
		return db_response>0

	def insertYatraData(self,sender_number,receiver_number,sender_name,receiver_name,datetime,datetimeServer):
		pingAndReconnect(self)
		self.c.execute("INSERT INTO yatra_data_2 (sender_number,receiver_number,sender_name,receiver_name,datetime,datetimeServer) VALUES (%s,%s,%s,%s,%s,%s);",(sender_number,receiver_number,sender_name,receiver_name,datetime,datetimeServer) )
		self.conn.commit()

	def getYatraStat(self):
		pingAndReconnect(self)
		db_response_1=self.c.execute("SELECT count(*) FROM yatra_data_2;")
		db_response_1=self.c.fetchall()
		db_parse_2=[{"Total People Trained:":x[0]} for x in db_response_1]
		db_response=self.c.execute("SELECT sender_number, max(sender_name), count(*) FROM flaskdb.yatra_data_2 group by sender_number order by (3) desc;")
		db_response=self.c.fetchall()
		db_parse=[{str(x[0]): "Name: "+x[1]+". People Trained: "+str(x[2])} for x in db_response]
		db_parse_2.append(db_parse)
		return json.dumps(db_parse_2, indent=4)

	def getYatraSiteData(self):
		pingAndReconnect(self)
		db_response_1=self.c.execute("SELECT * FROM flaskdb.temp10;")
		db_response_1=self.c.fetchall()
		db_parse=[{str(x[1]):[str(x[0]).decode("utf-8"),str(x[2]),str(x[3]),str(x[4])]} for x in db_response_1]
		return db_parse

	def getYatraSitePersonnelData(self, number):
		pingAndReconnect(self)
		db_response_1=self.c.execute("SELECT receiver_number,receiver_name,user,phone_number FROM flaskdb.temp7 WHERE sender_number = %s order by user DESC,phone_number DESC,receiver_number DESC;",(number,))
		db_response_1=self.c.fetchall()
		db_parse=[{str(x[0]):[str(x[1]).decode("utf-8"),str(x[2]),str(x[3])]} for x in db_response_1]
		return db_parse
#****************************************************************************



#****************************************************************************
	#exotel definition for ICTD
	def insertExotelData(self,caller_id,recharge_status,datetime):
		pingAndReconnect(self)
		self.c.execute("INSERT INTO exotel_data (caller_id,recharge_status,datetime) VALUES (%s,%s,%s);",(caller_id,recharge_status,datetime) )
		self.conn.commit()
#****************************************************************************



#****************************************************************************
	#swara app definitions
	def insertSwaraToken(self, senderBTMAC, receiverBTMAC, filename, appName, phoneNumber, carrierCode, datetime):
		pingAndReconnect(self)
		self.c.execute("INSERT INTO bultoo_transfer (senderBTMAC, receiverBTMAC, filename, appName, phoneNumber, carrierCode, datetime) VALUES (%s,%s,%s,%s,%s,%s,%s);",(senderBTMAC, receiverBTMAC, filename, appName, phoneNumber, carrierCode, datetime) )
		self.conn.commit()

	def getswarastat(self):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT count(*) FROM bultoo_transfer;")
		db_response=int(self.c.fetchall()[0][0])-15
		d={}
		d["Total Stories Shared"]=db_response
		blank=""
		db_response=self.c.execute("SELECT phoneNumber, count(*) FROM bultoo_transfer WHERE phoneNumber != %s and phoneNumber != \"a\" and phoneNumber != \"9717078576\" GROUP BY phoneNumber ORDER BY (2) DESC;",(blank,))
		db_response=self.c.fetchall()
		db_parse=[{str(x[0]):str(x[1])} for x in db_response]
		db_response=self.c.execute("SELECT SUBSTRING(datetime,1,8), count(*) FROM bultoo_transfer WHERE phoneNumber != %s and phoneNumber != \"a\" and phoneNumber != \"9717078576\" GROUP BY (1) ORDER BY (1) DESC;",(blank,))
		db_response=self.c.fetchall()
		db_parse2=[{str(x[0]):str(x[1])} for x in db_response]
		db_parse.extend(db_parse2)
		db_parse.append(d)
		return json.dumps(db_parse,indent=4)

	def insertSwaraRechargeData(self,phone_number,amount,status,datetime,wallet_amount_pre_try,wallet_amount_post_try,carrier_code,id):
		pingAndReconnect(self)
		self.c.execute("INSERT INTO swara_recharges (phone_number,amount,status,datetime,wallet_amount_pre_try,wallet_amount_post_try,carrier_code,rf1) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);",(phone_number,amount,status,datetime,wallet_amount_pre_try,wallet_amount_post_try,carrier_code,id))
		self.conn.commit()
		return str(wallet_amount_post_try)
#****************************************************************************



#****************************************************************************
	#Mobile Satyagraha definitions
	def insertUser(self,username,password_hash,name,email):
		pingAndReconnect(self)
		self.c.execute("INSERT INTO app_credentials (username, password_hash, name, email) VALUES (%s,%s,%s,%s);",(username,password_hash,name,email))
		self.conn.commit()

	def fetchAll(self):
		pingAndReconnect(self)
		db_response=self.c.execute(
			"SELECT id, message_input, user, user, status, tags, posted, title, audio_length FROM app_problem_list_backup_2 WHERE status = 3 AND tags LIKE \'%PROBLEM%\' ORDER BY posted DESC LIMIT 3;")
		db_response=self.c.fetchall()
		db_parse=[{"problem_id": x[0],
					"problem_text": x[1],
					"phone_number_r": x[2],
					"phone_number_o": x[3],
					"status": x[4],
					"comments": x[5],
					"datetime": str(x[6].strftime("%d %B")),
					"problem_desc": x[7],
					"duration": x[8]} for x in db_response]
		return json.dumps(db_parse)

	def fetchBlockSwaraBultoo(self,keyword,s,e):
		pingAndReconnect(self)
		keyword="%"+keyword+"%"
		z='{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
		print z
		y='{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()-datetime.timedelta(days=14))
		print y
		db_response=self.c.execute(
			"SELECT id, message_input, user, audio_file, status, tags, posted, title, audio_length FROM app_problem_list_backup_2 WHERE title like %s and posted >= %s and status = 3 ORDER BY posted DESC;"
			,(keyword,y))
		db_response=self.c.fetchall()
		db_parse=[{"problem_id": x[0],
					"problem_text": x[1],
					"phone_number_r": x[2],
					"audio_file": x[3],
					"status": x[4],
					"comments": x[5],
					"datetime": x[6].strftime("%d %B"),
					"problem_desc": x[7],
					"duration": x[8]} for x in db_response]
		return json.dumps(db_parse)

	def fetchBlockSwaraBultoo2(self,number,s,e):
		pingAndReconnect(self)
		number="%"+number+"%"
		db_response=self.c.execute(
			"SELECT id, message_input, user, audio_file, status, tags, posted, title, audio_length FROM app_problem_list_backup_2 WHERE user like %s and status = 3 ORDER BY posted DESC LIMIT %s, %s;"
			,(number,s,e))
		db_response=self.c.fetchall()
		db_parse=[{"problem_id": x[0],
					"problem_text": x[1],
					"phone_number_r": x[2],
					"audio_file": x[3],
					"status": x[4],
					"comments": x[5],
					"datetime": x[6].strftime("%d %B"),
					"problem_desc": x[7],
					"duration": x[8]} for x in db_response]
		return json.dumps(db_parse)
# Song story is for entertainment no timpact, news = situational awareness non-impact, culture= non impact, bultoo= radio program non imapct, problem= grieveance impact based, Issues for impact : coal mining, education,.... , nrega all cover impact. updated to loudblog
	def fetchBlock(self,s,e):
		pingAndReconnect(self)
		blank=""
		song="%SONG%"
		news="%NEWS%"
		culture="%CULTURE%"
		bultoo="%BULTOO%"
		problem="%PROBLEM%"
		coal="%COAL%"
		mining="%MINING%"
		education="%EDUCATION%"
		food="%FOOD%"
		forest="%FOREST%"
		land="%LAND%"
		electricity="%ELECTRICITY%"
		water="%WATER%"
		handpump="%HANDPUMP%"
		nrega="%NREGA%"
		db_response=self.c.execute(
			"SELECT id, message_input, user, user, status, tags, posted, title, audio_length FROM app_problem_list_backup_2 WHERE tags not like %s and tags not like %s and tags not like %s and tags not like %s and (tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s) and id not in (select problem_id from app_users_per_problem2 where user1 != %s and user2 != %s) ORDER BY posted DESC LIMIT %s, %s;"
			,(song,news,culture,bultoo,problem,coal,mining,education,food,forest,land,electricity,water,handpump,nrega,blank,blank,s,e))
		db_response=self.c.fetchall()
		db_parse=[{"problem_id": str(x[0]),
					"problem_text": x[1].decode("utf-8"),
					"phone_number_r": x[2],
					"phone_number_o": x[3],
					"status": str(x[4]),
					"comments": x[5],
					"datetime": str(x[6].strftime("%d %B")),
					"problem_desc": x[7].decode("utf-8"),
					"duration": x[8]} for x in db_response]
		return json.dumps(db_parse)

	def fetchQueryBlock(self,query,s,e):
		pingAndReconnect(self)
		query="%"+query.encode("utf-8")+"%"
		song="%SONG%"
		news="%NEWS%"
		culture="%CULTURE%"
		bultoo="%BULTOO%"
		problem="%PROBLEM%"
		coal="%COAL%"
		mining="%MINING%"
		education="%EDUCATION%"
		food="%FOOD%"
		forest="%FOREST%"
		land="%LAND%"
		electricity="%ELECTRICITY%"
		water="%WATER%"
		handpump="%HANDPUMP%"
		nrega="%NREGA%"
		db_response=self.c.execute(
			"SELECT id, message_input, user, user, status, tags, posted, title, audio_length FROM app_problem_list_backup_2 WHERE (message_input like %s or tags like %s or title like %s) and tags not like %s and tags not like %s and tags not like %s and tags not like %s and (tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s) ORDER BY posted DESC LIMIT %s, %s;"
			,(query,query,query,song,news,culture,bultoo,problem,coal,mining,education,food,forest,land,electricity,water,handpump,nrega,s,e))
		db_response=self.c.fetchall()
		db_parse=[{"problem_id": str(x[0]),
					"problem_text": x[1].decode("utf-8"),
					"phone_number_r": x[2],
					"phone_number_o": x[3],
					"status": str(x[4]),
					"comments": x[5],
					"datetime": str(x[6].strftime("%d %B")),
					"problem_desc": x[7].decode("utf-8"),
					"duration": x[8]} for x in db_response]
		return json.dumps(db_parse)

	def fetchProblemAgainstUser(self,username):
		pingAndReconnect(self)
		if str(username) == su: #Superuser
			db_response_2=self.c.execute(
				"SELECT id, message_input, user, user, status, tags, posted, title, audio_length FROM app_problem_list_backup_2 WHERE id in (SELECT problem_id FROM ms_su_problems);")
			db_response_2=self.c.fetchall()
			db_parse=[{"problem_id": str(x[0]),
						"problem_text": x[1].decode("utf-8"),
						"phone_number_r": x[2],
						"phone_number_o": x[3],
						"status": str(x[4]),
						"comments": x[5],
						"datetime": str(x[6].strftime("%d %B")),
						"problem_desc": x[7].decode("utf-8"),
						"duration": x[8]} for x in db_response_2]
			return json.dumps(db_parse)

		db_response_1=self.c.execute(
			"SELECT * FROM app_problems_per_user WHERE username = %s;",(username,))
		db_response_1=self.c.fetchall()
		if(len(db_response_1)>0):
			db_response=self.c.execute(
				"SELECT id, message_input, user, user, status, tags, posted, title, audio_length FROM app_problem_list_backup_2 WHERE id = %s OR id = %s;" ,(db_response_1[0][1],db_response_1[0][2]))
			db_response=self.c.fetchall()
			db_parse=[{"problem_id": str(x[0]),
						"problem_text": x[1].decode("utf-8"),
						"phone_number_r": x[2],
						"phone_number_o": x[3],
						"status": str(x[4]),
						"comments": x[5],
						"datetime": str(x[6].strftime("%d %B")),
						"problem_desc": x[7].decode("utf-8"),
						"duration": x[8]} for x in db_response]
			return json.dumps(db_parse)

	def fetchTest(self):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT message_input FROM app_problem_list_backup_2 WHERE status = 3 ORDER BY posted DESC LIMIT 3;")
		db_response=self.c.fetchall()
		db_parse=[[x[0].decode("utf-8")] for x in db_response]
		return db_parse

	def fetchOne(self, problem_id):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT id, message_input, user, user, status, tags, posted, title, audio_length FROM app_problem_list_backup_2 WHERE id = %s;",(problem_id,))
		db_response=self.c.fetchall()
		db_parse=[{"problem_id": str(x[0]),
					"problem_text": x[1].decode("utf-8"),
					"phone_number_r": x[2],
					"phone_number_o": x[3],
					"status": str(x[4]),
					"comments": x[5],
					"datetime": str(x[6].strftime("%d %B")),
					"problem_desc": x[7].decode("utf-8"),
					"duration": x[8]} for x in db_response][0]

		return json.dumps(db_parse)

	def registerComment(self,username,problem_id,comment):
		pingAndReconnect(self)
		z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
		self.c.execute("INSERT INTO app_comments (username, problem_id, comments, datetime) VALUES (%s,%s,%s,%s);",(username,problem_id,comment.encode("utf-8"),z))
		self.conn.commit()
		return "Done"

	def fetchComments(self,problem_id):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT * FROM app_comments WHERE problem_id = %s ORDER BY datetime DESC;",(problem_id,))
		db_response=self.c.fetchall()
		db_parse=[{"username": str(x[0]),
					"problem_id": str(x[1]),
					"comments": str(x[2]),
					"datetime": str(x[3])} for x in db_response]
		return json.dumps(db_parse)

	def userExists(self,username):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT DISTINCT username FROM app_credentials WHERE username = %s ;",(username,))
		return db_response>0

	def authenticateUser(self,username,password_hash):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT DISTINCT name FROM app_credentials WHERE username = %s and password_hash = %s;",(username,password_hash))
		db_response=self.c.fetchall()
		if len(db_response)>0:
			return db_response[0][0]
		else:
			return "incorrect password"

	def canAdoptProblem(self,username):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT * FROM app_problems_per_user WHERE username = %s;",(username,))
		db_response=self.c.fetchall()
		if(len(db_response)==0 or str(username) == su):#Superuser
			return "Yes"
		elif db_response[0][1] is '':
			return "Yes"
		elif db_response[0][2] is '':
			return "Yes"
		else:
			return "No"

	def userCount(self,problem_id):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT * FROM app_users_per_problem2 WHERE problem_id = %s;",(problem_id,))
		db_response=self.c.fetchall()
		if(len(db_response)==0):
			return 0
		elif db_response[0][1] is not '' and db_response[0][2] is not '':
			return 2
		elif db_response[0][1] is '' and db_response[0][2] is '':
			return 0
		else:
			return 1

	def adoptProblem(self,username,problem_id):
		pingAndReconnect(self)
		if str(username) == su: #Superuser
			self.c.execute("INSERT INTO ms_su_problems (problem_id) VALUES (%s);",(problem_id,))
			self.conn.commit()
			response="Adopted"
			return response

		db_response=self.c.execute("SELECT * FROM app_users_per_problem2 WHERE problem_id = %s;",(problem_id,))
		db_response=self.c.fetchall()
		if(len(db_response)==0):
			self.c.execute("INSERT INTO app_users_per_problem2 (problem_id, user1, user2) VALUES (%s,%s,%s);",(problem_id,username,''))
			self.conn.commit()
			response="Adopted"
		elif db_response[0][1] is '' and  db_response[0][2] is '':
			self.c.execute("UPDATE app_users_per_problem2 SET user1 = %s WHERE (problem_id = %s);",(username,problem_id))
			self.conn.commit()
			response= "Adopted"
		#elif db_response[0][2] is '':
		#	self.c.execute("UPDATE app_users_per_problem2 SET user2 = %s WHERE (problem_id = %s);",(username,problem_id))
		#	self.conn.commit()
		#	response= "Adopted"
		else:
			response= "Users Full"
		if response != "Users Full":
			database_flaskr.registerProblemAgainstUser(self,username,problem_id)
		return response

	def registerProblemAgainstUser(self,username,problem_id):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT * FROM app_problems_per_user WHERE username = %s;",(username,))
		db_response=self.c.fetchall()
		if(len(db_response)==0):
			self.c.execute("INSERT INTO app_problems_per_user (username, problem1, problem2) VALUES (%s,%s,%s);",(username,problem_id,''))
			self.conn.commit()
		elif db_response[0][1] is '':
			self.c.execute("UPDATE app_problems_per_user SET problem1 = %s WHERE (username = %s);",(problem_id,username))
			self.conn.commit()
		elif db_response[0][2] is '':
			self.c.execute("UPDATE app_problems_per_user SET problem2 = %s WHERE (username = %s);",(problem_id,username))
			self.conn.commit()

	def unAdoptProblem(self,username,problem_id):
		pingAndReconnect(self)
		if str(username) == su: #Superuser
			self.c.execute("DELETE from ms_su_problems WHERE (problem_id = %s);",(problem_id,))
			self.conn.commit()
			response= "UnAdopted"
			return response

		db_response=self.c.execute("SELECT * FROM app_users_per_problem2 WHERE problem_id = %s;",(problem_id,))
		db_response=self.c.fetchall()
		if db_response[0][1]==username:
			self.c.execute("UPDATE app_users_per_problem2 SET user1 = %s WHERE (problem_id = %s);",('',problem_id))
			self.conn.commit()
			response= "UnAdopted"
		elif db_response[0][2]==username:
			self.c.execute("UPDATE app_users_per_problem2 SET user2 = %s WHERE (problem_id = %s);",('',problem_id))
			self.conn.commit()
			response= "UnAdopted"
		else:
			response= "Was it really your problem?"
		if response != "Was it really your problem?":
			database_flaskr.deRegisterProblemAgainstUser(self,username,problem_id)
		return response

	def deRegisterProblemAgainstUser(self,username,problem_id):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT * FROM app_problems_per_user WHERE username = %s;",(username,))
		db_response=self.c.fetchall()
		if db_response[0][1]==problem_id:
			self.c.execute("UPDATE app_problems_per_user SET problem1 = %s WHERE (username = %s);",('',username))
			self.conn.commit()
		elif db_response[0][2]==problem_id:
			self.c.execute("UPDATE app_problems_per_user SET problem2 = %s WHERE (username = %s);",('',username))
			self.conn.commit()
#****************************************************************************
