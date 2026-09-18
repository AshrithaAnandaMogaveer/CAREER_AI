"""
Resume Analyzer Module
Handles PDF/DOC text extraction and NLP-based skill extraction
"""

import re
import PyPDF2
import docx
import spacy
from io import BytesIO
from typing import List, Dict, Set

# Load spaCy model (download with: python -m spacy download en_core_web_sm)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")


# Comprehensive skill dictionary
SKILL_DICTIONARY = {
    # Programming Languages
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'php', 
    'swift', 'kotlin', 'go', 'rust', 'scala', 'r', 'matlab', 'perl', 'shell',
    'bash', 'powershell', 'sql', 'html', 'css', 'sass', 'less',
    
    # Frameworks & Libraries
    'react', 'angular', 'vue', 'svelte', 'next.js', 'nuxt', 'gatsby',
    'django', 'flask', 'fastapi', 'express', 'nest.js', 'spring', 'spring boot',
    'laravel', 'rails', 'asp.net', '.net', 'node.js', 'nodejs',
    'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy',
    'matplotlib', 'seaborn', 'opencv', 'nltk', 'spacy',
    
    # Databases
    'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 'dynamodb',
    'oracle', 'sql server', 'sqlite', 'elasticsearch', 'neo4j', 'firebase',
    
    # Cloud & DevOps
    'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'k8s',
    'jenkins', 'gitlab ci', 'github actions', 'terraform', 'ansible',
    'ci/cd', 'microservices', 'serverless', 'lambda',
    
    # Tools & Technologies
    'git', 'github', 'gitlab', 'bitbucket', 'jira', 'confluence',
    'postman', 'swagger', 'rest api', 'graphql', 'grpc', 'websocket',
    'nginx', 'apache', 'linux', 'unix', 'windows server',
    
    # Data & Analytics
    'machine learning', 'deep learning', 'nlp', 'computer vision',
    'data analysis', 'data science', 'big data', 'hadoop', 'spark',
    'tableau', 'power bi', 'looker', 'data visualization',
    'statistics', 'predictive modeling', 'a/b testing',
    
    # Methodologies
    'agile', 'scrum', 'kanban', 'waterfall', 'devops', 'tdd', 'bdd',
    'design patterns', 'solid principles', 'clean code', 'refactoring',
    
    # Soft Skills
    'leadership', 'communication', 'teamwork', 'problem solving',
    'critical thinking', 'time management', 'project management',
    'collaboration', 'mentoring', 'presentation', 'negotiation',
    
    # Design
    'ui/ux', 'figma', 'sketch', 'adobe xd', 'photoshop', 'illustrator',
    'wireframing', 'prototyping', 'user research', 'responsive design',
    
    # Security
    'cybersecurity', 'penetration testing', 'owasp', 'encryption',
    'authentication', 'authorization', 'oauth', 'jwt', 'ssl/tls',
    
    # Mobile
    'android', 'ios', 'react native', 'flutter', 'xamarin', 'ionic',
    
    # Testing
    'unit testing', 'integration testing', 'e2e testing', 'jest',
    'pytest', 'junit', 'selenium', 'cypress', 'test automation',
    
    # Other
    'blockchain', 'web3', 'solidity', 'smart contracts', 'iot',
    'ar/vr', 'game development', 'unity', 'unreal engine'
}

# Skill synonyms for normalization
SKILL_SYNONYMS = {
    'js': 'javascript',
    'ts': 'typescript',
    'py': 'python',
    'k8s': 'kubernetes',
    'ml': 'machine learning',
    'dl': 'deep learning',
    'ai': 'artificial intelligence',
    'db': 'database',
    'api': 'rest api',
    'ci/cd': 'continuous integration',
    'aws': 'amazon web services',
    'gcp': 'google cloud platform',
}


