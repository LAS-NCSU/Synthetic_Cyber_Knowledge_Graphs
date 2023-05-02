from stix2validator import validate_file, validate_string, print_results,ValidationOptions
from stix2 import Indicator,ThreatActor,AttackPattern,Bundle, Relationship, parse
import json


example1 = Indicator(  type= "indicator",
                        spec_version= "2.1",
                  #      id= "indicator--a862ff86-68d9-42e5-8095-cd80c040e112", these are optional
                  #      created = "2020-06-24T15:04:40.048932Z",
                   #     modified = "2020-06-24T15:04:40.048932Z",
                        name = "File name",
                        pattern = "[file:hashes.md5 = 'd41d8cd98f00b204e9800998ecf8427e']",
                        pattern_type= "stix", #required
                        pattern_version= "2.1", #required
                        description= "A description.",
                        valid_from= "2020-06-24T15:04:40.048932Z")
example2 = example1.new_version(
                                   labels=["malicious-activity"],
                                   external_references= [{  "source_name": "capec",  
		                              "external_id": "CAPEC-163"  }   ]  )
example3 = ThreatActor(  type= "threat-actor",
                        spec_version= "2.1",
                        id= "threat-actor--56f3f0db-b5d5-431c-ae56-c18f02caf500", 
                        name = "russian haker",                     
                        description= "A particular form of spear phishing where the attacker claims that the target had won a contest, including personal details, to get them to click on a link.",
                        threat_actor_types =[{  "terrorist" }], 
                        roles =[{  "director" }], 
                        goals =[{  "world domination" }], 
                        sophistication =[{  "very" }] ,
                        resource_level =[{  "government" }], 
                        primary_motivation =[{  "ideology" }], 
                        secondary_motivations =[{  "no gf" }] 
                    )
example4 = AttackPattern(  type= "attack-pattern",
                        spec_version= "2.1",
                        id= "attack-pattern--7e33a43e-e34b-40ec-89da-36c9bb2cacd5",
                        created = "2016-05-12T08:17:27.000Z",  
	                    modified = "2016-05-12T08:17:27.000Z",  
                        name = "stupid_hack",                                               
                        description= "A particular form of spear phishing where the attacker claims that the target had won a contest, including personal details, to get them to click on a link.",
                        )
relationship1 = Relationship(relationship_type='name',                            
                            source_ref=example2.id,
                            target_ref=example3.id
                            )
relationship2 = Relationship(relationship_type='indicates',
                            source_ref=example2.id,
                            target_ref=example4.id
                            )
#might need to have all the code for creating objects in the same file, 
#as there will be objects that will reference each other
#still should make multiple objects
#put what we want to export to export in the array
#this will export each stix object as a json, note these files are named by there id

arr = [example1, example2, example3, example4, relationship1, relationship2]
#bundle = Bundle(arr)
#print(bundle._properties['objects'])
#options = ValidationOptions(strict=True, version="2.2")
for ex in arr:
    stix_json_string = ex.serialize(pretty=True)

    print(stix_json_string)
    fil = ex.id +".json"
    with open( fil, "w") as write_file: #set to name of file
        write_file.write(stix_json_string)


    results = validate_file(fil)
    if results.is_valid :
        print("this is a stix valid json" )
    else:
        print("this is not a stix valid json")
