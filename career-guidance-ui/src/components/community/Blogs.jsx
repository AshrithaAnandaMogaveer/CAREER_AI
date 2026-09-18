import React, { useState, useEffect } from 'react';
import { getStoredToken, getStoredUser } from '../../services/authService';
import CreateBlogModal from './CreateBlogModal';

const Blogs = () => {
  const token = getStoredToken();
  const currentUser = getStoredUser();
  const [blogs, setBlogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [deletingId, setDeletingId] = useState(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(null);
  const [likingId, setLikingId] = useState(null);

  useEffect(() => {
    fetchBlogs();
  }, []);

  const fetchBlogs = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:5000/api/community/blogs', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      if (data.success) {
        setBlogs(data.blogs || []);
      }
    } catch (error) {
      console.error('Error fetching blogs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleBlogCreated = () => {
    setShowCreateModal(false);
    fetchBlogs();
  };

  const handleDeleteClick = (blogId) => {
    setShowDeleteConfirm(blogId);
  };

  const handleDeleteConfirm = async () => {
    const blogId = showDeleteConfirm;
    try {
      setDeletingId(blogId);
      const response = await fetch(`http://localhost:5000/api/community/blogs/${blogId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      
      if (data.success) {
        // Remove the deleted blog from the list
        setBlogs(blogs.filter(blog => blog.id !== blogId));
        setShowDeleteConfirm(null);
      } else {
        alert(data.message || 'Failed to delete blog');
      }
    } catch (error) {
      console.error('Error deleting blog:', error);
      alert('Failed to delete blog. Please try again.');
    } finally {
      setDeletingId(null);
    }
  };

  const handleDeleteCancel = () => {
    setShowDeleteConfirm(null);
  };

  const handleLike = async (e, blogId) => {
    e.stopPropagation();
    if (likingId === blogId) return; // prevent double-click
    setLikingId(blogId);

    // Optimistic update — use likes_count field (what backend returns)
    setBlogs(prev => prev.map(b =>
      b.id === blogId ? { ...b, likes_count: (b.likes_count || 0) + 1 } : b
    ));

    try {
      const response = await fetch(
        `http://localhost:5000/api/community/posts/${blogId}/like`,
        { method: 'POST', headers: { 'Authorization': `Bearer ${token}` } }
      );
      const data = await response.json();
      if (data.success) {
        // Sync real count from server
        setBlogs(prev => prev.map(b =>
          b.id === blogId
            ? { ...b, likes_count: data.likes_count !== undefined ? data.likes_count : b.likes_count }
            : b
        ));
      } else {
        // Revert on failure
        setBlogs(prev => prev.map(b =>
          b.id === blogId ? { ...b, likes_count: Math.max(0, (b.likes_count || 1) - 1) } : b
        ));
      }
    } catch {
      // Revert on error
      setBlogs(prev => prev.map(b =>
        b.id === blogId ? { ...b, likes_count: Math.max(0, (b.likes_count || 1) - 1) } : b
      ));
    } finally {
      setLikingId(null);
    }
  };

  if (loading) {
    return <div className="text-center py-8 text-gray-400">Loading blogs...</div>;
  }

  return (
    <div>
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-2xl font-bold text-white">Blogs</h2>
          <p className="text-gray-400 text-sm mt-1">Share your knowledge and experiences</p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="px-4 py-2 bg-teal-500 text-white rounded-lg hover:bg-teal-600 transition"
        >
          + Write Blog
        </button>
      </div>

      {/* Blog Feed */}
      {blogs.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-400 mb-4">No blogs published yet</p>
          <button
            onClick={() => setShowCreateModal(true)}
            className="text-teal-500 hover:text-teal-400"
          >
            Write the first blog!
          </button>
        </div>
      ) : (
        <div className="space-y-6">
          {blogs.map((blog) => (
            <article
              key={blog.id}
              className="bg-dark p-6 rounded-lg border border-gray-700 hover:border-teal-500 transition cursor-pointer"
            >
              {/* Author Info */}
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-purple-500 rounded-full flex items-center justify-center text-white font-semibold">
                    {blog.author_name?.charAt(0).toUpperCase() || 'U'}
                  </div>
                  <div>
                    <p className="text-white font-medium">{blog.author_name || 'Anonymous'}</p>
                    <p className="text-gray-400 text-sm">
                      {new Date(blog.created_at).toLocaleDateString()} · {blog.read_time || '5'} min read
                    </p>
                  </div>
                </div>
                
                {/* Delete Button - Show for all blogs */}
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDeleteClick(blog.id);
                  }}
                  className="text-gray-400 hover:text-red-500 transition p-2"
                  title="Delete blog"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                </button>
              </div>

              {/* Blog Content */}
              <h3 className="text-2xl font-bold text-white mb-3 hover:text-teal-500 transition">
                {blog.title}
              </h3>
              
              <p className="text-gray-300 leading-relaxed mb-4 line-clamp-3">
                {blog.content}
              </p>

              {/* Video Player for Uploaded Videos */}
              {blog.video_url && (
                <div className="mb-4 rounded-lg overflow-hidden bg-black">
                  <video
                    width="100%"
                    height="400"
                    controls
                    className="w-full"
                  >
                    <source src={`http://localhost:5000/api/community/videos/${blog.video_url.split('/').pop()}`} type="video/mp4" />
                    Your browser does not support the video tag.
                  </video>
                </div>
              )}

              {/* Tags */}
              {blog.tags && blog.tags.length > 0 && (
                <div className="flex flex-wrap gap-2 mb-4">
                  {blog.tags.map((tag, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-gray-700 text-gray-300 text-xs rounded-full"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
              )}

              {/* Engagement Stats */}
              <div className="flex items-center gap-6 text-sm text-gray-400">
                <button
                  onClick={(e) => handleLike(e, blog.id)}
                  disabled={likingId === blog.id}
                  className={`flex items-center gap-1 transition ${likingId === blog.id ? 'opacity-50' : 'hover:text-teal-500'}`}
                >
                  <span>👍</span>
                  <span>{blog.likes_count || 0}</span>
                </button>
                <button className="flex items-center gap-1 hover:text-teal-500 transition">
                  <span>💬</span>
                  <span>{blog.comments_count || 0}</span>
                </button>
                <button className="flex items-center gap-1 hover:text-teal-500 transition">
                  <span>🔖</span>
                  <span>{blog.bookmarks || 0}</span>
                </button>
              </div>
            </article>
          ))}
        </div>
      )}

      {/* Create Blog Modal */}
      {showCreateModal && (
        <CreateBlogModal
          onClose={() => setShowCreateModal(false)}
          onSuccess={handleBlogCreated}
        />
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-dark p-6 rounded-lg border border-gray-700 max-w-md w-full mx-4">
            <h3 className="text-xl font-bold text-white mb-4">Delete Blog</h3>
            <p className="text-gray-300 mb-6">
              Are you sure you want to delete this blog? This action cannot be undone.
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

export default Blogs;