class ResumeAnalyzer:
    """Analyzes resumes to extract skills and metadata"""
    
    def __init__(self):
        self.nlp = nlp
        self.skill_dict = SKILL_DICTIONARY
        self.synonyms = SKILL_SYNONYMS
    
    def extract_text_from_pdf(self, file_stream: BytesIO) -> str:
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(file_stream)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise Exception(f"PDF extraction failed: {str(e)}")
    
    def extract_text_from_docx(self, file_stream: BytesIO) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_stream)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            raise Exception(f"DOCX extraction failed: {str(e)}")
    
    def extract_text(self, file_stream: BytesIO, filename: str) -> str:
        """Extract text based on file type"""
        if filename.lower().endswith('.pdf'):
            return self.extract_text_from_pdf(file_stream)
        elif filename.lower().endswith(('.doc', '.docx')):
            return self.extract_text_from_docx(file_stream)
        else:
            raise Exception("Unsupported file format")
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep alphanumeric and common punctuation
        text = re.sub(r'[^\w\s\-\+\#\./]', ' ', text)
        return text.strip()
    
    def normalize_skill(self, skill: str) -> str:
        """Normalize skill name"""
        skill = skill.lower().strip()
        # Check synonyms
        if skill in self.synonyms:
            return self.synonyms[skill]
        return skill
    
    def extract_skills_from_text(self, text: str) -> Set[str]:
        """Extract skills using NLP and dictionary matching"""
        text_lower = text.lower()
        extracted_skills = set()
        
        # Method 1: Direct dictionary matching
        for skill in self.skill_dict:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                extracted_skills.add(skill)
        
        # Method 2: NLP-based extraction
        doc = self.nlp(text)
        
        # Extract noun chunks that might be skills
        for chunk in doc.noun_chunks:
            normalized = self.normalize_skill(chunk.text)
            if normalized in self.skill_dict:
                extracted_skills.add(normalized)
        
        # Extract named entities (ORG, PRODUCT might be technologies)
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT', 'GPE']:
                normalized = self.normalize_skill(ent.text)
                if normalized in self.skill_dict:
                    extracted_skills.add(normalized)
        
        return extracted_skills
    
    def extract_experience_years(self, text: str) -> int:
        """Extract years of experience from text"""
        patterns = [
            r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
            r'experience\s*:?\s*(\d+)\+?\s*years?',
            r'(\d+)\+?\s*yrs?\s+(?:of\s+)?experience',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return int(match.group(1))
        
        return 0
    
    def extract_projects(self, text: str) -> List[str]:
        """Extract project descriptions"""
        projects = []
        
        # Look for project sections
        project_patterns = [
            r'projects?\s*:?\s*(.*?)(?=\n\n|\nexperience|\neducation|\nskills|$)',
            r'key\s+projects?\s*:?\s*(.*?)(?=\n\n|\nexperience|\neducation|\nskills|$)',
        ]
        
        for pattern in project_patterns:
            matches = re.finditer(pattern, text.lower(), re.DOTALL)
            for match in matches:
                project_text = match.group(1).strip()
                if project_text:
                    # Split by bullet points or line breaks
                    project_items = re.split(r'[\n•\-\*]', project_text)
                    projects.extend([p.strip() for p in project_items if p.strip() and len(p.strip()) > 20])
        
        return projects[:5]  # Return top 5 projects
    
    def extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        certifications = []
        
        # Look for certification sections
        cert_patterns = [
            r'certifications?\s*:?\s*(.*?)(?=\n\n|\nexperience|\neducation|\nskills|$)',
            r'certificates?\s*:?\s*(.*?)(?=\n\n|\nexperience|\neducation|\nskills|$)',
        ]
        
        for pattern in cert_patterns:
            matches = re.finditer(pattern, text.lower(), re.DOTALL)
            for match in matches:
                cert_text = match.group(1).strip()
                if cert_text:
                    # Split by bullet points or line breaks
                    cert_items = re.split(r'[\n•\-\*]', cert_text)
                    certifications.extend([c.strip() for c in cert_items if c.strip() and len(c.strip()) > 5])
        
        return certifications[:10]  # Return top 10 certifications
    
    def analyze_resume(self, file_stream: BytesIO, filename: str) -> Dict:
        """Complete resume analysis"""
        # Extract text
        raw_text = self.extract_text(file_stream, filename)
        cleaned_text = self.clean_text(raw_text)
        
        # Extract information
        skills = self.extract_skills_from_text(cleaned_text)
        experience_years = self.extract_experience_years(cleaned_text)
        projects = self.extract_projects(cleaned_text)
        certifications = self.extract_certifications(cleaned_text)
        
        return {
            'raw_text': raw_text,
            'cleaned_text': cleaned_text,
            'extracted_skills': sorted(list(skills)),
            'experience_years': experience_years,
            'projects': projects,
            'certifications': certifications,
            'total_skills': len(skills),
            'has_projects': len(projects) > 0,
            'has_certifications': len(certifications) > 0,
        }
