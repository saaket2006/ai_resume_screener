from enum import Enum

class UserRole(str, Enum):
    UNASSIGNED = "UNASSIGNED"
    RECRUITER = "RECRUITER"
    CANDIDATE = "CANDIDATE"

class CompanyType(str, Enum):
    STARTUP = "Startup"
    SME = "SME"
    ENTERPRISE = "Enterprise"
    MNC = "MNC"
    GOVERNMENT = "Government"
    EDUCATIONAL_INSTITUTION = "Educational Institution"
    CONSULTANCY = "Consultancy"
    NON_PROFIT = "Non-Profit"
    OTHER = "Other"
