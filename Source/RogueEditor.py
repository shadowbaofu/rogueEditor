import requests, json, random, os

'''
Description:

A simple pokerogue.net
profile and game save editor.

Author:

Onyxdev

'''

class pokeRogue:

    def __init__(self, user, password, log_error = True):
        
        #Login api url
        self.login_url = "https://api.pokerogue.net/account/login"
        
        #Get trainer data api url
        self.trainer_data_url = "https://api.pokerogue.net/savedata/get?datatype=0"
        
        #Update trainer data api url
        self.update_trainer_data_url = "https://api.pokerogue.net/savedata/update?datatype=0"
        
        #Get gamesave data api url (slot required) -> int 0-4
        self.gamesave_slot_url = "https://api.pokerogue.net/savedata/get?datatype=1&slot="
        
        #Update gamesave data api url (slot required) -> int 0-4
        self.update_gamesave_slot_url = "https://api.pokerogue.net/savedata/update?datatype=1&slot="
        
        #Login headers
        self.headers = {
            "content-type": "application/x-www-form-urlencoded",
            "sec-ch-ua": "\"Google Chrome\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""

            }
        
        #Login payload
        self.data = {
            "username": user,
            "password": password
            }   

        #Initiate authentication token    
        with requests.session() as s:
            
            try:
                
             self.auth = s.post(self.login_url, headers = self.headers, data = self.data).json()["token"]
             
            except Exception as e:
                
                if log_error:
                 print(f"Error on __init__ self.auth -> {e}")

        #Session headers with authentication token
        self.auth_headers = {
         "authorization": self.auth,
         "sec-ch-ua": "\"Google Chrome\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
         "sec-ch-ua-mobile": "?0",
         "sec-ch-ua-platform": "\"Windows\""
        }

        #Pokedex IDs by Pokemon name -> data['bulbasaur'] >> 1
        with open("./data/pokemon.json") as f:
            self.pokemon_id_by_name = json.loads(f.read())

    #Get trainer data -> json
    def get_trainer_data(self):
        
        try:
            
            with requests.session() as s:
                data = s.get(self.trainer_data_url, headers = self.auth_headers).json()
                return data
        
        except Exception as e:
            print(f"Error on get_trainer_data() -> {e}")

    #Get saved game data (slot required -> int 1-5) -> json
    def get_gamesave_data(self, slot=1):

        try:
            
            with requests.session() as s:
                data = s.get(f"{self.gamesave_slot_url}{slot-1}", headers = self.auth_headers).json()
                return data

        except Exception as e:
            print(f"Error on get_gamesave_data() -> {e}")

    #Update trainer data from json payload -> None
    def update_trainer_data(self, payload):

        try:

            with requests.session() as s:
                data = s.post(self.update_trainer_data_url, headers = self.auth_headers, json = payload)
                return data

        except Exception as e:
            print(f"Error on update_trainer_data() -> {e}")

    #Update game data from json payload (slot required -> int 1-5) -> None
    def update_gamesave_data(self, slot, payload):

        try:
            
            trainer = self.get_trainer_data()
            trainer_id, trainer_secretId = trainer["trainerId"], trainer["secretId"]
            url_ext = f"&trainerId={trainer_id}&secretId={trainer_secretId}"
            
            with requests.session() as s:
                data = s.post(f"{self.update_gamesave_slot_url}{slot-1}{url_ext}", headers = self.auth_headers, json = payload)
                return data

        except Exception as e:
           print(f"Error on update_gamesave_data() -> {e}")
           
    #Dump trainer data to json file -> None
    def dump_trainer_data(self):

        try:

            with open("trainer.json", "w") as f:
                f.write(json.dumps(self.get_trainer_data(), indent=2))
                print("Your trainer data has been dumped! -> trainer.json")

        except Exception as e:
            print(f"Error on dump_trainer_data() -> {e}")

    #Dump gamesave data to json file (slot required -> int 1-5) -> None
    def dump_gamesave_data(self, slot = None):

        try:

            if not slot:
                slot = int(input("Slot(1-5): "))
                if slot > 5: return print(f"This slot does not exist!")
                if slot < 1: return print(f"This slot does not exist!")

            with open(f"slot {slot}.json", "w") as f:
                f.write(json.dumps(self.get_gamesave_data(slot), indent=2))
                print(f"The saved game on slot {slot} has been dumped! -> slot {slot}.json")

        except Exception as e:
            print(f"Error on dump_trainer_data() -> {e}")


    #Update trainer data from json dump file as payload -> None
    def update_trainer_data_from_file(self):

        try:

            if "trainer.json" not in os.listdir():
                return print("trainer.json file was not found!")

            with open("trainer.json", "r") as f:
                data = json.loads(f.read())
                self.get_trainer_data()
                self.update_trainer_data(data)
                print("Your trainer data has been updated!")

        except Exception as e:
            print(f"Error on update_trainer_data_from_file() -> {e}")

    #Update gamesave data from json dump file as payload -> None
    def update_gamesave_data_from_file(self, slot = None):

        try:

            if not slot:
                slot = int(input("Slot(1-5): "))
                if slot > 5: return print(f"This slot does not exist!")
                if slot < 1: return print(f"This slot does not exist!")
                if f"slot {slot}.json" not in os.listdir(): return print(f"slot {slot}.json was not found!")

            with open(f"slot {slot}.json", "r") as f:
                data = json.loads(f.read())
                self.get_trainer_data()
                self.update_gamesave_data(slot, data)
                print(f"Your save data has been updated in slot: {slot}!")
                
        except Exception as e:
            pass

    #Display all available Pokemon -> None
    def pokedex(self):
        dex = []
        
        for pkm in self.pokemon_id_by_name['dex']:
            dex.append(f"{self.pokemon_id_by_name['dex'][pkm]}: {pkm}")
            
        print("\n".join(dex))
            
    #Unlock all starters with perfect ivs and all shiny variants -> None
    def unlock_all_starters(self):

        try:
        
            total_caught = 0
            total_seen = 0
            data = self.get_trainer_data()
            
            for entry in list(data["dexData"]):
                
                caught = random.randint(150, 250)
                seen = random.randint(150, 350)
                total_caught += caught
                total_seen += seen
                
                data["dexData"][entry] = {
                              "seenAttr": 479,
                              "caughtAttr": 255,
                              "natureAttr": 67108862,
                              "seenCount": seen,
                              "caughtCount": caught,
                              "hatchedCount": 0,
                              "ivs": [
                                31,
                                31,
                                31,
                                31,
                                31,
                                31
                              ]
                            }
                
                data["starterData"][entry] = {
                            "moveset": None,
                            "eggMoves": 15,
                            "candyCount": caught + 20,
                            "abilityAttr": 7,
                            "passiveAttr": 0,
                            "valueReduction": 0
                            }
                
                data["gameStats"]["battles"] = total_caught + random.randint(1, total_caught)
                data["gameStats"]["pokemonCaught"] = total_caught
                data["gameStats"]["pokemonSeen"] = total_seen
                data["gameStats"]["shinyPokemonCaught"] = len(list(data["dexData"])) * 2
                    
            self.update_trainer_data(data)
            print("All starter Pokemon has been unlocked with perfect IVS and every shiny form!")

        except Exception as e:
            print(f"Error on unlock_all_starters() -> {e}")
            
    #Modify/add a pokemon to starters -> None
    def starter_edit(self, dexId = None): # self.pokemon_id_by_name

        try:
            
            data = self.get_trainer_data()
            
            if not dexId:
                dexId = input("Which Pokemon?(Pokemon name / Pokedex ID): " )

                #Using Pokedex ID
                if dexId.isnumeric():
                    
                   if dexId not in data["starterData"]:
                       return print(f"There's no Pokemon with the ID: {dexId}")
                    
                #Using Pokemon name
                else:
                    
                    if dexId.lower() in self.pokemon_id_by_name["dex"]:
                        dexId = self.pokemon_id_by_name["dex"][dexId]
                        
                    else:
                       return print(f"There's no Pokemon with the Name: {dexId}")
                        
            isShiny = int(input("Do you want the Pokemon to be shiny? (1: Yes, 2: No)(number): "))
            if isShiny == 1:  isShiny = 255
            else: isShiny = 253
            seenAttr = 479
            caughtAttr = isShiny
            natureAttr = 67108862
            caught = int(input("How many of this Pokemon have you caught? (at least one) (+1 candy per)(number): "))
            hatched = int(input("How many of this pokemon have you hatched? (at least one) (+2 candy per hatch)(number): "))
            seenCount = int(input("How many of this Pokemon have you seen? (Needs to be more or equal to caught)(number): "))
            spatk_iv = int(input("What's the [special attack IV] of the Pokemon?(number): "))
            def_iv = int(input("What's the [defense IV] of the Pokemon?(number): "))
            atk_iv = int(input("What's the [attack IV] of the Pokemon?(number): "))
            hp_iv = int(input("What's the [health IV] of the Pokemon?(number): "))
            spd_iv = int(input("What's the [speed IV] of the Pokemon?(number): "))
            spdef_iv = int(input("What's the [special defense IV] of the Pokemon?(number): "))
            ivs = [spatk_iv, def_iv, atk_iv, hp_iv, spd_iv, spdef_iv]

            data["dexData"][dexId] = {
              "seenAttr": seenAttr,
              "caughtAttr": caughtAttr,
              "natureAttr": natureAttr,
              "seenCount": seenCount,
              "caughtCount": caught,
              "hatchedCount": hatched,
              "ivs": ivs
                }

            data["starterData"][dexId] = {
              "moveset": None,
              "eggMoves": 15,
              "candyCount": caught + (hatched * 2),
              "abilityAttr": 7,
              "passiveAttr": 0,
              "valueReduction": 0
                }

            self.get_trainer_data()
            self.update_trainer_data(data)
            print(f"The Pokemon with the dex entry of {dexId} has been updated!")

        except Exception as e:
            print(f"Error on starter_edit() -> {e}")

    #Modify the amount of egg gacha tickets you have -> None
    def egg_gacha(self):
        
        try:
            
            data = self.get_trainer_data()
            
            voucherCounts = {
                "0": int(input("How many [Common] tickets do you want to have?(number): ")),
                "1": int(input("How many [Rare] tickets do you want to have?(number): ")),
                "2": int(input("How many [Epic] tickets do you want to have?(number): ")),
                "3": int(input("How many [Legendary tickets do you want to have?(number):")) 
                }
            
            data["voucherCounts"] = voucherCounts
            self.update_trainer_data(data)
            print("Your gacha tickets has been updated!")
                
            
        except Exception as e:
            print(f"Error on egg_gacha() -> {e}")
   
    #Makes all your eggs hatch after the next wave -> None
    def hatch_all_eggs(self):
        
        try:
            
            data, eggs = self.get_trainer_data(), []
            
            if not data["eggs"]:
                return print("You have no eggs to hatch!")
            
            for egg in data["eggs"]:
                egg["hatchWaves"] = 0
                eggs.append(egg)
                
            data["eggs"] = eggs
            self.get_trainer_data()
            self.update_trainer_data(data)
            print("Done! -> Your eggs will hatch after the next wave!")
            
        except Exception as e:
            print(f"Error when hatching eggs: {e}")

        


