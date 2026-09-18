import React, { useState, useEffect, useRef } from 'react';
import { getStoredToken, getStoredUser } from '../services/authService';
import { uploadProfilePicture } from '../services/authService';
import ChatModal from '../components/community/ChatModal';
import CommunityChatRoom from '../components/community/CommunityChatRoom';

const Profile = () => {
  const [user, setUser] = useState(null);
  const [notifications, setNotifications] = useState([]);
  const [conversations, setConversations] = useState([]);
  const [unreadNotifications, setUnreadNotifications] = useState(0);
  const [unreadMessages, setUnreadMessages] = useState(0);
  const [loading, setLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [editedUser, setEditedUser] = useState({});
  const [openChat, setOpenChat] = useState(null); // { id, name, domain }
  const [openCommunity, setOpenCommunity] = useState(null); // community object for chat room
  const picInputRef = useRef(null);

  const token = getStoredToken();

  useEffect(() => {
    const storedUser = getStoredUser();
    if (storedUser) {
      setUser(storedUser);
      setEditedUser(storedUser);
    }
    fetchProfileData();
  }, []);

  const fetchProfileData = async () => {
    try {
      setLoading(true);

      // Fetch fresh user data from backend (ensures profile_picture is up to date)
      const userResponse = await fetch('http://localhost:5000/api/profile', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const userData = await userResponse.json();
      if (userData.success && userData.user) {
        setUser(userData.user);
        setEditedUser(userData.user);
        // Keep localStorage in sync
        localStorage.setItem('user', JSON.stringify(userData.user));
      }
      const notifResponse = await fetch(
        'http://localhost:5000/api/community/notifications?limit=10',
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      const notifData = await notifResponse.json();
      if (notifData.success) {
        setNotifications(notifData.notifications || []);
        setUnreadNotifications(notifData.unread_count || 0);
      }

      // Fetch conversations
      const convResponse = await fetch(
        'http://localhost:5000/api/community/conversations',
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      const convData = await convResponse.json();
      if (convData.success) {
        setConversations(convData.conversations || []);
        setUnreadMessages(convData.unread_total || 0);
      }
    } catch (error) {
      console.error('Error fetching profile data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePicUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const result = await uploadProfilePicture(file);
    if (result.success) {
      // Re-fetch profile to get updated picture
      const userResponse = await fetch('http://localhost:5000/api/profile', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const userData = await userResponse.json();
      if (userData.success && userData.user) {
        setUser(userData.user);
        localStorage.setItem('user', JSON.stringify(userData.user));
      }
    }
  };

  const handleEditToggle = () => {
    setIsEditing(!isEditing);
    if (isEditing) {
      // Reset to original values if canceling
      setEditedUser(user);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setEditedUser(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSaveProfile = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/user', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: editedUser.name,
          email: editedUser.email,
          domain: editedUser.domain
        })
      });

      const data = await response.json();
      if (data.success) {
        const updatedUser = { ...editedUser, ...data.user };
        setUser(updatedUser);
        setIsEditing(false);
        localStorage.setItem('user', JSON.stringify(updatedUser));
      } else {
        alert(data.message || 'Failed to update profile');
      }
    } catch (error) {
      console.error('Error updating profile:', error);
      alert('Failed to update profile');
    }
  };

  const markNotificationAsRead = async (notificationId) => {
    try {
      const response = await fetch(
        'http://localhost:5000/api/community/notifications/read',
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            notification_id: notificationId
          })
        }
      );

      if (response.ok) {
        // Refresh notifications
        fetchProfileData();
      }
    } catch (error) {
      console.error('Error marking notification as read:', error);
    }
  };

  const markAllNotificationsAsRead = async () => {
    try {
      const response = await fetch(
        'http://localhost:5000/api/community/notifications/read',
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            all: true
          })
        }
      );

      if (response.ok) {
        fetchProfileData();
      }
    } catch (error) {
      console.error('Error marking all notifications as read:', error);
    }
  };

  const deleteNotification = async (e, notificationId) => {
    e.stopPropagation();
    try {
      await fetch(`http://localhost:5000/api/community/notifications/${notificationId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setNotifications(prev => prev.filter(n => n.id !== notificationId));
    } catch (error) {
      console.error('Error deleting notification:', error);
    }
  };

  const deleteConversation = async (e, conversationId) => {
    e.stopPropagation();
    try {
      await fetch(`http://localhost:5000/api/community/conversations/${conversationId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setConversations(prev => prev.filter(c => c.conversation_id !== conversationId));
    } catch (error) {
      console.error('Error deleting conversation:', error);
    }
  };

  const handleNotificationClick = async (notif) => {
    // Mark as read
    if (!notif.is_read) markNotificationAsRead(notif.id);

    // For community group chat messages — open that community's chat room
    if (notif.type === 'NEW_COMMUNITY_MESSAGE' && notif.entity_id) {
      try {
        const res = await fetch(`http://localhost:5000/api/community/groups/${notif.entity_id}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await res.json();
        console.log('Community fetch result:', data);
        if (data.success && data.community) {
          setOpenCommunity(data.community);
        }
      } catch (e) { console.error('Community fetch error:', e); }
      return;
    }

    // Open chat with the actor if we have their ID (private DM notifications)
    if (notif.actor_id) {
      const name = notif.actor_name || notif.message?.split(' ')?.[0] || 'User';
      setOpenChat({ id: notif.actor_id, name, domain: '' });
    }
  };

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'POST_LIKE':
      case 'COMMENT_LIKE':
        return '❤️';
      case 'NEW_COMMENT':
      case 'COMMENT_REPLY':
        return '💬';
      case 'NEW_MESSAGE':
        return '✉️';
      case 'COMMUNITY_JOIN':
        return '👥';
      case 'NEW_POST':
        return '📝';
      case 'NEW_COMMUNITY_MESSAGE':
        return '💬';
      default:
        return '🔔';
    }
  };

  const formatTimestamp = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-primary flex items-center justify-center">
        <div className="text-white text-xl">Loading profile...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-primary py-20 px-4">
      <div className="container mx-auto max-w-6xl">
        <h1 className="text-4xl font-bold text-white mb-8">My Profile</h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Profile Info */}
          <div className="lg:col-span-2 space-y-6">
            {/* User Information Card */}
            <div className="bg-surface rounded-lg p-6 border border-gray-700">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-white">Profile Information</h2>
                <button
                  onClick={isEditing ? handleSaveProfile : handleEditToggle}
                  className={`px-4 py-2 rounded-lg transition ${
                    isEditing
                      ? 'bg-teal-500 hover:bg-teal-600 text-white'
                      : 'bg-gray-700 hover:bg-gray-600 text-white'
                  }`}
                >
                  {isEditing ? 'Save Changes' : 'Edit Profile'}
                </button>
              </div>

              {/* Profile Avatar */}
              <div className="flex items-center gap-6 mb-6">
                <div
                  className="relative w-24 h-24 rounded-full overflow-hidden flex-shrink-0 bg-gradient-to-br from-teal-500 to-purple-500 flex items-center justify-center text-white text-4xl font-bold cursor-pointer group"
                  onClick={() => picInputRef.current?.click()}
                  title="Click to change profile picture"
                >
                  {user?.profile_picture ? (
                    <img
                      src={`http://localhost:5000${user.profile_picture}`}
                      alt={user.name}
                      className="w-full h-full object-cover"
                      onError={(e) => { e.target.style.display = 'none'; }}
                    />
                  ) : (
                    user?.name?.charAt(0).toUpperCase() || 'U'
                  )}
                  {/* Hover overlay */}
                  <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center opacity-0 group-hover:opacity-100 transition">
                    <span className="text-white text-xs text-center">Change Photo</span>
                  </div>
                </div>
                <input
                  ref={picInputRef}
                  type="file"
                  accept="image/png,image/jpeg,image/gif,image/webp"
                  className="hidden"
                  onChange={handlePicUpload}
                />
                <div>
                  <h3 className="text-2xl font-bold text-white">{user?.name}</h3>
                  <p className="text-gray-400">{user?.email}</p>
                  <p className="text-gray-500 text-xs mt-1">Click avatar to change photo</p>
                </div>
              </div>

              {/* Editable Fields */}
              <div className="space-y-4">
                <div>
                  <label className="block text-gray-400 text-sm mb-2">Full Name</label>
                  {isEditing ? (
                    <input
                      type="text"
                      name="name"
                      value={editedUser.name || ''}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 bg-white border border-gray-600 rounded-lg text-black focus:border-teal-500 focus:outline-none"
                    />
                  ) : (
                    <p className="text-white text-lg">{user?.name}</p>
                  )}
                </div>

                <div>
                  <label className="block text-gray-400 text-sm mb-2">Email</label>
                  {isEditing ? (
                    <input
                      type="email"
                      name="email"
                      value={editedUser.email || ''}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 bg-white border border-gray-600 rounded-lg text-black focus:border-teal-500 focus:outline-none"
                    />
                  ) : (
                    <p className="text-white text-lg">{user?.email}</p>
                  )}
                </div>

                <div>
                  <label className="block text-gray-400 text-sm mb-2">Domain/Field</label>
                  {isEditing ? (
                    <input
                      type="text"
                      name="domain"
                      value={editedUser.domain || ''}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 bg-white border border-gray-600 rounded-lg text-black focus:border-teal-500 focus:outline-none"
                    />
                  ) : (
                    <p className="text-white text-lg">{user?.domain || 'Not specified'}</p>
                  )}
                </div>

                {isEditing && (
                  <button
                    onClick={handleEditToggle}
                    className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition"
                  >
                    Cancel
                  </button>
                )}
              </div>
            </div>

            {/* Notifications Card */}
            <div className="bg-surface rounded-lg p-6 border border-gray-700">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-white">
                  Community Notifications
                  {unreadNotifications > 0 && (
                    <span className="ml-3 px-3 py-1 bg-red-500 text-white text-sm rounded-full">
                      {unreadNotifications} new
                    </span>
                  )}
                </h2>
                {unreadNotifications > 0 && (
                  <button
                    onClick={markAllNotificationsAsRead}
                    className="text-teal-400 hover:text-teal-300 text-sm"
                  >
                    Mark all as read
                  </button>
                )}
              </div>

              {notifications.length === 0 ? (
                <p className="text-gray-400 text-center py-8">No notifications yet</p>
              ) : (
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {notifications.map((notif) => (
                    <div
                      key={notif.id}
                      className={`p-4 rounded-lg border transition cursor-pointer ${
                        notif.is_read
                          ? 'bg-dark border-gray-700'
                          : 'bg-teal-500 bg-opacity-10 border-teal-500'
                      }`}
                      onClick={() => handleNotificationClick(notif)}
                    >
                      <div className="flex items-start gap-3">
                        <span className="text-2xl">{getNotificationIcon(notif.type)}</span>
                        <div className="flex-1">
                          <p className="text-white font-semibold">{notif.title}</p>
                          <p className="text-gray-300 text-sm mt-1">{notif.message}</p>
                          <div className="flex items-center justify-between mt-2">
                            <p className="text-gray-500 text-xs">
                              {formatTimestamp(notif.timestamp)}
                            </p>
                            {notif.type === 'NEW_COMMUNITY_MESSAGE' ? (
                              <button
                                onClick={(e) => { e.stopPropagation(); handleNotificationClick(notif); }}
                                className="text-teal-400 text-xs hover:text-teal-300 transition"
                              >
                                Open Chat →
                              </button>
                            ) : notif.actor_id && notif.actor_name ? (
                              <button
                                onClick={(e) => { e.stopPropagation(); handleNotificationClick(notif); }}
                                className="text-teal-400 text-xs hover:text-teal-300 transition"
                              >
                                Reply →
                              </button>
                            ) : null}
                          </div>
                        </div>
                        {!notif.is_read && (
                          <div className="w-2 h-2 bg-teal-500 rounded-full mt-1 flex-shrink-0"></div>
                        )}
                        <button
                          onClick={(e) => deleteNotification(e, notif.id)}
                          className="text-gray-600 hover:text-red-400 transition flex-shrink-0 ml-1"
                          title="Delete notification"
                        >
                          ✕
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Right Column - Stats */}
          <div className="space-y-6">
            {/* Quick Stats Card */}
            <div className="bg-surface rounded-lg p-6 border border-gray-700">
              <h2 className="text-xl font-bold text-white mb-4">Activity Summary</h2>
              <div className="space-y-3">
                <div className="flex items-center justify-between p-3 bg-dark rounded-lg">
                  <span className="text-gray-400">Unread Notifications</span>
                  <span className="text-white font-bold">{unreadNotifications}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Chat Modal — opens when a conversation is clicked */}
      {openChat && openChat.id && (
        <ChatModal
          profile={openChat}
          onClose={() => { setOpenChat(null); fetchProfileData(); }}
        />
      )}

      {/* Community Chat Room — opens when a NEW_COMMUNITY_MESSAGE notification is clicked */}
      {openCommunity && (
        <CommunityChatRoom
          community={openCommunity}
          onClose={() => setOpenCommunity(null)}
        />
      )}
    </div>
  );
};

export default Profile;
