# Resume Builder Backend Implementation

## Flask Backend Structure

### File Structure
```
backend/
├── routes/
│   └── resume.py
├── utils/
│   ├── pdf_generator.py
│   └── docx_generator.py
├── app.py
└── requirements.txt
```

### Installation Requirements

Add to `requirements.txt`:
```
Flask==2.3.0
Flask-CORS==4.0.0
reportlab==4.0.4
python-docx==0.8.11
```

Install:
```bash
pip install -r requirements.txt
```

---

## 1. Resume Routes (`routes/resume.py`)

```python
from flask import Blueprint, request, send_file, jsonify
from utils.pdf_generator import generate_pdf_resume
from utils.docx_generator import generate_docx_resume
import io
import traceback

resume_bp = Blueprint('resume', __name__)

@resume_bp.route('/api/resume/download/pdf', methods=['POST'])
def download_pdf():
    """Generate and download PDF resume"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        template = data.get('template', 'modern')
        resume_data = data.get('resumeData', {})
        
        # Validate resume data
        if not resume_data.get('personalInfo', {}).get('name'):
            return jsonify({'error': 'Name is required'}), 400
        
        # Generate PDF
        pdf_buffer = generate_pdf_resume(resume_data, template)
        
        # Send file
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'resume_{resume_data["personalInfo"]["name"].replace(" ", "_")}.pdf'
        )
    
    except Exception as e:
        print(f"PDF Generation Error: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': 'Failed to generate PDF', 'details': str(e)}), 500


@resume_bp.route('/api/resume/download/docx', methods=['POST'])
def download_docx():
    """Generate and download DOCX resume"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        template = data.get('template', 'modern')
        resume_data = data.get('resumeData', {})
        
        # Validate resume data
        if not resume_data.get('personalInfo', {}).get('name'):
            return jsonify({'error': 'Name is required'}), 400
        
        # Generate DOCX
        docx_buffer = generate_docx_resume(resume_data, template)
        
        # Send file
        return send_file(
            docx_buffer,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            as_attachment=True,
            download_name=f'resume_{resume_data["personalInfo"]["name"].replace(" ", "_")}.docx'
        )
    
    except Exception as e:
        print(f"DOCX Generation Error: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': 'Failed to generate DOCX', 'details': str(e)}), 500
```

---

## 2. PDF Generator (`utils/pdf_generator.py`)

