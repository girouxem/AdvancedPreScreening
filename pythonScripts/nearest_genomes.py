# Using the new NCBI's datasets API to get the nearest available reference genomes for a given taxon or organism name.
# Input: TAX_ID or Name
# Output:
#     1- The nearest organism with available reference genomes
#     2- Accessions of the reference genomes
# Requirements:
# pip install --upgrade ncbi-datasets-pylib

import sys
import ncbi.datasets.openapi
from ncbi.datasets.openapi.api import taxonomy_api
from ncbi.datasets.openapi.model.v1_taxonomy_metadata_request import V1TaxonomyMetadataRequest
from ncbi.datasets.openapi.model.rpc_status import RpcStatus
from ncbi.datasets.openapi.model.v1_taxonomy_metadata_request_content_type import V1TaxonomyMetadataRequestContentType
from ncbi.datasets.openapi.model.v1_taxonomy_metadata_response import V1TaxonomyMetadataResponse
from ncbi.datasets.openapi import ApiClient as DatasetsApiClient
from ncbi.datasets import GenomeApi
import pprint
import argparse # eg testing

configuration = ncbi.datasets.openapi.Configuration(
    host="https://api.ncbi.nlm.nih.gov/datasets/v1"
)

# Optional API KEY
configuration.api_key_prefix['ApiKeyAuthHeader'] = '7f4be04d1855def2fe2aa44c9e2b94bc9a09' 

def nearest_available_taxon(lineage: list):
    with DatasetsApiClient() as api_client:
        api = GenomeApi(api_client)
        taxon = str(lineage.pop())
        response = api.assembly_descriptors_by_taxon(
            taxon=taxon,
            async_req=True,
            filters_reference_only = True,
            )
        result = response.get().to_dict()
        if "total_count" in result:
            accessions = [assembly["assembly"]["assembly_accession"] for assembly in result["assemblies"]]
            return (taxon, accessions)
        else:
            return nearest_available_taxon(lineage)        


def fetch_tax_info(tax_or_name):
    with ncbi.datasets.openapi.ApiClient(configuration) as api_client:
        api_instance = taxonomy_api.TaxonomyApi(api_client)
        v1_taxonomy_metadata_request = V1TaxonomyMetadataRequest(
            taxons=[str(tax_or_name)],
            returned_content=V1TaxonomyMetadataRequestContentType("COMPLETE"),
        ) 
        try:
            # Use taxonomic identifiers to get taxonomic metadata by post
            api_response = api_instance.taxonomy_metadata_post(v1_taxonomy_metadata_request)
            return api_response.to_dict()
        except ncbi.datasets.openapi.ApiException as e:
            print(f"Exception when calling TaxonomyApi->taxonomy_metadata_post: {e}")

def nearest_genomes(tax_or_name):
    organism_tax_or_name = tax_or_name
    info = fetch_tax_info(organism_tax_or_name)["taxonomy_nodes"][0]["taxonomy"]
    organism_name = info["organism_name"]
    organism_taxon = info["tax_id"]
    children = info["children"]
    full_lineage = info["lineage"] + [organism_taxon]
    nearest_taxon, accessions = nearest_available_taxon(full_lineage)
    nearest_organism_name = fetch_tax_info(nearest_taxon)["taxonomy_nodes"][0]["taxonomy"]["organism_name"]
    accns = accessions
    return accns
    
def nearest_genomes2(tax_or_name):
    organism_tax_or_name = tax_or_name
    info = fetch_tax_info(organism_tax_or_name)["taxonomy_nodes"][0]["taxonomy"]
    organism_name = info["organism_name"]
    organism_taxon = info["tax_id"]
    children = info["children"]
    full_lineage = info["lineage"] + [organism_taxon]
    nearest_taxon, accessions = nearest_available_taxon(full_lineage)
    nearest_organism_name = fetch_tax_info(nearest_taxon)["taxonomy_nodes"][0]["taxonomy"]["organism_name"]
    accns = accessions
    return accns

if __name__ == "__main__":
    organism_tax_or_name = "Aleurina"
    #organism_tax_or_name = input()
    #organism_tax_or_name = sys.argv()
    info = fetch_tax_info(organism_tax_or_name)["taxonomy_nodes"][0]["taxonomy"]
    organism_name = info["organism_name"]
    organism_taxon = info["tax_id"]
    children = info["children"]
    full_lineage = info["lineage"] + [organism_taxon]
    nearest_taxon, accessions = nearest_available_taxon(full_lineage)
    nearest_organism_name = fetch_tax_info(nearest_taxon)["taxonomy_nodes"][0]["taxonomy"]["organism_name"]

    print(f"query:             organism({organism_name}) taxon({organism_taxon})")
    print(f"nearest_available: organism({nearest_organism_name}) taxon({nearest_taxon})")
    print(f"found {len(accessions)} accessions.")
    print('-' * 20)
    pprint.pprint(accessions)
    #print(accessions) #  eg testing
