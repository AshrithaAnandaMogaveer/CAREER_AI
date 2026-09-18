"""
Dependency Graph Module
Implements DAG-based skill prerequisite management and topological sorting
"""

from typing import List, Dict, Set, Tuple
from collections import defaultdict, deque


# Comprehensive skill dependency matrix
SKILL_DEPENDENCIES = {
    # Frontend
    'react': ['javascript', 'html', 'css'],
    'angular': ['javascript', 'typescript', 'html', 'css'],
    'vue': ['javascript', 'html', 'css'],
    'next.js': ['react', 'javascript'],
    'typescript': ['javascript'],
    'redux': ['react', 'javascript'],
    
    # Backend
    'node.js': ['javascript'],
    'express': ['node.js', 'javascript'],
    'django': ['python'],
    'flask': ['python'],
    'spring boot': ['java'],
    'fastapi': ['python'],
    
    # Databases
    'mongodb': ['database fundamentals'],
    'postgresql': ['sql', 'database fundamentals'],
    'mysql': ['sql', 'database fundamentals'],
    'redis': ['database fundamentals'],
    
    # DevOps
    'docker': ['linux', 'command line'],
    'kubernetes': ['docker', 'linux'],
    'ci/cd': ['git', 'command line'],
    'jenkins': ['ci/cd'],
    'terraform': ['cloud computing', 'infrastructure'],
    'ansible': ['linux', 'command line'],
    
    # Cloud
    'aws': ['cloud computing'],
    'azure': ['cloud computing'],
    'gcp': ['cloud computing'],
    'lambda': ['aws', 'cloud computing'],
    'serverless': ['cloud computing'],
    
    # Data Science & ML
    'machine learning': ['python', 'statistics', 'linear algebra'],
    'deep learning': ['machine learning', 'python', 'calculus'],
    'tensorflow': ['python', 'machine learning'],
    'pytorch': ['python', 'machine learning'],
    'pandas': ['python'],
    'numpy': ['python'],
    'scikit-learn': ['python', 'machine learning'],
    'nlp': ['machine learning', 'python'],
    'computer vision': ['machine learning', 'python'],
    
    # Testing
    'unit testing': ['programming fundamentals'],
    'integration testing': ['unit testing'],
    'jest': ['javascript', 'unit testing'],
    'pytest': ['python', 'unit testing'],
    'selenium': ['programming fundamentals'],
    
    # Design
    'ui/ux': ['design principles'],
    'figma': ['ui/ux'],
    'responsive design': ['html', 'css'],
    
    # Security
    'cybersecurity': ['networking', 'programming fundamentals'],
    'penetration testing': ['cybersecurity', 'networking'],
    'encryption': ['cybersecurity'],
    
    # Mobile
    'react native': ['react', 'javascript'],
    'flutter': ['dart', 'mobile development'],
    'android': ['java', 'mobile development'],
    'ios': ['swift', 'mobile development'],
    
    # Fundamentals (no dependencies)
    'python': [],
    'java': [],
    'javascript': [],
    'html': [],
    'css': [],
    'sql': [],
    'git': [],
    'linux': [],
    'command line': [],
    'programming fundamentals': [],
    'database fundamentals': [],
    'networking': [],
    'statistics': [],
    'linear algebra': [],
    'calculus': [],
    'design principles': [],
    'cloud computing': [],
    'infrastructure': [],
    'mobile development': [],
    'dart': [],
    'swift': [],
}


