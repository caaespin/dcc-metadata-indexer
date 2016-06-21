# generage_metadata.py
# Generate metadata files from a tsv file.
# See "helper client" in https://ucsc-cgl.atlassian.net/wiki/display/DEV/Storage+Service+-+Functional+Spec
# MAY2016	chrisw

# imports
import logging
from optparse import OptionParser
import sys
import csv
import os
import errno
import jsonschema
import openpyxl
import json
import uuid
from sets import Set
# import shutil
import subprocess
import datetime
# import re

# methods and functions

def getOptions():
    """
    parse options
    """
    usage_text = []
    usage_text.append("%prog [options] [input Excel or tsv files]")
    usage_text.append("Data will be read from 'Sheet1' in the case of Excel file.")

    parser = OptionParser(usage="\n".join(usage_text))
    parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose",
                      help="Switch for verbose mode.")

    parser.add_option("-s", "--skip-upload", action="store_true", default=False, dest="skip_upload",
                      help="Switch to skip upload. Metadata files will be generated only.")

    parser.add_option("-m", "--metadataSchema", action="store", default="metadata_flattened.json", type="string",
                      dest="metadataSchemaFileName", help="flattened json schema file for metadata")

    parser.add_option("-d", "--outputDir", action="store", default="output_metadata", type="string",
                      dest="metadataOutDir",
                      help="output directory. In the case of colliding file names, the older file will be overwritten.")

    (options, args) = parser.parse_args()

    return (options, args, parser)

def jsonPP(obj):
    """
    Get a pretty stringified JSON
    """
    str = json.dumps(obj, indent=4, separators=(',', ': '), sort_keys=True)
    return str

def getNow():
    """
    Get a datetime object for utc NOW.
    Convert to ISO 8601 format with datetime.isoformat()
    """
    now = datetime.datetime.utcnow()
    return now

def getTimeDelta(startDatetime):
    """
    get a timedelta object. Get seconds elapsed with timedelta.total_seconds().
    """
    endDatetime = datetime.datetime.utcnow()
    timedeltaObj = endDatetime - startDatetime
    return timedeltaObj

def loadJsonObj(fileName):
    """
    Load a json object from a file.
    """
    try:
        file = open(fileName, "r")
        object = json.load(file)
        file.close()
    except Exception as exc:
        logging.exception("loadJsonObj")
    return object

def loadJsonSchema(fileName):
    """
    Load a json schema (actually just an object) from a file.
    """
    schema = loadJsonObj(fileName)
    return schema

def validateObjAgainstJsonSchema(obj, schema):
    """
    Validate an object against a schema.
    """
    try:
        jsonschema.validate(obj, schema)
    except Exception as exc:
        logging.error("jsonschema.validate FAILED in validateObjAgainstJsonSchema: %s" % (str(exc)))
        return False
    return True

def readFileLines(filename, strip=True):
    """
    Convenience method for getting an array of fileLines from a file.
    """
    fileLines = []
    file = open(filename, 'r')
    for line in file.readlines():
        if strip:
            line = line.rstrip("\r\n")
        fileLines.append(line)
    file.close()
    return fileLines

def readTsv(fileLines, d="\t"):
    """
    convenience method for reading TSV file lines into csv.DictReader obj.
    """
    reader = csv.DictReader(fileLines, delimiter=d)
    return reader

def normalizePropertyName(inputStr):
    """
    field names in the schema are all lower-snake-case
    """
    newStr = inputStr.encode('ascii', 'ignore').lower()
    newStr = newStr.replace(" ", "_")
    newStr = newStr.strip()
    return newStr

def processFieldNames(dictReaderObj):
    """
    normalize the field names in a DictReader obj
    """
    newDataList = []
    for dict in dictReaderObj:
        newDict = {}
        newDataList.append(newDict)
        for key in dict.keys():
            newKey = normalizePropertyName(key)
            newDict[newKey] = dict[key]
    return newDataList

