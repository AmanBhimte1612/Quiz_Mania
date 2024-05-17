import string
import sqlite3
import random
conn = sqlite3.connect('manager.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS QUESTIONBANK (QUESTION TEXT,OP1 TEXT,OP2 TEXT, OP3 TEXT,OP4 TEXT,ANS TEXT)")
conn.commit()

class Quiz():
  def __init__(self):
    pass
    
        
  def enter_question(self):
    choice=input("""How Do You Want to Enter Question,Enter:
            1:QuestionBankFile
            2:Manually One By One""")
    if int(choice)==1:
      path=input("Enter path of file")
      enter_question_by_file(path)
    else:
      
      enter_question_manually()

  def enter_question_by_file(self,path):
    print("this function is under construction")
    pass

  def enter_question_manually(self,):
    try:
      que=input("Enter Question : ")
      op1=input("Enter Option a : ")
      op2=input("Enter Option b : ")
      op3=input("Enter Option c : ")
      op4=input("Enter Option d : ")
      ans=input("Enter Answer  : ")
      cursor.execute(f"INSERT INTO QUESTIONBANK VALUES('{que}','{op1}','{op2}','{op3}','{op4}','{ans}')")
      
      conn.commit()
      choice=input("Question Successfully Inserted , Want to insert more :Y/N")
      if choice == "Y" or "y":
        enter_question_manually()
      else:
        pass
    except:
      print("Sorry Somthing went wrong Please reenter question")
      enter_question_manually()

  def fetch_questions_list(self,):
    Question_list=[]
    cursor.execute("SELECT * FROM QUESTIONBANK ORDER BY RANDOM() LIMIT 10")
    que_list=cursor.fetchall()
    conn.commit()
    conn.close()
    
    for t in que_list:
      ops = t[1:5]
      ops=list(ops)
      d={'que':t[0],'ops':ops,'ans':t[5]}
      Question_list.append(d)
      
    return Question_list

  def attempt(self,user):
    
    "#"*75
    "#"*75
    print("#"*25,"BEST OF LUCK FOR THE QUIZ","#"*25)
    "#"*75
    "#"*75
    Question_list=self.fetch_questions_list()
    # global Score
    Score=0
    print("Instruction:Enter Opstion only:a/b/c/d or Enter blank for Next")
    # print(Question_list)
    for ques in Question_list:
      ops=ques['Ops']
      # print(ops)
      # ops=random.shuffle(ops)
      # print(type(ops))
      Response=input(f"""{ques['Que']}

      a:{ops[0]}                 b:{ops[1]}
      
      c:{ops[2]}                 d:{ops[3]}
      
      Response:""")
      if Response =='a'or Response=='A':
        if ques['Ans']==ops[0]:
          Score+=1
          print("Answerr is ",ops[0])
      elif Response =='b' or Response=='B':
        if ques['Ans']==ops[1]:
          Score+=1
          print("Answerr is ",ops[1])

      elif Response =='c' or Response == 'C':
        if ques['Ans']==ops[2]:
          Score+=1
          print("Answerr is ",ops[2])

      elif Response =='d' or Response == 'D':
        if ques['Ans']==ops[3]:
          print("Answerr is ",ops[3])
          Score+=1
      elif Response=='':
        Score+=0
      else:
        print("Wrong input Please Enter Opstion only:a/b/c/d or Enter blank for Next")
        Score+=0
    print(f"Your Total Score is {Score}")
    
    cursor.execute(f"UPDATE REGISTER SET SCORE={Score} WHERE ENROLL={user[1]}")
    conn.commit()
    
  def show_score(self,user):
    cursor.execute(f"SELECT SCORE FROM REGISTER WHERE ENROLL={user[1]}")
    score=cursor.fetchone()
    conn.commit()
    print(f"Your Last Total Score is {score}")
    
    
if __name__=='__main__':
  main=Quiz()
  main.attempt(user)    

