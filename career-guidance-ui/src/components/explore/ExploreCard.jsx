import React from 'react';

const ExploreCard = ({ icon, title, description, children }) => {
  return (
    <div className="bg-[#161625] border border-gray-700 rounded-xl p-6 flex flex-col gap-4 hover:border-[#00cccc]/40 transition-colors duration-200">
      <div className="flex items-center gap-3">
        <span className="text-2xl">{icon}</span>
        <div>
          <h3 className="text-xl font-semibold text-white">{title}</h3>
          <p className="text-gray-400 text-sm mt-0.5">{description}</p>
        </div>
      </div>
      <div className="border-t border-gray-700/60 pt-4">
        {children}
      </div>
    </div>
  );
};

export default ExploreCard;