def setUuids(dataObj):
    """
    Set donor_uuid, specimen_uuid, and sample_uuid for dataObj. Uses uuid.uuid5().
    """
    keyFieldsMapping = {}
    keyFieldsMapping["donor_uuid"] = ["center_name", "submitter_donor_id"]

    keyFieldsMapping["specimen_uuid"] = list(keyFieldsMapping["donor_uuid"])
    keyFieldsMapping["specimen_uuid"].append("submitter_specimen_id")

    keyFieldsMapping["sample_uuid"] = list(keyFieldsMapping["specimen_uuid"])
    keyFieldsMapping["sample_uuid"].append("submitter_sample_id")

#     keyFieldsMapping["workflow_uuid"] = ["sample_uuid", "workflow_name", "workflow_version"]

    for uuidName in keyFieldsMapping.keys():
        keyList = []
        for field in keyFieldsMapping[uuidName]:
            if dataObj[field] is None:
                logging.error("%s not found in %s" % (field, jsonPP(dataObj)))
                return None
            keyList.append(dataObj[field].encode('ascii', 'ignore'))
        # was having some trouble with data coming out of openpyxl not being ascii
        s = "".join(keyList).lower()
        id = str(uuid.uuid5(uuid.NAMESPACE_URL, s))
        dataObj[uuidName] = id

    # must follow sample_uuid assignment
    workflow_uuid_keys = ["sample_uuid", "workflow_name", "workflow_version"]
    keyList = []
    for field in workflow_uuid_keys:
        if dataObj[field] is None:
            logging.error("%s not found in %s" % (field, jsonPP(dataObj)))
            return None
        keyList.append(dataObj[field].encode('ascii', 'ignore'))
    s = "".join(keyList).lower()
    id = str(uuid.uuid5(uuid.NAMESPACE_URL, s))
    dataObj["workflow_uuid"] = id

def getWorkflowUuid(sample_uuid, workflow_name, workflow_version):
    """
    Get a workflowUuid for use in this script.
    """
    keyList = []
    keyList.append(sample_uuid)
    keyList.append(workflow_name)
    keyList.append(workflow_version)
    s = "".join(keyList).encode('ascii', 'ignore').lower()
    workflowUuid = str(uuid.uuid5(uuid.NAMESPACE_URL, s))
    return workflowUuid

def getDataObj(dict, schema):
    """
    Pull data out from dict. Use the flattened schema to get the key names as well as validate.
    If validation fails, return None.
    """
    setUuids(dict)

#     schema["properties"]["workflow_uuid"] = {"type": "string"}
    propNames = schema["properties"].keys()

    dataObj = {}
    for propName in propNames:
        dataObj[propName] = dict[propName]

    if "workflow_uuid" in dict.keys():
        dataObj["workflow_uuid"] = dict["workflow_uuid"]

    isValid = validateObjAgainstJsonSchema(dataObj, schema)
    if (isValid):
        return dataObj
    else:
        logging.error("validation FAILED for \t%s\n" % (jsonPP(dataObj)))
        return None

def getDataDictFromXls(fileName, sheetName="Sheet1"):
    """
    Get list of dict objects from .xlsx,.xlsm,.xltx,.xltm.
    """
    logging.debug("attempt to read %s as xls file\n" % (fileName))
    workbook = openpyxl.load_workbook(fileName)
    sheetNames = workbook.get_sheet_names()
    logging.debug("sheetNames:\t%s\n" % (str(sheetNames)))

    worksheet = workbook.get_sheet_by_name(sheetName)

    headerRow = worksheet.rows[0]
    dataRows = worksheet.rows[1:]

    # map column index to column name
    colMapping = {}
    for colIdx in xrange(len(headerRow)):
        cell = headerRow[colIdx]
        value = cell.value
        if (value != None):
            colMapping[colIdx] = normalizePropertyName(value)

    # build up list of row data objs
    data = []
    for row in dataRows:
        rowDict = {}
        data.append(rowDict)
        for colIdx in colMapping.keys():
            colName = colMapping[colIdx]
            value = row[colIdx].value
            rowDict[colName] = value

    return data

