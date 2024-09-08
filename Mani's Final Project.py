import tkinter,sqlite3
from tkinter import ttk,messagebox

class PersonAuthenticator(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title("Mani's Final Project")
    def authenticator(self):
        self.errors=[]
        self.error_counter=1
        for i in range(15):
            #ID
            if i==0:
                try:
                    self.id=int(self.elements_list[i][1].get())
                except:
                    self.errors.append(f"{self.error_counter}.ID: You Must Enter Number.")
                    self.error_counter+=1
                else:
                    self.id=self.elements_list[i][1].get()
                    if len(self.id)==10:
                        pass
                    else:
                        self.errors.append(f"{self.error_counter}.ID: You Must Enter 10 Characters.")
                        self.error_counter+=1
            #First Name
            elif i==1:
                self.first_name_list=(self.elements_list[i][1].get()).split()
                self.first_name="".join(self.first_name_list)
                if self.first_name.isalpha():
                    if len(self.first_name)>3:
                        pass
                    else:
                        self.errors.append(f"{self.error_counter}.First Name: You Should Enter More Than 3 Letters.")
                        self.error_counter+=1
                else:
                    self.errors.append(f"{self.error_counter}.First Name: You Should Enter Alphabet Letters.")
                    self.error_counter+=1
            #Last Name
            elif i==2:
                self.last_name_list=(self.elements_list[i][1].get()).split()
                self.last_name="".join(self.last_name_list)
                if self.last_name.isalpha():
                    if len(self.last_name)>3:
                        pass
                    else:
                        self.errors.append(f"{self.error_counter}.Last Name: You Should Enter More Than 3 Letters.")
                        self.error_counter+=1
                else:
                    self.errors.append(f"{self.error_counter}.Last Name: You Should Only Enter Alphabet Letters.")
                    self.error_counter+=1
            #Age
            if i==3:
                try:
                    self.age=int(self.elements_list[i][1].get())
                except:
                    self.errors.append(f"{self.error_counter}.Age: You Must Enter Integer Number.")
                    self.error_counter+=1
                else:
                    if 1<self.age<120:
                        pass
                    else:
                        self.errors.append(f"{self.error_counter}.Age: Enter a Valid Number.")
                        self.error_counter+=1
            #Height
            if i==4:
                try:
                    self.height=float(self.elements_list[i][1].get())
                except:
                    self.errors.append(f"{self.error_counter}.Height: You Must Enter a Number.")
                    self.error_counter+=1
                else:
                    if 0.4<=self.height<=2.5:
                        pass
                    else:
                        self.errors.append(f"{self.error_counter}.Height: Enter a Valid Number.")
                        self.error_counter+=1
            #Weight
            if i==5:
                try:
                    self.weight=float(self.elements_list[i][1].get())
                except:
                    self.errors.append(f"{self.error_counter}.Weight: You Must Enter a Number.")
                    self.error_counter+=1
                else:
                    if 1.0<=self.weight<=250.0:
                        pass
                    else:
                        self.errors.append(f"{self.error_counter}.Weight: Enter a Valid Number.")
                        self.error_counter+=1
            #BMI
            if i==6:
                try:    
                    self.elements_list[i][1].config(state="normal")
                    self.elements_list[6][1].delete(0,tkinter.END)
                    self.elements_list[i][1].insert(0,f"{"{:.2f}".format(self.weight/self.height)}")
                    self.elements_list[i][1].config(state="readonly")
                except:
                    pass
            #phone number
            if i==12 and self.phone_input==True:
                try:
                    self.phn=int(self.elements_list[i][1].get())
                except:
                        self.errors.append(f"{self.error_counter}.Phone number: You Must Enter A Number.")
                        self.error_counter+=1
                else:
                    self.phn=self.elements_list[i][1].get()
                    if len(self.phn)==11:
                        pass
                    else:
                        self.errors.append(f"{self.error_counter}.Phone number: You Must Enter 11 Characters.")
                        self.error_counter+=1
                    if self.phn[0]=="0":
                        pass
                    else:
                        self.errors.append(f"{self.error_counter}.Phone number: It Should Start With '0'.")
                        self.error_counter+=1
            #mobile number
            if i==13 and self.mobile_input==True:
                try:
                    self.mn=int(self.elements_list[i][1].get())
                except:
                        self.errors.append(f"{self.error_counter}.Mobile number: You Must Enter A Number.")
                        self.error_counter+=1
                else:
                    self.mn=self.elements_list[i][1].get()
                    if len(self.mn)==11:
                        pass
                    else:
                        self.errors.append(f"{self.error_counter}.Mobile number: You Must Enter 11 Characters.")
                        self.error_counter+=1
                    if self.mn[0]=="0":
                        pass
                    else:
                        self.errors.append(f"{self.error_counter}.Mobile number: It Should Start With '0'.")
                        self.error_counter+=1
            if i==14 and self.email_input==True:
                self.email=self.elements_list[i][1].get()
                if self.email.count("@")==1 and self.email.count(".")==1:
                    import string
                    symbols=list(string.punctuation)
                    symbols.remove("@")
                    symbols.remove(".")
                    i=0
                    valid=True
                    while i<len(symbols) and valid:
                        if symbols[i] in self.email:
                            valid=False
                            self.errors.append(f"{self.error_counter}.Email Address: It's Not Valid.")
                            self.error_counter+=1
                        i+=1
                else:
                    self.errors.append(f"{self.error_counter}.Email Address: It's Not Valid.")
                    self.error_counter+=1
                        
        if len(self.errors)==0:
            messagebox.showinfo("Authentication","Authentication Successful")
            self.elements_list[-1][1].config(state="normal")
        else:
            self.errors_message="\n".join(self.errors)
            messagebox.showinfo("Authentication Errors",self.errors_message)
            self.elements_list[-1][1].config(state="disabled")

    def update_connections_entry_state(self):
        if self.connection_var_list[0].get()==1:
            self.elements_list[12][1].config(state="normal")
            self.phone_input=True
        else:
            self.elements_list[12][1].config(state="disabled")
            self.phone_input=False
        if self.connection_var_list[1].get()==1:
            self.elements_list[13][1].config(state="normal")
            self.mobile_input=True
        else:
            self.elements_list[13][1].config(state="disabled")
            self.mobile_input=False
        if self.connection_var_list[2].get()==1:
            self.elements_list[14][1].config(state="normal")
            self.email_input=True
        else:
            self.elements_list[14][1].config(state="disabled")
            self.email_input=False

    def update_towns(self, *args):
        selected_city = self.elements_list[9][1].get()  # Get the selected city
        towns = self.city_town_dict.get(selected_city, [])  # Get towns for the selected city
        self.elements_list[10][1].config(values=towns)  # Update the town ComboBox values

    def get_selected_radio_button_text(self):
        self.selected_value=self.gender_var.get()
        radio_button={
            "male":0,
            "female":1,
            "other":2
        }
        for i in range (3):
            for text, value in radio_button.items():
                if value == self.selected_value:
                    return text

    def save(self):
        import sqlite3
        my_connector=sqlite3.connect("AuthenticationDataBase.db")
        my_cursor=my_connector.cursor()
        my_cursor.execute("CREATE TABLE IF NOT EXISTS Informations(ID TEXT, First_Name TEXT, Last_Name TEXT, Age INTEGER, Height REAL, Weight REAL, BMI REAL, Gender TEXT, Soldier_State TEXT, City TEXT, Town TEXT, Phone_Number TEXT, Mobile_Number TEXT, Email_Address TEXT)")
        my_cursor.execute(f"INSERT INTO Informations VALUES('{self.id}','{self.first_name}','{self.last_name}','{self.age}','{self.height}','{self.weight}','{self.elements_list[6][1].get()}','{self.get_selected_radio_button_text()}','{self.elements_list[8][1].get()}','{self.elements_list[9][1].get()}','{self.elements_list[10][1].get()}','{self.elements_list[12][1].get()}','{self.elements_list[13][1].get()}','{self.elements_list[14][1].get()}')")
        for i in range(15):
            if i==7 or i==11:
                pass
            else:
                if i==6:
                    self.elements_list[i][1].config(state="normal")
                self.elements_list[i][1].delete(0,tkinter.END)
                if i==6:
                    self.elements_list[i][1].config(state="disabled")
        
        self.elements_list[-1][1].config(state="disabled")
        my_connector.commit()
        my_connector.close()

    def clear(self):
        for i in range(15):
            if i==7 or i==11:
                pass
            else:
                if i==6:
                    self.elements_list[i][1].config(state="normal")
                self.elements_list[i][1].delete(0,tkinter.END)
                if i==6:
                    self.elements_list[i][1].config(state="disabled")


    def create(self):
        self.text_matrix=[["ID:","First Name:","Last Name:","Age:","Height:","Weight:","BMI:","Gender:","Soldier Status:","City:","Town:","Connections:","Phone Number:",
                           "Mobile Number:","Email Address:","Authenticate"],["Male","Female","Other"],["Phone","Mobile","Email"],["Authenticate","Save","Clear"]]
        self.elements_list=[[None for i in range(4)] for j in range(16)]
        #Labels
        for i in range(len(self.text_matrix[0])-1):
            self.elements_list[i][0]=tkinter.Label(self,text=self.text_matrix[0][i],font=("Calibri",20))
        #Buttons
        for i in range(3):    
            self.elements_list[-1][i]=tkinter.Button(self,text=self.text_matrix[3][i],font=("Calibri",20),command=self.authenticator)
            if i==1:
                self.elements_list[-1][i].config(state="disabled",command=self.save)
            if i==2:
                self.elements_list[-1][i].config(command=self.clear)
        #Entries
        for i in range(15):
            self.elements_list[i][1]=tkinter.Entry(self,font=("Calibri",20,"bold"))
            if i==6:
                self.elements_list[i][1].config(state="disabled")
            if i>=12:
                self.elements_list[i][1].config(state="disabled")
        #Drop Downs
        self.checkbuttons_matrix= [["پایان خدمت","کفالت","معافیت موقت","دانش آموز کلاس دوازدهم"],["Tehran","Alborz","Markazi"]]
        for i in range(2):
            self.elements_list[8+i][1]=ttk.Combobox(self,values=self.checkbuttons_matrix[i],font=("Calibri",12))
            if i==0:
                self.elements_list[8][1].config(state="disabled")
        self.city_town_dict = {
            "Tehran": ["Tehran", "Qods", "Shariyar","Eslamshahr","Malard"],
            "Alborz": ["karaj", "Savojbolagh", "NazarAbad","Taleghan"],
            "Markazi": ["Arak", "Delijan", "Mahalat","Saveh","Tafresh"]
        }
        # City ComboBox
        self.elements_list[9][1] = ttk.Combobox(self, values=list(self.city_town_dict.keys()), font=("Calibri", 12))
        self.elements_list[9][1].bind("<<ComboboxSelected>>", self.update_towns)
        # Town ComboBox
        self.elements_list[10][1] = ttk.Combobox(self, font=("Calibri", 12))

        #Radio Buttons
        self.gender_var=tkinter.IntVar()
        self.gender_var.set(2)
        self.gender_var.trace_add('write',lambda *args: self.elements_list[8][1].config(state="disabled") if self.gender_var.get()!=0 else self.elements_list[8][1].config(state="normal"))
        for i in range (3):
            self.elements_list[7][1+i]=tkinter.Radiobutton(self, text=self.text_matrix[1][i], variable=self.gender_var, value=i)
        self.phone_input=False
        self.mobile_input=False
        self.email_input=False
        #Check Buttons
        self.connection_var_list=[]
        for i in range(3):
            self.connection_var_list.append(tkinter.IntVar())
            self.elements_list[11][i+1]=tkinter.Checkbutton(self,text=self.text_matrix[2][i],variable=self.connection_var_list[i],offvalue=0,onvalue=1,
                                                            command=self.update_connections_entry_state)
    def locate(self):
        #Labels
        for i in range(len(self.text_matrix[0])-1):
            self.elements_list[i][0].grid(row=i,column=0,sticky="w")
        #Buttons
        for i in range(3):
            self.elements_list[-1][i].grid(row=16,column=i,sticky="nsew")
        #Entries
        for i in range(15):
            if 6<i<12:
                pass
            else:
                self.elements_list[i][1].grid(row=i,column=1,columnspan=3)
        #Drop Downs
        for i in range(3):
            self.elements_list[8+i][1].grid(row=8+i,column=1,columnspan=3)
        # Radio Buttons
        for i in range(3):
            self.elements_list[7][1+i].grid(row=7, column=1+i, columnspan=3, sticky="w")
        #Check Buttons
        for i in range(3):
            self.elements_list[11][i+1].grid(row=11,column=i+1)

class SQLiteHandler(sqlite3.Connection):
    pass

class PersonAuthenticatorWithDatabase(PersonAuthenticator, SQLiteHandler):
    def __init__(self):
        PersonAuthenticator.__init__(self)
        SQLiteHandler.__init__(self)

sample=PersonAuthenticator()
sample.create()
sample.locate()
sample.mainloop()