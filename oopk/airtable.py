from airtable import Airtable
from system.models import AirtablePersonal


class AirTableConnection:

    def __init__(self, user_id:int, base_id:str, table_name:str) -> None:
     
     api_key = AirtablePersonal.objects.get(user = user_id).key
     self.airtable = Airtable(base_id = base_id, table_name = table_name, api_key = api_key)


    
class AirtableDataOperations(AirTableConnection):
   

   def comparison(self, records:list, view):
      
    self.get_all(view = view)

    not_found = []

    for item in records:
       
     if item not in self.air_data_total:
        not_found.append(item)
     
    return not_found
   
   def get_all(self, view:str):
      
    air_data = self.airtable.get_all(view = view )

    self.air_data_total = []

    for value in air_data:
         
         self.air_data_total.append(value["fields"])

    
    return self.air_data_total
   
   def insert_batch(self, records:list):
      
     result = self.airtable.batch_insert(records = records)

     return result
         



  

        





        