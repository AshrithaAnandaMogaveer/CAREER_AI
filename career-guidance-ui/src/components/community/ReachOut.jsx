import React, { useState, useEffect } from 'react';
import { getStoredToken } from '../../services/authService';
import ChatModal from './ChatModal';

const ReachOut = () => {
  const token = getStoredToken();
  const [profiles, setProfiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedProfile, setSelectedProfile] = useState(null);
  const [showChatModal, setShowChatModal] = useState(false);

  useEffect(() => {
    fetchRelatedProfiles();
  }, []);

  const fetchRelatedProfiles = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:5000/api/community/reach-out', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      if (data.success) {
        setProfiles(data.profiles || []);
      }
    } catch (error) {
      console.error('Error fetching profiles:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleMessageClick = (profile) => {
    setSelectedProfile(profile);
    setShowChatModal(true);
  };

  const getSimilarityColor = (percentage) => {
    if (percentage >= 80) return 'text-green-400';
    if (percentage >= 60) return 'text-teal-400';
    if (percentage >= 40) return 'text-yellow-400';
    return 'text-gray-400';
  };

  if (loading) {
    return <div className="text-center py-8 text-gray-400">Finding related profiles...</div>;
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-white">Reach Out</h2>
        <p className="text-gray-400 text-sm mt-1">
          Connect with professionals who share similar interests and skills
        </p>
      </div>

      {/* Profiles Grid */}
      {profiles.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-400">No related profiles found at the moment</p>
          <p className="text-gray-500 text-sm mt-2">
            Complete your profile to get better matches
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {profiles.map((profile) => (
            <div
              key={profile.id}
              className="bg-dark p-5 rounded-lg border border-gray-700 hover:border-teal-500 transition"
            >
              {/* Profile Header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-full overflow-hidden flex items-center justify-center bg-gradient-to-br from-teal-500 to-purple-500 text-white font-bold text-lg">
                    {profile.profile_picture ? (
                      <img
                        src={`http://localhost:5000${profile.profile_picture}`}
                        alt={profile.name}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      profile.name?.charAt(0).toUpperCase() || 'U'
                    )}
                  </div>
                  <div>
                    <h3 className="text-white font-semibold">{profile.name}</h3>
                    <p className="text-gray-400 text-sm">{profile.domain || 'Professional'}</p>
                  </div>
                </div>
              </div>

              {/* Similarity Score */}
              <div className="mb-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-gray-400 text-sm">Similarity</span>
                  <span className={`font-bold ${getSimilarityColor(profile.similarity_percentage)}`}>
                    {profile.similarity_percentage}%
                  </span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-2">
                  <div
                    className="bg-gradient-to-r from-teal-500 to-purple-500 h-2 rounded-full transition-all"
                    style={{ width: `${profile.similarity_percentage}%` }}
                  />
                </div>
              </div>

              {/* Common Skills */}
              {profile.common_skills && profile.common_skills.length > 0 && (
                <div className="mb-4">
                  <p className="text-gray-400 text-xs mb-2">Common Skills:</p>
                  <div className="flex flex-wrap gap-1">
                    {profile.common_skills.slice(0, 3).map((skill, index) => (
                      <span
                        key={index}
                        className="px-2 py-1 bg-teal-500 bg-opacity-20 text-teal-400 text-xs rounded"
                      >
                        {skill}
                      </span>
                    ))}
                    {profile.common_skills.length > 3 && (
                      <span className="px-2 py-1 text-gray-400 text-xs">
                        +{profile.common_skills.length - 3} more
                      </span>
                    )}
                  </div>
                </div>
              )}

              {/* Stats */}
              <div className="flex items-center gap-4 mb-4 text-sm text-gray-400">
                <span>📊 {profile.experience_years || 0}+ years</span>
                <span>🎯 {profile.projects_count || 0} projects</span>
              </div>

              {/* Message Button */}
              <button
                onClick={() => handleMessageClick(profile)}
                className="w-full py-2 bg-teal-500 text-white rounded-lg hover:bg-teal-600 transition flex items-center justify-center gap-2"
              >
                <span>💬</span>
                <span>Message</span>
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Chat Modal */}
      {showChatModal && selectedProfile && (
        <ChatModal
          profile={selectedProfile}
          onClose={() => {
            setShowChatModal(false);
            setSelectedProfile(null);
          }}
        />
      )}
    </div>
  );
};

export default ReachOut;
