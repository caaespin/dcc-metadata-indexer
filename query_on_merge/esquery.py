#queries using Elasticsearch using python

from elasticsearch import Elasticsearch
import json

es_host = 'localhost:9200'
es_type = "meta"
es = Elasticsearch([es_host])

es_name_query = ["donor1 and donor2 exist","all flags are 'true'","alignment normal and tumor exist","fastq normal and tumor exist"]

#sample queries
es_queries = [
   {
      "aggs": {
         "project_f": {
            "aggs": {
               "project": {
                  "terms": {
                     "field": "program",
                     "size": 1000
                  },
                  "aggs": {
                  "donor_id": {
                     "terms": {
                        "field": "project",
                        "size": 10000
                     }
                  }
               }
            }
         },
         "filter": {
            "fquery": {
               "query": {
                  "filtered": {
                     "query": {
                        "bool": {
                           "should": [ {
                              "query_string": {
                              "query": "*"
                           }
                           } ]
                        }
                     },
                     "filter": {
                        "bool": {
                           "must": [
                              {
                                 "terms": {
                                    "flags.donor1_exists": [
                                       'true'
                                    ]
                                 }
                              },
                              {
                                 "terms": {
                                    "flags.donor2_exists": [
                                       'true'
                                    ]
                                 }
                              }
                           ],
                           "must_not": [
                              {
                                 "terms": {
                                    "flags.fastqNormal_exists": [
                                       'true'
                                    ]
                                 }
                              },
                              {
                                 "terms": {
                                    "flags.fastqtumor_exists": [
                                       'true'
                                    ]
                                 }
                              }
                           ]
                        }
                     }
                  }
               }
            }
         }
      }
   },
      "size": 0
   },
   #donor1 and donor2 exist
   #How many samples are pending upload (they lack a sequence upload)?

   {
      "aggs": {
         "project_f": {
            "aggs": {
               "project": {
                  "terms": {
                     "field": "program",
                     "size": 1000
                  },
                  "aggs": {
                  "donor_id": {
                     "terms": {
                        "field": "project",
                        "size": 10000
                     }
                  }
               }
            }
         },
         "filter": {
            "fquery": {
               "query": {
                  "filtered": {
                     "query": {
                        "bool": {
                           "should": [ {
                              "query_string": {
                              "query": "*"
                           }
                           } ]
                        }
                     },
                     "filter": {
                        "bool": {
                           "must": [
                              {
                                 "terms": {
                                    "flags.alignmentNormal_exists": [
                                       'true'
                                    ]
                                 }
                              },
                              {
                                 "terms": {
                                    "flags.alignmentTumor_exists": [
                                       'true'
                                    ]
                                 }
                              },
                              {
                                 "terms": {
                                    "flags.fastqNormal_exists": [
                                       'true'
                                    ]
                                 }
                              },
                              {
                                 "terms": {
                                    "flags.fastqTumor_exists": [
                                       'true'
                                    ]
                                 }
                              },
                              {
                                 "terms": {
                                    "flags.donor1_exists": [
                                       'true'
                                    ]
                                 }
                              },
                              {
                                 "terms": {
                                    "flags.donor2_exists": [
                                       'true'
                                    ]
                                 }
                              },
                              {
                                 "terms": {
                                    "flags.variantCalling_exists": [
                                       'true'
                                    ]
                                 }
                              }
                           ]
                        }
                     }
                  }
               }
            }
         }
      }
   },
      "size": 0
   },
   #all flags are 'true'
   #How many donors are complete in their upload vs. how many have one or more missing samples?

   {
      "aggs": {
         "project_f": {
            "aggs": {
               "project": {
                  "terms": {
                     "field": "program",
                     "size": 1000
                  },
                  "aggs": {
                  "donor_id": {
                     "terms": {
                        "field": "project",
                        "size": 10000
                     }
                  }
               }
            }
         },
         "filter": {
            "fquery": {
               "query": {
                  "filtered": {
                     "query": {
                        "bool": {
                           "should": [ {
                              "query_string": {
                              "query": "*"
                           }
                           } ]
                        }
                     },
                     "filter": {
                        "bool": {
                           "must": [
                              {
                                 "terms": {
                                    "flags.alignmentNormal_exists": [
                                       'true'
                                    ]
                                 }
                              },
                              {
                                 "terms": {
                                    "flags.alignmentTumor_exists": [
                                       'true'
                                    ]
                                 }
                              }
                           ],
                           "must_not": [
                              {
                                 "terms": {
                                    "flags.variantCalling_exists": [
                                       'true'
                                    ]
                                 }
                              }
                           ]
                        }
                     }
                  }
               }
            }
         }
      }
   },
      "size": 0
   },
   #alignment normal and tumor exist
   #somatic variant calling does not exist
   #How many tumor WES/WGS/panel samples have alignment done but no somatic variant calling done?

   {
      "aggs": {
         "project_f": {
            "aggs": {
               "project": {
                  "terms": {
                     "field": "program",
                     "size": 1000
                  },
                  "aggs": {
                  "donor_id": {
                     "terms": {
                        "field": "project",
                        "size": 10000
                     }
                  }
               }
            }
         },
         "filter": {
            "fquery": {
               "query": {
                  "filtered": {
                     "query": {
                        "bool": {
                           "should": [ {
                              "query_string": {
                              "query": "*"
                           }
                           } ]
                        }
                     },
                     "filter": {
                        "bool": {
                           "must": [
                              {
                                 "terms": {
                                    "flags.fastqNormal_exists": [
                                       'true'
                                    ]
                                 }
                              },
                              {
                                 "terms": {
                                    "flags.fastqTumor_exists": [
                                       'true'
                                    ]
                                 }
                              }
                           ],
                           "must_not": [
                              {
                                 "terms": {
                                    "flags.alignmentNormal_exists": [
                                       'true'
                                    ]
                                 }
                              },
                              {
                                 "terms": {
                                    "flags.alignmentTumor_exists": [
                                       'true'
                                    ]
                                 }
                              }
                           ]
                        }
                     }
                  }
               }
            }
         }
      }
   },
      "size": 0
   }
   #fastq normal and tumor exist
   #alignment does not exist
   #How many samples have fastq uploaded but don’t have alignment?


   #How many tumor RNAseq samples have alignment done but no expression values done?
]

