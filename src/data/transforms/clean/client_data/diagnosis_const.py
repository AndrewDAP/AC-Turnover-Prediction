"""
Corpus information
"""
DIAGNOSIS_CORPUS_FILE_NAME = "client_diagnosis_corpus_frequency.json"
DIAGNOSIS_CORPUS_FILE_PATH = "src/data/transforms/clean/client_data"

"""
Certain terms are composed from a textual value and a numerical value
For the words in the list, we want to concatenate numbers that follow to their root
"""
COMPOSED_TERMS_ROOTS = ["stage", "ckd", "covid", "type", "non"]

"""
In a diagnosis, certain details are added following the key words in the list
This additional information are considered to have a "inverted impact" when it comes to analyzing
the text and must be removed
    Ex: "Cirrhosis of liver, non alcohol"
        Using traditional tokenization methods, the sentence would be tokenized as ["Cirrhosis, "liver", "alcohol"] 
        The token "alcohol" would then skew the analysis by removing the concept that it was "non alcohol"
"""
TRAILING_KEY_WORDS = ["without", "except", "not"]

"""
These characters are found inside strings and must be replaced to tokenize words correctly
the ""iii" and "ii" are transformed to numerical values to add specification to certain cases
"""
REPLACEABLE_CHARACTERS = [
    ("=", " "),
    ("-", " "),
    ("/", ""),
    ("non", "non-"),
    ("iii", "3"),
    ("ii", "2"),
]

"""
This list was made by reading through the client_data.csv DIAGNOSIS column
Mostly contains ambiguous words that are found in large quantities
Symbols and medical abbreviations are also listed
"""
CUSTOM_STOP_WORDS = [
    "h/o",
    "hx",
    "history",
    "unspecified",
    "site",
    "part",
    "due",
    "specified",
    "new",
    "diagnoses",
    "primary",
    "secondary",
    "presence",
    "cause",
    "since",
    "previous",
    "assessment",
    "other",
    "age",
    "related",
    "initial",
    "encounter",
    "closed",
    "elsewhere",
    "classified",
    "onset",
    "use",
    "current",
    "acquired",
    "right",
    "left",
    "rt",
    "r/t",
    "le",
    "(",
    ")",
    "[",
    "]",
    "'s",
    ",",
    "/",
    "x2",
    ".",
    ":",
    ";",
]
