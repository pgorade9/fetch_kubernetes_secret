# fetch_kubernetes_secret
Fetch Kubernetes Secret given a secret name
Sample code to add new entry in keyvault configurations:
**********************************************************************************************************************************
with open(DESKTOP_CONFIGURATION_PY, "w") as fp:
    for env in env_list:
        # data_partitions key was added
        # keyvault.get(env).update({"data_partitions": [keyvault[env]["data_partition_id"]]})
        
        # target_kind_item was added
        # target_kind_item = {"target_kind": {
        #     "csv_parser_wf_status_gsm": "csvparser:test:csvparser:1.0.0",
        #     "wellbore_ingestion_wf_gsm": "osdu:wks:work-product-component--WellboreTrajectory:1.1.0",
        #     "doc_ingestor_azure_ocr_wf": f"{keyvault[env]['data_partition_id']}:sourceTest:document:1.0.0",
        #     "shapefile_ingestor_wf_status_gsm": f"{keyvault[env]['data_partition_id']}:test:shapefile:1.0.0"
        # }}
        # if not env.endswith('ltops'):
        #     target_kind_item.get("target_kind").update({"Osdu_ingest": f"{keyvault[env]['data_partition_id']}:wks:Manifest:1.0.0"})
        # keyvault.get(env).update(target_kind_item)
        
        # dw_dn_host was added
        if env.endswith("ltops"):
            dw_dns_host = {"dw_dns_host":"https://evt-dw.app.evt-1.lightops.slb.com"}
            keyvault.get(env).update(dw_dns_host)
    fp.write(f"keyvault = {json.dumps(keyvault, indent=4)}")
**********************************************************************************************************************************