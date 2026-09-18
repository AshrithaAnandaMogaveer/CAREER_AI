"""
Video Resources Mapping Module
Maps learning topics to high-quality YouTube educational videos
Covers all domains: Software Development, Data Science, Machine Learning,
Web Development, Mobile Development, DevOps, Cybersecurity, Cloud Computing,
UI/UX Design, Product Management
"""

from typing import Dict, Optional


class VideoResourcesMapping:
    """
    Maps skills and topics to curated YouTube learning resources.
    Organised by domain so every target domain has relevant videos.
    """

    def __init__(self):
        # Format: skill_or_topic -> (video_title, video_url)
        self.video_resources = {

            # ── Machine Learning ──────────────────────────────────────────────
            'Machine Learning': (
                'Machine Learning Full Course - Learn Machine Learning',
                'https://www.youtube.com/watch?v=GwIo3gDZCVQ'
            ),
            'ML Fundamentals & Concepts': (
                'Machine Learning Basics | Introduction To Machine Learning',
                'https://www.youtube.com/watch?v=ukzFI9rgwfU'
            ),
            'Linear Regression': (
                'Linear Regression - Fun and Easy Machine Learning',
                'https://www.youtube.com/watch?v=ZkjP5RJLQF4'
            ),
            'Logistic Regression': (
                'Logistic Regression - Fun and Easy Machine Learning',
                'https://www.youtube.com/watch?v=yIYKR4sgzI8'
            ),
            'Decision Trees': (
                'Decision Tree Classification Clearly Explained!',
                'https://www.youtube.com/watch?v=_L39rN6gz7Y'
            ),
            'Random Forest & Ensemble Methods': (
                'Random Forest - Fun and Easy Machine Learning',
                'https://www.youtube.com/watch?v=D_2LkhMJcfY'
            ),
            'Support Vector Machines': (
                'Support Vector Machines (SVMs) - A Complete Guide',
                'https://www.youtube.com/watch?v=efR1C6CvhmE'
            ),
            'Model Evaluation & Metrics': (
                'Machine Learning Model Evaluation Metrics',
                'https://www.youtube.com/watch?v=LbX4X71-TFI'
            ),
            'Feature Engineering': (
                'Feature Engineering for Machine Learning',
                'https://www.youtube.com/watch?v=6WDFfaYtN6s'
            ),

            # ── Deep Learning ─────────────────────────────────────────────────
            'Deep Learning': (
                'Deep Learning Full Course 2024 | Deep Learning Tutorial',
                'https://www.youtube.com/watch?v=VyWAvY2CF9c'
            ),
            'Neural Networks Basics': (
                'Neural Networks Explained in 5 Minutes',
                'https://www.youtube.com/watch?v=aircAruvnKk'
            ),
            'Convolutional Neural Networks (CNN)': (
                'Convolutional Neural Networks (CNNs) Explained',
                'https://www.youtube.com/watch?v=YRhxdVk_sIs'
            ),
            'Recurrent Neural Networks (RNN)': (
                'Recurrent Neural Networks (RNN) Tutorial',
                'https://www.youtube.com/watch?v=LHXXI4-IEns'
            ),

            # ── Data Science ──────────────────────────────────────────────────
            'Data Science': (
                'Data Science Full Course - Learn Data Science in 10 Hours',
                'https://www.youtube.com/watch?v=ua-CiDNNj30'
            ),
            'Data Analysis': (
                'Data Analysis with Python - Full Course for Beginners',
                'https://www.youtube.com/watch?v=r-uOLxNrNk8'
            ),
            'Data Analysis Fundamentals': (
                'Data Analysis Full Course | Data Analytics Tutorial',
                'https://www.youtube.com/watch?v=ua-CiDNNj30'
            ),
            'Exploratory Data Analysis (EDA)': (
                'Exploratory Data Analysis in Python - Full Tutorial',
                'https://www.youtube.com/watch?v=xi0vhXFPegw'
            ),
            'Data Cleaning & Preprocessing': (
                'Data Cleaning in Python - Full Tutorial',
                'https://www.youtube.com/watch?v=bDhvCp3_lYw'
            ),
            'Statistical Analysis': (
                'Statistics for Data Science | Statistics Tutorial',
                'https://www.youtube.com/watch?v=xxpc-HPKN28'
            ),
            'Data Visualization': (
                'Data Visualization with Python - Matplotlib & Seaborn',
                'https://www.youtube.com/watch?v=a9UrKTVEeZA'
            ),
            'Pandas & NumPy': (
                'Pandas & NumPy Full Tutorial - Python for Data Science',
                'https://www.youtube.com/watch?v=vmEHCJofslg'
            ),
            'Statistics': (
                'Statistics - A Full University Course on Data Science Basics',
                'https://www.youtube.com/watch?v=xxpc-HPKN28'
            ),
            'NLP': (
                'Natural Language Processing (NLP) Tutorial with Python',
                'https://www.youtube.com/watch?v=X2vAabgKiuM'
            ),

            # ── Python ────────────────────────────────────────────────────────
            'Python': (
                'Python Tutorial for Beginners - Learn Python in 5 Hours',
                'https://www.youtube.com/watch?v=t8pPdKYpowI'
            ),
            'Python Basics & Syntax': (
                'Python Tutorial for Beginners - Learn Python in 5 Hours',
                'https://www.youtube.com/watch?v=t8pPdKYpowI'
            ),
            'Data Types & Variables': (
                'Python Data Types and Variables',
                'https://www.youtube.com/watch?v=ppsCxnNm-JI'
            ),
            'Control Flow (if/else, loops)': (
                'Python Control Flow: If, Elif, Else, For, While',
                'https://www.youtube.com/watch?v=PqFKRqpHrjw'
            ),
            'Functions & Modules': (
                'Python Functions Tutorial',
                'https://www.youtube.com/watch?v=9Os0o3wzS_I'
            ),
            'Object-Oriented Programming': (
                'Python OOP Tutorial - Object Oriented Programming',
                'https://www.youtube.com/watch?v=JeznW_7DlB0'
            ),
            'File Handling & I/O': (
                'Python File Handling Tutorial',
                'https://www.youtube.com/watch?v=Uh2ebFW8OYM'
            ),
            'Error Handling & Exceptions': (
                'Python Exception Handling Tutorial',
                'https://www.youtube.com/watch?v=NIWwJbo-9_8'
            ),
            'Libraries & Package Management': (
                'Python Packages and Modules',
                'https://www.youtube.com/watch?v=GxCXiSkm6no'
            ),

            # ── SQL / Databases ───────────────────────────────────────────────
            'SQL': (
                'SQL Tutorial - Full Database Course for Beginners',
                'https://www.youtube.com/watch?v=HXV3zeQKqGY'
            ),
            'SQL Basics & Syntax': (
                'SQL Tutorial - Full Database Course for Beginners',
                'https://www.youtube.com/watch?v=HXV3zeQKqGY'
            ),
            'SELECT Queries & Filtering': (
                'SQL SELECT Statement Tutorial',
                'https://www.youtube.com/watch?v=9Pzj7Aj25lw'
            ),
            'JOINs (INNER, LEFT, RIGHT, FULL)': (
                'SQL Joins Explained - Inner, Left, Right, and Full',
                'https://www.youtube.com/watch?v=9yeOJ0ZMUYw'
            ),
            'Aggregate Functions & GROUP BY': (
                'SQL Aggregate Functions and GROUP BY',
                'https://www.youtube.com/watch?v=YId-EJxKgRw'
            ),

            # ── Web Development ───────────────────────────────────────────────
            'Web Development': (
                'Web Development Full Course - 10 Hours | Web Development Tutorial',
                'https://www.youtube.com/watch?v=Q33KBiDriJY'
            ),
            'HTML': (
                'HTML Tutorial for Beginners - Full Course',
                'https://www.youtube.com/watch?v=qz0aGYrrlhU'
            ),
            'CSS': (
                'CSS Tutorial - Zero to Hero (Complete Course)',
                'https://www.youtube.com/watch?v=1Rs2ND1ryYc'
            ),
            'JavaScript': (
                'JavaScript Tutorial for Beginners - Full Course in 8 Hours',
                'https://www.youtube.com/watch?v=Qqx_wzMmFeA'
            ),
            'JavaScript Fundamentals': (
                'JavaScript Tutorial for Beginners - Full Course in 8 Hours',
                'https://www.youtube.com/watch?v=Qqx_wzMmFeA'
            ),
            'React': (
                'React Tutorial for Beginners',
                'https://www.youtube.com/watch?v=SqcY0GlETPk'
            ),
            'React Fundamentals': (
                'React Tutorial for Beginners',
                'https://www.youtube.com/watch?v=SqcY0GlETPk'
            ),
            'Node.js': (
                'Node.js Tutorial for Beginners - Full Course',
                'https://www.youtube.com/watch?v=TlB_eWDSMt4'
            ),
            'Node.js Basics': (
                'Node.js Tutorial for Beginners - Full Course',
                'https://www.youtube.com/watch?v=TlB_eWDSMt4'
            ),
            'REST API': (
                'REST API Tutorial - REST Client, REST Service and API Calls',
                'https://www.youtube.com/watch?v=qbLc5a9jdXo'
            ),

            # ── Software Development ──────────────────────────────────────────
            'Software Development': (
                'Software Development Life Cycle (SDLC) - Full Course',
                'https://www.youtube.com/watch?v=i-QyW8D3ei0'
            ),
            'Data Structures': (
                'Data Structures Easy to Advanced Course - Full Tutorial',
                'https://www.youtube.com/watch?v=RBSGKlAvoiM'
            ),
            'Algorithms': (
                'Algorithms and Data Structures Tutorial - Full Course',
                'https://www.youtube.com/watch?v=8hly31xKli0'
            ),
            'System Design': (
                'System Design Full Course - Learn System Design',
                'https://www.youtube.com/watch?v=MbjObHmDbZo'
            ),
            'Design Patterns': (
                'Design Patterns in Object Oriented Programming',
                'https://www.youtube.com/watch?v=v9ejT8FO-7I'
            ),
            'Git': (
                'Git Tutorial for Beginners - Git & GitHub Fundamentals',
                'https://www.youtube.com/watch?v=RGOj5yH7evk'
            ),
            'Git Basics & Setup': (
                'Git Tutorial for Beginners - Git & GitHub Fundamentals',
                'https://www.youtube.com/watch?v=RGOj5yH7evk'
            ),

            # ── DevOps ────────────────────────────────────────────────────────
            'DevOps': (
                'DevOps Tutorial for Beginners | Learn DevOps in 7 Hours',
                'https://www.youtube.com/watch?v=hQcFE0RD0cQ'
            ),
            'Docker': (
                'Docker Tutorial for Beginners - Full Course',
                'https://www.youtube.com/watch?v=3c-iBn73dDE'
            ),
            'Docker Basics & Concepts': (
                'Docker Tutorial for Beginners - Full Course',
                'https://www.youtube.com/watch?v=3c-iBn73dDE'
            ),
            'Kubernetes': (
                'Kubernetes Tutorial for Beginners - Full Course',
                'https://www.youtube.com/watch?v=X48VuDVv0do'
            ),
            'Kubernetes Architecture': (
                'Kubernetes Tutorial for Beginners - Full Course',
                'https://www.youtube.com/watch?v=X48VuDVv0do'
            ),
            'CI/CD': (
                'CI/CD Pipeline Tutorial | Continuous Integration and Deployment',
                'https://www.youtube.com/watch?v=R8_veQiYBjI'
            ),
            'Linux': (
                'Linux Command Line Full Course - Beginner to Advanced',
                'https://www.youtube.com/watch?v=sWbUDq4S6Y8'
            ),
            'Terraform': (
                'Terraform Course - Automate your AWS cloud infrastructure',
                'https://www.youtube.com/watch?v=SLB_c_ayRMo'
            ),

            # ── Cloud Computing ───────────────────────────────────────────────
            'Cloud Computing': (
                'Cloud Computing Full Course | Cloud Computing Tutorial',
                'https://www.youtube.com/watch?v=M988_fsOSWo'
            ),
            'AWS': (
                'AWS Tutorial for Beginners - Full Course',
                'https://www.youtube.com/watch?v=ulprqHHWlng'
            ),
            'AWS Fundamentals': (
                'AWS Tutorial for Beginners - Full Course',
                'https://www.youtube.com/watch?v=ulprqHHWlng'
            ),
            'EC2 & Compute Services': (
                'AWS EC2 Tutorial For Beginners',
                'https://www.youtube.com/watch?v=iHX-jtKIVNA'
            ),
            'S3 & Storage': (
                'AWS S3 Tutorial For Beginners',
                'https://www.youtube.com/watch?v=tfU0JEZjcsg'
            ),
            'Azure': (
                'Microsoft Azure Full Course - AZ-900 Azure Fundamentals',
                'https://www.youtube.com/watch?v=NKEFWyqJ5XA'
            ),
            'Google Cloud Platform': (
                'Google Cloud Platform Full Course | GCP Tutorial',
                'https://www.youtube.com/watch?v=IUU6OR8yHCc'
            ),
            'Cloud Architecture': (
                'Cloud Architecture Fundamentals - AWS, Azure, GCP',
                'https://www.youtube.com/watch?v=M988_fsOSWo'
            ),
            'Serverless Computing': (
                'Serverless Computing Explained - AWS Lambda Tutorial',
                'https://www.youtube.com/watch?v=97q30JjEq9Y'
            ),
            'Cloud Security': (
                'Cloud Security Tutorial | Cloud Security Fundamentals',
                'https://www.youtube.com/watch?v=0lly9msZfd8'
            ),
            'Cloud Networking': (
                'AWS Networking Fundamentals - VPC, Subnets, Security Groups',
                'https://www.youtube.com/watch?v=hiKPPy584Mg'
            ),
            'Cloud Cost Optimization': (
                'AWS Cost Optimization - Best Practices and Strategies',
                'https://www.youtube.com/watch?v=XHngKB3dHQw'
            ),
            'Cloud Migration': (
                'Cloud Migration Strategy - How to Move to the Cloud',
                'https://www.youtube.com/watch?v=09SxmFMFHiQ'
            ),

            # ── Cybersecurity ─────────────────────────────────────────────────
            'Cybersecurity': (
                'Cybersecurity Full Course for Beginners',
                'https://www.youtube.com/watch?v=U_P23SqJaDc'
            ),
            'Network Security': (
                'Network Security Tutorial | Introduction to Network Security',
                'https://www.youtube.com/watch?v=E03gh1huvW4'
            ),
            'Ethical Hacking': (
                'Ethical Hacking Full Course - Learn Ethical Hacking in 10 Hours',
                'https://www.youtube.com/watch?v=dz7Ntp7KQGA'
            ),
            'Penetration Testing': (
                'Penetration Testing Full Course | Ethical Hacking Tutorial',
                'https://www.youtube.com/watch?v=3Kq1MIfTWCE'
            ),
            'Web Application Security': (
                'Web Application Security Testing Tutorial - OWASP Top 10',
                'https://www.youtube.com/watch?v=WtHnT73NaaQ'
            ),
            'Cryptography': (
                'Cryptography Full Course | Cryptography and Network Security',
                'https://www.youtube.com/watch?v=AQDCe585Lnc'
            ),
            'Security Operations (SOC)': (
                'SOC Analyst Full Course | Security Operations Center',
                'https://www.youtube.com/watch?v=Bt5fh3wQUAQ'
            ),
            'Incident Response': (
                'Incident Response Tutorial | Cybersecurity Incident Handling',
                'https://www.youtube.com/watch?v=rPkiGDFBMaI'
            ),

            # ── Mobile Development ────────────────────────────────────────────
            'Mobile Development': (
                'Mobile App Development Full Course - Android & iOS',
                'https://www.youtube.com/watch?v=0-S5a0eXPoc'
            ),
            'React Native': (
                'React Native Tutorial for Beginners - Build a React Native App',
                'https://www.youtube.com/watch?v=0-S5a0eXPoc'
            ),
            'Flutter': (
                'Flutter Course for Beginners - Build iOS and Android Apps',
                'https://www.youtube.com/watch?v=VPvVD8t02U8'
            ),
            'Android Development': (
                'Android Development for Beginners - Full Course',
                'https://www.youtube.com/watch?v=fis26HvvDII'
            ),
            'iOS Development': (
                'iOS Development Course - Use Swift and SwiftUI',
                'https://www.youtube.com/watch?v=comQ1-x2a1Q'
            ),
            'Mobile UI Design': (
                'Mobile UI Design Tutorial - Figma for Mobile Apps',
                'https://www.youtube.com/watch?v=FTFaQWZBqQ8'
            ),
            'App Performance Optimization': (
                'Mobile App Performance Optimization Tips and Techniques',
                'https://www.youtube.com/watch?v=0-S5a0eXPoc'
            ),
            'Mobile App Testing': (
                'Mobile App Testing Tutorial | Mobile Testing Strategies',
                'https://www.youtube.com/watch?v=m_MdkFBqPE4'
            ),

            # ── UI/UX Design ──────────────────────────────────────────────────
            'UI/UX Design': (
                'UI UX Design Tutorial - Full Course for Beginners',
                'https://www.youtube.com/watch?v=c9Wg6Cb_YlU'
            ),
            'UX Research': (
                'UX Research Methods - Full Course for Beginners',
                'https://www.youtube.com/watch?v=tLM9xNMGB_s'
            ),
            'User Research': (
                'User Research Methods and Best Practices',
                'https://www.youtube.com/watch?v=tLM9xNMGB_s'
            ),
            'Wireframing': (
                'Wireframing Tutorial - How to Create Wireframes',
                'https://www.youtube.com/watch?v=qpH7-KFWZRI'
            ),
            'Prototyping': (
                'Prototyping in Figma - Full Tutorial for Beginners',
                'https://www.youtube.com/watch?v=lTIeZ2ahEkQ'
            ),
            'Figma': (
                'Figma Tutorial for Beginners - Complete Course',
                'https://www.youtube.com/watch?v=FTFaQWZBqQ8'
            ),
            'Design Systems': (
                'Design Systems Tutorial - How to Build a Design System',
                'https://www.youtube.com/watch?v=wc5krC28ynQ'
            ),
            'Usability Testing': (
                'Usability Testing Tutorial - How to Conduct User Testing',
                'https://www.youtube.com/watch?v=0YL0xoSmyZI'
            ),
            'Interaction Design': (
                'Interaction Design Tutorial - Principles and Best Practices',
                'https://www.youtube.com/watch?v=c9Wg6Cb_YlU'
            ),
            'Visual Design': (
                'Visual Design Principles - Full Course',
                'https://www.youtube.com/watch?v=_Jtn0-4tX2I'
            ),
            'Accessibility (a11y)': (
                'Web Accessibility Tutorial - WCAG Guidelines',
                'https://www.youtube.com/watch?v=20SHvU2PKsM'
            ),

            # ── Product Management ────────────────────────────────────────────
            'Product Management': (
                'Product Management Full Course | Product Manager Tutorial',
                'https://www.youtube.com/watch?v=yUWmL9oNDo0'
            ),
            'Product Strategy': (
                'Product Strategy - How to Build a Product Strategy',
                'https://www.youtube.com/watch?v=ebQPAeoADgk'
            ),
            'Product Roadmap': (
                'Product Roadmap Tutorial - How to Build a Product Roadmap',
                'https://www.youtube.com/watch?v=ebQPAeoADgk'
            ),
            'Agile & Scrum': (
                'Agile Scrum Full Course | Agile Scrum Tutorial',
                'https://www.youtube.com/watch?v=gy1c4_YixCo'
            ),
            'User Stories & Requirements': (
                'User Stories Tutorial - How to Write User Stories',
                'https://www.youtube.com/watch?v=apOvF9NVguA'
            ),
            'Product Analytics': (
                'Product Analytics Tutorial - Metrics and KPIs for PMs',
                'https://www.youtube.com/watch?v=yUWmL9oNDo0'
            ),
            'Stakeholder Management': (
                'Stakeholder Management Tutorial for Product Managers',
                'https://www.youtube.com/watch?v=yUWmL9oNDo0'
            ),
            'Go-to-Market Strategy': (
                'Go To Market Strategy - How to Launch a Product',
                'https://www.youtube.com/watch?v=ebQPAeoADgk'
            ),
            'Competitive Analysis': (
                'Competitive Analysis Tutorial - How to Analyze Competitors',
                'https://www.youtube.com/watch?v=ebQPAeoADgk'
            ),
            'Product Discovery': (
                'Product Discovery Tutorial - How to Discover Product Opportunities',
                'https://www.youtube.com/watch?v=yUWmL9oNDo0'
            ),
            'OKRs & KPIs': (
                'OKRs Tutorial - How to Set Objectives and Key Results',
                'https://www.youtube.com/watch?v=EIcpFZ5rbHc'
            ),
            'Prioritization Frameworks': (
                'Product Prioritization Frameworks - RICE, MoSCoW, Kano',
                'https://www.youtube.com/watch?v=yUWmL9oNDo0'
            ),
            'A/B Testing': (
                'A/B Testing Tutorial - How to Run Experiments',
                'https://www.youtube.com/watch?v=zFMgpxG-chM'
            ),
            'Customer Journey Mapping': (
                'Customer Journey Map Tutorial - How to Create a CJM',
                'https://www.youtube.com/watch?v=mSxpVRo3BLg'
            ),
            'Market Research': (
                'Market Research Tutorial - How to Do Market Research',
                'https://www.youtube.com/watch?v=ebQPAeoADgk'
            ),
        }

        # Domain-level fallback videos — used when a skill has no direct match
        self.domain_videos = {
            'Product Management': (
                'Product Management Full Course | Product Manager Tutorial',
                'https://www.youtube.com/watch?v=yUWmL9oNDo0'
            ),
            'UI/UX Design': (
                'UI UX Design Tutorial - Full Course for Beginners',
                'https://www.youtube.com/watch?v=c9Wg6Cb_YlU'
            ),
            'Mobile Development': (
                'Mobile App Development Full Course - Android & iOS',
                'https://www.youtube.com/watch?v=0-S5a0eXPoc'
            ),
            'Cloud Computing': (
                'Cloud Computing Full Course | Cloud Computing Tutorial',
                'https://www.youtube.com/watch?v=M988_fsOSWo'
            ),
            'Cybersecurity': (
                'Cybersecurity Full Course for Beginners',
                'https://www.youtube.com/watch?v=U_P23SqJaDc'
            ),
            'DevOps': (
                'DevOps Tutorial for Beginners | Learn DevOps in 7 Hours',
                'https://www.youtube.com/watch?v=hQcFE0RD0cQ'
            ),
            'Data Science': (
                'Data Science Full Course - Learn Data Science in 10 Hours',
                'https://www.youtube.com/watch?v=ua-CiDNNj30'
            ),
            'Machine Learning': (
                'Machine Learning Full Course - Learn Machine Learning',
                'https://www.youtube.com/watch?v=GwIo3gDZCVQ'
            ),
            'Web Development': (
                'Web Development Full Course - 10 Hours | Web Development Tutorial',
                'https://www.youtube.com/watch?v=Q33KBiDriJY'
            ),
            'Software Development': (
                'Software Development Life Cycle (SDLC) - Full Course',
                'https://www.youtube.com/watch?v=i-QyW8D3ei0'
            ),
        }

    def get_video_resource(self, topic: str, skill: str = '', domain: str = '') -> Dict[str, str]:
        """
        Get video resource with priority:
          1. Exact topic match
          2. Exact skill match
          3. Domain-level fallback video
          4. Fuzzy match on topic/skill
          5. YouTube search scoped to skill + domain
        """
        # 1. Exact topic match
        if topic in self.video_resources:
            title, url = self.video_resources[topic]
            return {'title': title, 'url': url, 'platform': 'YouTube'}

        # 2. Exact skill match
        if skill and skill in self.video_resources:
            title, url = self.video_resources[skill]
            return {'title': title, 'url': url, 'platform': 'YouTube'}

        # 3. Domain-level fallback — ensures domain-relevant video even for unknown skills
        if domain and domain in self.domain_videos:
            title, url = self.domain_videos[domain]
            return {'title': title, 'url': url, 'platform': 'YouTube'}
        if skill and skill in self.domain_videos:
            title, url = self.domain_videos[skill]
            return {'title': title, 'url': url, 'platform': 'YouTube'}

        # 4. Fuzzy match — prefer skill name over topic name
        topic_lower = topic.lower()
        skill_lower = skill.lower() if skill else ''
        best_key, best_score = None, 0

        for key in self.video_resources:
            key_lower = key.lower()
            if skill_lower and skill_lower in key_lower:
                score = 3
            elif key_lower in topic_lower or topic_lower in key_lower:
                score = 1
            else:
                continue
            if score > best_score:
                best_score = score
                best_key = key

        if best_key:
            title, url = self.video_resources[best_key]
            return {'title': title, 'url': url, 'platform': 'YouTube'}

        # 5. YouTube search scoped to skill + domain
        return self._generate_search_url(topic, skill, domain)

    def _generate_search_url(self, topic: str, skill: str = '', domain: str = '') -> Dict[str, str]:
        """Generate a YouTube search URL scoped to the skill and domain"""
        parts = [p for p in [domain, skill, topic, 'tutorial'] if p]
        search_query = '+'.join(p.replace(' ', '+') for p in parts)
        label = skill or domain or topic
        return {
            'title': f'Search: {label} - {topic} Tutorial',
            'url': f'https://www.youtube.com/results?search_query={search_query}',
            'platform': 'YouTube',
            'is_search': True
        }

    def has_video(self, topic: str) -> bool:
        return topic in self.video_resources

    def get_all_topics_with_videos(self) -> list:
        return list(self.video_resources.keys())
