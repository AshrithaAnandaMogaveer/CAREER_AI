import { useEffect } from 'react';

/**
 * Toast notification — auto-dismisses after 3s.
 * Props: message (string), type ('error'|'success'), onClose (fn), onRetry (fn, optional)
 */
const Toast = ({ message, type = 'error', onClose, onRetry }) => {
  useEffect(() => {
    const timer = setTimeout(onClose, 3000);
    return () => clearTimeout(timer);
  }, [onClose]);

  const colors =
    type === 'success'
      ? 'bg-emerald-900/90 border-emerald-500/40 text-emerald-300'
      : 'bg-red-900/90 border-red-500/40 text-red-300';

  return (
    <div
      className={`fixed bottom-5 right-5 z-50 flex items-center gap-3 px-4 py-3 rounded-lg border text-sm shadow-lg ${colors}`}
      role="alert"
    >
      <span className="flex-1">{message}</span>
      {onRetry && (
        <button
          onClick={() => { onClose(); onRetry(); }}
          className="underline text-xs opacity-80 hover:opacity-100 whitespace-nowrap"
        >
          Retry
        </button>
      )}
      <button onClick={onClose} className="opacity-60 hover:opacity-100 text-base leading-none">✕</button>
    </div>
  );
};

export default Toast;
