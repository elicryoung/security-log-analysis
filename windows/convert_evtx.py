from Evtx.Evtx import Evtx

# This script converts .evtx files to XML format for easier analysis.
input_file = "windows/2.DACL_DCSync_Right_Powerview_ Add-DomainObjectAcl.evtx"
output_file = "dcsync.xml"

# Convert the .evtx file to XML format
with Evtx(input_file) as log:
    with open(output_file, "w") as f: # Open the output file for writing
        for record in log.records(): # Iterate through each record in the .evtx file
            f.write(record.xml()) # Write the XML representation of the record to the output file
            f.write("\n") # Add a newline after each record for better readability



input_file = "windows/3.LM_typical_IIS_webshell_sysmon_1_10_traces.evtx"
output_file = "webshell.xml"

with Evtx(input_file) as log:
    with open(output_file, "w") as f:
        for record in log.records():
            f.write(record.xml())
            f.write("\n")