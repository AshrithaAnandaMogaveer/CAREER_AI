import React, { useState } from 'react';
import { getStoredToken } from '../../services/authService';

const FeedbackModal = ({ onClose, onSuccess }) => {
  const token = getStoredToken();
  const [formData, setFormData] = useState({
    content: '',
    category: 'General'
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const categories = [
    'General',
    'Feature Request',
    'Bug Report',
    'UI/UX',
    'Performance',
    'Content',
    'Other'
  ];

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:5000/api/community/feedback', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (data.success) {
        onSuccess();
      } else {
        setError(data.message || 'Failed to submit feedback');
      }
    } catch (err) {
      setError('Server error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
      <div className="bg-surface rounded-lg max-w-lg w-full p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-2xl font-bold text-white">Submit Feedback</h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white text-2xl"
          >
            ×
          </button>
        </div>

        {error && (
          <div className="bg-red-500 text-white p-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-300 mb-2">Category</label>
            <select
              name="category"
              value={formData.category}
              onChange={handleChange}
              className="w-full px-4 py-2 bg-white border border-gray-600 rounded text-gray-900 focus:border-teal-500 focus:outline-none"
            >
              {categories.map((cat) => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>
          </div>

          <div className="mb-6">
            <label className="block text-gray-300 mb-2">Your Feedback</label>
            <textarea
              name="content"
              value={formData.content}
              onChange={handleChange}
              rows="6"
              className="w-full px-4 py-2 bg-white border border-gray-600 rounded text-gray-900 focus:border-teal-500 focus:outline-none resize-none"
              placeholder="Share your thoughts, suggestions, or report issues..."
              required
            />
            <p className="text-gray-500 text-xs mt-1">
              {formData.content.length} / 1000 characters
            </p>
          </div>

          <div className="flex gap-3">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 py-2 bg-gray-700 text-white rounded hover:bg-gray-600 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading || !formData.content.trim()}
              className="flex-1 py-2 bg-teal-500 text-white rounded hover:bg-teal-600 transition disabled:opacity-50"
            >
              {loading ? 'Submitting...' : 'Submit'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default FeedbackModal;
