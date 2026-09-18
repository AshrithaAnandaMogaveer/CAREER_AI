import React from 'react';
import { useNavigate } from 'react-router-dom';
import CareerSnapshot from '../components/explore/CareerSnapshot';
import FutureSimulation from '../components/explore/FutureSimulation';
import CareerComparator from '../components/explore/CareerComparator';
import SkillROI from '../components/explore/SkillROI';
import ConfusionSolver from '../components/explore/ConfusionSolver';
import RealityCheck from '../components/explore/RealityCheck';
import ExploreRoutinePrompt from '../components/explore/ExploreRoutinePrompt';

const Explore = () => {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen bg-[#0f0f1a] pt-24 pb-16 px-4">
      <div className="max-w-6xl mx-auto">

        {/* Header */}
        <div className="mb-8">
          <p className="text-[#00cccc] text-sm font-medium tracking-widest uppercase mb-3">
            Career Intelligence
          </p>
          <h1 className="text-3xl md:text-4xl font-bold text-white mb-3">
            Explore Career Intelligence
          </h1>
          <p className="text-gray-400 text-base max-w-xl">
            Make informed career decisions using data-driven insights and AI-powered tools.
          </p>
          <div className="mt-5 h-px bg-gradient-to-r from-[#00cccc]/30 via-gray-700 to-transparent" />
        </div>

        {/* Personalized Career Snapshot */}
        <CareerSnapshot />

        {/* Smart Routine Prompt — shown when missing skills exist */}
        <ExploreRoutinePrompt navigate={navigate} />

        {/* Feature Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <FutureSimulation />
          <CareerComparator />
          <SkillROI />
          <ConfusionSolver />
          <div className="md:col-span-2 md:max-w-[calc(50%-12px)]">
            <RealityCheck />
          </div>
        </div>

      </div>
    </div>
  );
};

export default Explore;
