import configparser
import os
from datetime import datetime

class Config:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance=super(Config, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.file='config.ini'
        self.c=configparser.ConfigParser()
        self.c.read(self.file)
        print(f"Configuration File: {os.path.abspath(self.file)}")
        self.init_vars()
        if not os.path.exists(self.file):
            self.create()
        
    def init_vars(self):
        self.sections=["Test", "Test 2", "Dataset"]
        self.Test_Var: dict={"Name":"Bob", "Age":"12"}
        self.Dataset_Var: dict={"LastUpdated":f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}
        

    def create(self):
        for section in self.sections:
            self.c[f"{section}"]={}
            if hasattr(self, f"{section}_Var"):
                obj_dict=getattr(self, f"{section}_Var")
                for attribute, value in obj_dict.items():
                    self.c[section][attribute]= value
            with open(self.file, 'w') as f:
                self.c.write(f)

    def set(self, section, attribute, value):
        if section not in self.sections:
            raise ValueError("Unrecognized Section")
        self.c[section][attribute]=value
        with open(self.file, 'w') as f:
            self.c.write(f)
            
    def get(self, section, attribute):
        if section not in self.sections:
            raise ValueError("Unrecognized Section")
        if attribute not in self.c[section]:
            raise ValueError("Unrecognized Attribute")
        return self.c[section][attribute]
        

    def dump(self):
        f=open(self.file, 'r')
        contents=f.read()
        print(contents)

if __name__ == "__main__":
    test=Config()
    test.dump()
    