```python
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.colors import HexColor
import io


def generate_pdf_resume(resume_data, template='modern'):
    """
    Generate PDF resume using reportlab.platypus
    ATS-friendly: No canvas, no absolute positioning
    """
    buffer = io.BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Container for flowables
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=HexColor('#1a1a1a'),
        spaceAfter=6,
        alignment=TA_CENTER if template == 'minimal' else TA_LEFT
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=HexColor('#2563eb'),
        spaceAfter=6,
        spaceBefore=12,
        borderWidth=0,
        borderColor=HexColor('#2563eb'),
        borderPadding=0,
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=11,
        textColor=HexColor('#1a1a1a'),
        spaceAfter=3,
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor('#4a4a4a'),
        spaceAfter=6,
    )
    
    small_style = ParagraphStyle(
        'CustomSmall',
        parent=styles['Normal'],
        fontSize=9,
        textColor=HexColor('#6a6a6a'),
        spaceAfter=3,
    )
    
    # Personal Information
    personal_info = resume_data.get('personalInfo', {})
    name = personal_info.get('name', 'Your Name')
    
    story.append(Paragraph(name, title_style))
    
    contact_parts = []
    if personal_info.get('email'):
        contact_parts.append(personal_info['email'])
    if personal_info.get('phone'):
        contact_parts.append(personal_info['phone'])
    if personal_info.get('location'):
        contact_parts.append(personal_info['location'])
    
    if contact_parts:
        story.append(Paragraph(' | '.join(contact_parts), small_style))
    
    links_parts = []
    if personal_info.get('linkedin'):
        links_parts.append(personal_info['linkedin'])
    if personal_info.get('github'):
        links_parts.append(personal_info['github'])
    
    if links_parts:
        story.append(Paragraph(' | '.join(links_parts), small_style))
    
    story.append(Spacer(1, 0.2*inch))
    
    # Professional Summary
    summary = resume_data.get('summary', '')
    if summary:
        story.append(Paragraph('PROFESSIONAL SUMMARY', heading_style))
        story.append(Paragraph(summary, normal_style))
        story.append(Spacer(1, 0.1*inch))
    
    # Skills
    skills = resume_data.get('skills', [])
    if skills and any(skills):
        story.append(Paragraph('SKILLS', heading_style))
        skills_text = ' • '.join([s for s in skills if s])
        story.append(Paragraph(skills_text, normal_style))
        story.append(Spacer(1, 0.1*inch))
    
    # Experience
    experience = resume_data.get('experience', [])
    if experience:
        story.append(Paragraph('EXPERIENCE', heading_style))
        for exp in experience:
            if exp.get('role') or exp.get('company'):
                role_company = f"<b>{exp.get('role', 'Role')}</b> - {exp.get('company', 'Company')}"
                story.append(Paragraph(role_company, subheading_style))
                
                if exp.get('duration'):
                    story.append(Paragraph(exp['duration'], small_style))
                
                if exp.get('description'):
                    story.append(Paragraph(exp['description'], normal_style))
                
                story.append(Spacer(1, 0.05*inch))
        story.append(Spacer(1, 0.1*inch))
    
    # Education
    education = resume_data.get('education', [])
    if education:
        story.append(Paragraph('EDUCATION', heading_style))
        for edu in education:
            if edu.get('degree') or edu.get('institution'):
                degree_inst = f"<b>{edu.get('degree', 'Degree')}</b> - {edu.get('institution', 'Institution')}"
                story.append(Paragraph(degree_inst, subheading_style))
                
                year_grade = []
                if edu.get('year'):
                    year_grade.append(edu['year'])
                if edu.get('grade'):
                    year_grade.append(f"Grade: {edu['grade']}")
                
                if year_grade:
                    story.append(Paragraph(' | '.join(year_grade), small_style))
                
                story.append(Spacer(1, 0.05*inch))
        story.append(Spacer(1, 0.1*inch))
    
    # Projects
    projects = resume_data.get('projects', [])
    if projects:
        story.append(Paragraph('PROJECTS', heading_style))
        for project in projects:
            if project.get('title'):
                story.append(Paragraph(f"<b>{project['title']}</b>", subheading_style))
                
                if project.get('techStack'):
                    story.append(Paragraph(f"<i>Tech Stack: {project['techStack']}</i>", small_style))
                
                if project.get('description'):
                    story.append(Paragraph(project['description'], normal_style))
                
                story.append(Spacer(1, 0.05*inch))
        story.append(Spacer(1, 0.1*inch))
    
    # Certifications
    certifications = resume_data.get('certifications', [])
    if certifications and any(certifications):
        story.append(Paragraph('CERTIFICATIONS', heading_style))
        cert_items = [ListItem(Paragraph(cert, normal_style)) for cert in certifications if cert]
        story.append(ListFlowable(cert_items, bulletType='bullet'))
        story.append(Spacer(1, 0.1*inch))
    
    # Achievements
    achievements = resume_data.get('achievements', [])
    if achievements and any(achievements):
        story.append(Paragraph('ACHIEVEMENTS', heading_style))
        achievement_items = [ListItem(Paragraph(ach, normal_style)) for ach in achievements if ach]
        story.append(ListFlowable(achievement_items, bulletType='bullet'))
    
    # Build PDF
    doc.build(story)
    
    buffer.seek(0)
    return buffer
```

---

## 3. DOCX Generator (`utils/docx_generator.py`)

