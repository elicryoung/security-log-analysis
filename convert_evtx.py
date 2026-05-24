from Evtx.Evtx import Evtx

input_file = "windows/2.DACL_DCSync_Right_Powerview_ Add-DomainObjectAcl.evtx"
output_file = "dcsync.xml"

with Evtx(input_file) as log:
    with open(output_file, "w") as f:
        for record in log.records():
            f.write(record.xml())
            f.write("\n")



input_file = "windows/3.LM_typical_IIS_webshell_sysmon_1_10_traces.evtx"
output_file = "webshell.xml"

with Evtx(input_file) as log:

    with open(output_file, "w") as f:

        for record in log.records():

            f.write(record.xml())

            f.write("\n")