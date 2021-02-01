from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob
from datetime import datetime
import random 
from pathlib import Path

Builder.load_file('env/design.kv')

class FrontScreen(Screen):
    def go_to_login(self):
        self.manager.current = "login_screen"

    def sign_up(self):
        self.manager.current = "sign_up_screen"      

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def forget_pass(self):
        self.manager.current = "forget_screen"    

    def login(self, uname, pword):    
        with open("users.json") as file:
            users = json.load(file)

        if uname in users and users[uname]['password'] == pword:
            self.manager.current = 'login_screen_success' 

        else:
            self.ids.login_wrong.text = "Wrong username or password"      

class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users:
            self.ids.wrong_uname.text = "Username exist , go to login page and then click forget password to set new password"
        else: 
            users[uname] = {'username': uname, 'password': pword, 'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

            with open("users.json", 'w') as file:
                json.dump(users, file)
            self.manager.current = "sign_up_screen_success"
    
    def login_page(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

class  SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "front_screen"

    def get_quote(self, feel):
        feel = feel.lower()
        available_feeling = glob.glob("env/quotes/*txt")
        
        available_feeling = [Path(filename).stem for filename in available_feeling] #[happy, sad, unloved]
        
        if feel in available_feeling:
            with open (f"env/quotes/{feel}.txt" , encoding="utf8") as file: 
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else :
            self.ids.quote.text = "try feelings among (Happy, Sad , Unloved and angry)"   

class ForgetScreen(Screen):

    def update_pass(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        
        if uname in users:
            users[uname]['password'] = pword
            with open("users.json", 'w') as file:
                json.dump(users, file)
            
            self.ids.login_wrong.text = "Updated , click login button"
             
        else:
            self.ids.login_wrong.text = "Username doesnt exist, visit sign-up page"

    def sign_up(self):
        self.manager.current = "sign_up_screen"
        self.manager.transition.direction = "right"

    def login_page(self):
        self.manager.current = "login_screen"        
      
class ImageButton(ButtonBehavior, HoverBehavior, Image ):
    pass 

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__=="__main__":
    MainApp().run()       