#sample json_docs
json_docs = [
   {"tumor_specimen": [{"samples": [{"alignment": {"workflow_description": "This is the alignment for specimen PD41189 from donor CGP_donor_1199138__", "qc_metrics": {"insert_size_sd": 313, "coverage_average": 123.4, "insert_size_average": 10456}, "workflow_inputs": [{"file_storage_bundle_files": {"foo2__fastq__gz": {"file_storage_uri": "9014505b-fa59-4913-a05c-4666c6efe198", "file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}, "foo1__fastq__gz": {"file_storage_uri": "ae616ade-3734-4c48-a609-f2b292ecdbc7", "file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}}, "file_storage_metadata_json_uri": "153c380c-0bcb-4ee9-abdf-629db73a62e5", "file_storage_bundle_uri": "0e99945c-631e-4123-9158-5132a8fe2150"}], "workflow_bundle_url": "http://foo__bar/bwa-workflow", "host_metrics": {"vm_instance_type": "m1__xlarge", "vm_instance_cores": 4, "vm_instance_mem_gb": 256, "vm_region": "us-east-1", "vm_location": "aws"}, "workflow_version": "1__0__0", "parent_uuids": ["e1156a51-6265-4d9a-9bc8-ebccf40126b5"], "workflow_source_url": "http://foo__bar/bwa-workflow-src", "workflow_outputs": {"foo__bam__bai": {"file_type_label": "bai", "file_type_cv_terms": ["EDAM:278392"]}, "foo__bam": {"file_type_label": "bam", "file_type_cv_terms": ["EDAM:1293829"]}}, "workflow_params": {"param2": 2389239, "param1": 12121}, "workflow_name": "bwa-mem-alignment", "timing_metrics": {"overall_stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016", "step_timing": {"alignment": {"stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016", "start_time_utc": "Thu Apr 14 22:18:30 UTC 2016", "walltime_seconds": 60000}}, "overall_walltime_seconds": 60000, "overall_start_time_utc": "Thu Apr 14 22:18:30 UTC 2016"}}, "sample_attributes": {"example_sample_attribute": "EGAN00001000597"}, "submitter_sample_id": "PD41189-1T", "sequence_upload": {"workflow_description": "This is the upload of the fastq from a sample using the submission script__", "qc_metrics": {}, "workflow_bundle_url": "http://foo__bar/tool", "workflow_inputs": {}, "host_metrics": {"vm_instance_type": "m1__xlarge", "vm_instance_cores": 4, "vm_instance_mem_gb": 256, "vm_region": "us-east-1", "vm_location": "aws"}, "workflow_version": "1__0__0", "parent_uuids": ["e1156a51-6265-4d9a-9bc8-ebccf40126b5"], "workflow_source_url": "http://foo__bar/tool-src", "workflow_outputs": {"foo1b__fastq__gz": {"file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}, "foo2b__fastq__gz": {"file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}}, "analysis_attributes": {"sequencing_strategy": "WGS"}, "workflow_name": "fastq-submission", "timing_metrics": {}}, "sample_uuid": "e1156a51-6265-4d9a-9bc8-ebccf40126b5"}], "submitter_specimen_id": "PD41189T", "submitter_specimen_type": "Primary tumour - solid tissue", "specimen_attributes": {"example_specimen_attribute": "string"}, "specimen_uuid": "1bc259b7-3d87-4390-ae60-a92130651be4"}], "project": "BRCA-UK", "somatic_variant_calling": {"workflow_description": "This is the variant calling for specimen PD41189 from donor CGP_donor_1199138__", "timing_metrics": {"overall_stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016", "step_timing": {"variant_calling": {"stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016", "start_time_utc": "Thu Apr 14 22:18:30 UTC 2016", "walltime_seconds": 60000}}, "overall_walltime_seconds": 60000, "overall_start_time_utc": "Thu Apr 14 22:18:30 UTC 2016"}, "workflow_bundle_url": "http://foo__bar/sanger-workflow", "workflow_inputs": [{"file_storage_bundle_files": {"foo__bam__bai": {"file_storage_uri": "04731ba6-9d5a-42f8-a25a-bf6416d7f00a", "file_type_label": "bai", "file_type_cv_terms": ["EDAM:123232"]}, "foo__bam": {"file_storage_uri": "ae616ade-3734-4c48-a609-f2b292ecdbc7", "file_type_label": "bam", "file_type_cv_terms": ["EDAM:1293829"]}}, "file_storage_metadata_json_uri": "050a0b5b-ba9a-4200-96f8-fc7982f02416", "file_storage_bundle_uri": "b6525378-d904-4276-b42a-5cf01506ca8a"}], "host_metrics": {"vm_instance_type": "m1__xlarge", "vm_instance_cores": 4, "vm_instance_mem_gb": 256, "vm_region": "us-east-1", "vm_location": "aws"}, "workflow_version": "1__0__0", "parent_uuids": ["00d2116c-5640-4f07-b758-2d877470d684"], "analysis_attributes": {"use_ctrl": "PD41189", "assembly_short_name": "GRCh37"}, "workflow_source_url": "http://foo__bar/sanger-workflow-src", "workflow_params": {"param2": 2389239, "param1": 12121}, "workflow_name": "sanger-variant-calling", "qc_metrics": {"contamination_percent": 1.2, "variants_called": 3456423}, "workflow_outputs": {"foo__vcf": {"file_type_label": "vcf", "file_type_cv_terms": ["EDAM:12293829"]}, "foo__vcf__tbi": {"file_type_label": "tbi", "file_type_cv_terms": ["EDAM:2783392"]}}}, "donor_attributes": {"ega_sample_accession": "EGAN00001000597"}, "submitter_donor_id": "CGP_donor_1199138", "center_name": "WTSI", "donor_uuid": "00d2116c-5640-4f07-b758-2d877470d684", "flags": {"donor1_exists": 'true', "alignmentNormal_exists": 'true', "alignmentTumor_exists": 'true', "variantCalling_exists": 'true', "donor2_exists": 'true', "fastqNormal_exists": 'true', "fastqTumor_exists": 'true'}, "program": "ICGC", "normal_specimen": [{"samples": [{"alignment": {"workflow_description": "This is the alignment for specimen PD41189 from donor CGP_donor_1199138__", "qc_metrics": {"insert_size_sd": 313, "coverage_average": 123.4, "insert_size_average": 10456}, "workflow_inputs": [{"file_storage_bundle_files": {"foo2__fastq__gz": {"file_storage_uri": "9014505b-fa59-4913-a05c-4666c6efe198", "file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}, "foo1__fastq__gz": {"file_storage_uri": "ae616ade-3734-4c48-a609-f2b292ecdbc7", "file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}}, "file_storage_metadata_json_uri": "153c380c-0bcb-4ee9-abdf-629db73a62e5", "file_storage_bundle_uri": "0e99945c-631e-4123-9158-5132a8fe2150"}], "workflow_bundle_url": "http://foo__bar/bwa-workflow", "host_metrics": {"vm_instance_type": "m1__xlarge", "vm_instance_cores": 4, "vm_instance_mem_gb": 256, "vm_region": "us-east-1", "vm_location": "aws"}, "workflow_version": "1__0__0", "parent_uuids": ["0c653582-4087-41b5-ab51-15fbf5119be6"], "workflow_source_url": "http://foo__bar/bwa-workflow-src", "workflow_outputs": {"foo__bam__bai": {"file_type_label": "bai", "file_type_cv_terms": ["EDAM:278392"]}, "foo__bam": {"file_type_label": "bam", "file_type_cv_terms": ["EDAM:1293829"]}}, "workflow_params": {"param2": 2389239, "param1": 12121}, "workflow_name": "bwa-mem-alignment", "timing_metrics": {"overall_stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016", "step_timing": {"alignment": {"stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016", "start_time_utc": "Thu Apr 14 22:18:30 UTC 2016", "walltime_seconds": 60000}}, "overall_walltime_seconds": 60000, "overall_start_time_utc": "Thu Apr 14 22:18:30 UTC 2016"}}, "sample_attributes": {"example_sample_attribute": "EGAN00001000597"}, "submitter_sample_id": "PD41189-1", "sequence_upload": {"workflow_description": "This is the upload of the fastq from a sample using the submission script__", "qc_metrics": {}, "workflow_bundle_url": "http://foo__bar/tool", "workflow_inputs": {}, "host_metrics": {"vm_instance_type": "m1__xlarge", "vm_instance_cores": 4, "vm_instance_mem_gb": 256, "vm_region": "us-east-1", "vm_location": "aws"}, "workflow_version": "1__0__0", "parent_uuids": ["0c653582-4087-41b5-ab51-15fbf5119be6"], "workflow_source_url": "http://foo__bar/tool-src", "workflow_outputs": {"foo2__fastq__gz": {"file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}, "foo1__fastq__gz": {"file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}}, "analysis_attributes": {"sequencing_strategy": "WGS"}, "workflow_name": "fastq-submission", "timing_metrics": {}}, "sample_uuid": "0c653582-4087-41b5-ab51-15fbf5119be6"}], "submitter_specimen_id": "PD41189", "submitter_specimen_type": "Normal - solid tissue", "specimen_attributes": {"example_specimen_attribute": "string"}, "specimen_uuid": "3516639e-d480-415d-90e7-1566b41fd03e"}]},
   {"tumor_specimen": [{"samples": [{"sample_uuid": "e1156a51-6265-4d9a-9bc8-ebccf40126b5", "sample_attributes": {"example_sample_attribute": "EGAN00001000597"}, "submitter_sample_id": "PD41189-1T"}], "specimen_uuid": "1bc259b7-3d87-4390-ae60-a92130651be4", "specimen_attributes": {"example_specimen_attribute": "string"}, "submitter_specimen_id": "PD41189T", "submitter_specimen_type": "Primary tumour - solid tissue"}], "program": "ICGC", "flags": {"fastqNormal_exists": 'false', "alignmentTumor_exists": 'false', "variantCalling_exists": 'false', "donor1_exists": 'true', "fastqTumor_exists": 'false', "alignmentNormal_exists": 'false', "donor2_exists": 'true'}, "normal_specimen": [{"samples": [{"sample_uuid": "0c653582-4087-41b5-ab51-15fbf5119be6", "sample_attributes": {"example_sample_attribute": "EGAN00001000597"}, "submitter_sample_id": "PD41189-1"}], "specimen_uuid": "3516639e-d480-415d-90e7-1566b41fd03e", "specimen_attributes": {"example_specimen_attribute": "string"}, "submitter_specimen_id": "PD41189", "submitter_specimen_type": "Normal - solid tissue"}], "donor_attributes": {"ega_sample_accession": "EGAN00001000597"}, "donor_uuid": "00d2116c-5640-4f07-b758-2d877470d684", "center_name": "WTSI", "submitter_donor_id": "CGP_donor_1199138", "project": "BRCA-UK"},
   {"donor_uuid": "00d2116c-5640-4f07-b758-2d877470d684", "program": "ICGC", "center_name": "WTSI", "tumor_specimen": [{"samples": [{"sample_uuid": "e1156a51-6265-4d9a-9bc8-ebccf40126b5", "submitter_sample_id": "PD41189-1T", "sample_attributes": {"example_sample_attribute": "EGAN00001000597"}}], "submitter_specimen_id": "PD41189T", "specimen_attributes": {"example_specimen_attribute": "string"}, "specimen_uuid": "1bc259b7-3d87-4390-ae60-a92130651be4", "submitter_specimen_type": "Primary tumour - solid tissue"}], "submitter_donor_id": "CGP_donor_1199138", "project": "BRCA-UK", "donor_attributes": {"ega_sample_accession": "EGAN00001000597"}, "normal_specimen": [{"samples": [{"sample_uuid": "0c653582-4087-41b5-ab51-15fbf5119be6", "submitter_sample_id": "PD41189-1", "sample_attributes": {"example_sample_attribute": "EGAN00001000597"}, "sequence_upload": {"workflow_version": "1__0__0", "analysis_attributes": {"sequencing_strategy": "WGS"}, "workflow_name": "fastq-submission", "workflow_bundle_url": "http://foo__bar/tool", "workflow_description": "This is the upload of the fastq from a sample using the submission script__", "parent_uuids": ["0c653582-4087-41b5-ab51-15fbf5119be6"], "workflow_outputs": {"foo2__fastq__gz": {"file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}, "foo1__fastq__gz": {"file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}}, "host_metrics": {"vm_location": "aws", "vm_instance_cores": 4, "vm_instance_mem_gb": 256, "vm_region": "us-east-1", "vm_instance_type": "m1__xlarge"}, "qc_metrics": {}, "timing_metrics": {}, "workflow_inputs": {}, "workflow_source_url": "http://foo__bar/tool-src"}}], "submitter_specimen_id": "PD41189", "specimen_attributes": {"example_specimen_attribute": "string"}, "specimen_uuid": "3516639e-d480-415d-90e7-1566b41fd03e", "submitter_specimen_type": "Normal - solid tissue"}], "flags": {"donor1_exists": 'true', "alignmentTumor_exists": 'false', "fastqTumor_exists": 'false', "alignmentNormal_exists": 'false', "donor2_exists": 'true', "fastqNormal_exists": 'true', "variantCalling_exists": 'false'}},
   {"center_name": "WTSI", "project": "BRCA-UK", "submitter_donor_id": "CGP_donor_1199138", "program": "ICGC", "flags": {"fastqTumor_exists": 'false', "donor1_exists": 'true', "alignmentNormal_exists": 'true', "donor2_exists": 'true', "variantCalling_exists": 'false', "fastqNormal_exists": 'true', "alignmentTumor_exists": 'false'}, "normal_specimen": [{"submitter_specimen_type": "Normal - solid tissue", "specimen_attributes": {"example_specimen_attribute": "string"}, "submitter_specimen_id": "PD41189", "specimen_uuid": "3516639e-d480-415d-90e7-1566b41fd03e", "samples": [{"sample_uuid": "0c653582-4087-41b5-ab51-15fbf5119be6", "sample_attributes": {"example_sample_attribute": "EGAN00001000597"}, "alignment": {"timing_metrics": {"overall_stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016", "overall_walltime_seconds": 60000, "step_timing": {"alignment": {"walltime_seconds": 60000, "start_time_utc": "Thu Apr 14 22:18:30 UTC 2016", "stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016"}}, "overall_start_time_utc": "Thu Apr 14 22:18:30 UTC 2016"}, "workflow_params": {"param1": 12121, "param2": 2389239}, "workflow_name": "bwa-mem-alignment", "parent_uuids": ["0c653582-4087-41b5-ab51-15fbf5119be6"], "workflow_outputs": {"foo__bam__bai": {"file_type_cv_terms": ["EDAM:278392"], "file_type_label": "bai"}, "foo__bam": {"file_type_cv_terms": ["EDAM:1293829"], "file_type_label": "bam"}}, "host_metrics": {"vm_instance_type": "m1__xlarge", "vm_instance_mem_gb": 256, "vm_region": "us-east-1", "vm_instance_cores": 4, "vm_location": "aws"}, "workflow_version": "1__0__0", "workflow_description": "This is the alignment for specimen PD41189 from donor CGP_donor_1199138__", "workflow_source_url": "http://foo__bar/bwa-workflow-src", "qc_metrics": {"insert_size_sd": 313, "insert_size_average": 10456, "coverage_average": 123.4}, "workflow_inputs": [{"file_storage_metadata_json_uri": "153c380c-0bcb-4ee9-abdf-629db73a62e5", "file_storage_bundle_uri": "0e99945c-631e-4123-9158-5132a8fe2150", "file_storage_bundle_files": {"foo2__fastq__gz": {"file_type_cv_terms": ["EDAM:123232"], "file_type_label": "fastq", "file_storage_uri": "9014505b-fa59-4913-a05c-4666c6efe198"}, "foo1__fastq__gz": {"file_type_cv_terms": ["EDAM:123232"], "file_type_label": "fastq", "file_storage_uri": "ae616ade-3734-4c48-a609-f2b292ecdbc7"}}}], "workflow_bundle_url": "http://foo__bar/bwa-workflow"}, "submitter_sample_id": "PD41189-1", "sequence_upload": {"timing_metrics": {}, "analysis_attributes": {"sequencing_strategy": "WGS"}, "workflow_name": "fastq-submission", "parent_uuids": ["0c653582-4087-41b5-ab51-15fbf5119be6"], "workflow_outputs": {"foo2__fastq__gz": {"file_type_cv_terms": ["EDAM:123232"], "file_type_label": "fastq"}, "foo1__fastq__gz": {"file_type_cv_terms": ["EDAM:123232"], "file_type_label": "fastq"}}, "host_metrics": {"vm_location": "aws", "vm_instance_mem_gb": 256, "vm_region": "us-east-1", "vm_instance_type": "m1__xlarge", "vm_instance_cores": 4}, "workflow_version": "1__0__0", "workflow_description": "This is the upload of the fastq from a sample using the submission script__", "workflow_source_url": "http://foo__bar/tool-src", "qc_metrics": {}, "workflow_inputs": {}, "workflow_bundle_url": "http://foo__bar/tool"}}]}], "donor_uuid": "00d2116c-5640-4f07-b758-2d877470d684", "tumor_specimen": [{"submitter_specimen_type": "Primary tumour - solid tissue", "specimen_attributes": {"example_specimen_attribute": "string"}, "submitter_specimen_id": "PD41189T", "specimen_uuid": "1bc259b7-3d87-4390-ae60-a92130651be4", "samples": [{"sample_uuid": "e1156a51-6265-4d9a-9bc8-ebccf40126b5", "sample_attributes": {"example_sample_attribute": "EGAN00001000597"}, "submitter_sample_id": "PD41189-1T"}]}], "donor_attributes": {"ega_sample_accession": "EGAN00001000597"}},
   {"tumor_specimen": [{"specimen_uuid": "1bc259b7-3d87-4390-ae60-a92130651be4", "submitter_specimen_type": "Primary tumour - solid tissue", "samples": [{"sample_uuid": "e1156a51-6265-4d9a-9bc8-ebccf40126b5", "submitter_sample_id": "PD41189-1T", "sample_attributes": {"example_sample_attribute": "EGAN00001000597"}, "sequence_upload": {"workflow_bundle_url": "http://foo__bar/tool", "parent_uuids": ["e1156a51-6265-4d9a-9bc8-ebccf40126b5"], "workflow_description": "This is the upload of the fastq from a sample using the submission script__", "workflow_version": "1__0__0", "workflow_inputs": {}, "workflow_name": "fastq-submission", "qc_metrics": {}, "workflow_source_url": "http://foo__bar/tool-src", "workflow_outputs": {"foo2b__fastq__gz": {"file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}, "foo1b__fastq__gz": {"file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}}, "analysis_attributes": {"sequencing_strategy": "WGS"}, "host_metrics": {"vm_instance_mem_gb": 256, "vm_instance_type": "m1__xlarge", "vm_region": "us-east-1", "vm_instance_cores": 4, "vm_location": "aws"}, "timing_metrics": {}}, "alignment": {"workflow_bundle_url": "http://foo__bar/bwa-workflow", "parent_uuids": ["e1156a51-6265-4d9a-9bc8-ebccf40126b5"], "workflow_description": "This is the alignment for specimen PD41189 from donor CGP_donor_1199138__", "workflow_version": "1__0__0", "workflow_inputs": [{"file_storage_bundle_uri": "0e99945c-631e-4123-9158-5132a8fe2150", "file_storage_bundle_files": {"foo1__fastq__gz": {"file_type_label": "fastq", "file_storage_uri": "ae616ade-3734-4c48-a609-f2b292ecdbc7", "file_type_cv_terms": ["EDAM:123232"]}, "foo2__fastq__gz": {"file_type_label": "fastq", "file_storage_uri": "9014505b-fa59-4913-a05c-4666c6efe198", "file_type_cv_terms": ["EDAM:123232"]}}, "file_storage_metadata_json_uri": "153c380c-0bcb-4ee9-abdf-629db73a62e5"}], "workflow_name": "bwa-mem-alignment", "qc_metrics": {"insert_size_sd": 313, "insert_size_average": 10456, "coverage_average": 123.4}, "workflow_source_url": "http://foo__bar/bwa-workflow-src", "workflow_outputs": {"foo__bam": {"file_type_label": "bam", "file_type_cv_terms": ["EDAM:1293829"]}, "foo__bam__bai": {"file_type_label": "bai", "file_type_cv_terms": ["EDAM:278392"]}}, "workflow_params": {"param2": 2389239, "param1": 12121}, "host_metrics": {"vm_instance_cores": 4, "vm_location": "aws", "vm_region": "us-east-1", "vm_instance_mem_gb": 256, "vm_instance_type": "m1__xlarge"}, "timing_metrics": {"step_timing": {"alignment": {"start_time_utc": "Thu Apr 14 22:18:30 UTC 2016", "stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016", "walltime_seconds": 60000}}, "overall_walltime_seconds": 60000, "overall_start_time_utc": "Thu Apr 14 22:18:30 UTC 2016", "overall_stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016"}}}], "submitter_specimen_id": "PD41189T", "specimen_attributes": {"example_specimen_attribute": "string"}}], "flags": {"fastqNormal_exists": 'true', "fastqTumor_exists": 'true', "alignmentTumor_exists": 'true', "donor2_exists": 'true', "variantCalling_exists": 'false', "donor1_exists": 'true', "alignmentNormal_exists": 'true'}, "center_name": "WTSI", "submitter_donor_id": "CGP_donor_1199138", "project": "BRCA-UK", "program": "ICGC", "donor_attributes": {"ega_sample_accession": "EGAN00001000597"}, "donor_uuid": "00d2116c-5640-4f07-b758-2d877470d684", "normal_specimen": [{"specimen_uuid": "3516639e-d480-415d-90e7-1566b41fd03e", "submitter_specimen_type": "Normal - solid tissue", "samples": [{"sample_uuid": "0c653582-4087-41b5-ab51-15fbf5119be6", "submitter_sample_id": "PD41189-1", "sample_attributes": {"example_sample_attribute": "EGAN00001000597"}, "sequence_upload": {"workflow_bundle_url": "http://foo__bar/tool", "parent_uuids": ["0c653582-4087-41b5-ab51-15fbf5119be6"], "workflow_description": "This is the upload of the fastq from a sample using the submission script__", "workflow_version": "1__0__0", "workflow_inputs": {}, "workflow_name": "fastq-submission", "qc_metrics": {}, "workflow_source_url": "http://foo__bar/tool-src", "workflow_outputs": {"foo1__fastq__gz": {"file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}, "foo2__fastq__gz": {"file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}}, "analysis_attributes": {"sequencing_strategy": "WGS"}, "host_metrics": {"vm_instance_mem_gb": 256, "vm_instance_type": "m1__xlarge", "vm_region": "us-east-1", "vm_instance_cores": 4, "vm_location": "aws"}, "timing_metrics": {}}, "alignment": {"workflow_bundle_url": "http://foo__bar/bwa-workflow", "parent_uuids": ["0c653582-4087-41b5-ab51-15fbf5119be6"], "workflow_description": "This is the alignment for specimen PD41189 from donor CGP_donor_1199138__", "workflow_version": "1__0__0", "workflow_inputs": [{"file_storage_bundle_uri": "0e99945c-631e-4123-9158-5132a8fe2150", "file_storage_bundle_files": {"foo1__fastq__gz": {"file_type_label": "fastq", "file_storage_uri": "ae616ade-3734-4c48-a609-f2b292ecdbc7", "file_type_cv_terms": ["EDAM:123232"]}, "foo2__fastq__gz": {"file_type_label": "fastq", "file_storage_uri": "9014505b-fa59-4913-a05c-4666c6efe198", "file_type_cv_terms": ["EDAM:123232"]}}, "file_storage_metadata_json_uri": "153c380c-0bcb-4ee9-abdf-629db73a62e5"}], "workflow_name": "bwa-mem-alignment", "qc_metrics": {"insert_size_sd": 313, "insert_size_average": 10456, "coverage_average": 123.4}, "workflow_source_url": "http://foo__bar/bwa-workflow-src", "workflow_outputs": {"foo__bam": {"file_type_label": "bam", "file_type_cv_terms": ["EDAM:1293829"]}, "foo__bam__bai": {"file_type_label": "bai", "file_type_cv_terms": ["EDAM:278392"]}}, "workflow_params": {"param2": 2389239, "param1": 12121}, "host_metrics": {"vm_instance_cores": 4, "vm_location": "aws", "vm_region": "us-east-1", "vm_instance_mem_gb": 256, "vm_instance_type": "m1__xlarge"}, "timing_metrics": {"step_timing": {"alignment": {"start_time_utc": "Thu Apr 14 22:18:30 UTC 2016", "stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016", "walltime_seconds": 60000}}, "overall_walltime_seconds": 60000, "overall_start_time_utc": "Thu Apr 14 22:18:30 UTC 2016", "overall_stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016"}}}], "submitter_specimen_id": "PD41189", "specimen_attributes": {"example_specimen_attribute": "string"}}]},
   {"project": "BRCA-UK", "tumor_specimen": [{"samples": [{"sample_uuid": "e1156a51-6265-4d9a-9bc8-ebccf40126b5", "sequence_upload": {"workflow_description": "This is the upload of the fastq from a sample using the submission script__", "workflow_bundle_url": "http://foo__bar/tool", "qc_metrics": {}, "workflow_source_url": "http://foo__bar/tool-src", "workflow_outputs": {"foo1b__fastq__gz": {"file_type_cv_terms": ["EDAM:123232"], "file_type_label": "fastq"}, "foo2b__fastq__gz": {"file_type_cv_terms": ["EDAM:123232"], "file_type_label": "fastq"}}, "analysis_attributes": {"sequencing_strategy": "WGS"}, "workflow_name": "fastq-submission", "timing_metrics": {}, "parent_uuids": ["e1156a51-6265-4d9a-9bc8-ebccf40126b5"], "workflow_inputs": {}, "workflow_version": "1__0__0", "host_metrics": {"vm_instance_type": "m1__xlarge", "vm_location": "aws", "vm_instance_mem_gb": 256, "vm_region": "us-east-1", "vm_instance_cores": 4}}, "submitter_sample_id": "PD41189-1T", "sample_attributes": {"example_sample_attribute": "EGAN00001000597"}}], "submitter_specimen_type": "Primary tumour - solid tissue", "specimen_attributes": {"example_specimen_attribute": "string"}, "submitter_specimen_id": "PD41189T", "specimen_uuid": "1bc259b7-3d87-4390-ae60-a92130651be4"}], "flags": {"alignmentTumor_exists": 'false', "donor1_exists": 'true', "variantCalling_exists": 'false', "alignmentNormal_exists": 'true', "donor2_exists": 'true', "fastqTumor_exists": 'true', "fastqNormal_exists": 'true'}, "normal_specimen": [{"samples": [{"sample_uuid": "0c653582-4087-41b5-ab51-15fbf5119be6", "alignment": {"workflow_description": "This is the alignment for specimen PD41189 from donor CGP_donor_1199138__", "workflow_bundle_url": "http://foo__bar/bwa-workflow", "qc_metrics": {"coverage_average": 123.4, "insert_size_sd": 313, "insert_size_average": 10456}, "workflow_source_url": "http://foo__bar/bwa-workflow-src", "workflow_outputs": {"foo__bam__bai": {"file_type_cv_terms": ["EDAM:278392"], "file_type_label": "bai"}, "foo__bam": {"file_type_cv_terms": ["EDAM:1293829"], "file_type_label": "bam"}}, "workflow_params": {"param2": 2389239, "param1": 12121}, "workflow_name": "bwa-mem-alignment", "timing_metrics": {"step_timing": {"alignment": {"start_time_utc": "Thu Apr 14 22:18:30 UTC 2016", "walltime_seconds": 60000, "stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016"}}, "overall_stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016", "overall_walltime_seconds": 60000, "overall_start_time_utc": "Thu Apr 14 22:18:30 UTC 2016"}, "parent_uuids": ["0c653582-4087-41b5-ab51-15fbf5119be6"], "workflow_inputs": [{"file_storage_metadata_json_uri": "153c380c-0bcb-4ee9-abdf-629db73a62e5", "file_storage_bundle_uri": "0e99945c-631e-4123-9158-5132a8fe2150", "file_storage_bundle_files": {"foo1__fastq__gz": {"file_type_cv_terms": ["EDAM:123232"], "file_storage_uri": "ae616ade-3734-4c48-a609-f2b292ecdbc7", "file_type_label": "fastq"}, "foo2__fastq__gz": {"file_type_cv_terms": ["EDAM:123232"], "file_storage_uri": "9014505b-fa59-4913-a05c-4666c6efe198", "file_type_label": "fastq"}}}], "workflow_version": "1__0__0", "host_metrics": {"vm_instance_type": "m1__xlarge", "vm_location": "aws", "vm_instance_mem_gb": 256, "vm_region": "us-east-1", "vm_instance_cores": 4}}, "sequence_upload": {"workflow_description": "This is the upload of the fastq from a sample using the submission script__", "workflow_bundle_url": "http://foo__bar/tool", "qc_metrics": {}, "workflow_source_url": "http://foo__bar/tool-src", "workflow_outputs": {"foo1__fastq__gz": {"file_type_cv_terms": ["EDAM:123232"], "file_type_label": "fastq"}, "foo2__fastq__gz": {"file_type_cv_terms": ["EDAM:123232"], "file_type_label": "fastq"}}, "analysis_attributes": {"sequencing_strategy": "WGS"}, "workflow_name": "fastq-submission", "timing_metrics": {}, "parent_uuids": ["0c653582-4087-41b5-ab51-15fbf5119be6"], "workflow_inputs": {}, "workflow_version": "1__0__0", "host_metrics": {"vm_instance_type": "m1__xlarge", "vm_location": "aws", "vm_instance_mem_gb": 256, "vm_region": "us-east-1", "vm_instance_cores": 4}}, "submitter_sample_id": "PD41189-1", "sample_attributes": {"example_sample_attribute": "EGAN00001000597"}}], "submitter_specimen_type": "Normal - solid tissue", "specimen_attributes": {"example_specimen_attribute": "string"}, "submitter_specimen_id": "PD41189", "specimen_uuid": "3516639e-d480-415d-90e7-1566b41fd03e"}], "center_name": "WTSI", "program": "ICGC", "submitter_donor_id": "CGP_donor_1199138", "donor_uuid": "00d2116c-5640-4f07-b758-2d877470d684", "donor_attributes": {"ega_sample_accession": "EGAN00001000597"}},
   {"tumor_specimen": [{"samples": [{"alignment": {"workflow_description": "This is the alignment for specimen PD41189 from donor CGP_donor_1199138__", "qc_metrics": {"insert_size_sd": 313, "coverage_average": 123.4, "insert_size_average": 10456}, "workflow_inputs": [{"file_storage_bundle_files": {"foo2__fastq__gz": {"file_storage_uri": "9014505b-fa59-4913-a05c-4666c6efe198", "file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}, "foo1__fastq__gz": {"file_storage_uri": "ae616ade-3734-4c48-a609-f2b292ecdbc7", "file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}}, "file_storage_metadata_json_uri": "153c380c-0bcb-4ee9-abdf-629db73a62e5", "file_storage_bundle_uri": "0e99945c-631e-4123-9158-5132a8fe2150"}], "workflow_bundle_url": "http://foo__bar/bwa-workflow", "host_metrics": {"vm_instance_type": "m1__xlarge", "vm_instance_cores": 4, "vm_instance_mem_gb": 256, "vm_region": "us-east-1", "vm_location": "aws"}, "workflow_version": "1__0__0", "parent_uuids": ["e1156a51-6265-4d9a-9bc8-ebccf40126b5"], "workflow_source_url": "http://foo__bar/bwa-workflow-src", "workflow_outputs": {"foo__bam__bai": {"file_type_label": "bai", "file_type_cv_terms": ["EDAM:278392"]}, "foo__bam": {"file_type_label": "bam", "file_type_cv_terms": ["EDAM:1293829"]}}, "workflow_params": {"param2": 2389239, "param1": 12121}, "workflow_name": "bwa-mem-alignment", "timing_metrics": {"overall_stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016", "step_timing": {"alignment": {"stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016", "start_time_utc": "Thu Apr 14 22:18:30 UTC 2016", "walltime_seconds": 60000}}, "overall_walltime_seconds": 60000, "overall_start_time_utc": "Thu Apr 14 22:18:30 UTC 2016"}}, "sample_attributes": {"example_sample_attribute": "EGAN00001000597"}, "submitter_sample_id": "PD41189-1T", "sequence_upload": {"workflow_description": "This is the upload of the fastq from a sample using the submission script__", "qc_metrics": {}, "workflow_bundle_url": "http://foo__bar/tool", "workflow_inputs": {}, "host_metrics": {"vm_instance_type": "m1__xlarge", "vm_instance_cores": 4, "vm_instance_mem_gb": 256, "vm_region": "us-east-1", "vm_location": "aws"}, "workflow_version": "1__0__0", "parent_uuids": ["e1156a51-6265-4d9a-9bc8-ebccf40126b5"], "workflow_source_url": "http://foo__bar/tool-src", "workflow_outputs": {"foo1b__fastq__gz": {"file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}, "foo2b__fastq__gz": {"file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}}, "analysis_attributes": {"sequencing_strategy": "WGS"}, "workflow_name": "fastq-submission", "timing_metrics": {}}, "sample_uuid": "e1156a51-6265-4d9a-9bc8-ebccf40126b5"}], "submitter_specimen_id": "PD41189T", "submitter_specimen_type": "Primary tumour - solid tissue", "specimen_attributes": {"example_specimen_attribute": "string"}, "specimen_uuid": "1bc259b7-3d87-4390-ae60-a92130651be4"}], "project": "BRCA-UK", "somatic_variant_calling": {"workflow_description": "This is the variant calling for specimen PD41189 from donor CGP_donor_1199138__", "timing_metrics": {"overall_stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016", "step_timing": {"variant_calling": {"stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016", "start_time_utc": "Thu Apr 14 22:18:30 UTC 2016", "walltime_seconds": 60000}}, "overall_walltime_seconds": 60000, "overall_start_time_utc": "Thu Apr 14 22:18:30 UTC 2016"}, "workflow_bundle_url": "http://foo__bar/sanger-workflow", "workflow_inputs": [{"file_storage_bundle_files": {"foo__bam__bai": {"file_storage_uri": "04731ba6-9d5a-42f8-a25a-bf6416d7f00a", "file_type_label": "bai", "file_type_cv_terms": ["EDAM:123232"]}, "foo__bam": {"file_storage_uri": "ae616ade-3734-4c48-a609-f2b292ecdbc7", "file_type_label": "bam", "file_type_cv_terms": ["EDAM:1293829"]}}, "file_storage_metadata_json_uri": "050a0b5b-ba9a-4200-96f8-fc7982f02416", "file_storage_bundle_uri": "b6525378-d904-4276-b42a-5cf01506ca8a"}], "host_metrics": {"vm_instance_type": "m1__xlarge", "vm_instance_cores": 4, "vm_instance_mem_gb": 256, "vm_region": "us-east-1", "vm_location": "aws"}, "workflow_version": "1__0__0", "parent_uuids": ["00d2116c-5640-4f07-b758-2d877470d684"], "analysis_attributes": {"use_ctrl": "PD41189", "assembly_short_name": "GRCh37"}, "workflow_source_url": "http://foo__bar/sanger-workflow-src", "workflow_params": {"param2": 2389239, "param1": 12121}, "workflow_name": "sanger-variant-calling", "qc_metrics": {"contamination_percent": 1.2, "variants_called": 3456423}, "workflow_outputs": {"foo__vcf": {"file_type_label": "vcf", "file_type_cv_terms": ["EDAM:12293829"]}, "foo__vcf__tbi": {"file_type_label": "tbi", "file_type_cv_terms": ["EDAM:2783392"]}}}, "donor_attributes": {"ega_sample_accession": "EGAN00001000597"}, "submitter_donor_id": "CGP_donor_1199138", "center_name": "WTSI", "donor_uuid": "00d2116c-5640-4f07-b758-2d877470d684", "flags": {"donor1_exists": 'true', "alignmentNormal_exists": 'true', "alignmentTumor_exists": 'true', "variantCalling_exists": 'true', "donor2_exists": 'true', "fastqNormal_exists": 'true', "fastqTumor_exists": 'true'}, "program": "ICGC", "normal_specimen": [{"samples": [{"alignment": {"workflow_description": "This is the alignment for specimen PD41189 from donor CGP_donor_1199138__", "qc_metrics": {"insert_size_sd": 313, "coverage_average": 123.4, "insert_size_average": 10456}, "workflow_inputs": [{"file_storage_bundle_files": {"foo2__fastq__gz": {"file_storage_uri": "9014505b-fa59-4913-a05c-4666c6efe198", "file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}, "foo1__fastq__gz": {"file_storage_uri": "ae616ade-3734-4c48-a609-f2b292ecdbc7", "file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}}, "file_storage_metadata_json_uri": "153c380c-0bcb-4ee9-abdf-629db73a62e5", "file_storage_bundle_uri": "0e99945c-631e-4123-9158-5132a8fe2150"}], "workflow_bundle_url": "http://foo__bar/bwa-workflow", "host_metrics": {"vm_instance_type": "m1__xlarge", "vm_instance_cores": 4, "vm_instance_mem_gb": 256, "vm_region": "us-east-1", "vm_location": "aws"}, "workflow_version": "1__0__0", "parent_uuids": ["0c653582-4087-41b5-ab51-15fbf5119be6"], "workflow_source_url": "http://foo__bar/bwa-workflow-src", "workflow_outputs": {"foo__bam__bai": {"file_type_label": "bai", "file_type_cv_terms": ["EDAM:278392"]}, "foo__bam": {"file_type_label": "bam", "file_type_cv_terms": ["EDAM:1293829"]}}, "workflow_params": {"param2": 2389239, "param1": 12121}, "workflow_name": "bwa-mem-alignment", "timing_metrics": {"overall_stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016", "step_timing": {"alignment": {"stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016", "start_time_utc": "Thu Apr 14 22:18:30 UTC 2016", "walltime_seconds": 60000}}, "overall_walltime_seconds": 60000, "overall_start_time_utc": "Thu Apr 14 22:18:30 UTC 2016"}}, "sample_attributes": {"example_sample_attribute": "EGAN00001000597"}, "submitter_sample_id": "PD41189-1", "sequence_upload": {"workflow_description": "This is the upload of the fastq from a sample using the submission script__", "qc_metrics": {}, "workflow_bundle_url": "http://foo__bar/tool", "workflow_inputs": {}, "host_metrics": {"vm_instance_type": "m1__xlarge", "vm_instance_cores": 4, "vm_instance_mem_gb": 256, "vm_region": "us-east-1", "vm_location": "aws"}, "workflow_version": "1__0__0", "parent_uuids": ["0c653582-4087-41b5-ab51-15fbf5119be6"], "workflow_source_url": "http://foo__bar/tool-src", "workflow_outputs": {"foo2__fastq__gz": {"file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}, "foo1__fastq__gz": {"file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}}, "analysis_attributes": {"sequencing_strategy": "WGS"}, "workflow_name": "fastq-submission", "timing_metrics": {}}, "sample_uuid": "0c653582-4087-41b5-ab51-15fbf5119be6"}], "submitter_specimen_id": "PD41189", "submitter_specimen_type": "Normal - solid tissue", "specimen_attributes": {"example_specimen_attribute": "string"}, "specimen_uuid": "3516639e-d480-415d-90e7-1566b41fd03e"}]},
   {"tumor_specimen": [{"specimen_uuid": "1bc259b7-3d87-4390-ae60-a92130651be4", "submitter_specimen_type": "Primary tumour - solid tissue", "samples": [{"sample_uuid": "e1156a51-6265-4d9a-9bc8-ebccf40126b5", "submitter_sample_id": "PD41189-1T", "sample_attributes": {"example_sample_attribute": "EGAN00001000597"}, "sequence_upload": {"workflow_bundle_url": "http://foo__bar/tool", "parent_uuids": ["e1156a51-6265-4d9a-9bc8-ebccf40126b5"], "workflow_description": "This is the upload of the fastq from a sample using the submission script__", "workflow_version": "1__0__0", "workflow_inputs": {}, "workflow_name": "fastq-submission", "qc_metrics": {}, "workflow_source_url": "http://foo__bar/tool-src", "workflow_outputs": {"foo2b__fastq__gz": {"file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}, "foo1b__fastq__gz": {"file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}}, "analysis_attributes": {"sequencing_strategy": "WGS"}, "host_metrics": {"vm_instance_mem_gb": 256, "vm_instance_type": "m1__xlarge", "vm_region": "us-east-1", "vm_instance_cores": 4, "vm_location": "aws"}, "timing_metrics": {}}, "alignment": {"workflow_bundle_url": "http://foo__bar/bwa-workflow", "parent_uuids": ["e1156a51-6265-4d9a-9bc8-ebccf40126b5"], "workflow_description": "This is the alignment for specimen PD41189 from donor CGP_donor_1199138__", "workflow_version": "1__0__0", "workflow_inputs": [{"file_storage_bundle_uri": "0e99945c-631e-4123-9158-5132a8fe2150", "file_storage_bundle_files": {"foo1__fastq__gz": {"file_type_label": "fastq", "file_storage_uri": "ae616ade-3734-4c48-a609-f2b292ecdbc7", "file_type_cv_terms": ["EDAM:123232"]}, "foo2__fastq__gz": {"file_type_label": "fastq", "file_storage_uri": "9014505b-fa59-4913-a05c-4666c6efe198", "file_type_cv_terms": ["EDAM:123232"]}}, "file_storage_metadata_json_uri": "153c380c-0bcb-4ee9-abdf-629db73a62e5"}], "workflow_name": "bwa-mem-alignment", "qc_metrics": {"insert_size_sd": 313, "insert_size_average": 10456, "coverage_average": 123.4}, "workflow_source_url": "http://foo__bar/bwa-workflow-src", "workflow_outputs": {"foo__bam": {"file_type_label": "bam", "file_type_cv_terms": ["EDAM:1293829"]}, "foo__bam__bai": {"file_type_label": "bai", "file_type_cv_terms": ["EDAM:278392"]}}, "workflow_params": {"param2": 2389239, "param1": 12121}, "host_metrics": {"vm_instance_cores": 4, "vm_location": "aws", "vm_region": "us-east-1", "vm_instance_mem_gb": 256, "vm_instance_type": "m1__xlarge"}, "timing_metrics": {"step_timing": {"alignment": {"start_time_utc": "Thu Apr 14 22:18:30 UTC 2016", "stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016", "walltime_seconds": 60000}}, "overall_walltime_seconds": 60000, "overall_start_time_utc": "Thu Apr 14 22:18:30 UTC 2016", "overall_stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016"}}}], "submitter_specimen_id": "PD41189T", "specimen_attributes": {"example_specimen_attribute": "string"}}], "flags": {"fastqNormal_exists": 'true', "fastqTumor_exists": 'true', "alignmentTumor_exists": 'true', "donor2_exists": 'true', "variantCalling_exists": 'false', "donor1_exists": 'true', "alignmentNormal_exists": 'true'}, "center_name": "WTSI", "submitter_donor_id": "CGP_donor_1199138", "project": "BRCA-UK", "program": "ICGC", "donor_attributes": {"ega_sample_accession": "EGAN00001000597"}, "donor_uuid": "00d2116c-5640-4f07-b758-2d877470d684", "normal_specimen": [{"specimen_uuid": "3516639e-d480-415d-90e7-1566b41fd03e", "submitter_specimen_type": "Normal - solid tissue", "samples": [{"sample_uuid": "0c653582-4087-41b5-ab51-15fbf5119be6", "submitter_sample_id": "PD41189-1", "sample_attributes": {"example_sample_attribute": "EGAN00001000597"}, "sequence_upload": {"workflow_bundle_url": "http://foo__bar/tool", "parent_uuids": ["0c653582-4087-41b5-ab51-15fbf5119be6"], "workflow_description": "This is the upload of the fastq from a sample using the submission script__", "workflow_version": "1__0__0", "workflow_inputs": {}, "workflow_name": "fastq-submission", "qc_metrics": {}, "workflow_source_url": "http://foo__bar/tool-src", "workflow_outputs": {"foo1__fastq__gz": {"file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}, "foo2__fastq__gz": {"file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}}, "analysis_attributes": {"sequencing_strategy": "WGS"}, "host_metrics": {"vm_instance_mem_gb": 256, "vm_instance_type": "m1__xlarge", "vm_region": "us-east-1", "vm_instance_cores": 4, "vm_location": "aws"}, "timing_metrics": {}}, "alignment": {"workflow_bundle_url": "http://foo__bar/bwa-workflow", "parent_uuids": ["0c653582-4087-41b5-ab51-15fbf5119be6"], "workflow_description": "This is the alignment for specimen PD41189 from donor CGP_donor_1199138__", "workflow_version": "1__0__0", "workflow_inputs": [{"file_storage_bundle_uri": "0e99945c-631e-4123-9158-5132a8fe2150", "file_storage_bundle_files": {"foo1__fastq__gz": {"file_type_label": "fastq", "file_storage_uri": "ae616ade-3734-4c48-a609-f2b292ecdbc7", "file_type_cv_terms": ["EDAM:123232"]}, "foo2__fastq__gz": {"file_type_label": "fastq", "file_storage_uri": "9014505b-fa59-4913-a05c-4666c6efe198", "file_type_cv_terms": ["EDAM:123232"]}}, "file_storage_metadata_json_uri": "153c380c-0bcb-4ee9-abdf-629db73a62e5"}], "workflow_name": "bwa-mem-alignment", "qc_metrics": {"insert_size_sd": 313, "insert_size_average": 10456, "coverage_average": 123.4}, "workflow_source_url": "http://foo__bar/bwa-workflow-src", "workflow_outputs": {"foo__bam": {"file_type_label": "bam", "file_type_cv_terms": ["EDAM:1293829"]}, "foo__bam__bai": {"file_type_label": "bai", "file_type_cv_terms": ["EDAM:278392"]}}, "workflow_params": {"param2": 2389239, "param1": 12121}, "host_metrics": {"vm_instance_cores": 4, "vm_location": "aws", "vm_region": "us-east-1", "vm_instance_mem_gb": 256, "vm_instance_type": "m1__xlarge"}, "timing_metrics": {"step_timing": {"alignment": {"start_time_utc": "Thu Apr 14 22:18:30 UTC 2016", "stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016", "walltime_seconds": 60000}}, "overall_walltime_seconds": 60000, "overall_start_time_utc": "Thu Apr 14 22:18:30 UTC 2016", "overall_stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016"}}}], "submitter_specimen_id": "PD41189", "specimen_attributes": {"example_specimen_attribute": "string"}}]},
   {"project": "BRCA-UK", "tumor_specimen": [{"samples": [{"sample_uuid": "e1156a51-6265-4d9a-9bc8-ebccf40126b5", "sequence_upload": {"workflow_description": "This is the upload of the fastq from a sample using the submission script__", "workflow_bundle_url": "http://foo__bar/tool", "qc_metrics": {}, "workflow_source_url": "http://foo__bar/tool-src", "workflow_outputs": {"foo1b__fastq__gz": {"file_type_cv_terms": ["EDAM:123232"], "file_type_label": "fastq"}, "foo2b__fastq__gz": {"file_type_cv_terms": ["EDAM:123232"], "file_type_label": "fastq"}}, "analysis_attributes": {"sequencing_strategy": "WGS"}, "workflow_name": "fastq-submission", "timing_metrics": {}, "parent_uuids": ["e1156a51-6265-4d9a-9bc8-ebccf40126b5"], "workflow_inputs": {}, "workflow_version": "1__0__0", "host_metrics": {"vm_instance_type": "m1__xlarge", "vm_location": "aws", "vm_instance_mem_gb": 256, "vm_region": "us-east-1", "vm_instance_cores": 4}}, "submitter_sample_id": "PD41189-1T", "sample_attributes": {"example_sample_attribute": "EGAN00001000597"}}], "submitter_specimen_type": "Primary tumour - solid tissue", "specimen_attributes": {"example_specimen_attribute": "string"}, "submitter_specimen_id": "PD41189T", "specimen_uuid": "1bc259b7-3d87-4390-ae60-a92130651be4"}], "flags": {"alignmentTumor_exists": 'false', "donor1_exists": 'true', "variantCalling_exists": 'false', "alignmentNormal_exists": 'true', "donor2_exists": 'true', "fastqTumor_exists": 'true', "fastqNormal_exists": 'true'}, "normal_specimen": [{"samples": [{"sample_uuid": "0c653582-4087-41b5-ab51-15fbf5119be6", "alignment": {"workflow_description": "This is the alignment for specimen PD41189 from donor CGP_donor_1199138__", "workflow_bundle_url": "http://foo__bar/bwa-workflow", "qc_metrics": {"coverage_average": 123.4, "insert_size_sd": 313, "insert_size_average": 10456}, "workflow_source_url": "http://foo__bar/bwa-workflow-src", "workflow_outputs": {"foo__bam__bai": {"file_type_cv_terms": ["EDAM:278392"], "file_type_label": "bai"}, "foo__bam": {"file_type_cv_terms": ["EDAM:1293829"], "file_type_label": "bam"}}, "workflow_params": {"param2": 2389239, "param1": 12121}, "workflow_name": "bwa-mem-alignment", "timing_metrics": {"step_timing": {"alignment": {"start_time_utc": "Thu Apr 14 22:18:30 UTC 2016", "walltime_seconds": 60000, "stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016"}}, "overall_stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016", "overall_walltime_seconds": 60000, "overall_start_time_utc": "Thu Apr 14 22:18:30 UTC 2016"}, "parent_uuids": ["0c653582-4087-41b5-ab51-15fbf5119be6"], "workflow_inputs": [{"file_storage_metadata_json_uri": "153c380c-0bcb-4ee9-abdf-629db73a62e5", "file_storage_bundle_uri": "0e99945c-631e-4123-9158-5132a8fe2150", "file_storage_bundle_files": {"foo1__fastq__gz": {"file_type_cv_terms": ["EDAM:123232"], "file_storage_uri": "ae616ade-3734-4c48-a609-f2b292ecdbc7", "file_type_label": "fastq"}, "foo2__fastq__gz": {"file_type_cv_terms": ["EDAM:123232"], "file_storage_uri": "9014505b-fa59-4913-a05c-4666c6efe198", "file_type_label": "fastq"}}}], "workflow_version": "1__0__0", "host_metrics": {"vm_instance_type": "m1__xlarge", "vm_location": "aws", "vm_instance_mem_gb": 256, "vm_region": "us-east-1", "vm_instance_cores": 4}}, "sequence_upload": {"workflow_description": "This is the upload of the fastq from a sample using the submission script__", "workflow_bundle_url": "http://foo__bar/tool", "qc_metrics": {}, "workflow_source_url": "http://foo__bar/tool-src", "workflow_outputs": {"foo1__fastq__gz": {"file_type_cv_terms": ["EDAM:123232"], "file_type_label": "fastq"}, "foo2__fastq__gz": {"file_type_cv_terms": ["EDAM:123232"], "file_type_label": "fastq"}}, "analysis_attributes": {"sequencing_strategy": "WGS"}, "workflow_name": "fastq-submission", "timing_metrics": {}, "parent_uuids": ["0c653582-4087-41b5-ab51-15fbf5119be6"], "workflow_inputs": {}, "workflow_version": "1__0__0", "host_metrics": {"vm_instance_type": "m1__xlarge", "vm_location": "aws", "vm_instance_mem_gb": 256, "vm_region": "us-east-1", "vm_instance_cores": 4}}, "submitter_sample_id": "PD41189-1", "sample_attributes": {"example_sample_attribute": "EGAN00001000597"}}], "submitter_specimen_type": "Normal - solid tissue", "specimen_attributes": {"example_specimen_attribute": "string"}, "submitter_specimen_id": "PD41189", "specimen_uuid": "3516639e-d480-415d-90e7-1566b41fd03e"}], "center_name": "WTSI", "program": "ICGC", "submitter_donor_id": "CGP_donor_1199138", "donor_uuid": "00d2116c-5640-4f07-b758-2d877470d684", "donor_attributes": {"ega_sample_accession": "EGAN00001000597"}},
   {"tumor_specimen": [{"specimen_uuid": "1bc259b7-3d87-4390-ae60-a92130651be4", "submitter_specimen_type": "Primary tumour - solid tissue", "samples": [{"sample_uuid": "e1156a51-6265-4d9a-9bc8-ebccf40126b5", "submitter_sample_id": "PD41189-1T", "sample_attributes": {"example_sample_attribute": "EGAN00001000597"}, "sequence_upload": {"workflow_bundle_url": "http://foo__bar/tool", "parent_uuids": ["e1156a51-6265-4d9a-9bc8-ebccf40126b5"], "workflow_description": "This is the upload of the fastq from a sample using the submission script__", "workflow_version": "1__0__0", "workflow_inputs": {}, "workflow_name": "fastq-submission", "qc_metrics": {}, "workflow_source_url": "http://foo__bar/tool-src", "workflow_outputs": {"foo2b__fastq__gz": {"file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}, "foo1b__fastq__gz": {"file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}}, "analysis_attributes": {"sequencing_strategy": "WGS"}, "host_metrics": {"vm_instance_mem_gb": 256, "vm_instance_type": "m1__xlarge", "vm_region": "us-east-1", "vm_instance_cores": 4, "vm_location": "aws"}, "timing_metrics": {}}, "alignment": {"workflow_bundle_url": "http://foo__bar/bwa-workflow", "parent_uuids": ["e1156a51-6265-4d9a-9bc8-ebccf40126b5"], "workflow_description": "This is the alignment for specimen PD41189 from donor CGP_donor_1199138__", "workflow_version": "1__0__0", "workflow_inputs": [{"file_storage_bundle_uri": "0e99945c-631e-4123-9158-5132a8fe2150", "file_storage_bundle_files": {"foo1__fastq__gz": {"file_type_label": "fastq", "file_storage_uri": "ae616ade-3734-4c48-a609-f2b292ecdbc7", "file_type_cv_terms": ["EDAM:123232"]}, "foo2__fastq__gz": {"file_type_label": "fastq", "file_storage_uri": "9014505b-fa59-4913-a05c-4666c6efe198", "file_type_cv_terms": ["EDAM:123232"]}}, "file_storage_metadata_json_uri": "153c380c-0bcb-4ee9-abdf-629db73a62e5"}], "workflow_name": "bwa-mem-alignment", "qc_metrics": {"insert_size_sd": 313, "insert_size_average": 10456, "coverage_average": 123.4}, "workflow_source_url": "http://foo__bar/bwa-workflow-src", "workflow_outputs": {"foo__bam": {"file_type_label": "bam", "file_type_cv_terms": ["EDAM:1293829"]}, "foo__bam__bai": {"file_type_label": "bai", "file_type_cv_terms": ["EDAM:278392"]}}, "workflow_params": {"param2": 2389239, "param1": 12121}, "host_metrics": {"vm_instance_cores": 4, "vm_location": "aws", "vm_region": "us-east-1", "vm_instance_mem_gb": 256, "vm_instance_type": "m1__xlarge"}, "timing_metrics": {"step_timing": {"alignment": {"start_time_utc": "Thu Apr 14 22:18:30 UTC 2016", "stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016", "walltime_seconds": 60000}}, "overall_walltime_seconds": 60000, "overall_start_time_utc": "Thu Apr 14 22:18:30 UTC 2016", "overall_stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016"}}}], "submitter_specimen_id": "PD41189T", "specimen_attributes": {"example_specimen_attribute": "string"}}], "flags": {"fastqNormal_exists": 'true', "fastqTumor_exists": 'true', "alignmentTumor_exists": 'true', "donor2_exists": 'true', "variantCalling_exists": 'false', "donor1_exists": 'true', "alignmentNormal_exists": 'true'}, "center_name": "WTSI", "submitter_donor_id": "CGP_donor_1199138", "project": "BRCA-UK", "program": "ICGC", "donor_attributes": {"ega_sample_accession": "EGAN00001000597"}, "donor_uuid": "00d2116c-5640-4f07-b758-2d877470d684", "normal_specimen": [{"specimen_uuid": "3516639e-d480-415d-90e7-1566b41fd03e", "submitter_specimen_type": "Normal - solid tissue", "samples": [{"sample_uuid": "0c653582-4087-41b5-ab51-15fbf5119be6", "submitter_sample_id": "PD41189-1", "sample_attributes": {"example_sample_attribute": "EGAN00001000597"}, "sequence_upload": {"workflow_bundle_url": "http://foo__bar/tool", "parent_uuids": ["0c653582-4087-41b5-ab51-15fbf5119be6"], "workflow_description": "This is the upload of the fastq from a sample using the submission script__", "workflow_version": "1__0__0", "workflow_inputs": {}, "workflow_name": "fastq-submission", "qc_metrics": {}, "workflow_source_url": "http://foo__bar/tool-src", "workflow_outputs": {"foo1__fastq__gz": {"file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}, "foo2__fastq__gz": {"file_type_label": "fastq", "file_type_cv_terms": ["EDAM:123232"]}}, "analysis_attributes": {"sequencing_strategy": "WGS"}, "host_metrics": {"vm_instance_mem_gb": 256, "vm_instance_type": "m1__xlarge", "vm_region": "us-east-1", "vm_instance_cores": 4, "vm_location": "aws"}, "timing_metrics": {}}, "alignment": {"workflow_bundle_url": "http://foo__bar/bwa-workflow", "parent_uuids": ["0c653582-4087-41b5-ab51-15fbf5119be6"], "workflow_description": "This is the alignment for specimen PD41189 from donor CGP_donor_1199138__", "workflow_version": "1__0__0", "workflow_inputs": [{"file_storage_bundle_uri": "0e99945c-631e-4123-9158-5132a8fe2150", "file_storage_bundle_files": {"foo1__fastq__gz": {"file_type_label": "fastq", "file_storage_uri": "ae616ade-3734-4c48-a609-f2b292ecdbc7", "file_type_cv_terms": ["EDAM:123232"]}, "foo2__fastq__gz": {"file_type_label": "fastq", "file_storage_uri": "9014505b-fa59-4913-a05c-4666c6efe198", "file_type_cv_terms": ["EDAM:123232"]}}, "file_storage_metadata_json_uri": "153c380c-0bcb-4ee9-abdf-629db73a62e5"}], "workflow_name": "bwa-mem-alignment", "qc_metrics": {"insert_size_sd": 313, "insert_size_average": 10456, "coverage_average": 123.4}, "workflow_source_url": "http://foo__bar/bwa-workflow-src", "workflow_outputs": {"foo__bam": {"file_type_label": "bam", "file_type_cv_terms": ["EDAM:1293829"]}, "foo__bam__bai": {"file_type_label": "bai", "file_type_cv_terms": ["EDAM:278392"]}}, "workflow_params": {"param2": 2389239, "param1": 12121}, "host_metrics": {"vm_instance_cores": 4, "vm_location": "aws", "vm_region": "us-east-1", "vm_instance_mem_gb": 256, "vm_instance_type": "m1__xlarge"}, "timing_metrics": {"step_timing": {"alignment": {"start_time_utc": "Thu Apr 14 22:18:30 UTC 2016", "stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016", "walltime_seconds": 60000}}, "overall_walltime_seconds": 60000, "overall_start_time_utc": "Thu Apr 14 22:18:30 UTC 2016", "overall_stop_time_utc": "Thu Apr 14 24:18:30 UTC 2016"}}}], "submitter_specimen_id": "PD41189", "specimen_attributes": {"example_specimen_attribute": "string"}}]}
]

#loading above json_docs
for i in json_docs:
   res = es.index("es-index", es_type, i)
   es.indices.refresh(index="es-index")

#checking the number of documents
res = es.search(index="es-index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
   print("%(center_name)s %(program)s: %(project)s" % hit["_source"])

#querying documents using queries above
for q_index in range(len(es_queries)):
   response = es.search(index="es-index", body=es_queries[q_index])
   #print(json.dumps(response, indent=2))
   for p in response['aggregations']['project_f']['project'].get('buckets'):
      count = p.get('doc_count')
      donors = p.get('donor_id').get('buckets')
      project = p.get('key')
   
   print(es_name_query[q_index])
   print("count:",count)
   print("donors:",donors)
   print("project: "+project+"\n")