if __name__ ==  '__main__':

    with open("./data/data.json") as f:
         data = json.loads(f.read())

    print(data["startup_message"])
    
    while True:
        
        try:
            
            print("\n<Pokerogue account>")
            username, password = input("Username: "), input("Password: ")
            rogueEditor = pokeRogue(username, password, log_error = False)
            break
        
        except:
            print("Incorrect login information/server down... try again!")

    print(f"Successfully logged in as: {username.capitalize()}")
               
    func = {
        "1": rogueEditor.hatch_all_eggs,
        "2": rogueEditor.dump_trainer_data,
        "3": rogueEditor.dump_gamesave_data,
        "4": rogueEditor.update_trainer_data_from_file,
        "5": rogueEditor.update_gamesave_data_from_file,
        "6": rogueEditor.starter_edit,
        "7": rogueEditor.egg_gacha,
        "8": rogueEditor.unlock_all_starters,
        "9": rogueEditor.pokedex
        }
    
    cmd = ["<------------------------- COMMANDS ------------------------>",
           "1: Hatch all eggs",
           "2: Dump trainer data to json file",
           "3: Dump save data (slot 1-5) to json file",
           "4: Update trainer data from the dumped json file",
           "5: Update save data (slot 1-5) from the dumped json file",
           "6: Add/Modify a starter Pokemon (Pokemon name or Pokedex Id): ",
           "7: Modify the amount of egg gacha tickets you have",
           "8: Unlock all starters with perfect ivs and all shiny variants",
           "9: Display all starter Pokemon names with their Ids",
           "---------------------------------------------------------------"
           ]
    
    while True:
        
        print("\n".join(cmd))
        command = input("Command: ")
        
        if command in func:
           func[command]()
            
        else:
           print("Command not found!")
