"""
Report Generator Module
Generates PDF reports for career analysis results
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime
from io import BytesIO
from typing import Dict, List


class ReportGenerator:
    """Generates comprehensive PDF reports for career analysis"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#0f0f1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#00cccc'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#0f0f1a'),
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            spaceAfter=8,
            alignment=TA_JUSTIFY,
            leading=14
        ))
        
        # Bullet point
        self.styles.add(ParagraphStyle(
            name='BulletPoint',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=colors.HexColor('#333333'),
            leftIndent=20,
            spaceAfter=6,
            bulletIndent=10
        ))
    
    def _create_header_footer(self, canvas_obj, doc):
        """Add header and footer to each page"""
        canvas_obj.saveState()
        
        # Header
        canvas_obj.setFont('Helvetica-Bold', 10)
        canvas_obj.setFillColor(colors.HexColor('#00cccc'))
        canvas_obj.drawString(inch, letter[1] - 0.5 * inch, "CareerAI - Career Analysis Report")
        
        # Footer
        canvas_obj.setFont('Helvetica', 8)
        canvas_obj.setFillColor(colors.HexColor('#666666'))
        canvas_obj.drawString(inch, 0.5 * inch, f"Generated on {datetime.now().strftime('%B %d, %Y')}")
        canvas_obj.drawRightString(letter[0] - inch, 0.5 * inch, f"Page {doc.page}")
        
        canvas_obj.restoreState()
    
    def _create_score_table(self, score: float, label: str) -> Table:
        """Create a visual score table"""
        # Determine color based on score
        if score >= 80:
            color = colors.HexColor('#00cc66')  # Green
        elif score >= 60:
            color = colors.HexColor('#ffcc00')  # Yellow
        else:
            color = colors.HexColor('#ff6666')  # Red
        
        data = [
            [label, f"{score}%"]
        ]
        
        table = Table(data, colWidths=[3 * inch, 1.5 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f5f5f5')),
            ('TEXTCOLOR', (0, 0), (0, 0), colors.HexColor('#333333')),
            ('TEXTCOLOR', (1, 0), (1, 0), color),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('PADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
        ]))
        
        return table
    
    def _create_skills_table(self, skills: List[str], title: str) -> Table:
        """Create a table for skills"""
        # Split skills into rows of 3
        rows = []
        for i in range(0, len(skills), 3):
            row = skills[i:i+3]
            # Pad with empty strings if needed
            while len(row) < 3:
                row.append('')
            rows.append(row)
        
        if not rows:
            rows = [['No skills listed', '', '']]
        
        table = Table(rows, colWidths=[2 * inch, 2 * inch, 2 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9f9f9')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
        ]))
        
        return table
    
    def generate_report(self, analysis_data: Dict, user_info: Dict = None) -> BytesIO:
        """Generate complete PDF report"""
        buffer = BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=inch,
            leftMargin=inch,
            topMargin=inch,
            bottomMargin=inch
        )
        
        # Container for PDF elements
        story = []
        
        # Title Page
        story.append(Spacer(1, 0.5 * inch))
        story.append(Paragraph("Career Analysis Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.2 * inch))
        
        if user_info:
            story.append(Paragraph(
                f"Prepared for: {user_info.get('name', 'User')}",
                self.styles['CustomBody']
            ))
            story.append(Paragraph(
                f"Target Domain: {user_info.get('domain', 'Not specified')}",
                self.styles['CustomBody']
            ))
            # Machine-readable marker so fileParser can extract domain reliably
            story.append(Paragraph(
                f"TARGET_DOMAIN_VALUE: {user_info.get('domain', 'Not specified')}",
                self.styles['CustomBody']
            ))
        
        story.append(Paragraph(
            f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            self.styles['CustomBody']
        ))
        story.append(Spacer(1, 0.5 * inch))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 0.1 * inch))
        
        readiness = analysis_data.get('readiness_score', {})
        story.append(self._create_score_table(
            readiness.get('total_score', 0),
            "Career Readiness Score"
        ))
        story.append(Spacer(1, 0.2 * inch))
        
        resume_strength = analysis_data.get('resume_strength', {})
        story.append(self._create_score_table(
            resume_strength.get('total_strength', 0),
            "Resume Strength Score"
        ))
        story.append(Spacer(1, 0.3 * inch))
        
        # Confidence Level
        confidence = readiness.get('confidence_level', 'Medium')
        story.append(Paragraph(
            f"<b>Confidence Level:</b> {confidence}",
            self.styles['CustomBody']
        ))
        story.append(Spacer(1, 0.3 * inch))
        
        # Skills Analysis
        story.append(Paragraph("Skills Analysis", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 0.1 * inch))
        
        # Extracted Skills
        extracted_skills = analysis_data.get('extracted_skills', [])
        story.append(Paragraph(
            f"<b>Total Skills Identified:</b> {len(extracted_skills)}",
            self.styles['CustomBody']
        ))
        story.append(Spacer(1, 0.1 * inch))
        
        if extracted_skills:
            story.append(Paragraph("Your Skills:", self.styles['SectionHeader']))
            story.append(self._create_skills_table(extracted_skills[:15], "Skills"))
            story.append(Spacer(1, 0.2 * inch))
        
        # Skill Coverage
        story.append(Paragraph(
            f"<b>Required Skills Coverage:</b> {readiness.get('required_coverage', 0)}% "
            f"({readiness.get('matched_required', 0)}/{readiness.get('total_required', 0)})",
            self.styles['CustomBody']
        ))
        story.append(Paragraph(
            f"<b>Preferred Skills Coverage:</b> {readiness.get('preferred_coverage', 0)}% "
            f"({readiness.get('matched_preferred', 0)}/{readiness.get('total_preferred', 0)})",
            self.styles['CustomBody']
        ))
        story.append(Spacer(1, 0.3 * inch))
        
        # Skill Gaps
        story.append(Paragraph("Skill Gap Analysis", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 0.1 * inch))
        
        missing_skills = analysis_data.get('missing_skills', {})
        critical_skills = missing_skills.get('critical', [])
        recommended_skills = missing_skills.get('recommended', [])
        
        if critical_skills:
            story.append(Paragraph("Critical Skills to Learn:", self.styles['SectionHeader']))
            for skill in critical_skills[:10]:
                story.append(Paragraph(f"• {skill}", self.styles['BulletPoint']))
            story.append(Spacer(1, 0.2 * inch))
        
        if recommended_skills:
            story.append(Paragraph("Recommended Skills:", self.styles['SectionHeader']))
            for skill in recommended_skills[:10]:
                story.append(Paragraph(f"• {skill}", self.styles['BulletPoint']))
            story.append(Spacer(1, 0.3 * inch))
        
        # Resume Strength Breakdown
        story.append(PageBreak())
        story.append(Paragraph("Resume Strength Analysis", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 0.1 * inch))
        
        strength_data = [
            ['Component', 'Score', 'Max'],
            ['Skills', f"{resume_strength.get('skill_score', 0)}", '30'],
            ['Projects', f"{resume_strength.get('project_score', 0)}", '20'],
            ['Certifications', f"{resume_strength.get('certification_score', 0)}", '15'],
            ['Experience', f"{resume_strength.get('experience_score', 0)}", '15'],
            ['Impact Keywords', f"{resume_strength.get('impact_score', 0)}", '10'],
            ['Metrics', f"{resume_strength.get('metric_score', 0)}", '10'],
        ]
        
        strength_table = Table(strength_data, colWidths=[2.5 * inch, 1.5 * inch, 1.5 * inch])
        strength_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00cccc')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9f9f9')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('PADDING', (0, 1), (-1, -1), 8),
        ]))
        
        story.append(strength_table)
        story.append(Spacer(1, 0.3 * inch))
        
        # Common Mistakes
        mistakes = analysis_data.get('mistakes', [])
        if mistakes:
            story.append(Paragraph("Areas for Improvement", self.styles['CustomSubtitle']))
            story.append(Spacer(1, 0.1 * inch))
            
            for mistake in mistakes:
                severity_color = '#ff6666' if mistake['severity'] == 'high' else '#ffcc00'
                story.append(Paragraph(
                    f"<b><font color='{severity_color}'>⚠</font> {mistake['message']}</b>",
                    self.styles['CustomBody']
                ))
                story.append(Paragraph(
                    f"<i>Suggestion: {mistake['suggestion']}</i>",
                    self.styles['BulletPoint']
                ))
                story.append(Spacer(1, 0.1 * inch))
            
            story.append(Spacer(1, 0.2 * inch))
        
        # Improvement Suggestions
        suggestions = analysis_data.get('suggestions', [])
        if suggestions:
            story.append(Paragraph("Personalized Recommendations", self.styles['CustomSubtitle']))
            story.append(Spacer(1, 0.1 * inch))
            
            for suggestion in suggestions:
                story.append(Paragraph(f"• {suggestion}", self.styles['BulletPoint']))
            
            story.append(Spacer(1, 0.3 * inch))
        
        # Suggested Domains
        suggested_domains = analysis_data.get('suggested_domains', [])
        if suggested_domains:
            story.append(Paragraph("Recommended Career Paths", self.styles['CustomSubtitle']))
            story.append(Spacer(1, 0.1 * inch))
            
            domain_data = [['Domain', 'Match %', 'Matched Skills']]
            for domain in suggested_domains[:5]:
                domain_data.append([
                    domain['domain'],
                    f"{domain['match_percentage']}%",
                    f"{domain['matched_skills']}/{domain['total_skills']}"
                ])
            
            domain_table = Table(domain_data, colWidths=[2.5 * inch, 1.5 * inch, 1.5 * inch])
            domain_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6b46c1')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9f9f9')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('PADDING', (0, 1), (-1, -1), 8),
            ]))
            
            story.append(domain_table)
            story.append(Spacer(1, 0.3 * inch))
        
        # Next Steps
        story.append(PageBreak())
        story.append(Paragraph("Next Steps", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 0.1 * inch))
        
        next_steps = [
            "Review the skill gaps and prioritize learning critical skills",
            "Work on 2-3 substantial projects to demonstrate your abilities",
            "Update your resume with quantifiable achievements and metrics",
            "Consider obtaining relevant certifications in your target domain",
            "Build a portfolio showcasing your best work",
            "Network with professionals in your target field",
            "Practice technical interviews and coding challenges",
            "Stay updated with industry trends and emerging technologies"
        ]
        
        for step in next_steps:
            story.append(Paragraph(f"• {step}", self.styles['BulletPoint']))
        
        story.append(Spacer(1, 0.5 * inch))
        
        # Footer note
        story.append(Paragraph(
            "<i>This report is generated by CareerAI's intelligent analysis system. "
            "Use it as a guide to improve your career readiness and resume quality.</i>",
            self.styles['CustomBody']
        ))
        
        # Build PDF
        doc.build(story, onFirstPage=self._create_header_footer, onLaterPages=self._create_header_footer)
        
        # Get PDF data
        buffer.seek(0)
        return buffer