class DependencyGraph:
    """Manages skill dependencies using Directed Acyclic Graph"""
    
    def __init__(self):
        self.dependencies = SKILL_DEPENDENCIES
        self.graph = defaultdict(list)
        self.in_degree = defaultdict(int)
    
    def normalize_skill(self, skill: str) -> str:
        """Normalize skill name for matching"""
        return skill.lower().strip()
    
    def get_dependencies(self, skill: str) -> List[str]:
        """Get direct dependencies for a skill"""
        normalized = self.normalize_skill(skill)
        return self.dependencies.get(normalized, [])
    
    def build_graph(self, skills: List[str]) -> None:
        """Build dependency graph for given skills"""
        self.graph.clear()
        self.in_degree.clear()
        
        # Normalize all skills
        normalized_skills = [self.normalize_skill(s) for s in skills]
        
        # Build graph with dependencies
        all_skills = set(normalized_skills)
        
        # Add dependencies recursively
        for skill in normalized_skills:
            self._add_skill_with_deps(skill, all_skills)
        
        # Build adjacency list and in-degree count
        for skill in all_skills:
            deps = self.get_dependencies(skill)
            for dep in deps:
                if dep in all_skills:
                    self.graph[dep].append(skill)
                    self.in_degree[skill] += 1
            
            # Ensure all skills are in in_degree
            if skill not in self.in_degree:
                self.in_degree[skill] = 0
    
    def _add_skill_with_deps(self, skill: str, all_skills: Set[str]) -> None:
        """Recursively add skill and its dependencies"""
        deps = self.get_dependencies(skill)
        for dep in deps:
            if dep not in all_skills:
                all_skills.add(dep)
                self._add_skill_with_deps(dep, all_skills)
    
    def topological_sort(self, skills: List[str]) -> List[str]:
        """
        Perform topological sort to determine learning order
        Returns skills in order from prerequisites to advanced
        """
        self.build_graph(skills)
        
        # Kahn's algorithm for topological sorting
        queue = deque()
        result = []
        
        # Find all nodes with in-degree 0
        for skill in self.in_degree:
            if self.in_degree[skill] == 0:
                queue.append(skill)
        
        # Process queue
        while queue:
            skill = queue.popleft()
            result.append(skill)
            
            # Reduce in-degree for neighbors
            for neighbor in self.graph[skill]:
                self.in_degree[neighbor] -= 1
                if self.in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # Check for cycles (shouldn't happen with our data)
        if len(result) != len(self.in_degree):
            # Return original order if cycle detected
            return [self.normalize_skill(s) for s in skills]
        
        return result
    
    def get_learning_path(self, target_skills: List[str], current_skills: List[str] = None) -> List[Dict]:
        """
        Generate complete learning path with levels
        Returns list of skill groups by dependency level
        """
        if current_skills is None:
            current_skills = []
        
        # Normalize inputs
        target_normalized = [self.normalize_skill(s) for s in target_skills]
        current_normalized = set([self.normalize_skill(s) for s in current_skills])
        
        # Get topologically sorted order
        sorted_skills = self.topological_sort(target_normalized)
        
        # Filter out already known skills
        skills_to_learn = [s for s in sorted_skills if s not in current_normalized]
        
        # Group by dependency level
        levels = []
        remaining = set(skills_to_learn)
        
        while remaining:
            current_level = []
            for skill in list(remaining):
                deps = self.get_dependencies(skill)
                # Check if all dependencies are satisfied
                if all(dep in current_normalized or dep not in remaining for dep in deps):
                    current_level.append(skill)
            
            if not current_level:
                # No progress possible, add remaining skills
                current_level = list(remaining)
            
            levels.append({
                'level': len(levels) + 1,
                'skills': current_level,
                'description': self._get_level_description(len(levels) + 1, current_level)
            })
            
            # Mark these skills as learned for next iteration
            for skill in current_level:
                current_normalized.add(skill)
                remaining.discard(skill)
        
        return levels
    
    def _get_level_description(self, level: int, skills: List[str]) -> str:
        """Generate description for skill level"""
        if level == 1:
            return "Foundation - Core prerequisites"
        elif level == 2:
            return "Intermediate - Building on fundamentals"
        elif level == 3:
            return "Advanced - Specialized skills"
        else:
            return f"Expert - Level {level} skills"
    
    def get_prerequisite_chain(self, skill: str) -> List[str]:
        """Get complete prerequisite chain for a skill"""
        normalized = self.normalize_skill(skill)
        chain = []
        visited = set()
        
        def dfs(s):
            if s in visited:
                return
            visited.add(s)
            
            deps = self.get_dependencies(s)
            for dep in deps:
                dfs(dep)
            
            chain.append(s)
        
        dfs(normalized)
        return chain
    
    def estimate_learning_time(self, skill: str, base_hours: int = 20) -> int:
        """
        Estimate learning time based on dependency depth
        More dependencies = more time needed
        """
        normalized = self.normalize_skill(skill)
        deps = self.get_dependencies(normalized)
        
        if not deps:
            return base_hours
        
        # Add time for each dependency level
        depth = len(self.get_prerequisite_chain(normalized))
        return base_hours + (depth * 5)
    
    def validate_learning_order(self, ordered_skills: List[str]) -> Tuple[bool, List[str]]:
        """
        Validate if skills are in correct learning order
        Returns (is_valid, violations)
        """
        violations = []
        learned = set()
        
        for skill in ordered_skills:
            normalized = self.normalize_skill(skill)
            deps = self.get_dependencies(normalized)
            
            for dep in deps:
                if dep not in learned:
                    violations.append(f"{skill} requires {dep} but it comes later")
            
            learned.add(normalized)
        
        return len(violations) == 0, violations
