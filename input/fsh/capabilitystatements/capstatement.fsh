Instance: VHLDocumentResponderCapStatement
InstanceOf: CapabilityStatement
Usage: #definition
* url = "https://smart.who.int/smart-pilgrimage/CapabilityStatement/VHLDocumentResponder"
* name = "VHL DocumentResponder"
* title = "VHL Document Responder (server)"
* status = #active
* experimental = false
* date = "2024-12-31"
* description = "VHL Responder (server)."
* kind = #requirements
* fhirVersion = #4.0.1
* format[0] = #application/fhir+xml
* format[+] = #application/fhir+json
* imports = "https://profiles.ihe.net/ITI/MHD/CapabilityStatement/IHE.MHD.DocumentResponder"
* rest
  * mode = #server
  * resource[+]
    * type = #List
    // * profile = "https://profiles.ihe.net/ITI/MHD/StructureDefinition/IHE.MHD.List"
    // * supportedProfile[0] = "https://profiles.ihe.net/ITI/MHD/StructureDefinition/IHE.MHD.UnContained.Comprehensive.SubmissionSet"
    // * supportedProfile[+] = "https://profiles.ihe.net/ITI/MHD/StructureDefinition/IHE.MHD.Comprehensive.SubmissionSet"
    // * supportedProfile[+] = "https://profiles.ihe.net/ITI/MHD/StructureDefinition/IHE.MHD.Minimal.SubmissionSet"
    // * supportedProfile[+] = "https://profiles.ihe.net/ITI/MHD/StructureDefinition/IHE.MHD.Comprehensive.Folder"
    // * supportedProfile[+] = "https://profiles.ihe.net/ITI/MHD/StructureDefinition/IHE.MHD.Minimal.Folder"
    // * interaction[0].code = #read
    // * interaction[+].code = #search-type
    * searchParam[0]
      * name = "_include"
      * definition = "http://hl7.org/fhir/build/SearchParameter/Resource-_list"
      * type = #special
      * documentation = "Servers is IHE extension on parameters defined as SearchParameter/List-SourceId, of type token, specifies the source (author) value supplied in the List Resource."

