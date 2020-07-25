#--------------------------- physical_properties ----------------------------------------
class physical_properties:

    def if_valune_non_0(self,val):
        if val ==None:
            return(0)
        else:
            return(val)

    def __init__ (self,area, built_area, private_area, rooms, bathrooms, floors, time):

       self.time = self.if_valune_non_0(area)
       self.area = self.if_valune_non_0(area)
       self.rooms = self.if_valune_non_0(rooms)
       self.floors = self.if_valune_non_0(floors)
       self.bathrooms = self.if_valune_non_0(bathrooms)
       self.built_area = self.if_valune_non_0(built_area)
       self.private_area = self.if_valune_non_0(private_area)

    #---------------- functions --------------       
    def get_time(self):
        return(self.time)

    def change_time(self,N_time):
        self.time=N_time
    #----
    def get_area(self):
        return(self.area)

    def change_area(self,N_area):
        self.area=N_area
    #----
    def get_rooms(self):
        return(self.rooms)

    def change_rooms(self,N_rooms):
        self.rooms=N_rooms
    #----
    def get_floors(self):
        return(self.floors)

    def change_floors(self,N_floors):
        self.floors=N_floors
    #----
    def get_bathrooms(self):
        return(self.bathrooms)

    def change_bathrooms(self,N_bathrooms):
        self.bathrooms=N_bathrooms
    #----
    def get_built_area(self):
        return(self.built_area)

    def change_built_area(self,N_built_area):
        self.built_area=N_built_area
    #----

    def get_private_area(self):
        return(self.private_area)

    def change_private_area(self,N_private_area):
        self.private_area=N_private_area
    #----

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

    #---------------- functions --------------       
    def get_stratum(self):
        return(self.stratum)

    def change_stratum(self,N_stratum):
        self.stratum=N_stratum
    #----
    def get_localidad(self):
        return(self.localidad)

    def change_localidad(self,N_localidad):
        self.localidad=N_localidad
    #----
    def get_cadastral_neighborhood(self):
        return(self.cadastral_neighborhood)

    def change_cadastral_neighborhood(self,N_cadastral_neighborhood):
        self.cadastral_neighborhood=N_cadastral_neighborhood
    #----
    def get_common_neighborhood(self):
        return(self.common_neighborhood)

    def change_common_neighborhood(self,N_common_neighborhood):
        self.common_neighborhood=N_common_neighborhood
  
 



        
apartamento_1=physical_properties(100,120,110,2,2,5,6)
print(apartamento_1.get_time())