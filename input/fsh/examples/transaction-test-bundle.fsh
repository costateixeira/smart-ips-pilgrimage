Alias: $loinc = http://loinc.org

// this is a Bundle to post to a test server



Instance: bundle-transaction
InstanceOf: Bundle
Usage: #example
* meta.lastUpdated = "2014-08-18T01:43:30Z"
* type = #transaction
* entry[0]
  * fullUrl = "urn:uuid:61ebe359-bfdc-4613-8bf2-100000000001"
  * resource = List1
  * request
    * method = #PUT
    * url = "List/List1"
* entry[+]
  * fullUrl = "urn:uuid:61ebe359-bfdc-4613-8bf2-100000000002"
  * resource = List2
  * request
    * method = #PUT
    * url = "List/List2"
* entry[+]
  * fullUrl = "urn:uuid:61ebe359-bfdc-4613-8bf2-100000000003"
  * resource = List3
  * request
    * method = #PUT
    * url = "List/List3"

* entry[+]
  * fullUrl = "urn:uuid:61ebe359-bfdc-4613-8bf2-200000000001"
  * resource = DocRef1
  * request
    * method = #PUT
    * url = "DocRef1"
* entry[+]
  * fullUrl = "urn:uuid:61ebe359-bfdc-4613-8bf2-200000000002"
  * resource = DocRef2
  * request
    * method = #PUT
    * url = "DocumentReference/DocRef2"
// * entry[+]
//   * fullUrl = "urn:uuid:61ebe359-bfdc-4613-8bf2-200000000003"
//   * resource = DocRef3
//   * request
//     * method = #PUT
//     * url = "DocumentReference/DocRef3"



Instance: List1
InstanceOf: Folder
Usage: #example
* title = "This is the good folder"
//* subject.reference = "Patient/2b90dd2b-2dab-4c75-9bb9-a355e07401e8" 
* status = #current
* entry.item = Reference (DocRef1)


Instance: List2
InstanceOf: Folder
Usage: #example
* title = "This is an old folder"
//* subject.reference = "Patient/2b90dd2b-2dab-4c75-9bb9-a355e07401e8" 
* status = #retired


Instance: List3
InstanceOf: List
Usage: #example
* mode = #working
* title = "This is another type of list"
* code = #some-other-list
* status = #current
//* subject.reference = "Patient/2b90dd2b-2dab-4c75-9bb9-a355e07401e8" 



Instance: DocRef1
InstanceOf: DocumentReference
Title:      "DocumentReference for Comprehensive fully filled metadata for a document in a Binary"
Description: "For bundling Example of a Comprehensive DocumentReference resource."
Usage: #example
* meta.security = http://terminology.hl7.org/CodeSystem/v3-ActReason#HTEST
* status = #current
* type = http://loinc.org#60591-5
* category = http://loinc.org#11369-6
* date = 2020-02-01T23:50:50-05:00
* content.format = http://ihe.net/fhir/ihe.formatcode.fhir/CodeSystem/formatcode#urn:ihe:iti:xds-sd:text:2008
* content.attachment.url = "urn:uuid:cccccccc-2222-0000-0000-000000000002"
* content.attachment.contentType = #text/plain
* content.attachment.hash = "MGE0ZDU1YThkNzc4ZTUwMjJmYWI3MDE5NzdjNWQ4NDBiYmM0ODZkMA=="
* content.attachment.size = 11



Instance:   DocRef2
InstanceOf: DocumentReference
Title:      "DocumentReference for IPS document Bundle"
Description: "Example of a DocumentReference for an IPS document bundle."
Usage: #example
* meta.security = http://terminology.hl7.org/CodeSystem/v3-ActReason#HTEST
* status = #current
* type = http://loinc.org#60591-5
* category = http://loinc.org#11369-6
* date = 2020-02-01T23:50:50-05:00
* content.format = http://ihe.net/fhir/ihe.formatcode.fhir/CodeSystem/formatcode#urn:ihe:pcc:ips:2020
* content.attachment.url = "/Bundle/myIPS"
* content.attachment.contentType = #application/json+fhir



// 



//Instance: DocRef3
// InstanceOf: DocumentReference
// Title: "Dummy Binary document that says: Hello World"
// Description: """
// For Bundling Example binary that 
// - holds \"Hello World\"
// - size 11
// - hash 0a4d55a8d778e5022fab701977c5d840bbc486d0
// - base64 of the hash MGE0ZDU1YThkNzc4ZTUwMjJmYWI3MDE5NzdjNWQ4NDBiYmM0ODZkMA==
// """
// Usage: #example
// * meta.security = http://terminology.hl7.org/CodeSystem/v3-ActReason#HTEST
// * contentType = #text/plain
// * data = "SGVsbG8gV29ybGQ="




