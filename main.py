from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
import sqlalchemy as sa
from urllib.parse import quote_plus
import matplotlib.pyplot as plt
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import pyodbc
import pandas as pd
import pickle
import os

SCOPES = ['SCOPES']

class BackEnd():
    
    def sql_to_csv(self):
        self.server = self.server_entry.get() # type: ignore
        self.database = self.database_entry.get() # type: ignore
        self.driver = self.driver_entry.get() # type: ignore
        self.usuario = self.usuario_entry.get() # type: ignore
        self.senha = self.senha_entry.get() # type: ignore
        try:
            #if Python pyodbc connect to Sql Server using SQL Server Authentication ⬇
            #self.engine_stmt =('mssql+pyodbc://%s:%s@%s/%s?driver=%s" % (self.usuario,self.senha,self.server, self.database, self.driver))
            self.engine_stmt = ("mssql+pyodbc://%s/%s?driver=%s" % (self.server, self.database, self.driver))
            self.engine = create_engine(self.engine_stmt)
            with self.engine.begin() as conn:
                print("1")
                data = pd.read_sql_query(sa.text("SELECT * FROM Production.Product"), conn)
                data.to_csv(r'CSV.csv', index = False, )
                self.engine.dispose()
            self.upload_files()
        except:
            messagebox.showerror(title="Title", message="Error")
    def get_gdrive_service(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        try:
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'client_secret.json', SCOPES)
                    creds = flow.run_local_server(port=8080)
                # Save the credentials for the next run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
            # return Google Drive API service
            
        except:
            messagebox.showerror(title="Title", message="Error")
        return build('drive', 'v3', credentials=creds, static_discovery=False)

    def upload_files(self):
        service = self.get_gdrive_service()
        folder_id = 'Your Folder Id'
        file_names = ['file.csv']
        mime_types = ['text/csv']
        try:    
            for file_name, mime_type in zip(file_names, mime_types):
                file_metadata = {
                    'name': file_name,
                    'parents': [folder_id]
                }
                media = MediaFileUpload(filename=file_name, mimetype=mime_type, resumable=True)
                request =service.files().update(
                    fileId="Your File Id",
                    media_body=media   
                )
        except:
            messagebox.showerror(title="Title", message="Error")



class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        self.pagina()
        self.pagina_widgets()
        self.get_gdrive_service()

    def pagina(self):
        self.geometry("400x380")
        self.title("Title")
        self.resizable(False, False)
        self.iconbitmap("icon.ico")
        self._set_appearance_mode("dark")
    def pagina_widgets(self):
        #self.get_gdrive_service()
        #Frame
        self.frame = ctk.CTkFrame(self, width=380, height=360, fg_color="gray18", bg_color="gray18")
        self.frame.place(x=10,y=10)
        #Image
        img = ctk.CTkImage(Image.open("image.png"), size=(100, 100))
        self.lb_img = ctk.CTkLabel(self.frame, text="", image=img)
        self.lb_img.place(x=135, y=0)
        #Entry
        self.driver_entry = ctk.CTkEntry(self.frame, width=200, placeholder_text="Drive", text_color="white",
                                                 font=("Roboto", 12), corner_radius=15, fg_color="black", border_color="black")
        self.driver_entry.place(x=90, y=90)
        self.server_entry = ctk.CTkEntry(self.frame, width=200, placeholder_text="Server", text_color="white",
                                                 font=("Roboto", 12), corner_radius=15, fg_color="black", border_color="black")
        self.server_entry.place(x=90, y=130)
        self.database_entry = ctk.CTkEntry(self.frame, width=200, placeholder_text="Database", text_color="white",
                                                 font=("Roboto", 12), corner_radius=15, fg_color="black", border_color="black")
        self.database_entry.place(x=90, y=170)
        self.usuario_entry = ctk.CTkEntry(self.frame, width=200, placeholder_text="User", text_color="white",
                                                 font=("Roboto", 12), corner_radius=15, fg_color="black", border_color="black")
        self.usuario_entry.place(x=90, y=210)
        self.senha_entry = ctk.CTkEntry(self.frame, width=200, placeholder_text="Password",text_color="white", show="*",
                                                 font=("Roboto", 12), corner_radius=15, fg_color="black", border_color="black")
        self.senha_entry.place(x=90, y=250)
        #Button
        self.btn_cadastro = ctk.CTkButton(self.frame, width=100, fg_color="Dodger blue", hover_color="sky blue", text="Connect".upper(),
                                       font=("Roboto", 12), text_color="snow",
                                       corner_radius=15, command=self.sql_to_csv)
        self.btn_cadastro.place(x=135, y=305)
        
        
if __name__=="__main__":
    app = App()
    app.mainloop()