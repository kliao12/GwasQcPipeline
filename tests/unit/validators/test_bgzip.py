"""Test BGZIP validation.

Since this is a binary format, it would be really hard to test individual
issues. For now I am just testing that a good file passes.
"""
from cgr_gwas_qc.validators.bgzip import validate


def test_good_vcf_file_vaidates(vcf_file):
    validate(vcf_file)


def test_good_tbi_file_vaidates(vcf_file):
    validate(vcf_file.with_suffix(".gz.tbi"))
