import spacy
from typing import List
import re

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    pass

# A comprehensive list of real-world technical skills to ensure accuracy
TECH_SKILLS = {
    "python", "java", "javascript", "c++", "c#", "ruby", "go", "php", "typescript", "swift",
    "html", "css", "react", "angular", "vue", "django", "flask", "fastapi", "spring", "express",
    "node.js", "next.js", "bootstrap", "tailwind", "jquery", "sass", "less",
    "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "cassandra", "oracle",
    "sqlite", "dynamodb", "mariadb", "couchdb",
    "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "terraform", "ansible",
    "git", "linux", "jira", "agile", "scrum", "kanban", "github", "gitlab", "bitbucket",
    "machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch", 
    "scikit-learn", "keras", "pandas", "numpy", "matplotlib", "seaborn", "data analysis", 
    "data science", "data engineering", "big data", "hadoop", "spark", "kafka", "airflow", 
    "tableau", "power bi", "excel", "nosql", "ci/cd", "devops", "mlops", "data visualization",
    "rest", "graphql", "soap", "microservices", "serverless", "blockchain", "web3", "smart contracts",
    "solidity", "rust", "kotlin", "scala", "dart", "flutter", "react native", "xamarin",
    "unity", "unreal engine", "game development", "ar/vr", "ui/ux", "figma", "adobe xd", "sketch",
    "photoshop", "illustrator", "premiere pro", "after effects", "invision", "zeplin",
    "cybersecurity", "penetration testing", "ethical hacking", "cryptography", "network security",
    "information security", "vulnerability assessment", "incident response", "digital forensics",
    "system administration", "network administration", "bash", "powershell", "shell scripting",
    "c", "objective-c", "ruby on rails", "laravel", "codeigniter", "symfony", "cakephp", "yii",
    "zend framework", "meteor", "ember.js", "backbone.js", "polymer", "aurelia", "meteor.js",
    "rxjs", "ngrx", "redux", "mobx", "vuex", "apollo", "relay", "webpack", "babel", "parcel",
    "rollup", "gulp", "grunt", "npm", "yarn", "bower", "composer", "pip", "conda", "maven",
    "gradle", "ant", "make", "cmake", "gcc", "clang", "gdb", "lldb", "valgrind", "profiling",
    "debugging", "testing", "unit testing", "integration testing", "e2e testing", "tdd", "bdd",
    "pytest", "unittest", "rspec", "jest", "mocha", "jasmine", "karma", "cypress", "selenium",
    "puppeteer", "playwright", "appium", "postman", "swagger", "openapi", "grpc", "websockets",
    "webrtc", "socket.io", "oauth", "jwt", "saml", "openid connect", "sso", "iam", "active directory",
    "ldap", "kerberos", "radius", "tacacs", "vpn", "ipsec", "ssl/tls", "ssh", "ftp", "sftp",
    "smtp", "pop3", "imap", "http/https", "dns", "dhcp", "tcp/ip", "udp", "icmp", "bgp", "ospf",
    "eigrp", "rip", "vlan", "stp", "vxlan", "sdn", "nfv", "openflow", "netconf", "restconf",
    "yang", "snmp", "syslog", "netflow", "sflow", "ipfix", "packet capture", "wireshark",
    "tcpdump", "nmap", "metasploit", "burp suite", "owasp zap", "nessus", "openvas", "qualys",
    "nexpose", "alienvault", "splunk", "arcsight", "qradar", "logstash", "kibana", "fluentd",
    "graylog", "datadog", "new relic", "appdynamics", "dynatrace", "prometheus", "grafana",
    "zabbix", "nagios", "sensu", "icinga", "pagerduty", "opsgenie", "victorops", "slack",
    "microsoft teams", "zoom", "webex", "confluence", "notion", "trello", "asana", "monday.com",
    "smartsheet", "airtable", "salesforce", "hubspot", "marketo", "pardot", "mailchimp",
    "sendgrid", "twilio", "stripe", "braintree", "paypal", "authorize.net", "shopify", "magento",
    "woocommerce", "bigcommerce", "wordpress", "drupal", "joomla", "ghost", "strapi", "contentful",
    "sanity", "prismic", "netlify", "vercel", "heroku", "digitalocean", "linode", "vultr",
    "cloudflare", "fastly", "akamai", "nginx", "apache", "iis", "tomcat", "jboss", "weblogic",
    "websphere", "glassfish", "jetty", "puma", "unicorn", "gunicorn", "uwsgi", "mod_wsgi",
    "celery", "rabbitmq", "activemq", "zeromq", "sqs", "sns", "kinesis", "eventbridge",
    "step functions", "lambda", "ecs", "eks", "fargate", "s3", "ebs", "efs", "fsx", "glacier",
    "rds", "aurora", "redshift", "athena", "emr", "glue", "sagemaker", "rekognition",
    "polly", "lex", "kendra", "comprehend", "translate", "transcribe", "textract", "forecast",
    "personalize", "fraud detector", "lookout for vision", "lookout for equipment", "panorama",
    "monitron", "iot core", "iot greengrass", "iot analytics", "iot events", "iot sitewise",
    "genai", "generative ai", "llm", "large language models", "prompt engineering", "langchain", "agents",
    
    # --- Broad Semantic Categories (Needed so the JD Extractor captures them to trigger expansions) ---
    "web development", "software development", "software engineering", "backend development", "frontend development",
    "backend", "frontend", "full stack", "fullstack", "machine learning", "artificial intelligence", "ai",
    "data science", "databases", "cloud computing", "devops", "object-oriented programming", "oop", "nlp"
}

def extract_skills(text: str) -> List[str]:
    """
    Extracts key skills and technical terms using a robust hybrid approach:
    1. A comprehensive predefined dictionary of real-world technical skills
    2. Structural acronym extraction (e.g. API, AWS, CI/CD)
    """
    doc = nlp(text)
    skills = set()
    text_lower = text.lower()
    
    # 1. Exact match from predefined comprehensive dictionary
    for skill in TECH_SKILLS:
        if skill in text_lower:
            # Avoid partial matches inside other words (like "c" inside "react")
            pattern = r'(?<![a-zA-Z0-9\-])' + re.escape(skill) + r'(?![a-zA-Z0-9\-])'
            if re.search(pattern, text_lower):
                skills.add(skill)
                
    # 2. Extract Acronyms dynamically using Regex (e.g., API, HTTP)
    for token in doc:
        is_acronym = bool(re.match(r'^[A-Z]{2,}(/[A-Z]{2,})?$', token.text))
        if is_acronym:
            skills.add(token.text.lower())
            
    return sorted(list(skills))
