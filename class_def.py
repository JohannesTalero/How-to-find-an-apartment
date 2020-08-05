import numpy as np
#--------------------------- physical_properties ----------------------------------------
class physical_properties:

    def if_valune_non_0(self,val):
        if (val == None or val == np.nan):
            return(0)
        else:
            return(val)

    def __init__ (self, built_area, private_area, rooms, bathrooms, floors, time):

       self.time = time
       self.rooms = self.if_valune_non_0(rooms)
       self.floors = self.if_valune_non_0(floors)
       self.bathrooms = self.if_valune_non_0(bathrooms)
       self.built_area = self.if_valune_non_0(built_area)
       self.private_area = self.if_valune_non_0(private_area)

    def summary(self,save=False):
        properties=[self.built_area, self.private_area, self.rooms, self.bathrooms, self.floors, self.time, self.private_area, self.rooms, self.bathrooms, self.floors, self.time]
        print(f"""
              ---------------------------
              built_area: {self.built_area}
              private_area: {self.private_area}
              rooms: {self.rooms}
              bathrooms: {self.bathrooms}
              floors: {self.floors}
              time: {self.time}
              ---------------------------
              """)
        if save:
            return(properties)
            print("""saved
             ---------------------------
                  """)
        else:
            print("""
            not saved
            ---------------------------
                  """)            
    
#--------------------------- Contextual_properties ----------------------------------------
class contextual_properties:

    def if_valune_non_0(self,val):
        if val ==None:
            return(0)
        else:
            return(val)

    def __init__ (self,common_neighborhood, cadastral_neighborhood, localidad, stratum):
       self.localidad = self.if_valune_non_0(localidad)
       self.stratum = self.if_valune_non_0(stratum)
       self.cadastral_neighborhood = self.if_valune_non_0(cadastral_neighborhood)
       self.common_neighborhood = self.if_valune_non_0(common_neighborhood)

    def summary(self,save=False):
        properties=[self.common_neighborhood, self.cadastral_neighborhood, self.localidad, self.stratum]
        print(f"""
              ---------------------------
              common neighborhood: {self.common_neighborhood}
              cadastral neighborhood: {self.cadastral_neighborhood}
              localidad: {self.localidad}
              stratum: {self.stratum}

              ---------------------------
              """)
        if save:
            return(properties)
            print("""saved
             ---------------------------
                  """)
        else:
            print("""
            not saved
            ---------------------------
                  """)            
 

#--------------------------- Parking_properties ----------------------------------------
class parking_properties:

    def if_valune_non_0(self,val):
        if val ==None:
            return(0)
        else:
            return(val)

    def __init__ (self,parking, kind, deposit):
       self.parking = self.if_valune_non_0(parking)
       self.kind = kind
       self.deposit = self.if_valune_non_0(deposit)

    def summary(self,save=False):
        properties=[self.parking, self.kind, self.deposit]
        print(f"""
              ---------------------------
              parking: {self.parking}
              kind: {self.kind}
              deposit: {self.deposit}
              ---------------------------
              """)
        if save:
            return(properties)
            print("""saved
             ---------------------------
                  """)
        else:
            print("""
            not saved
            ---------------------------
                  """)            
 

#--------------------------- additional_properties ----------------------------------------
class additional_properties:

    def __init__ (self, Heater, terrace, stove):
       self.Heater = Heater
       self.terrace = terrace
       self.stove = stove


    def summary(self,save=False):
        properties=[self.Heater, self.terrace, self.stove]
        print(f"""
              ---------------------------
              Heater: {self.Heater}
              terrace: {self.terrace}
              stove: {self.stove}
              ---------------------------
              """)
        if save:
            return(properties)
            print("""saved
             ---------------------------
                  """)
        else:
            print("""
            not saved
            ---------------------------
                  """)            
                  
#--------------------------- apartments ----------------------------------------
class apartment:

    def __init__ (self, Lease_value, Administration_value, Description, Image, URL, Negotiate_Price, physical_properties_N, contextual_properties_N, parking_properties_N, additional_features_N):
       self.Lease_value = Lease_value
       self.Administration_value = Administration_value
       self.Description = Description
       self.Image = Image
       self.URL = URL
       self.Negotiate_Price = Negotiate_Price
       self.physical_properties_N = physical_properties_N
       self.contextual_properties_N = contextual_properties_N
       self.parking_properties_N = parking_properties_N
       self.additional_features_N = additional_features_N
       self.score=1500
       self.games=0
       self.win=0
       self.rival_score_a=0
    
    def summary(self,save=False):
        properties=[self.Lease_value, self.Administration_value, self.Description, self.Image, self.URL, self.Negotiate_Price, self.physical_properties_N,
                    self.contextual_properties_N, self.parking_properties_N, self.additional_features_N, self.score,self.games]
        print(f"""
              ---------------------------
              Lease_value: {self.Lease_value}
              Administration_value: {self.Administration_value}
              Description: {self.Description}
              Image: {self.Image}
              URL: {self.URL}
              Negotiate_Price: {self.Negotiate_Price}
              score: {self.score}
              games: {self.games}
              ---------------------------
              """)
        self.physical_properties_N.summary()
        self.contextual_properties_N.summary()
        self.parking_properties_N.summary()
        self.additional_features_N.summary()
              
        if save:
            return(properties)
            print("""saved
             ---------------------------
                  """)
        else:
            print("""
            not saved
            ---------------------------
                  """)            
