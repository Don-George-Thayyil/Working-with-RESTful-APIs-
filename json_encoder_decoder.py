import json

class Vehicle:
    def __init__(self, reg_no, year_of_prod, no_of_passngr, mass_of_vehicle):
        self.reg_no = reg_no
        self.year_of_prod = year_of_prod
        self.no_of_passngr = no_of_passngr
        self.mass_of_vehicle = mass_of_vehicle
class Encoder(json.JSONEncoder):
    def default(self, object):
        if isinstance(object, Vehicle):
            return object.__dict__
        else:
            return super().default(self,object)

def decoder(w):
    return Vehicle(w["reg_no"], w["year_of_prod"], w["no_of_passngr"], w["mass_of_vehicle"])

def run():
    print("What can I do for you ?")
    prompt = input("\t1.Encode JSON string.\n\t2.Decode a JSON string.\nChoose: ")
    try:
        if int(prompt) not in [1,2]:
            raise Exception ("Select 1 or 2")
    except Exception:
        print("Please enter a number")
    else:
        if int(prompt) == 1:
            print("you have selected Encoder")
            reg_no = year_of_prod = no_of_passngr = mass_of_vehicle = ""
            while reg_no == "" or not reg_no.isalnum():
                reg_no = input("Enter a registration number of the vehicle: ")
            while year_of_prod == "" or not year_of_prod.isdigit():
                year_of_prod = input("Enter the year of production: ")
            while no_of_passngr == "" or not no_of_passngr.isdigit():
                no_of_passngr = input("Enter the number of passengers: ")
            while mass_of_vehicle == "" or not mass_of_vehicle.isdigit():
                mass_of_vehicle = input("Enter the mass of the vehicle: ")

            vehicle1 = Vehicle(reg_no, year_of_prod, no_of_passngr, mass_of_vehicle)
            for key, value in vehicle1.__dict__.items():
                print(f"{key} : {value}")

            json_data = json.dumps(vehicle1, cls = Encoder)
            
            print("JSON string is :\n\t",json_data)
        else:
            print("You have selected Decoder !!")
            string = input("Enter the json string below \n string = ")
            try:
                vehicle1 = json.loads(string, object_hook=decoder)
                print("The attributes dictionary of newly created object is: ")
                print("\t vehicle1 = ",vehicle1.__dict__)
            except Exception:
                print("json.load didn't work")
            
            
run()

            

        
    