```python
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io


def generate_docx_resume(resume_data, template='modern'):
    """
    Generate DOCX resume using python-docx
    ATS-friendly with proper heading hierarchy
    """
    doc = Document()
    
    # Set margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
    
    # Personal Information
    personal_info = resume_data.get('personalInfo', {})
    name = personal_info.get('name', 'Your Name')
    
    # Name (Title)
    name_para = doc.add_paragraph()
    name_run = name_para.add_run(name)
    name_run.font.size = Pt(24)
    name_run.font.bold = True
    name_run.font.color.rgb = RGBColor(26, 26, 26)
    name_para.alignment = WD_ALIGN_PARAGRAPH.CENTER if template == 'minimal' else WD_ALIGN_PARAGRAPH.LEFT
    
    # Contact Info
    contact_parts = []
    if personal_info.get('email'):
        contact_parts.append(personal_info['email'])
    if personal_info.get('phone'):
        contact_parts.append(personal_info['phone'])
    if personal_info.get('location'):
        contact_parts.append(personal_info['location'])
    
    if contact_parts:
        contact_para = doc.add_paragraph(' | '.join(contact_parts))
        contact_para.runs[0].font.size = Pt(10)
        contact_para.runs[0].font.color.rgb = RGBColor(106, 106, 106)
    
    # Links
    links_parts = []
    if personal_info.get('linkedin'):
        links_parts.append(personal_info['linkedin'])
    if personal_info.get('github'):
        links_parts.append(personal_info['github'])
    
    if links_parts:
        links_para = doc.add_paragraph(' | '.join(links_parts))
        links_para.runs[0].font.size = Pt(10)
        links_para.runs[0].font.color.rgb = RGBColor(37, 99, 235)
    
    doc.add_paragraph()  # Spacer
    
    # Professional Summary
    summary = resume_data.get('summary', '')
    if summary:
        add_section_heading(doc, 'PROFESSIONAL SUMMARY')
        summary_para = doc.add_paragraph(summary)
        summary_para.runs[0].font.size = Pt(10)
    
    # Skills
    skills = resume_data.get('skills', [])
    if skills and any(skills):
        add_section_heading(doc, 'SKILLS')
        skills_text = ' • '.join([s for s in skills if s])
        skills_para = doc.add_paragraph(skills_text)
        skills_para.runs[0].font.size = Pt(10)
    
    # Experience
    experience = resume_data.get('experience', [])
    if experience:
        add_section_heading(doc, 'EXPERIENCE')
        for exp in experience:
            if exp.get('role') or exp.get('company'):
                # Role and Company
                role_para = doc.add_paragraph()
                role_run = role_para.add_run(f"{exp.get('role', 'Role')} - {exp.get('company', 'Company')}")
                role_run.font.size = Pt(11)
                role_run.font.bold = True
                
                # Duration
                if exp.get('duration'):
                    duration_para = doc.add_paragraph(exp['duration'])
                    duration_para.runs[0].font.size = Pt(9)
                    duration_para.runs[0].font.italic = True
                
                # Description
                if exp.get('description'):
                    desc_para = doc.add_paragraph(exp['description'])
                    desc_para.runs[0].font.size = Pt(10)
    
    # Education
    education = resume_data.get('education', [])
    if education:
        add_section_heading(doc, 'EDUCATION')
        for edu in education:
            if edu.get('degree') or edu.get('institution'):
                # Degree and Institution
                edu_para = doc.add_paragraph()
                edu_run = edu_para.add_run(f"{edu.get('degree', 'Degree')} - {edu.get('institution', 'Institution')}")
                edu_run.font.size = Pt(11)
                edu_run.font.bold = True
                
                # Year and Grade
                year_grade = []
                if edu.get('year'):
                    year_grade.append(edu['year'])
                if edu.get('grade'):
                    year_grade.append(f"Grade: {edu['grade']}")
                
                if year_grade:
                    year_para = doc.add_paragraph(' | '.join(year_grade))
                    year_para.runs[0].font.size = Pt(9)
    
    # Projects
    projects = resume_data.get('projects', [])
    if projects:
        add_section_heading(doc, 'PROJECTS')
        for project in projects:
            if project.get('title'):
                # Project Title
                title_para = doc.add_paragraph()
                title_run = title_para.add_run(project['title'])
                title_run.font.size = Pt(11)
                title_run.font.bold = True
                
                # Tech Stack
                if project.get('techStack'):
                    tech_para = doc.add_paragraph(f"Tech Stack: {project['techStack']}")
                    tech_para.runs[0].font.size = Pt(9)
                    tech_para.runs[0].font.italic = True
                
                # Description
                if project.get('description'):
                    desc_para = doc.add_paragraph(project['description'])
                    desc_para.runs[0].font.size = Pt(10)
    
    # Certifications
    certifications = resume_data.get('certifications', [])
    if certifications and any(certifications):
        add_section_heading(doc, 'CERTIFICATIONS')
        for cert in certifications:
            if cert:
                cert_para = doc.add_paragraph(cert, style='List Bullet')
                cert_para.runs[0].font.size = Pt(10)
    
    # Achievements
    achievements = resume_data.get('achievements', [])
    if achievements and any(achievements):
        add_section_heading(doc, 'ACHIEVEMENTS')
        for ach in achievements:
            if ach:
                ach_para = doc.add_paragraph(ach, style='List Bullet')
                ach_para.runs[0].font.size = Pt(10)
    
    # Save to buffer
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer


def add_section_heading(doc, text):
    """Add a section heading with consistent styling"""
    heading = doc.add_paragraph()
    heading_run = heading.add_run(text)
    heading_run.font.size = Pt(14)
    heading_run.font.bold = True
    heading_run.font.color.rgb = RGBColor(37, 99, 235)
    heading.space_before = Pt(12)
    heading.space_after = Pt(6)
```

