import React, { useState, useEffect } from 'react';
import { getStoredToken, getStoredUser } from '../../services/authService';
import CreateCommunityModal from './CreateCommunityModal';
import CommunityChatRoom from './CommunityChatRoom';
import ChatModal from './ChatModal';

const CommunityGroups = () => {
  const token = getStoredToken();
  const currentUser = getStoredUser();
  const [communities, setCommunities] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [activeTab, setActiveTab] = useState('all'); // 'all' or 'recommended'
  const [selectedCommunity, setSelectedCommunity] = useState(null);
  const [deletingId, setDeletingId] = useState(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(null);
  const [unreadConversations, setUnreadConversations] = useState([]);
  const [openChat, setOpenChat] = useState(null);

  useEffect(() => {
    fetchCommunities();
    fetchRecommendations();
    fetchUnreadMessages();
    const interval = setInterval(fetchUnreadMessages, 15000);
    return () => clearInterval(interval);
  }, []);

  const fetchUnreadMessages = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/community/conversations', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await res.json();
      if (data.success) {
        const withUnread = (data.conversations || []).filter(c => c.unread_count > 0);
        setUnreadConversations(withUnread);
      }
    } catch (e) {}
  };

  const fetchCommunities = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:5000/api/community/groups', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      if (data.success) {
        setCommunities(data.communities || []);
      }
    } catch (error) {
      console.error('Error fetching communities:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchRecommendations = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/community/recommended', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      if (data.success) {
        setRecommendations(data.recommendations || []);
      }
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
  };

  const handleJoinCommunity = async (communityId) => {
    try {
      const response = await fetch('http://localhost:5000/api/community/join', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ community_id: communityId })
      });
      const data = await response.json();
      if (data.success) {
        // Refresh both lists
        fetchCommunities();
        fetchRecommendations();
      } else {
        alert(data.message || 'Failed to join community');
      }
    } catch (error) {
      console.error('Error joining community:', error);
      alert('Failed to join community. Please try again.');
    }
  };

  const handleCommunityCreated = () => {
    setShowCreateModal(false);
    fetchCommunities();
    fetchRecommendations();
  };

  const handleDeleteClick = (communityId) => {
    setShowDeleteConfirm(communityId);
  };

  const handleDeleteConfirm = async () => {
    const communityId = showDeleteConfirm;
    try {
      setDeletingId(communityId);
      const response = await fetch(`http://localhost:5000/api/community/groups/${communityId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      
      if (data.success) {
        // Remove the deleted community from both lists
        setCommunities(communities.filter(c => c.id !== communityId));
        setRecommendations(recommendations.filter(c => c.id !== communityId));
        setShowDeleteConfirm(null);
      } else {
        alert(data.message || 'Failed to delete community');
      }
    } catch (error) {
      console.error('Error deleting community:', error);
      alert('Failed to delete community. Please try again.');
    } finally {
      setDeletingId(null);
    }
  };

  const handleDeleteCancel = () => {
    setShowDeleteConfirm(null);
  };

  const renderCommunityCard = (community, isRecommended = false) => {
    return (
    <div
      key={community.id}
      className="bg-dark p-5 rounded-lg border border-gray-700 hover:border-teal-500 transition"
    >
      {isRecommended && community.similarity_score && (
        <div className="mb-3 flex items-center gap-2">
          <span className="px-2 py-1 bg-teal-500/20 text-teal-400 text-xs rounded-full">
            ⭐ {community.similarity_score}% Match
          </span>
        </div>
      )}
      
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-white mb-1">{community.name}</h3>
          <p className="text-sm text-gray-400 line-clamp-2">{community.description}</p>
        </div>
        
        {/* Delete Button - Show for all communities */}
        <button
          onClick={(e) => {
            e.stopPropagation();
            handleDeleteClick(community.id);
          }}
          className="text-gray-400 hover:text-red-500 transition p-2 ml-2"
          title="Delete community"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
        </button>
      </div>
      
      {isRecommended && community.matching_tags && community.matching_tags.length > 0 && (
        <div className="mb-3">
          <p className="text-xs text-gray-500 mb-1">Matching interests:</p>
          <div className="flex flex-wrap gap-1">
            {community.matching_tags.slice(0, 3).map((tag, idx) => (
              <span key={idx} className="px-2 py-0.5 bg-purple-500/20 text-purple-400 text-xs rounded">
                {tag}
              </span>
            ))}
          </div>
        </div>
      )}
      
      <div className="flex items-center justify-between mt-4">
        <div className="flex items-center gap-4 text-sm text-gray-400">
          <span>📝 {community.posts_count || 0}</span>
        </div>
      </div>

      <div className="mt-4">
        {community.is_member ? (
          <button
            onClick={() => setSelectedCommunity(community)}
            className="w-full py-2 bg-teal-500 text-white rounded-lg hover:bg-teal-600 transition"
          >
            💬 Open Chat Room
          </button>
        ) : (
          <button
            onClick={() => handleJoinCommunity(community.id)}
            className="w-full py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition"
          >
            Join Community
          </button>
        )}
      </div>
    </div>
    );
  };

  if (loading) {
    return <div className="text-center py-8 text-gray-400">Loading communities...</div>;
  }

  return (
    <div>
      {/* Header with Create Button */}
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-white">Community Groups</h2>
        <button
          onClick={() => setShowCreateModal(true)}
          className="px-4 py-2 bg-teal-500 text-white rounded-lg hover:bg-teal-600 transition"
        >
          + Create Community
        </button>
      </div>

      {/* Unread Messages Notification */}
      {unreadConversations.length > 0 && (
        <div className="mb-6 bg-dark rounded-lg border border-teal-500/40 p-4">
          <h3 className="text-white font-semibold mb-3 flex items-center gap-2">
            💬 Unread Messages
            <span className="px-2 py-0.5 bg-teal-500 text-white text-xs rounded-full">
              {unreadConversations.reduce((sum, c) => sum + c.unread_count, 0)}
            </span>
          </h3>
          <div className="space-y-2">
            {unreadConversations.map((conv) => (
              <div
                key={conv.conversation_id}
                onClick={() => setOpenChat({ id: conv.other_user?.id, name: conv.other_user?.name, domain: conv.other_user?.domain || 'Professional' })}
                className="flex items-center gap-3 p-3 bg-surface rounded-lg border border-gray-700 hover:border-teal-500 cursor-pointer transition"
              >
                <div className="w-9 h-9 bg-gradient-to-br from-teal-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold flex-shrink-0">
                  {conv.other_user?.name?.charAt(0).toUpperCase() || 'U'}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-white font-medium truncate">{conv.other_user?.name}</p>
                  <p className="text-gray-400 text-xs truncate">{conv.last_message_preview || 'New message'}</p>
                </div>
                <span className="px-2 py-0.5 bg-teal-500 text-white text-xs rounded-full flex-shrink-0">
                  {conv.unread_count} new
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="flex gap-4 mb-6 border-b border-gray-700">
        <button
          onClick={() => setActiveTab('recommended')}
          className={`pb-3 px-4 font-medium transition ${
            activeTab === 'recommended'
              ? 'text-teal-400 border-b-2 border-teal-400'
              : 'text-gray-400 hover:text-gray-300'
          }`}
        >
          ⭐ Recommended for You
        </button>
        <button
          onClick={() => setActiveTab('all')}
          className={`pb-3 px-4 font-medium transition ${
            activeTab === 'all'
              ? 'text-teal-400 border-b-2 border-teal-400'
              : 'text-gray-400 hover:text-gray-300'
          }`}
        >
          All Communities
        </button>
      </div>

      {/* Content */}
      {activeTab === 'recommended' ? (
        <div>
          {recommendations.length === 0 ? (
            <div className="text-center py-12 bg-dark rounded-lg border border-gray-700">
              <p className="text-gray-400 mb-2">No recommendations available</p>
              <p className="text-sm text-gray-500">
                Complete your profile with skills and interests to get personalized recommendations
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {recommendations.map((community) => renderCommunityCard(community, true))}
            </div>
          )}
        </div>
      ) : (
        <div>
          {communities.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-400 mb-4">No communities available yet</p>
              <button
                onClick={() => setShowCreateModal(true)}
                className="text-teal-500 hover:text-teal-400"
              >
                Be the first to create one!
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {communities.map((community) => renderCommunityCard(community, false))}
            </div>
          )}
        </div>
      )}

      {/* Create Community Modal */}
      {showCreateModal && (
        <CreateCommunityModal
          onClose={() => setShowCreateModal(false)}
          onSuccess={handleCommunityCreated}
        />
      )}

      {/* Community Chat Room */}
      {selectedCommunity && (
        <CommunityChatRoom
          community={selectedCommunity}
          onClose={() => setSelectedCommunity(null)}
        />
      )}

      {/* Direct Message Chat Modal */}
      {openChat && openChat.id && (
        <ChatModal
          profile={openChat}
          onClose={() => { setOpenChat(null); fetchUnreadMessages(); }}
        />
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-dark p-6 rounded-lg border border-gray-700 max-w-md w-full mx-4">
            <h3 className="text-xl font-bold text-white mb-4">Delete Community</h3>
            <p className="text-gray-300 mb-6">
              Are you sure you want to delete this community? This action cannot be undone and will affect all members.
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

export default CommunityGroups;
