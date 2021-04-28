"""
Genetic Relationship and Fingerprinting
---------------------------------------

GRAF is a package that allows estmation or relatedness and ancestry.

Relatedness
+++++++++++

.. csv-table::
    :header: name, dtype, description

    ID1, string,
    ID2, string,
    HG_match, int, number of SNPs with matched genotypes when only homozygous SNPs are counted
    HG_miss, int, number of SNPs with mismatched genotypes when only homozygous SNPs are counted
    HGMR, float, Homozygous Genotype Mismatch Rate (%)
    AG_match, int, number of SNPs with matched genotypes when all SNPs are counted
    AG_miss, int, number of SNPs with mismatched genotypes when all SNPs are counted
    AGMR, float, All Genotype Mismatch Rate (%)
    relationship, string, relationship determined by sample genotypes.
    p_value, float, probability that the genetic relationship is NOT the predicted type

Relationship Values
*******************

Categories are assigned by GRAF.

.. csv-table::
    :header: name, description

    ID, duplicate or MZ twin
    PO, parent-offspring
    FS, full sibling
    D2, 2nd degree relative
    D3, 3rd degree relative
    UN, unrelated

References:
    - https://github.com/ncbi/graf
    - Jin Y, Schäffer AA, Sherry ST, and Feolo M (2017). Quickly identifying
      identical and closely related subjects in large databases using genotype
      data. PLoS One. 12(6):e0179106.
"""
import pandas as pd

from cgr_gwas_qc.typing import PathLike

DTYPES = {
    "ID1": "string",
    "ID2": "string",
    "HG_match": "UInt32",
    "HG_miss": "UInt32",
    "HGMR": "float",
    "AG_match": "UInt32",
    "AG_miss": "UInt32",
    "AGMR": "float",
    "relationship": "string",
    "p_value": "float",
}


def read_relatedness(filename: PathLike) -> pd.DataFrame:
    """Reads the table generated by ``graf --out``

    Returns:
        pd.DataFrame

        - ID1
        - ID2
        - HG_match
        - HG_miss
        - HGMR
        - AG_match
        - AG_miss
        - AGMR
        - relationship {ID, PO, FS, D2, D3, UN}
        - p_value

    References:
        - https://github.com/ncbi/graf#output-files
    """

    def _sort_ids(x: pd.Series) -> pd.Series:
        x["ID1"], x["ID2"] = sorted([x.sample1, x.sample2])
        return x

    return (
        pd.read_csv(filename, sep="\t", comment="#")
        .apply(_sort_ids, axis=1)
        .rename(
            {
                "HG match": "HG_match",
                "HG miss": "HG_miss",
                "AG match": "AG_match",
                "AG miss": "AG_miss",
                "geno relation": "relationship",
            },
            axis=1,
        )
        .reindex(DTYPES.keys(), axis=1)
    )