---

## 4. Update Main App (`app.py`)

```python
from flask import Flask
from flask_cors import CORS
from routes.resume import resume_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Register blueprints
app.register_blueprint(resume_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

---

## Testing the Backend

### 1. Start Flask Server
```bash
python app.py
```

### 2. Test with cURL

**PDF Download:**
```bash
curl -X POST http://localhost:5000/api/resume/download/pdf \
  -H "Content-Type: application/json" \
  -d '{
    "template": "modern",
    "resumeData": {
      "personalInfo": {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890"
      },
      "summary": "Experienced software engineer",
      "skills": ["Python", "React", "Node.js"],
      "experience": [],
      "education": [],
      "projects": [],
      "certifications": [],
      "achievements": []
    }
  }' \
  --output resume.pdf
```

**DOCX Download:**
```bash
curl -X POST http://localhost:5000/api/resume/download/docx \
  -H "Content-Type: application/json" \
  -d '{
    "template": "modern",
    "resumeData": {
      "personalInfo": {
        "name": "John Doe",
        "email": "john@example.com"
      },
      "summary": "Experienced software engineer",
      "skills": ["Python", "React"],
      "experience": [],
      "education": [],
      "projects": [],
      "certifications": [],
      "achievements": []
    }
  }' \
  --output resume.docx
```

---

## Security Considerations

1. **Input Validation**: Validate all resume data fields
2. **Sanitization**: Remove HTML/script tags from text fields
3. **Rate Limiting**: Add rate limiting to prevent abuse
4. **File Size Limits**: Limit resume data size
5. **Authentication**: Add JWT authentication if needed

---

## ATS Compatibility Checklist

✅ No tables (using Platypus flowables)  
✅ No images in resume body  
✅ Standard fonts (Arial, Helvetica)  
✅ Clear section headings  
✅ Proper heading hierarchy  
✅ No absolute positioning  
✅ Semantic structure  
✅ Consistent spacing  

---

## Frontend Integration

The frontend is already configured to call these endpoints:
- `http://localhost:5000/api/resume/download/pdf`
- `http://localhost:5000/api/resume/download/docx`

Make sure Flask server is running on port 5000 before testing downloads.
