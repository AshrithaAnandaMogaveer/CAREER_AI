import React, { useState, useEffect } from 'react';
import { getStoredToken, getStoredUser } from '../../services/authService';
import FeedbackModal from './FeedbackModal';

const Feedback = () => {
  const token = getStoredToken();
  const user = getStoredUser();
  const currentUser = getStoredUser();
  const [feedbacks, setFeedbacks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [deletingId, setDeletingId] = useState(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(null);

  useEffect(() => {
    fetchFeedbacks();
  }, []);

  const fetchFeedbacks = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:5000/api/community/feedback', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      if (data.success) {
        setFeedbacks(data.feedbacks || []);
      }
    } catch (error) {
      console.error('Error fetching feedbacks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFeedbackSubmitted = () => {
    setShowModal(false);
    fetchFeedbacks();
  };

  const handleDeleteClick = (feedbackId) => {
    setShowDeleteConfirm(feedbackId);
  };

  const handleDeleteConfirm = async () => {
    const feedbackId = showDeleteConfirm;
    try {
      setDeletingId(feedbackId);
      const response = await fetch(`http://localhost:5000/api/community/feedback/${feedbackId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      
      if (data.success) {
        // Remove the deleted feedback from the list
        setFeedbacks(feedbacks.filter(f => f.id !== feedbackId));
        setShowDeleteConfirm(null);
      } else {
        alert(data.message || 'Failed to delete feedback');
      }
    } catch (error) {
      console.error('Error deleting feedback:', error);
      alert('Failed to delete feedback. Please try again.');
    } finally {
      setDeletingId(null);
    }
  };

  const handleDeleteCancel = () => {
    setShowDeleteConfirm(null);
  };

  if (loading) {
    return <div className="text-center py-8 text-gray-400">Loading feedback...</div>;
  }

  return (
    <div>
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-2xl font-bold text-white">Feedback & Suggestions</h2>
          <p className="text-gray-400 text-sm mt-1">Share your thoughts and help us improve</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2 bg-teal-500 text-white rounded-lg hover:bg-teal-600 transition"
        >
          + Submit Feedback
        </button>
      </div>

      {/* Feedback List */}
      {feedbacks.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-400 mb-4">No feedback yet</p>
          <button
            onClick={() => setShowModal(true)}
            className="text-teal-500 hover:text-teal-400"
          >
            Be the first to share your thoughts!
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {feedbacks.map((feedback) => (
            <div
              key={feedback.id}
              className="bg-dark p-5 rounded-lg border border-gray-700"
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-teal-500 rounded-full flex items-center justify-center text-white font-semibold">
                    {feedback.author_name?.charAt(0).toUpperCase() || 'U'}
                  </div>
                  <div>
                    <p className="text-white font-medium">{feedback.author_name || 'Anonymous'}</p>
                    <p className="text-gray-400 text-sm">{new Date(feedback.created_at).toLocaleDateString()}</p>
                  </div>
                </div>
                
                <div className="flex items-center gap-2">
                  {feedback.category && (
                    <span className="px-3 py-1 bg-purple-500 bg-opacity-20 text-purple-400 text-xs rounded-full">
                      {feedback.category}
                    </span>
                  )}
                  
                  {/* Delete Button - Show for all feedback */}
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteClick(feedback.id);
                    }}
                    className="text-gray-400 hover:text-red-500 transition p-2"
                    title="Delete feedback"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                  </button>
                </div>
              </div>
              
              <p className="text-gray-300 leading-relaxed">{feedback.content}</p>

              {feedback.upvotes !== undefined && (
                <div className="mt-4 flex items-center gap-4">
                  <button className="flex items-center gap-1 text-gray-400 hover:text-teal-500 transition">
                    <span>👍</span>
                    <span className="text-sm">{feedback.upvotes}</span>
                  </button>
                  <button className="flex items-center gap-1 text-gray-400 hover:text-gray-300 transition">
                    <span>💬</span>
                    <span className="text-sm">{feedback.replies_count || 0}</span>
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Feedback Modal */}
      {showModal && (
        <FeedbackModal
          onClose={() => setShowModal(false)}
          onSuccess={handleFeedbackSubmitted}
        />
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-dark p-6 rounded-lg border border-gray-700 max-w-md w-full mx-4">
            <h3 className="text-xl font-bold text-white mb-4">Delete Feedback</h3>
            <p className="text-gray-300 mb-6">
              Are you sure you want to delete this feedback? This action cannot be undone.
            </p>
            <div className="flex gap-3 justify-end">
              <button
                onClick={handleDeleteCancel}
                disabled={deletingId !== null}
                className="px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition disabled:opacity-50"
              >
                Cancel
              </button>
              <button
                onClick={handleDeleteConfirm}
                disabled={deletingId !== null}
                className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition disabled:opacity-50"
              >
                {deletingId ? 'Deleting...' : 'Delete'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Feedback;
