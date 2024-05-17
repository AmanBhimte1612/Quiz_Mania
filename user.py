


import sqlite3

class User:
    log=False
    user=()
    def __init__(self):
        self.conn = sqlite3.connect('manager.db')
        print(User.user)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS USER (NAME TEXT, CONTACT TEXT, EMAIL TEXT, PASS TEXT, SCORE INT)")
        self.conn.commit()
        self.conn.close()
        # User.log = False
        

    def insert_user_data(self, name, contact, mail, password):
        """THIS FUNCTION WILL INSERT DATA INTO DATABASE"""
        try:
            print("insert")
            self.cursor.execute("INSERT INTO USER (NAME, CONTACT, EMAIL, PASS, SCORE) VALUES (?,?,?,?,?)", (name, contact, mail, password, 0))
            self.conn.commit()
            self.conn.close()
            return True
        except Exception as e:
            print("Something went wrong try again:", e)
            return False

    def check_password(self):
        """THIS FUNCTION WILL CHECK PASSWORD IF PASSWORD IS IS VALID OR NOT"""
        while True:
            pwd = input("Confirm your password: ")
            if self.validate_pass(pwd):
                return pwd
            else:
                print("Invalid password. Password must be between 8 to 20 characters and contain at least one uppercase letter, one lowercase letter, one digit, and one special character.")
                
                
    def check_email(self):
        """THIS FUNCTION WILL CHECK EMAIL IF ITS VALID OR NOT"""
        mail = input("Please enter a valid email address example 'example@gmail.com'")
        if "@gmail.com" in mail:
            return mail
        else:
            print("Invalid Email")
            # print("Please enter a valid email address example 'example@gmail.com'")
            self.check_email(self)
            
            
    def check_contact(self):
        """THIS FUNCTION WILL CHECK CONTACT IS VALID OR NOT"""
        contact = input("Please Enter a valid contact name example contact should have 10 digits")
        if contact.isdigit() and len(contact)==10:
            return contact
        else:
            print("Invalid Contact")
            self.check_contact()
            
            
            
    def check_enrollment(self):
        """THIS FUNCTION WILL CHECK IF ENROLLMENT NUMBER IS VALID OR NOT"""
        enro = input("Enter your Enrollment Number of atleast 5 le: ")
        if  len(enro)==5:
            self.cursor.execute("SELECT * FROM REGISTER WHERE ENROLL = ?", (enro,))
            en= self.cursor.fetchone()
            if en is not None:
                print(f"This enrollement number is already registered as Name '{en[0]}'")
                self.check_enrollment()
            else:
                return enro
        else:
            print("Invalid Enrollment")
            self.check_enrollment()
            
            
    def register(self,user):
        
        if self.insert_user_data(user[0],user[1],user[2],user[3]):
            return True
        else:
            return False

    def validate_pass(self, password):
        """"THIS FUNCTION WILL VALIDATE PASSWORD"""        
        l = u = d = s = 0
        if 8 <= len(password) <= 20:
            for i in password:
                if i.isupper():
                    u += 1
                elif i.islower():
                    l += 1
                elif i.isdigit():
                    d += 1
                else:
                    s += 1
            if l > 0 and d > 0 and u > 0 and s > 0:
                return True
        return False
    

    def login(self,email, password):
        
        self.cursor.execute("SELECT * FROM USER WHERE EMAIL = ?",(email,))
        user = self.cursor.fetchone()
        print("User",user)
        User.user = user
        # Check if user exists and compare passwords
        if user and user[3] == password:
            return True
        else:
            return False

    def check_savedpassword(self, password, user):
        if user[4] == password:
            print("Login Successful !!!")
            print(f"HELLO {user[0]}")
            User.log = True
            return True
        else:
            print("Wrong Password try again")
            return False

    def showprofile(self,user,log):
        print("#"*75)
        print("#"*75)
        print("#"*25,"WELCOME TO PROFILE PAGE","#"*25)
        print("#"*75)
        print("#"*75)
        if log is True:
            print(f"""
                Your Full Name:{user[0]}
                Enrollment No:{user[1]}
                Contact:{user[2]}
                Email:{user[3]}             
                """)
            choice=input("Do you want to update profile::Y/N:")
            if choice == 'Y' or choice =='y':
                self.updateprofile()

    def updateprofile(self):
        print("#"*75)
        print("#"*75)
        print("#"*25,"UPDATE PROFILE","#"*25)
        print("#"*75)
        print("#"*75)
        data_parameter=['NAME','CONTACT','MAIL','PASS']
        try:
            choice=int(input("""Enter Data You wanna update
                NAME:1
                ,CONTACT:2
                ,MAIL:3
                ,PASSWORD:4"""))
            DATA=input(f"Enter Your {data_parameter[choice-1]}:")
            try: 
                self.cursor.execute(f"UPDATE REGISTER SET {data_parameter[choice-1]} = '{DATA}' WHERE {data_parameter[choice-1]} = '{User.user[choice-1]}' ")
                self.conn.commit()
                self.cursor.execute("SELECT * FROM REGISTER WHERE ENROLL = %s", (User.user[1],))
                User.user = self.cursor.fetchone()
                print("Update Successfully")
                return User.user
            except Exception as e:
                print("Error updating profile",e)
        except:
            print("Error updating profile Please choose right Options")
        


if __name__ == "__main__":
    user = User()
    # user.login()
    user.register()