import React, { useState } from 'react';
import CommunityGroups from '../components/community/CommunityGroups';
import Feedback from '../components/community/Feedback';

const Community = () => {
  const [activeTab, setActiveTab] = useState('groups');

  const tabs = [
    { id: 'groups', label: 'Community Groups', icon: '👥' },
    { id: 'feedback', label: 'Feedback', icon: '💬' },
  ];

  const renderContent = () => {
    switch (activeTab) {
      case 'groups':
        return <CommunityGroups />;
      case 'feedback':
        return <Feedback />;
      default:
        return <CommunityGroups />;
    }
  };

  return (
    <div className="min-h-screen bg-dark text-white pt-24 pb-8">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-teal mb-2">Community</h1>
          <p className="text-gray-400">Connect, share, and grow with fellow professionals</p>
        </div>

        {/* Tab Navigation */}
        <div className="bg-surface rounded-lg p-2 mb-6 flex gap-2 overflow-x-auto">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-6 py-3 rounded-lg transition whitespace-nowrap ${
                activeTab === tab.id
                  ? 'bg-teal-500 text-white'
                  : 'text-gray-400 hover:text-white hover:bg-dark'
              }`}
            >
              <span>{tab.icon}</span>
              <span className="font-medium">{tab.label}</span>
            </button>
          ))}
        </div>

        {/* Content Area */}
        <div className="bg-surface rounded-lg p-6">
          {renderContent()}
        </div>
      </div>
    </div>
  );
};

export default Community;
