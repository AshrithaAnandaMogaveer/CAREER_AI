/**
 * ReasoningBox — shared "Why this result?" explainability section.
 * Drop it below any result block. Pass reasoning as string[].
 */
const ReasoningBox = ({ reasoning }) => {
  if (!reasoning || reasoning.length === 0) return null;

  return (
    <div className="border-t border-gray-700/50 pt-3 mt-1">
      <p className="text-gray-500 text-xs font-medium mb-1.5">Why this result?</p>
      <ul className="space-y-1">
        {reasoning.map((point, i) => (
          <li key={i} className="flex items-start gap-2 text-xs text-gray-400 leading-relaxed">
            <span className="mt-0.5 w-1 h-1 rounded-full bg-gray-600 flex-shrink-0" />
            {point}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ReasoningBox;
