import { useState, useRef } from 'react';
import { Download, FileText, Loader } from 'lucide-react';
import Button from '../Button';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';

const DownloadButtons = ({ resumeData, selectedTemplate, previewTheme = 'light' }) => {
  const [loading, setLoading] = useState({ pdf: false, docx: false });
  const [error, setError] = useState('');

  const downloadAsPDF = async () => {
    setLoading(prev => ({ ...prev, pdf: true }));
    setError('');

    try {
      // Find the resume preview element
      const resumeElement = document.querySelector('[data-resume-preview]');
      
      if (!resumeElement) {
        throw new Error('Resume preview not found');
      }

      // Temporarily set to light theme for export
      const originalBg = resumeElement.style.backgroundColor;
      resumeElement.style.backgroundColor = 'white';

      // Capture the resume as canvas
      const canvas = await html2canvas(resumeElement, {
        scale: 2, // Higher quality
        useCORS: true,
        logging: false,
        backgroundColor: '#ffffff',
      });

      // Restore original background
      resumeElement.style.backgroundColor = originalBg;

      // Calculate PDF dimensions (A4 size)
      const imgWidth = 210; // A4 width in mm
      const imgHeight = (canvas.height * imgWidth) / canvas.width;

      // Create PDF
      const pdf = new jsPDF({
        orientation: imgHeight > imgWidth ? 'portrait' : 'portrait',
        unit: 'mm',
        format: 'a4',
      });

      const imgData = canvas.toDataURL('image/png');
      pdf.addImage(imgData, 'PNG', 0, 0, imgWidth, imgHeight);

      // Download
      const fileName = `${resumeData.personalInfo?.name || 'Resume'}_${Date.now()}.pdf`;
      pdf.save(fileName.replace(/\s+/g, '_'));

    } catch (err) {
      console.error('PDF download error:', err);
      setError('Failed to download PDF. Please try again.');
    } finally {
      setLoading(prev => ({ ...prev, pdf: false }));
    }
  };

  const downloadAsDOCX = async () => {
    setLoading(prev => ({ ...prev, docx: true }));
    setError('');

    try {
      // For DOCX, we'll use the backend API
      const response = await fetch(`http://localhost:5000/api/resume/download/docx`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          template: selectedTemplate,
          resumeData: resumeData,
        }),
      });

      if (!response.ok) {
        // If backend not available, show message
        throw new Error('DOCX export requires backend server');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${resumeData.personalInfo?.name || 'Resume'}_${Date.now()}.docx`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

    } catch (err) {
      console.error('DOCX download error:', err);
      setError('DOCX export coming soon. Use PDF for now.');
    } finally {
      setLoading(prev => ({ ...prev, docx: false }));
    }
  };

  return (
    <div className="flex items-center gap-3">
      {error && (
        <span className="text-red-400 text-sm">{error}</span>
      )}
      
      <button
        onClick={downloadAsPDF}
        disabled={loading.pdf || loading.docx}
        className="flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-red-600 to-red-700 text-white rounded-lg hover:from-red-700 hover:to-red-800 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
      >
        {loading.pdf ? (
          <Loader className="animate-spin" size={18} />
        ) : (
          <Download size={18} />
        )}
        <span className="text-sm font-medium">PDF</span>
      </button>

      <button
        onClick={downloadAsDOCX}
        disabled={loading.pdf || loading.docx}
        className="flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg hover:from-blue-700 hover:to-blue-800 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
      >
        {loading.docx ? (
          <Loader className="animate-spin" size={18} />
        ) : (
          <FileText size={18} />
        )}
        <span className="text-sm font-medium">DOCX</span>
      </button>
    </div>
  );
};

export default DownloadButtons;
