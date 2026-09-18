import React, { useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';

const ResetPassword = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get('token') || '';

  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (password.length < 6) { setError('Password must be at least 6 characters'); return; }
    if (password !== confirm) { setError('Passwords do not match'); return; }
    if (!token) { setError('Invalid reset link'); return; }

    setLoading(true);
    try {
      const res = await fetch('http://localhost:5000/api/reset-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token, new_password: password })
      });
      const data = await res.json();
      if (data.success) {
        setSuccess(true);
        setTimeout(() => navigate('/'), 3000);
      } else {
        setError(data.message || 'Reset failed');
      }
    } catch {
      setError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-primary flex items-center justify-center p-4">
      <div className="glass rounded-2xl w-full max-w-md p-8">
        <h2 className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent mb-2 text-center">
          Set New Password
        </h2>
        <p className="text-gray-400 text-sm text-center mb-6">Enter your new password below.</p>

        {success ? (
          <div className="text-center space-y-4">
            <div className="text-5xl">✅</div>
            <p className="text-white font-semibold">Password reset successfully!</p>
            <p className="text-gray-400 text-sm">Redirecting to home in 3 seconds...</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-gray-400 text-sm mb-1">New Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-4 py-2 bg-white border border-gray-600 rounded-lg text-gray-900 focus:border-purple-500 focus:outline-none"
                required
              />
            </div>
            <div>
              <label className="block text-gray-400 text-sm mb-1">Confirm Password</label>
              <input
                type="password"
                value={confirm}
                onChange={(e) => setConfirm(e.target.value)}
                placeholder="••••••••"
                className="w-full px-4 py-2 bg-white border border-gray-600 rounded-lg text-gray-900 focus:border-purple-500 focus:outline-none"
                required
              />
            </div>

            {error && (
              <p className="text-red-400 text-sm p-3 bg-red-500/10 border border-red-500/30 rounded-lg">{error}</p>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-semibold hover:opacity-90 transition disabled:opacity-50"
            >
              {loading ? 'Resetting...' : 'Reset Password'}
            </button>
          </form>
        )}
      </div>
    </div>
  );
};

export default ResetPassword;
