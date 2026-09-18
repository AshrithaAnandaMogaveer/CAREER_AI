import React, { useState, useEffect } from 'react';
import { getStoredToken } from '../../services/authService';

const Feed = () => {
  const token = getStoredToken();
  const [feed, setFeed] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // 'all', 'blog', 'feedback'
  const [showScores, setShowScores] = useState(false);

  useEffect(() => {
    fetchFeed();
  }, [filter]);

  const fetchFeed = async () => {
    try {
      setLoading(true);
      const typeParam = filter !== 'all' ? `?type=${filter}` : '';
      const scoresParam = showScores ? (typeParam ? '&' : '?') + 'include_scores=true' : '';
      
      const response = await fetch(
        `http://localhost:5000/api/community/feed${typeParam}${scoresParam}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      const data = await response.json();
      if (data.success) {
        setFeed(data.feed || []);
        setStats(data.stats);
      }
    } catch (error) {
      console.error('Error fetching feed:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatTimeAgo = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.floor((now - date) / 1000);
    
    if (seconds < 60) return 'just now';
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
    if (seconds < 604800) return `${Math.floor(seconds / 86400)}d ago`;
    return `${Math.floor(seconds / 604800)}w ago`;
  };

  const getPostTypeColor = (type) => {
    return type === 'BLOG' ? 'text-purple-400' : 'text-teal-400';
  };

  const getPostTypeIcon = (type) => {
    return type === 'BLOG' ? '📝' : '💬';
  };

  if (loading) {
    return <div className="text-center py-8 text-gray-400">Loading feed...</div>;
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-white mb-2">Your Feed</h2>
        {stats && stats.personalization_enabled && (
          <p className="text-sm text-gray-400">
            ✨ Personalized based on your interests
          </p>
        )}
      </div>

      {/* Filters */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex gap-2">
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded-lg transition ${
              filter === 'all'
                ? 'bg-teal-500 text-white'
                : 'bg-dark text-gray-400 hover:text-gray-300'
            }`}
          >
            All Posts
          </button>
          <button
            onClick={() => setFilter('blog')}
            className={`px-4 py-2 rounded-lg transition ${
              filter === 'blog'
                ? 'bg-purple-500 text-white'
                : 'bg-dark text-gray-400 hover:text-gray-300'
            }`}
          >
            📝 Blogs
          </button>
          <button
            onClick={() => setFilter('feedback')}
            className={`px-4 py-2 rounded-lg transition ${
              filter === 'feedback'
                ? 'bg-teal-500 text-white'
                : 'bg-dark text-gray-400 hover:text-gray-300'
            }`}
          >
            💬 Feedback
          </button>
        </div>

        {/* Debug toggle */}
        <button
          onClick={() => {
            setShowScores(!showScores);
            fetchFeed();
          }}
          className="text-xs text-gray-500 hover:text-gray-400"
        >
          {showScores ? 'Hide' : 'Show'} Scores
        </button>
      </div>

      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-4 gap-4 mb-6">
          <div className="bg-dark p-4 rounded-lg border border-gray-700">
            <div className="text-2xl font-bold text-white">{stats.total_posts}</div>
            <div className="text-sm text-gray-400">Total Posts</div>
          </div>
          <div className="bg-dark p-4 rounded-lg border border-gray-700">
            <div className="text-2xl font-bold text-purple-400">{stats.blog_posts}</div>
            <div className="text-sm text-gray-400">Blogs</div>
          </div>
          <div className="bg-dark p-4 rounded-lg border border-gray-700">
            <div className="text-2xl font-bold text-teal-400">{stats.feedback_posts}</div>
            <div className="text-sm text-gray-400">Feedback</div>
          </div>
          <div className="bg-dark p-4 rounded-lg border border-gray-700">
            <div className="text-2xl font-bold text-green-400">{stats.recent_posts_24h}</div>
            <div className="text-sm text-gray-400">Last 24h</div>
          </div>
        </div>
      )}

      {/* Feed */}
      {feed.length === 0 ? (
        <div className="text-center py-12 bg-dark rounded-lg border border-gray-700">
          <p className="text-gray-400 mb-2">No posts in your feed yet</p>
          <p className="text-sm text-gray-500">
            Check back later or create some content!
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {feed.map((post) => (
            <div
              key={post.id}
              className="bg-dark p-6 rounded-lg border border-gray-700 hover:border-teal-500 transition"
            >
              {/* Header */}
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{getPostTypeIcon(post.post_type)}</span>
                  <div>
                    <h3 className="text-lg font-semibold text-white">
                      {post.title || 'Untitled'}
                    </h3>
                    <div className="flex items-center gap-2 text-sm text-gray-400">
                      <span>{post.author_name || 'Anonymous'}</span>
                      <span>•</span>
                      <span>{formatTimeAgo(post.created_at)}</span>
                      <span>•</span>
                      <span className={getPostTypeColor(post.post_type)}>
                        {post.post_type}
                      </span>
                    </div>
                  </div>
                </div>
                
                {/* Rank Score Badge */}
                <div className="flex flex-col items-end gap-1">
                  <span className="px-3 py-1 bg-teal-500/20 text-teal-400 text-sm rounded-full">
                    ⭐ {post.rank_score}%
                  </span>
                  {post.read_time && (
                    <span className="text-xs text-gray-500">{post.read_time} min read</span>
                  )}
                </div>
              </div>

              {/* Content */}
              <p className="text-gray-300 mb-4 line-clamp-3">{post.content}</p>

              {/* Tags */}
              {post.tags && post.tags.length > 0 && (
                <div className="flex flex-wrap gap-2 mb-4">
                  {post.tags.slice(0, 5).map((tag, idx) => (
                    <span
                      key={idx}
                      className="px-2 py-1 bg-gray-700 text-gray-300 text-xs rounded"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              )}

              {/* Score Breakdown (Debug) */}
              {showScores && post.score_breakdown && (
                <div className="mb-4 p-3 bg-gray-800 rounded text-xs">
                  <div className="grid grid-cols-3 gap-2 text-gray-400">
                    <div>
                      <span className="text-gray-500">Recency:</span> {post.score_breakdown.recency_score}%
                      <span className="text-gray-600"> ({post.score_breakdown.hours_since_post}h)</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Engagement:</span> {post.score_breakdown.engagement_score}%
                    </div>
                    <div>
                      <span className="text-gray-500">Relevance:</span> {post.score_breakdown.relevance_score}%
                    </div>
                  </div>
                </div>
              )}

              {/* Engagement */}
              <div className="flex items-center gap-6 text-sm text-gray-400">
                <button className="flex items-center gap-2 hover:text-teal-400 transition">
                  <span>👍</span>
                  <span>{post.likes_count || 0}</span>
                </button>
                <button className="flex items-center gap-2 hover:text-teal-400 transition">
                  <span>💬</span>
                  <span>{post.comments_count || 0}</span>
                </button>
                <button className="flex items-center gap-2 hover:text-teal-400 transition">
                  <span>👁️</span>
                  <span>{post.views_count || 0}</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Feed;
