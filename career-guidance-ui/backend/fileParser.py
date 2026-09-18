"""
File Parser Module
Extracts skill data from uploaded PDF/DOCX analysis reports
"""

import json
import PyPDF2
from docx import Document
import re
from typing import Dict, List, Any


class FileParser:
    def __init__(self):
        self.skill_keywords = [
            # Tech skills
            'Python', 'JavaScript', 'React', 'Node.js',
            'SQL', 'MongoDB', 'Docker', 'Kubernetes', 'AWS', 'Azure',
            'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch',
            'Statistics', 'Data Science', 'DevOps', 'Git',
            'Pandas', 'NumPy', 'NLP', 'Computer Vision',
            # Product Management skills
            'Product Strategy', 'Roadmapping', 'Agile', 'Scrum',
            'User Stories', 'Stakeholder Management', 'A/B Testing',
            'Data Analysis', 'Jira', 'Confluence', 'Analytics',
            'Product Discovery', 'OKRs', 'KPIs', 'Market Research',
            'Competitive Analysis', 'Go-to-Market Strategy',
            'Customer Journey Mapping', 'Prioritization',
            # UI/UX skills
            'Figma', 'Wireframing', 'Prototyping', 'User Research',
            'Usability Testing', 'Design Systems', 'Adobe XD',
            # Mobile skills
            'React Native', 'Flutter', 'Swift', 'Kotlin',
            # Cybersecurity skills
            'Penetration Testing', 'Networking', 'Encryption',
            'Cybersecurity', 'OWASP', 'Linux',
            # Cloud skills
            'GCP', 'Terraform', 'Serverless', 'Microservices',
        ]

        # Domain-specific required skills — used when PDF/DOCX is uploaded
        # and the target domain is known from the user's profile
        self.domain_required_skills = {
            'Product Management': [
                'Product Strategy', 'Roadmapping', 'Agile', 'Scrum',
                'User Stories', 'Stakeholder Management',
                'A/B Testing', 'Data Analysis', 'Analytics',
                'Go-to-Market Strategy', 'Competitive Analysis',
                'Customer Journey Mapping', 'OKRs', 'Market Research'
            ],
            'UI/UX Design': [
                'Figma', 'Wireframing', 'Prototyping', 'User Research',
                'Usability Testing', 'Design Systems', 'Adobe XD',
                'Interaction Design', 'Visual Design', 'Accessibility'
            ],
            'Mobile Development': [
                'React Native', 'Flutter', 'Swift', 'Kotlin',
                'Android Development', 'iOS Development',
                'Mobile UI Design', 'App Performance Optimization'
            ],
            'Cloud Computing': [
                'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes',
                'Terraform', 'Serverless', 'Cloud Security',
                'Cloud Architecture', 'Cloud Networking'
            ],
            'Cybersecurity': [
                'Networking', 'Linux', 'Penetration Testing',
                'Cybersecurity', 'OWASP', 'Encryption',
                'Ethical Hacking', 'Security Operations (SOC)',
                'Incident Response', 'Web Application Security'
            ],
            'DevOps': [
                'Linux', 'Docker', 'Kubernetes', 'CI/CD',
                'Terraform', 'Git', 'AWS', 'Monitoring'
            ],
            'Data Science': [
                'Python', 'SQL', 'Statistics', 'Machine Learning',
                'Pandas', 'NumPy', 'Data Analysis', 'Data Visualization'
            ],
            'Machine Learning': [
                'Python', 'Machine Learning', 'Deep Learning',
                'TensorFlow', 'PyTorch', 'Statistics', 'NLP'
            ],
            'Web Development': [
                'HTML', 'CSS', 'JavaScript', 'React',
                'Node.js', 'REST API', 'Git', 'SQL'
            ],
            'Software Development': [
                'Python', 'JavaScript', 'Git', 'SQL',
                'REST API', 'Data Structures', 'Algorithms', 'Docker'
            ],
        }
    
    def parse_file(self, file_path: str, file_type: str, user_domain: str = '') -> Dict[str, Any]:
        """
        Parse uploaded file and extract skill data

        Args:
            file_path: Path to uploaded file
            file_type: 'pdf', 'docx', or 'json'
            user_domain: User's target domain (overrides file-detected domain)

        Returns:
            Dictionary with missingSkills, priorityScores, gapSeverity
        """
        if file_type == 'json':
            return self._parse_json(file_path)
        elif file_type == 'pdf':
            return self._parse_pdf(file_path, user_domain)
        elif file_type == 'docx':
            return self._parse_docx(file_path, user_domain)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    def _parse_json(self, file_path: str) -> Dict[str, Any]:
        """Parse JSON file from Analyze module"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract data with fallbacks
        missing_skills = data.get('missingSkills', [])
        if isinstance(missing_skills, dict):
            # Handle nested structure
            critical = missing_skills.get('critical', [])
            recommended = missing_skills.get('recommended', [])
            missing_skills = critical + recommended
        
        priority_scores = data.get('priorityScores', {})
        gap_severity = data.get('gapSeverity', {})
        
        # Convert gap severity strings to floats
        normalized_gap = {}
        severity_map = {'critical': 0.9, 'high': 0.7, 'medium': 0.5, 'low': 0.3}
        
        for skill, severity in gap_severity.items():
            if isinstance(severity, str):
                normalized_gap[skill] = severity_map.get(severity.lower(), 0.5)
            else:
                normalized_gap[skill] = float(severity) / 100 if severity > 1 else float(severity)
        
        return {
            'missingSkills': missing_skills,
            'priorityScores': priority_scores,
            'gapSeverity': normalized_gap,
            'targetDomain': data.get('targetDomain', 'General'),
            'readinessScore': data.get('readinessScore', 50),
            'existingSkills': data.get('extractedSkills', [])
        }
    
    def _parse_pdf(self, file_path: str, user_domain: str = '') -> Dict[str, Any]:
        """Parse PDF file and extract skills"""
        text = ""
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text += page.extract_text()
        
        return self._extract_skills_from_text(text, user_domain)
    
    def _parse_docx(self, file_path: str, user_domain: str = '') -> Dict[str, Any]:
        """Parse DOCX file and extract skills"""
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        
        return self._extract_skills_from_text(text, user_domain)
    
    def _extract_skills_from_text(self, text: str, user_domain: str = '') -> Dict[str, Any]:
        """Extract skills from plain text using pattern matching"""
        missing_skills = []
        priority_scores = {}
        gap_severity = {}

        text_lower = text.lower()

        # ── Determine target domain ────────────────────────────────────────────
        # 1. Try the unambiguous machine-readable marker first
        domain = None
        import re as _re
        match = _re.search(
            r'TARGET_DOMAIN_VALUE\s*[:\-]\s*([A-Za-z][A-Za-z0-9 /&+\-]+)',
            text, _re.IGNORECASE
        )
        if not match:
            match = _re.search(
                r'target\s+domain\s*[:\-]\s*([A-Za-z][A-Za-z0-9 /&+\-]+)',
                text, _re.IGNORECASE
            )
        if match:
            domain = match.group(1).strip()

        # 2. User's profile domain overrides everything
        if user_domain:
            domain = user_domain

        # 3. Keyword-based fallback only when domain still unknown
        if not domain:
            domain_keywords = {
                'Machine Learning': ['machine learning', 'deep learning', 'neural network', 'tensorflow', 'pytorch'],
                'Data Science': ['data science', 'data analyst', 'analytics', 'pandas', 'numpy', 'tableau'],
                'Software Development': ['software development', 'software engineer', 'backend', 'programming'],
                'Web Development': ['web development', 'frontend', 'fullstack', 'full stack', 'react', 'node.js'],
                'DevOps': ['devops', 'infrastructure', 'deployment', 'kubernetes', 'ci/cd'],
                'Cybersecurity': ['cybersecurity', 'security', 'penetration testing'],
                'Cloud Computing': ['cloud', 'aws', 'azure', 'gcp'],
                'Mobile Development': ['mobile', 'android', 'ios', 'flutter', 'react native'],
                'UI/UX Design': ['ui/ux', 'figma', 'wireframe', 'user experience', 'design'],
                'Product Management': ['product management', 'product manager', 'roadmap', 'agile', 'scrum'],
            }
            for domain_name, keywords in domain_keywords.items():
                if any(kw in text_lower for kw in keywords):
                    domain = domain_name
                    break

        if not domain:
            domain = 'General'

        # ── Build missing skills list ──────────────────────────────────────────
        # If we know the domain, use its required skill list directly.
        # This guarantees PM → PM skills, not random tech skills from the PDF body.
        if domain in self.domain_required_skills:
            skill_list = self.domain_required_skills[domain]
        else:
            skill_list = self.skill_keywords

        for skill in skill_list:
            # Always include domain-specific skills as missing (user is learning them)
            # For generic keywords, only include if mentioned in the text
            if domain in self.domain_required_skills:
                missing_skills.append(skill)
                priority_scores[skill] = 0.7
                gap_severity[skill] = 0.6
            elif skill.lower() in text_lower:
                missing_skills.append(skill)
                frequency = text_lower.count(skill.lower())
                priority_scores[skill] = min(frequency / 10, 1.0)
                if 'critical' in text_lower or 'urgent' in text_lower:
                    gap_severity[skill] = 0.8
                elif 'important' in text_lower or 'high' in text_lower:
                    gap_severity[skill] = 0.6
                else:
                    gap_severity[skill] = 0.4

        return {
            'missingSkills': missing_skills,
            'priorityScores': priority_scores,
            'gapSeverity': gap_severity,
            'targetDomain': domain,
            'readinessScore': 50,
            'existingSkills': []
        }


if __name__ == "__main__":
    # Test
    parser = FileParser()
    
    # Test JSON parsing
    test_data = {
        'missingSkills': ['Python', 'React', 'Docker'],
        'priorityScores': {'Python': 0.9, 'React': 0.7, 'Docker': 0.6},
        'gapSeverity': {'Python': 'high', 'React': 'medium', 'Docker': 'low'},
        'targetDomain': 'Software Development'
    }
    
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_data, f)
        temp_path = f.name
    
    result = parser.parse_file(temp_path, 'json')
    print("Parsed data:", json.dumps(result, indent=2))
    
    import os
    os.unlink(temp_path)
    print("✅ FileParser test passed")
