"""
Skill Topics Mapping Module
Maps skills to structured learning topics/subtopics for dynamic routine generation
Each topic includes a learning objective
"""

from typing import List, Dict, Any


class SkillTopicsMapping:
    """
    Comprehensive skill-to-topics mapping for dynamic routine generation
    Each skill is broken down into weekly learning topics with objectives
    """
    
    def __init__(self):
        # Format: skill -> list of (topic_name, learning_objective)
        self.skill_topics = {
            # Programming Languages
            'Python': [
                ('Python Basics & Syntax', 'Understand Python syntax, variables, and basic operations'),
                ('Data Types & Variables', 'Master Python data types including strings, numbers, lists, and dictionaries'),
                ('Control Flow (if/else, loops)', 'Learn conditional statements and iteration with for/while loops'),
                ('Functions & Modules', 'Create reusable functions and organize code with modules'),
                ('Object-Oriented Programming', 'Understand classes, objects, inheritance, and polymorphism'),
                ('File Handling & I/O', 'Read and write files, handle different file formats'),
                ('Error Handling & Exceptions', 'Implement try-except blocks and handle errors gracefully'),
                ('Libraries & Package Management', 'Use pip, virtual environments, and popular Python libraries')
            ],
            'JavaScript': [
                ('JavaScript Fundamentals', 'Understand variables, data types, and basic syntax'),
                ('DOM Manipulation', 'Select and modify HTML elements dynamically'),
                ('ES6+ Features', 'Master arrow functions, destructuring, spread operator, and template literals'),
                ('Async Programming (Promises, Async/Await)', 'Handle asynchronous operations and API calls'),
                ('Event Handling', 'Respond to user interactions and browser events'),
                ('JSON & APIs', 'Work with JSON data and consume RESTful APIs'),
                ('Error Handling', 'Implement error handling and debugging techniques'),
                ('Modern JavaScript Patterns', 'Apply design patterns and best practices')
            ],
            'Java': [
                ('Java Syntax & Basics', 'Understand Java syntax, variables, and data types'),
                ('Object-Oriented Programming', 'Master classes, objects, inheritance, and interfaces'),
                ('Collections Framework', 'Use ArrayList, HashMap, and other collection classes'),
                ('Exception Handling', 'Implement try-catch blocks and custom exceptions'),
                ('Multithreading', 'Create and manage threads for concurrent programming'),
                ('File I/O & Streams', 'Read and write files using streams'),
                ('JDBC & Database Connectivity', 'Connect to databases and execute SQL queries'),
                ('Java 8+ Features', 'Use lambda expressions, streams, and functional interfaces')
            ],
            'C++': [
                ('C++ Basics & Syntax', 'Understand C++ syntax, variables, and basic operations'),
                ('Pointers & References', 'Master memory addresses, pointers, and references'),
                ('Object-Oriented Programming', 'Implement classes, inheritance, and polymorphism'),
                ('STL (Standard Template Library)', 'Use vectors, maps, sets, and algorithms'),
                ('Memory Management', 'Allocate and deallocate memory, prevent memory leaks'),
                ('Templates & Generic Programming', 'Create generic functions and classes'),
                ('Exception Handling', 'Handle errors using try-catch blocks'),
                ('Advanced C++ Features', 'Apply move semantics, smart pointers, and modern C++ features')
            ],
            
            # Data Science & ML
            'Machine Learning': [
                ('ML Fundamentals & Concepts', 'Understand supervised vs unsupervised learning and ML workflow'),
                ('Linear Regression', 'Build regression models and understand cost functions'),
                ('Logistic Regression', 'Implement classification models for binary outcomes'),
                ('Decision Trees', 'Create tree-based models and understand splitting criteria'),
                ('Random Forest & Ensemble Methods', 'Combine multiple models for better predictions'),
                ('Support Vector Machines', 'Understand margin maximization and kernel tricks'),
                ('Model Evaluation & Metrics', 'Evaluate models using accuracy, precision, recall, and F1-score'),
                ('Feature Engineering', 'Create and select features to improve model performance')
            ],
            'Deep Learning': [
                ('Neural Networks Basics', 'Understand neurons, layers, and forward propagation'),
                ('Activation Functions & Backpropagation', 'Learn how neural networks learn through gradient descent'),
                ('Convolutional Neural Networks (CNN)', 'Build image classification models'),
                ('Recurrent Neural Networks (RNN)', 'Process sequential data and time series'),
                ('LSTM & GRU', 'Handle long-term dependencies in sequences'),
                ('Transfer Learning', 'Use pre-trained models for new tasks'),
                ('Model Optimization', 'Apply regularization, dropout, and hyperparameter tuning'),
                ('Deep Learning Frameworks', 'Master TensorFlow or PyTorch for model development')
            ],
            'Data Analysis': [
                'Data Analysis Fundamentals',
                'Exploratory Data Analysis (EDA)',
                'Data Cleaning & Preprocessing',
                'Statistical Analysis',
                'Data Visualization',
                'Pandas & NumPy',
                'Data Interpretation',
                'Reporting & Insights'
            ],
            'Statistics': [
                'Descriptive Statistics',
                'Probability Theory',
                'Distributions & Sampling',
                'Hypothesis Testing',
                'Confidence Intervals',
                'Regression Analysis',
                'ANOVA & Chi-Square Tests',
                'Bayesian Statistics'
            ],
            'NLP': [
                'NLP Fundamentals',
                'Text Preprocessing',
                'Tokenization & Stemming',
                'Word Embeddings (Word2Vec, GloVe)',
                'Sentiment Analysis',
                'Named Entity Recognition',
                'Transformers & BERT',
                'NLP Applications'
            ],
            
            # Data Tools
            'SQL': [
                'SQL Basics & Syntax',
                'SELECT Queries & Filtering',
                'JOINs (INNER, LEFT, RIGHT, FULL)',
                'Aggregate Functions & GROUP BY',
                'Subqueries & CTEs',
                'Indexes & Query Optimization',
                'Stored Procedures & Functions',
                'Database Design & Normalization'
            ],
            'Pandas': [
                'Pandas Basics',
                'DataFrames & Series',
                'Data Selection & Filtering',
                'Data Cleaning & Transformation',
                'Grouping & Aggregation',
                'Merging & Joining DataFrames',
                'Time Series Analysis',
                'Advanced Pandas Operations'
            ],
            'NumPy': [
                'NumPy Arrays Basics',
                'Array Operations',
                'Indexing & Slicing',
                'Mathematical Operations',
                'Broadcasting',
                'Linear Algebra with NumPy',
                'Random Number Generation',
                'Performance Optimization'
            ],
            
            # Web Development
            'React': [
                'React Fundamentals',
                'JSX & Components',
                'Props & State',
                'Hooks (useState, useEffect)',
                'Event Handling',
                'Conditional Rendering',
                'React Router',
                'State Management (Context API, Redux)'
            ],
            'Node.js': [
                'Node.js Basics',
                'NPM & Package Management',
                'File System & Modules',
                'Express.js Framework',
                'RESTful API Development',
                'Middleware & Routing',
                'Database Integration',
                'Authentication & Security'
            ],
            'HTML': [
                'HTML Basics & Structure',
                'Semantic HTML',
                'Forms & Input Elements',
                'Tables & Lists',
                'Multimedia (Images, Video, Audio)',
                'HTML5 Features',
                'Accessibility Best Practices',
                'SEO Fundamentals'
            ],
            'CSS': [
                'CSS Basics & Selectors',
                'Box Model & Layout',
                'Flexbox',
                'CSS Grid',
                'Responsive Design',
                'CSS Animations & Transitions',
                'CSS Preprocessors (SASS/LESS)',
                'Modern CSS Techniques'
            ],
            'Angular': [
                'Angular Fundamentals',
                'Components & Templates',
                'Data Binding',
                'Directives & Pipes',
                'Services & Dependency Injection',
                'Routing & Navigation',
                'Forms & Validation',
                'HTTP & Observables'
            ],
            'Vue.js': [
                'Vue.js Basics',
                'Vue Components',
                'Data Binding & Directives',
                'Computed Properties & Watchers',
                'Event Handling',
                'Vue Router',
                'Vuex State Management',
                'Vue CLI & Build Tools'
            ],
            
            # Backend & Databases
            'Django': [
                'Django Basics & Setup',
                'Models & ORM',
                'Views & URL Routing',
                'Templates & Template Language',
                'Forms & Validation',
                'Authentication & Authorization',
                'Django REST Framework',
                'Deployment & Production'
            ],
            'Flask': [
                'Flask Basics',
                'Routing & Views',
                'Templates (Jinja2)',
                'Forms & WTForms',
                'Database Integration (SQLAlchemy)',
                'RESTful APIs',
                'Authentication & Sessions',
                'Flask Extensions'
            ],
            'MongoDB': [
                'MongoDB Basics',
                'CRUD Operations',
                'Querying & Filtering',
                'Indexing',
                'Aggregation Framework',
                'Data Modeling',
                'Replication & Sharding',
                'MongoDB with Node.js/Python'
            ],
            'PostgreSQL': [
                'PostgreSQL Basics',
                'Advanced SQL Queries',
                'Indexes & Performance',
                'Transactions & ACID',
                'Stored Procedures & Functions',
                'JSON Support',
                'Replication & Backup',
                'PostgreSQL Administration'
            ],
            
            # DevOps & Cloud
            'Docker': [
                'Docker Basics & Concepts',
                'Docker Images & Containers',
                'Dockerfile & Building Images',
                'Docker Compose',
                'Volumes & Networking',
                'Docker Registry',
                'Container Orchestration Basics',
                'Docker Best Practices'
            ],
            'Kubernetes': [
                'Kubernetes Architecture',
                'Pods & Deployments',
                'Services & Networking',
                'ConfigMaps & Secrets',
                'Persistent Volumes',
                'Helm Charts',
                'Monitoring & Logging',
                'Kubernetes Security'
            ],
            'AWS': [
                'AWS Fundamentals',
                'EC2 & Compute Services',
                'S3 & Storage',
                'RDS & Databases',
                'Lambda & Serverless',
                'VPC & Networking',
                'IAM & Security',
                'CloudFormation & Infrastructure as Code'
            ],
            'CI/CD': [
                'CI/CD Fundamentals',
                'Version Control (Git)',
                'Build Automation',
                'Testing Automation',
                'Deployment Pipelines',
                'Jenkins/GitLab CI/GitHub Actions',
                'Continuous Monitoring',
                'DevOps Best Practices'
            ],
            'Linux': [
                'Linux Basics & Commands',
                'File System & Permissions',
                'Process Management',
                'Shell Scripting',
                'Package Management',
                'Networking & SSH',
                'System Administration',
                'Linux Security'
            ],
            'Terraform': [
                'Infrastructure as Code Basics',
                'Terraform Syntax & Configuration',
                'Providers & Resources',
                'Variables & Outputs',
                'State Management',
                'Modules & Reusability',
                'Terraform Cloud',
                'Best Practices & Patterns'
            ],
            
            # Data Structures & Algorithms
            'Data Structures': [
                'Arrays & Strings',
                'Linked Lists',
                'Stacks & Queues',
                'Trees & Binary Trees',
                'Graphs',
                'Hash Tables',
                'Heaps & Priority Queues',
                'Advanced Data Structures'
            ],
            'Algorithms': [
                'Algorithm Complexity (Big O)',
                'Sorting Algorithms',
                'Searching Algorithms',
                'Recursion & Backtracking',
                'Dynamic Programming',
                'Greedy Algorithms',
                'Graph Algorithms',
                'Algorithm Design Patterns'
            ],
            
            # Tools & Version Control
            'Git': [
                'Git Basics & Setup',
                'Commits & Branches',
                'Merging & Rebasing',
                'Remote Repositories',
                'Pull Requests & Code Review',
                'Git Workflows',
                'Conflict Resolution',
                'Advanced Git Techniques'
            ],
            'REST API': [
                'REST Principles',
                'HTTP Methods & Status Codes',
                'API Design Best Practices',
                'Authentication & Authorization',
                'API Documentation',
                'Error Handling',
                'Versioning',
                'Testing APIs'
            ],
            
            # Mobile Development
            'React Native': [
                'React Native Basics',
                'Components & Styling',
                'Navigation',
                'State Management',
                'Native Modules',
                'API Integration',
                'Debugging & Testing',
                'Deployment (iOS & Android)'
            ],
            'Flutter': [
                'Flutter Basics & Dart',
                'Widgets & Layouts',
                'State Management',
                'Navigation & Routing',
                'API Integration',
                'Local Storage',
                'Testing',
                'Publishing Apps'
            ],
            
            # Testing
            'Unit Testing': [
                ('Testing Fundamentals', 'Understand the principles and importance of software testing'),
                ('Test-Driven Development (TDD)', 'Write tests before code to drive design decisions'),
                ('Unit Test Frameworks', 'Use pytest, JUnit, or Jest for writing unit tests'),
                ('Mocking & Stubbing', 'Isolate units under test using mocks and stubs'),
                ('Test Coverage', 'Measure and improve code coverage'),
                ('Integration Testing', 'Test interactions between components'),
                ('Best Practices', 'Apply testing best practices and patterns'),
                ('Continuous Testing', 'Integrate testing into CI/CD pipelines')
            ],
            
            # Security
            'Cybersecurity': [
                ('Security Fundamentals', 'Understand core cybersecurity concepts and threat landscape'),
                ('Network Security', 'Secure networks using firewalls, VPNs, and IDS/IPS'),
                ('Cryptography Basics', 'Apply encryption, hashing, and digital signatures'),
                ('Web Application Security', 'Identify and fix OWASP Top 10 vulnerabilities'),
                ('Authentication & Authorization', 'Implement secure auth mechanisms'),
                ('Security Testing', 'Perform vulnerability assessments and penetration testing'),
                ('Incident Response', 'Detect, contain, and recover from security incidents'),
                ('Security Best Practices', 'Apply security hardening and compliance standards')
            ],

            # Product Management
            'Product Strategy': [
                ('Product Vision & Mission', 'Define a compelling product vision aligned with business goals'),
                ('Market Analysis', 'Analyze market size, trends, and opportunities'),
                ('Competitive Analysis', 'Evaluate competitors and identify differentiation opportunities'),
                ('Product Positioning', 'Define how your product stands out in the market'),
                ('Business Model Design', 'Design sustainable revenue and value delivery models'),
                ('Strategic Roadmapping', 'Build a long-term product roadmap aligned with strategy'),
                ('OKRs & KPIs', 'Set measurable objectives and track key performance indicators'),
                ('Go-to-Market Strategy', 'Plan product launch and market entry strategies')
            ],
            'Roadmapping': [
                ('Roadmap Fundamentals', 'Understand types of roadmaps and when to use them'),
                ('Prioritization Frameworks', 'Apply RICE, MoSCoW, Kano, and other frameworks'),
                ('Stakeholder Alignment', 'Align roadmap with engineering, design, and business teams'),
                ('Outcome-Based Roadmaps', 'Shift from feature lists to outcome-driven planning'),
                ('Roadmap Communication', 'Present roadmaps to different audiences effectively'),
                ('Quarterly Planning', 'Break roadmap into actionable quarterly plans'),
                ('Dependency Management', 'Identify and manage cross-team dependencies'),
                ('Roadmap Review & Iteration', 'Continuously update roadmap based on learnings')
            ],
            'Agile': [
                ('Agile Fundamentals', 'Understand Agile values, principles, and the Agile Manifesto'),
                ('Scrum Framework', 'Master sprints, ceremonies, and Scrum roles'),
                ('Kanban Method', 'Visualize workflow and limit work in progress'),
                ('User Stories & Acceptance Criteria', 'Write effective user stories with clear acceptance criteria'),
                ('Sprint Planning & Execution', 'Plan and execute sprints effectively'),
                ('Retrospectives & Continuous Improvement', 'Run effective retrospectives to improve team performance'),
                ('Agile Metrics', 'Track velocity, cycle time, and burndown charts'),
                ('Scaling Agile', 'Apply SAFe, LeSS, or other scaling frameworks')
            ],
            'Scrum': [
                ('Scrum Roles', 'Understand Product Owner, Scrum Master, and Development Team roles'),
                ('Scrum Events', 'Master Sprint Planning, Daily Scrum, Review, and Retrospective'),
                ('Product Backlog Management', 'Create, refine, and prioritize the product backlog'),
                ('Sprint Backlog & Execution', 'Plan and track sprint work effectively'),
                ('Definition of Done', 'Establish clear quality standards for completed work'),
                ('Scrum Artifacts', 'Use Product Backlog, Sprint Backlog, and Increment effectively'),
                ('Velocity & Estimation', 'Estimate story points and track team velocity'),
                ('Scrum at Scale', 'Apply Scrum across multiple teams')
            ],
            'User Stories': [
                ('User Story Fundamentals', 'Understand the structure and purpose of user stories'),
                ('Writing Effective User Stories', 'Apply the INVEST criteria for quality user stories'),
                ('Acceptance Criteria', 'Define clear, testable acceptance criteria'),
                ('Story Mapping', 'Build user story maps to visualize the user journey'),
                ('Epics & Features', 'Organize stories into epics and features'),
                ('Backlog Refinement', 'Continuously refine and estimate backlog items'),
                ('Story Splitting', 'Break large stories into smaller, deliverable pieces'),
                ('BDD & Gherkin', 'Write behavior-driven scenarios using Given-When-Then')
            ],
            'Stakeholder Management': [
                ('Stakeholder Identification', 'Identify and map all relevant stakeholders'),
                ('Stakeholder Analysis', 'Assess stakeholder influence, interest, and needs'),
                ('Communication Planning', 'Create a stakeholder communication plan'),
                ('Managing Expectations', 'Set and manage realistic expectations with stakeholders'),
                ('Conflict Resolution', 'Navigate disagreements and find win-win solutions'),
                ('Executive Communication', 'Present product updates to leadership effectively'),
                ('Cross-functional Collaboration', 'Work effectively with engineering, design, and sales'),
                ('Feedback Collection', 'Gather and synthesize stakeholder feedback')
            ],
            'A/B Testing': [
                ('Experimentation Fundamentals', 'Understand hypothesis-driven product development'),
                ('A/B Test Design', 'Design statistically valid A/B experiments'),
                ('Statistical Significance', 'Understand p-values, confidence intervals, and sample sizes'),
                ('Metrics & Success Criteria', 'Define primary and guardrail metrics for experiments'),
                ('Running Experiments', 'Use tools like Optimizely, LaunchDarkly, or custom solutions'),
                ('Analyzing Results', 'Interpret experiment results and make data-driven decisions'),
                ('Multivariate Testing', 'Test multiple variables simultaneously'),
                ('Experimentation Culture', 'Build a culture of continuous experimentation')
            ],
            'Product Analytics': [
                ('Analytics Fundamentals', 'Understand product metrics and analytics frameworks'),
                ('Funnel Analysis', 'Analyze user funnels and identify drop-off points'),
                ('Cohort Analysis', 'Track user behavior over time using cohort analysis'),
                ('Retention Analysis', 'Measure and improve user retention'),
                ('Analytics Tools', 'Use Mixpanel, Amplitude, Google Analytics, or similar tools'),
                ('Data-Driven Decision Making', 'Make product decisions based on data and insights'),
                ('Dashboard Creation', 'Build product dashboards for key metrics'),
                ('Qualitative Research', 'Combine quantitative data with user interviews and surveys')
            ],
            'Market Research': [
                ('Research Fundamentals', 'Understand qualitative vs quantitative research methods'),
                ('User Interviews', 'Conduct effective user interviews to uncover insights'),
                ('Surveys & Questionnaires', 'Design and analyze surveys for product research'),
                ('Competitive Intelligence', 'Gather and analyze competitor information'),
                ('Market Sizing', 'Estimate TAM, SAM, and SOM for your product'),
                ('Persona Development', 'Create data-driven user personas'),
                ('Jobs-to-be-Done Framework', 'Apply JTBD theory to understand user motivations'),
                ('Research Synthesis', 'Synthesize research findings into actionable insights')
            ],
            'Go-to-Market Strategy': [
                ('GTM Fundamentals', 'Understand the components of a go-to-market strategy'),
                ('Target Audience Definition', 'Define and segment your target market'),
                ('Value Proposition Design', 'Craft a compelling value proposition'),
                ('Pricing Strategy', 'Develop pricing models aligned with value and market'),
                ('Distribution Channels', 'Select and optimize distribution channels'),
                ('Launch Planning', 'Plan and execute a successful product launch'),
                ('Sales Enablement', 'Equip sales teams with tools and messaging'),
                ('Post-Launch Optimization', 'Measure launch success and iterate quickly')
            ],
            'Competitive Analysis': [
                ('Competitive Landscape Mapping', 'Identify and categorize direct and indirect competitors'),
                ('Feature Comparison', 'Compare product features across competitors'),
                ('SWOT Analysis', 'Assess strengths, weaknesses, opportunities, and threats'),
                ('Positioning Maps', 'Visualize competitive positioning'),
                ('Win/Loss Analysis', 'Analyze why deals are won or lost against competitors'),
                ('Competitive Monitoring', 'Set up systems to track competitor moves'),
                ('Differentiation Strategy', 'Define and communicate your unique advantages'),
                ('Competitive Pricing Analysis', 'Benchmark pricing against competitors')
            ],
            'Customer Journey Mapping': [
                ('Journey Map Fundamentals', 'Understand the purpose and components of journey maps'),
                ('User Research for Journey Maps', 'Gather data to inform journey mapping'),
                ('Touchpoint Identification', 'Map all customer touchpoints across channels'),
                ('Pain Point Analysis', 'Identify friction and pain points in the journey'),
                ('Opportunity Identification', 'Find opportunities to improve the customer experience'),
                ('Emotional Journey Mapping', 'Capture customer emotions at each stage'),
                ('Service Blueprint', 'Map front-stage and back-stage processes'),
                ('Journey Map Presentation', 'Present journey maps to drive organizational change')
            ],
            'OKRs': [
                ('OKR Fundamentals', 'Understand the OKR framework and its benefits'),
                ('Writing Effective Objectives', 'Craft inspiring, qualitative objectives'),
                ('Defining Key Results', 'Write measurable, time-bound key results'),
                ('OKR Alignment', 'Align OKRs across teams and the organization'),
                ('OKR Check-ins', 'Conduct regular OKR reviews and updates'),
                ('Grading OKRs', 'Score OKRs objectively at the end of the cycle'),
                ('OKR Pitfalls', 'Avoid common OKR mistakes and anti-patterns'),
                ('OKR Tools', 'Use tools like Lattice, Gtmhub, or Notion for OKR tracking')
            ],
            'Prioritization': [
                ('Prioritization Fundamentals', 'Understand why prioritization is critical in product management'),
                ('RICE Framework', 'Apply Reach, Impact, Confidence, Effort scoring'),
                ('MoSCoW Method', 'Categorize features as Must-have, Should-have, Could-have, Won\'t-have'),
                ('Kano Model', 'Classify features by customer satisfaction impact'),
                ('Value vs Effort Matrix', 'Prioritize based on value delivered vs effort required'),
                ('Opportunity Scoring', 'Use opportunity scoring to identify high-value areas'),
                ('Stakeholder-Driven Prioritization', 'Balance stakeholder input with data-driven decisions'),
                ('Continuous Prioritization', 'Maintain a living prioritization process')
            ],
        }
    
    def get_topics(self, skill: str) -> List[Dict[str, str]]:
        """
        Get learning topics with objectives for a skill
        
        Args:
            skill: Skill name
        
        Returns:
            List of dictionaries with 'topic' and 'objective' keys
        """
        # Case-insensitive lookup
        skill_lower = skill.lower()
        
        for key, topics_data in self.skill_topics.items():
            if key.lower() == skill_lower:
                # Check if topics are tuples (topic, objective) or just strings
                if topics_data and isinstance(topics_data[0], tuple):
                    return [
                        {'topic': topic, 'objective': objective}
                        for topic, objective in topics_data
                    ]
                else:
                    # Legacy format - generate objectives
                    return [
                        {'topic': topic, 'objective': self._generate_objective(skill, topic)}
                        for topic in topics_data
                    ]
        
        # Return generic topics if skill not found
        return self._generate_generic_topics(skill)
    
    def _generate_objective(self, skill: str, topic: str) -> str:
        """Generate a learning objective for a topic"""
        return f"Understand and apply {topic} concepts in {skill}"
    
    def _generate_generic_topics(self, skill: str) -> List[Dict[str, str]]:
        """Generate generic topics with objectives for unmapped skills"""
        generic_topics = [
            (f'{skill} Fundamentals', f'Understand core concepts and principles of {skill}'),
            (f'{skill} Core Concepts', f'Master essential {skill} techniques and methodologies'),
            (f'{skill} Practical Applications', f'Apply {skill} to real-world scenarios and projects'),
            (f'{skill} Best Practices', f'Learn industry standards and best practices for {skill}'),
            (f'{skill} Advanced Topics', f'Explore advanced concepts and techniques in {skill}'),
            (f'{skill} Real-World Projects', f'Build practical projects using {skill}'),
            (f'{skill} Tools & Ecosystem', f'Master tools and frameworks related to {skill}'),
            (f'{skill} Mastery & Optimization', f'Optimize and refine {skill} skills for professional use')
        ]
        
        return [
            {'topic': topic, 'objective': objective}
            for topic, objective in generic_topics
        ]
    
    def get_all_skills(self) -> List[str]:
        """Get list of all mapped skills"""
        return list(self.skill_topics.keys())
    
    def has_mapping(self, skill: str) -> bool:
        """Check if skill has explicit mapping"""
        skill_lower = skill.lower()
        return any(key.lower() == skill_lower for key in self.skill_topics.keys())


if __name__ == "__main__":
    # Test
    mapper = SkillTopicsMapping()
    
    print("Testing Skill Topics Mapping:")
    print("="*60)
    
    # Test 1: Machine Learning
    ml_topics = mapper.get_topics('Machine Learning')
    print(f"\nMachine Learning Topics ({len(ml_topics)}):")
    for i, topic in enumerate(ml_topics, 1):
        print(f"  Week {i}: {topic}")
    
    # Test 2: Python
    python_topics = mapper.get_topics('Python')
    print(f"\nPython Topics ({len(python_topics)}):")
    for i, topic in enumerate(python_topics, 1):
        print(f"  Week {i}: {topic}")
    
    # Test 3: Unknown skill
    unknown_topics = mapper.get_topics('Blockchain')
    print(f"\nBlockchain Topics (generic) ({len(unknown_topics)}):")
    for i, topic in enumerate(unknown_topics, 1):
        print(f"  Week {i}: {topic}")
    
    print(f"\n✅ Total mapped skills: {len(mapper.get_all_skills())}")
