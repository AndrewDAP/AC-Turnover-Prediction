"""
Corpus information
"""
JOB_TITLE_CORPUS_FILE_NAME = "employee_job_title_corpus_frequency.json"
JOB_TITLE_CORPUS_FILE_PATH = "src/data/transforms/clean/employee_data"

"""
Token equivalents
"""
HHA_TOKENS = ("home", "health", "aide")
CERTIFIED_NURSE_ASSISTANT_TOKENS = ("certified", "nurse", "assistant")

"""
Dictionary of abbreviations found in the job titles as keys and equivalent terms as values
"""
EQUIVALENT_TERMS = {
    "hha": HHA_TOKENS,
    "cna": CERTIFIED_NURSE_ASSISTANT_TOKENS,
}
