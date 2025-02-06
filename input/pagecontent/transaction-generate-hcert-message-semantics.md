The [SHL specifications](https://build.fhir.org/ig/HL7/smart-health-cards-and-links/links-specification.html)shall be followed to create a [HCERT](https://www.smart.who.int/trust/StructureDefinition-Hcert.html) within a [CWT structure](https://www.smart.who.int/trust/StructureDefinition-CWT.html).

- Generate VHL
- Build VHL manifest json that points to signed pdf content
- Generate VHLink  URL for Manifest
- Construct VHLink Payload
  - Minified
  - Base64urlencoded
  - Prefixed with shlink:/
  - Build HCERT containing SHL 
  - Build CWT with header payload and signature
