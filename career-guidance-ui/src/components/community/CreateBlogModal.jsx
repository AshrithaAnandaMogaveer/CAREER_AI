import React, { useState } from 'react';
import { getStoredToken } from '../../services/authService';

const CreateBlogModal = ({ onClose, onSuccess }) => {
  const token = getStoredToken();
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    tags: ''
  });
  const [videoFile, setVideoFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleVideoChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Validate file size (max 100MB)
      const maxSize = 100 * 1024 * 1024; // 100MB
      if (file.size > maxSize) {
        setError('Video file size must be less than 100MB');
        return;
      }
      
      // Validate file type
      const allowedTypes = ['video/mp4', 'video/avi', 'video/mov', 'video/wmv', 'video/webm', 'video/mkv', 'video/mpeg', 'video/mpg'];
      if (!allowedTypes.includes(file.type)) {
        setError('Invalid video format. Allowed: MP4, AVI, MOV, WMV, WEBM, MKV, MPEG');
        return;
      }
      
      setError('');
      setVideoFile(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Create FormData for file upload
      const formDataToSend = new FormData();
      formDataToSend.append('title', formData.title);
      formDataToSend.append('content', formData.content);
      formDataToSend.append('tags', formData.tags);
      
      if (videoFile) {
        formDataToSend.append('video', videoFile);
      }

      const response = await fetch('http://localhost:5000/api/community/blogs', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
          // Don't set Content-Type - browser will set it with boundary for multipart/form-data
        },
        body: formDataToSend
      });

      const data = await response.json();

      if (data.success) {
        onSuccess();
      } else {
        setError(data.message || 'Failed to publish blog');
      }
    } catch (err) {
      setError('Server error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4 overflow-y-auto">
      <div className="bg-surface rounded-lg max-w-3xl w-full p-6 my-8">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-2xl font-bold text-white">Write a Blog</h3>
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
            <label className="block text-gray-300 mb-2">Title</label>
            <input
              type="text"
              name="title"
              value={formData.title}
              onChange={handleChange}
              className="w-full px-4 py-2 bg-white border border-gray-600 rounded text-gray-900 focus:border-teal-500 focus:outline-none"
              placeholder="Enter an engaging title..."
              required
            />
          </div>

          <div className="mb-4">
            <label className="block text-gray-300 mb-2">Content</label>
            <textarea
              name="content"
              value={formData.content}
              onChange={handleChange}
              rows="12"
              className="w-full px-4 py-2 bg-white border border-gray-600 rounded text-gray-900 focus:border-teal-500 focus:outline-none resize-none"
              placeholder="Write your blog content here... Share your insights, experiences, and knowledge."
              required
            />
            <p className="text-gray-500 text-xs mt-1">
              {formData.content.length} characters
            </p>
          </div>

          <div className="mb-6">
            <label className="block text-gray-300 mb-2">Tags</label>
            <input
              type="text"
              name="tags"
              value={formData.tags}
              onChange={handleChange}
              className="w-full px-4 py-2 bg-white border border-gray-600 rounded text-gray-900 focus:border-teal-500 focus:outline-none"
              placeholder="e.g., React, JavaScript, Career (comma-separated)"
            />
            <p className="text-gray-500 text-xs mt-1">
              Add relevant tags to help others discover your blog
            </p>
          </div>

          <div className="mb-6">
            <label className="block text-gray-300 mb-2">Upload Video (Optional)</label>
            <input
              type="file"
              accept="video/*"
              onChange={handleVideoChange}
              className="w-full px-4 py-2 bg-white border border-gray-600 rounded text-gray-900 focus:border-teal-500 focus:outline-none file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-teal-50 file:text-teal-700 hover:file:bg-teal-100"
            />
            {videoFile && (
              <p className="text-teal-400 text-sm mt-2">
                ✓ Selected: {videoFile.name} ({(videoFile.size / (1024 * 1024)).toFixed(2)} MB)
              </p>
            )}
            <p className="text-gray-500 text-xs mt-1">
              Upload a video file (MP4, AVI, MOV, WMV, WEBM, MKV, MPEG - Max 100MB)
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
              disabled={loading || !formData.title.trim() || !formData.content.trim()}
              className="flex-1 py-2 bg-teal-500 text-white rounded hover:bg-teal-600 transition disabled:opacity-50"
            >
              {loading ? 'Publishing...' : 'Publish Blog'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateBlogModal;
