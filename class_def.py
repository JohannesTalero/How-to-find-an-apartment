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

 

#--------------------------- Parking_properties ----------------------------------------
class parking_properties:

    def if_valune_non_0(self,val):
        if val ==None:
            return(0)
        else:
            return(val)

    def __init__ (self,parking, kind, deposit):
       self.parking = self.if_valune_non_0(localidad)
       self.kind = kind
       self.deposit = self.if_valune_non_0(deposit)


#--------------------------- apartments ----------------------------------------
class additional_features:

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
       self.score=0
    




        
apartamento_1=physical_properties(100,120,110,2,2,5,6)
print(apartamento_1.time)
apartamento_1.time=-10
print(apartamento_1.time)