def ln_s(file_path, link_path):
    """
    ln -s
    note: will not clobber existing file
    """
    try:
        os.symlink(file_path, link_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            if os.path.isdir(link_path):
                logging.error("linking failed -> %s is an existing directory" % (link_path))
            elif os.path.isfile(link_path):
                logging.error("linking failed -> %s is an existing file" % (link_path))
            elif os.path.islink(link_path):
                logging.error("linking failed -> %s is an existing link" % (link_path))
        else:
            logging.error("raising error")
            raise
    return None

def mkdir_p(path):
    """
    mkdir -p
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
    return None

def getObj(dataObjs, queryObj):
    """
    Check to see if queryObj is contained in some object in dataObjs by checking for identical key:value pairs.
    If match is found, return the matched object in dataObjs.
    If no match is found, return None.
    """
    for dataObj in dataObjs:
        foundMismatch = False
        if not isinstance(dataObj, dict):
            continue
        for key in queryObj.keys():
            queryVal = queryObj[key]
            dataVal = dataObj[key]
            if queryVal != dataVal:
                foundMismatch = True
                break
        if foundMismatch == True:
            continue
        else:
            return dataObj

    return None

def getWorkflowObjects(flatMetadataObj):
    """
    For each flattened metadata object, build up a metadataObj with correct structure.
    """
    schema_version = "0.0.1"
    num_files_written = 0

    commonObjMap = {}
    for metaObj in flatMetadataObj:
        workflow_uuid = metaObj["workflow_uuid"]
        if workflow_uuid in commonObjMap.keys():
            pass
        else:
            workflowObj = {}
            commonObjMap[workflow_uuid] = workflowObj
            workflowObj["program"] = metaObj["program"]
            workflowObj["project"] = metaObj["project"]
            workflowObj["center_name"] = metaObj["center_name"]
            workflowObj["submitter_donor_id"] = metaObj["submitter_donor_id"]
            workflowObj["donor_uuid"] = metaObj["donor_uuid"]

            workflowObj["timestamp"] = getNow().isoformat()
            workflowObj["schema_version"] = schema_version

            workflowObj["specimen"] = []

            # add specimen
            specObj = {}
            workflowObj["specimen"].append(specObj)
            specObj["submitter_specimen_id"] = metaObj["submitter_specimen_id"]
            specObj["submitter_specimen_type"] = metaObj["submitter_specimen_type"]
            specObj["specimen_uuid"] = metaObj["specimen_uuid"]
            specObj["samples"] = []

            # add sample
            sampleObj = {}
            specObj["samples"].append(sampleObj)
            sampleObj["submitter_sample_id"] = metaObj["submitter_sample_id"]
            sampleObj["sample_uuid"] = metaObj["sample_uuid"]

            # add workflow
            workFlowObj = {}
            analysis_type = metaObj["analysis_type"]
            sampleObj[analysis_type] = workFlowObj

            workFlowObj["workflow_name"] = metaObj["workflow_name"]
            workFlowObj["workflow_version"] = metaObj["workflow_version"]
            workFlowObj["analysis_type"] = metaObj["analysis_type"]
            workFlowObj["workflow_outputs"] = []
            workFlowObj["bundle_uuid"] = metaObj["workflow_uuid"]

        # retrieve workflow
        workflowObj = commonObjMap[workflow_uuid]
        analysis_type = metaObj["analysis_type"]
        wf_outputsObj = workflowObj["specimen"][0]["samples"][0][analysis_type]["workflow_outputs"]

        # add file info
        fileInfoObj = {}
        wf_outputsObj.append(fileInfoObj)
        fileInfoObj["file_type"] = metaObj["file_type"]
        fileInfoObj["file_path"] = metaObj["file_path"]

    return commonObjMap

def writeJson(directory, fileName, jsonObj):
    """
    Dump a json object to the specified directory/fileName. Creates directory if necessary.
    NOTE: will clobber the existing file
    """
    success = None
    try:
        mkdir_p(directory)
        filePath = os.path.join(directory, fileName)
        file = open(filePath, 'w')
        json.dump(jsonObj, file, indent=4, separators=(',', ': '), sort_keys=True)
        success = 1
    except Exception as exc:
        logging.exception("ERROR writing %s/%s\n" % (directory, fileName))
        success = 0
    finally:
        file.close()
    return success

def writeDataBundleDirs(structuredMetaDataObjMap, outputDir):
    """
    For each structuredMetaDataObj, prepare a data bundle dir for each workflow
    """
    numFilesWritten = 0
    for workflow_uuid in structuredMetaDataObjMap.keys():
        metaObj = structuredMetaDataObjMap[workflow_uuid]

        # get outputDir (bundle_uuid)
        bundlePath = os.path.join(outputDir, workflow_uuid)

        # get analysis_type
        sampleObj = metaObj["specimen"][0]["samples"][0]
        analysis_type = None
        for obj in sampleObj.values():
            if (isinstance(obj, dict)) and ("analysis_type" in obj.keys()):
                analysis_type = obj["analysis_type"]
                break
        if analysis_type == None:
            logging.error("no analysis found in %s" % (jsonPP(metaObj)))
            continue

        # link data file(s)
        wf_outputsObj = sampleObj[analysis_type]["workflow_outputs"]
        for outputObj in wf_outputsObj:
            file_path = outputObj["file_path"]
            fullFilePath = os.path.join(os.getcwd(), file_path)
            filename = os.path.basename(file_path)
            linkPath = os.path.join(bundlePath, filename)
            mkdir_p(bundlePath)
            ln_s(fullFilePath, linkPath)

        # write metadata
        numFilesWritten += writeJson(bundlePath, "metadata.json", metaObj)

    return numFilesWritten

def uploadMultipleFilesViaExternalScript(filePaths):
    """
    1. Upload multiple files with the ucsc-storage-client/ucsc-upload.sh script.
    2. Parse the output from ucsc-upload.sh to get the object ids of the uploads.
    3. Return a mapping of filePath to object id.
    """
    startDatetime = getNow()

    # check correct file paths
    fullFilePaths = []
    if not os.path.isfile("ucsc-storage-client/ucsc-upload.sh"):
        logging.critical("missing file: %s\n" % ("ucsc-storage-client/ucsc-upload.sh"))
    for filePath in filePaths:
        fullFilePath = os.path.join(os.getcwd(), filePath)
        if not os.path.isfile(fullFilePath):
            pass
#             logging.warning("missing file: %s\n" % (fullFilePath))
        fullFilePaths.append(fullFilePath)

    # build command string
    command = ["/bin/bash", "ucsc-upload.sh"]
    command.extend(fullFilePaths)
    command = " ".join(command)
    logging.debug("command:\t%s\n" % (command))

    # execute script, capture output
    try:
        output = subprocess.check_output(command, cwd="ucsc-storage-client", stderr=subprocess.STDOUT, shell=True)
        logging.debug("output:%s\n" % (str(output)))
    except Exception as exc:
        logging.exception("ERROR while uploading files")
        output = ""
    finally:
        logging.info("done uploading files")

    # parse output for object ids
    objectIdInfo = parseUploadOutputForObjectIds(output)

    runTime = getTimeDelta(startDatetime)
    logging.info("upload took %s s for %s files." % (str(runTime), str(len(objectIdInfo.keys()))))

    return objectIdInfo

def createDirWithSymLinks(targetDir, paths):
    """
    ln_s a list of paths into the targetDir
    """
    mkdir_p(targetDir)
    for path in paths:
        fileName = os.path.basename(path)
        file_path = os.path.join(os.getcwd(), path)
        link_path = os.path.join(targetDir, fileName)
        ln_s(file_path, link_path)

def uploadViaTempDir(tempDirName, filePaths):
    """
      1. create temp directory
      2. create links to upload paths
      3. upload directory contents
      4. clean up
      5. return upload object IDs
    """
    tempDirFullPath = os.path.join(os.getcwd(), tempDirName)

    # CAREFUL HERE!
    subprocess.call(["rm", "-rf", tempDirFullPath])
    createDirWithSymLinks(tempDirName, filePaths)

    uploadPath = os.path.join(os.getcwd(), tempDirName, "*")
    logging.debug("uploadPath %s" % uploadPath)
    idMapping = uploadMultipleFilesViaExternalScript([uploadPath])

    subprocess.call(["rm", "-rf", tempDirFullPath])
    return idMapping

def updateWorkFlowFileUuids(metadataObj, idMapping):
    """
    update file_uuid in metadata object. idMapping is a dict that maps fileName to file_uuid
    """
    modified = False
    workflowUuid = getWorkflowUuid(metadataObj["parent_uuids"][0], metadataObj["workflow_name"], metadataObj["workflow_version"])
    for workflow_output in metadataObj["workflow_outputs"]:
        file_path = workflow_output["file_path"]
        fileName = os.path.basename(file_path)
        filePathWithUuid = workflowUuid + "_" + fileName
        if filePathWithUuid in idMapping.keys():
            pass
            file_uuid = idMapping[filePathWithUuid]
            workflow_output["file_uuid"] = file_uuid
            modified = True
        else:
            logging.warning("no object ID found for %s" % (filePathWithUuid))
    return modified

def setupLogging(logfileName, logFormat, logLevel, logToConsole=True):
    """
    Setup simultaneous logging to file and console.
    """
#     logFormat = "%(asctime)s %(levelname)s %(funcName)s:%(lineno)d %(message)s"
    logging.basicConfig(filename=logfileName, level=logging.NOTSET, format=logFormat)
    if logToConsole:
        console = logging.StreamHandler()
        console.setLevel(logLevel)
        formatter = logging.Formatter(logFormat)
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
    return None

def registerBundleUpload(upload, manifest, accessToken):
     """
     java
         -Djavax.net.ssl.trustStore=ssl/cacerts
         -Djavax.net.ssl.trustStorePassword=changeit
         -Dserver.baseUrl=https://storage.ucsc-cgl.org:8444
         -DaccessToken=${accessToken}
         -jar dcc-metadata-client-0.0.16-SNAPSHOT/lib/dcc-metadata-client.jar
         -i ${upload}
         -o ${manifest}
         -m manifest.txt
     """

     return None

def performBundleUpload(manifest, accessToken):
    """
    Java
        -Djavax.net.ssl.trustStore=ssl/cacerts
        -Djavax.net.ssl.trustStorePassword=changeit
        -Dmetadata.url=https://storage.ucsc-cgl.org:8444
        -Dmetadata.ssl.enabled=true
        -Dclient.ssl.custom=false
        -Dstorage.url=https://storage.ucsc-cgl.org:5431
        -DaccessToken=${accessToken}
        -jar icgc-storage-client-1.0.14-SNAPSHOT/lib/icgc-storage-client.jar upload
        --manifest ${manifest}/manifest.txt
    """

    return None

#:####################################

def main():
    startTime = getNow()
    (options, args, parser) = getOptions()

    if len(args) == 0:
        logging.critical("no input files\n")
        sys.exit(1)

    if options.verbose:
        logLevel = logging.DEBUG
    else:
        logLevel = logging.INFO
    logfileName = os.path.basename(__file__).replace(".py", ".log")
    logFormat = "%(asctime)s %(levelname)s %(funcName)s:%(lineno)d %(message)s"
    setupLogging(logfileName, logFormat, logLevel)

    logging.debug('options:\t%s\n' % (str(options)))
    logging.debug('args:\t%s\n' % (str(args)))

    tempDirName = os.path.basename(__file__) + "_temp"

    # load flattened metadata schema
    metadataSchema = loadJsonSchema(options.metadataSchemaFileName)

    flatMetadataObjs = []

    # iter over input files
    for fileName in args:
        try:
            # attempt to process as xls file
            fileDataList = getDataDictFromXls(fileName)
        except Exception as exc:
            # attempt to process as tsv file
            logging.info("couldn't read %s as excel file\n" % fileName)
            logging.info("---now trying to read as tsv file\n")
            fileLines = readFileLines(fileName)
            reader = readTsv(fileLines)
            fileDataList = processFieldNames(reader)

        for data in fileDataList:
            metaObj = getDataObj(data, metadataSchema)

            if metaObj == None:
                continue

            flatMetadataObjs.append(metaObj)

    # get structured workflow objects
    structuredWorkflowObjMap = getWorkflowObjects(flatMetadataObjs)

    # write metadata files and link data files
    numFilesWritten = writeDataBundleDirs(structuredWorkflowObjMap, options.metadataOutDir)
#     numFilesWritten = writeMetadataOutput(structuredWorkflowObjMap, options.metadataOutDir)
    logging.info("number of metadata files written: %s\n" % (str(numFilesWritten)))

    if (options.skip_upload):
        logging.info("Skipping data upload steps.\n")
        runTime = getTimeDelta(startTime).total_seconds()
        logging.info("program ran for %s s." % str(runTime))
        return None
    else:
        logging.info("Now attempting to upload data.\n")

    # UPLOAD SECTION
    # TODO section below is very broken
    uploadCounts = {}
    uploadCounts["workflowOutputs"] = 0
    uploadCounts["metadata"] = 0
    numFilesWritten = 0
    jsonFilePaths = []
    workflowOutputPaths = []
    for dirName, subdirList, fileList in os.walk(options.metadataOutDir):
        if dirName == options.metadataOutDir:
            continue
        logging.info('looking in directory: %s\n' % dirName)
        for fileName in fileList:
            filePath = os.path.join(dirName, fileName)
            logging.debug("filePath\t%s" % filePath)
            if filePath.endswith(".json"):
                jsonFilePaths.append(filePath)
            else:
                workflowOutputPaths.append(filePath)

    # upload workflowOutputs and get object IDs
    logging.info("First, upload workflow outputs to get file_uuids.")
    idMapping = uploadViaTempDir(tempDirName, workflowOutputPaths)
    logging.debug("idMapping\t%s" % (jsonPP(idMapping)))

    uploadCounts["workflowOutputs"] += len(idMapping.keys())

    # get correct file names
    processedIdMapping = {}
    for key in idMapping.keys():
        newKey = os.path.basename(key)
        processedIdMapping[newKey] = idMapping[key]
    idMapping = processedIdMapping

    # update metadata jsons with file_uuid (upload object ID)
    logging.debug("jsonFilePaths\t%s" % (jsonPP(jsonFilePaths)))
    for filePath in jsonFilePaths:
        if filePath.endswith("biospecimen.json"):
            pass
        else:
            metadataObj = loadJsonObj(filePath)
            isModified = updateWorkFlowFileUuids(metadataObj, idMapping)
            if isModified:
                logging.debug("%s was modified" % filePath)
                numFilesWritten += writeJson(os.getcwd(), filePath, metadataObj)

    # upload jsonFilePaths
    logging.info("Now, upload metadata json files.")
    idMapping = uploadViaTempDir(tempDirName, jsonFilePaths)
    logging.debug("idMapping\t%s" % (jsonPP(idMapping)))

    uploadCounts["metadata"] += len(idMapping.keys())

    logging.info("file upload count\t%s\n" % (json.dumps(uploadCounts)))
    logging.info("number of updated metadata files:%s\n" % (str(numFilesWritten)))

    runTime = getTimeDelta(startTime).total_seconds()
    logging.info("program ran for %s s." % str(runTime))
    logging.shutdown()
    return None

# main program section
if __name__ == "__main__":
    main()
