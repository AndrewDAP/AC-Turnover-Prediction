"""
Corpus information
"""
SERVICE_DESCRIPTION_CORPUS_FILE_NAME = (
    "visits_service_description_corpus_frequency.json"
)
SERVICE_DESCRIPTION_CORPUS_FILE_PATH = "src/data/transforms/clean/visit_data"

"""
Minimal frequency of words for tokenization
"""
MIN_FREQUENCY = 500

"""
Most common token equivalents
"""
HHA_TOKENS = ("home", "health", "aide")
HOMEMAKER_TOKENS = ("homemaker",)
CERTIFIED_NURSE_ASSISTANT_TOKENS = ("certified", "nurse", "assistant")
LONG_TERM_CARE_TOKENS = ("long", "term", "care")
WORKERS_COMPENSATION_TOKENS = ("WORKERS", "COMPENSATION")
AIDE_TOKENS = ("aide",)
PRIVATE_TOKENS = ("private",)
LIVE_IN_TOKENS = ("live", "in")
WEEKEND_TOKENS = ("weekend",)
WEEKDAY_TOKENS = ("weekday",)
VISIT_TOKENS = ("visit",)
GROUP_TOKENS = ("group",)
VETERANS_AFFAIR_TOKENS = ("veterans", "affair")

"""
- Dictionary of common errors, typos and abbreviations found in the service descriptions of visits as keys 
  and equivalent terms as values
"""
EQUIVALENT_TERMS = {
    "hha": HHA_TOKENS,
    "haa": HHA_TOKENS,
    "hhg": HHA_TOKENS,
    "hhw": HHA_TOKENS,
    "hh": HHA_TOKENS,
    "chha": HHA_TOKENS,
    "h": HHA_TOKENS,
    "hhha": HHA_TOKENS,
    "hhav": HHA_TOKENS + VISIT_TOKENS,
    "hhag": HHA_TOKENS + GROUP_TOKENS,
    "hhaw": HHA_TOKENS + WEEKEND_TOKENS,
    "hhava": HHA_TOKENS + VETERANS_AFFAIR_TOKENS,
    "hhagw": HHA_TOKENS + GROUP_TOKENS + WEEKEND_TOKENS,
    "hhaltc": HHA_TOKENS + LONG_TERM_CARE_TOKENS,
    "hmkr": HOMEMAKER_TOKENS,
    "hmrk": HOMEMAKER_TOKENS,
    "cna": CERTIFIED_NURSE_ASSISTANT_TOKENS,
    "cnav": CERTIFIED_NURSE_ASSISTANT_TOKENS + VISIT_TOKENS,
    "cnaw": CERTIFIED_NURSE_ASSISTANT_TOKENS + WEEKEND_TOKENS,
    "ltc": LONG_TERM_CARE_TOKENS,
    "ltci": LONG_TERM_CARE_TOKENS,
    "w/c": WORKERS_COMPENSATION_TOKENS,
    "wc": WORKERS_COMPENSATION_TOKENS,
    "aid": AIDE_TOKENS,
    "aig": AIDE_TOKENS,
    "prv": PRIVATE_TOKENS,
    "priv": PRIVATE_TOKENS,
    "pvt": PRIVATE_TOKENS,
    "g": GROUP_TOKENS,
    "li": LIVE_IN_TOKENS,
    "liv": LIVE_IN_TOKENS,
    "weeke": WEEKEND_TOKENS,
    "weeken": WEEKEND_TOKENS,
    "weekkend": WEEKEND_TOKENS,
    "weekknd": WEEKEND_TOKENS,
    "weekdend": WEEKEND_TOKENS,
    "weekwend": WEEKEND_TOKENS,
    "weeked": WEEKEND_TOKENS,
    "weekends": WEEKEND_TOKENS,
    "weeekend": WEEKEND_TOKENS,
    "w": WEEKEND_TOKENS,
    "wkend": WEEKEND_TOKENS,
    "wknd": WEEKEND_TOKENS,
    "wd": WEEKDAY_TOKENS,
    "wday": WEEKDAY_TOKENS,
    "wkday": WEEKDAY_TOKENS,
    "weday": WEEKDAY_TOKENS,
    "wekday": WEEKDAY_TOKENS,
    "weekkday": WEEKDAY_TOKENS,
    "weekeday": WEEKDAY_TOKENS,
    "v": VISIT_TOKENS,
    "va": VETERANS_AFFAIR_TOKENS,
    "pp": ("private", "pay"),
    "comp": ("compensation",),
    "tra": ("training",),
    "pc": ("personal", "care"),
    "uncomp": ("uncompensated",),
    "rn": ("registered", "nurse"),
    "assesment": ("assessment",),
    "rc": ("respite", "care"),
    "ccn": ("community", "care", "network"),
}

"""
Mask to remove words from the NLTK stopwords list
"""
STOP_WORDS_MASK = ["in"]

"""
  - Custom stopwords
  - Created by looking at the SERVICE_DESCRIPTION corpus, copying the words with a higher frequency than 
    the minimum cutoff and and removing the words we want to keep
"""
CUSTOM_STOP_WORDS = [
    "nwt",
    "hun",
    "hrs",
    "snl",
    "hours",
    "week",
    "ctr",
    "acr",
    "cac",
    "f",
    "wk",
    "hrly",
    "assoc",
    "hr",
    "dba",
    "ah",
    "ccn",
    "h",
    "clsrm",
    "victor",
    "giunco",
    "ega",
    "res",
    "supv",
    "cm",
    "hour",
    "atria",
    "living",
    "well",
    "x",
    "tuesday",
    "wee",
    "comp",
    "premium",
    "c",
    "max",
    "quinton",
    "short",
    "current",
    "mgh",
    "per",
    "rnv",
    "v",
    "brighthouse",
    "mf",
    "unit",
    "nnl",
    "tricare",
    "compliance",
    "tra",
    "policy",
    "blend",
    "year",
    "matt",
    "account",
    "kk",
    "bwh",
    "mor",
    "ins",
    "john",
    "hancock",
    "new",
    "contact",
    "triwest",
    "landing",
    "lac",
    "acsp",
    "duty",
    "hnj",
    "cs",
    "paradigm",
    "vcn",
    "weeks",
    "single",
    "donagh",
    "arvada",
    "arc",
    "camden",
    "county",
    "ply",
    "elsie",
    "gee",
    "njm",
    "dch",
    "mal",
    "e",
    "thru",
    "payor",
    "trust",
    "jewish",
    "family",
    "funder",
    "united",
    "dud",
    "genworth",
    "red",
    "overnight",
    "lisa",
    "bass",
    "one",
    "call",
    "insurance",
    "minutes",
    "waiver",
    "less",
    "block",
    "wendy",
    "lewis",
    "diem",
    "yr",
    "msf",
    "prn",
    "ms",
    "society",
    "wg",
    "cw",
    "kerry",
    "wpt",
    "mayflower",
    "weekly",
    "use",
    "philly",
    "vv",
    "virtual",
    "advsrs",
    "monday",
    "friday",
    "kim",
    "metlife",
    "summit",
    "place",
    "jh",
]
