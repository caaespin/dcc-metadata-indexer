from pprint import pprint
from jsonmerge import merge
from jsonspec.validators import load    #for validation
import json

files = ['sample_individual_metadata_bundle_jsons/','1a_donor_biospecimen.json','1b_donor_biospecimen.json','2a_fastq_upload.json','2b_fastq_upload.json','3a_alignment.json','3b_alignment.json','4_variant_calling.json']
data = []
flags = []
specimen_type = ['normal_specimen','tumor_specimen'] 
type = ['samples','sample_uuid','sequence_upload','alignment']
result = {}
flagsWithStr = {}

#Note: the files must be in this particular order:
#folderName, donor, donor, fastqNormal, fastqTumor, alignmentNormal, alignmentTumor, variantCalling

def openFiles(files):
   for i in range(len(files)-1):
      try: 
         with open(files[0]+files[i+1]) as data_file:
            data.append(json.load(data_file))
         flags.append("true")
      except FileNotFoundError:
         print ('File not found: '+files[i+1])
         flags.append("false")
         data.append(0)
         
def assignBranch(data, flags):
   # finds the uuid in 2a, 2b, 3a, 3b and then adds data to the correct branch
   # j controls the type (normal or tumor). k and i place the data in the correct place
   i=0 
   k=0
   for j in range(2,6):
      if (flags[j] == "true"):
         workflows={}
         for uuid in data[j]['parent_uuids']:
            #print ("UUIDs: "+uuid)
            workflows[uuid] = data[j]
         specimens = result[specimen_type[j%2]]
         for specimen in specimens:
            samples = specimen[type[0]]
            for sample in samples:
               sample_uuid = sample[type[1]]
               #print(sample_uuid)
               sample[type[2+k]] = workflows[sample_uuid]
               #pprint(sample)
      i=i+1
      if (i%2==0):
         k=1

def assignVariant(data):
   if (flags[6] == "true"):
      workflows={}
      for uuid in data[6]['parent_uuids']:
         #print ("UUIDs: "+uuid)
         workflows[uuid] = data[6]
      donor_uuid = result['donor_uuid']
      result['somatic_variant_calling'] = workflows[donor_uuid]


def dumpResult(result):
   with open('merge.json', 'w') as outfile:
      #newidtype = dict(_id=1, _type='meta') #could use this for elasticsearch bulk queries
      #newindex = dict(index = newidtype)
      #json.dump(newindex, outfile)
      #outfile.write('\n')
      json.dump(result, outfile)
      
def createFlags(flags):
   flagsWithStr = dict(zip(['donor1_exists', 'donor2_exists', 'fastqNormal_exists', 'fastqTumor_exists', 'alignmentNormal_exists', 'alignmentTumor_exists', 'variantCalling_exists'], flags))
   result['flags'] = flagsWithStr

def validateResult():
   # data will validate against this schema
   with open('metadata_model_no_uri.json') as data_file:    
      schema = json.load(data_file)

   #loading into jsonspec
   validator = load(schema)

   # validate result against schema
   validator.validate(result)

openFiles(files)
#Assuming that the donor documents will always exist
result = merge(data[0], data[1])   
assignBranch(data, flags)
assignVariant(data)
createFlags(flags)
validateResult()
dumpResult(result)
#pprint(result)





