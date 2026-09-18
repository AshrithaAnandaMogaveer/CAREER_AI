"""
Test script for feed ranking engine
Creates sample posts and tests ranking algorithm
"""

import sys
import os
from datetime import datetime, timedelta

# Add backend to path
backend_path = os.path.dirname(os.path.abspath(__file__))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app_config import create_app
from community_models import db, Post, UserProfile, PostType
from user_model import User
from feed_ranking_engine import FeedRankingEngine


def create_sample_posts():
    """Create sample posts with varying recency and engagement"""
    app = create_app()
    
    with app.app_context():
        print("Creating sample posts...")
        
        # Get test user
        test_user = User.query.filter_by(email='test@example.com').first()
        if not test_user:
            print("Test user not found. Please sign up first.")
            return
        
        print(f"✓ Found test user: {test_user.name} (ID: {test_user.id})")
        
        # Sample posts with different characteristics
        posts_data = [
            {
                'title': 'Getting Started with Python Machine Learning',
                'content': 'A comprehensive guide to ML with Python, covering scikit-learn, pandas, and numpy.',
                'post_type': PostType.BLOG,
                'tags': ['Python', 'Machine Learning', 'Data Science', 'AI'],
                'hours_ago': 2,
                'likes': 25,
                'comments': 8
            },
            {
                'title': 'React Hooks Best Practices',
                'content': 'Learn the best practices for using React Hooks in your applications.',
                'post_type': PostType.BLOG,
                'tags': ['React', 'JavaScript', 'Web Development', 'Frontend'],
                'hours_ago': 5,
                'likes': 18,
                'comments': 5
            },
            {
                'title': 'Cloud Architecture Patterns',
                'content': 'Exploring modern cloud architecture patterns for scalable applications.',
                'post_type': PostType.BLOG,
                'tags': ['Cloud Computing', 'AWS', 'Architecture', 'DevOps'],
                'hours_ago': 12,
                'likes': 30,
                'comments': 12
            },
            {
                'title': 'Feature Request: Dark Mode',
                'content': 'Would love to see a dark mode option for better nighttime viewing.',
                'post_type': PostType.FEEDBACK,
                'tags': ['UI/UX', 'Feature Request'],
                'hours_ago': 1,
                'likes': 45,
                'comments': 15
            },
            {
                'title': 'Introduction to TypeScript',
                'content': 'Why TypeScript is becoming essential for modern JavaScript development.',
                'post_type': PostType.BLOG,
                'tags': ['TypeScript', 'JavaScript', 'Web Development'],
                'hours_ago': 24,
                'likes': 12,
                'comments': 3
            },
            {
                'title': 'Docker for Beginners',
                'content': 'A beginner-friendly guide to containerization with Docker.',
                'post_type': PostType.BLOG,
                'tags': ['Docker', 'DevOps', 'Containers'],
                'hours_ago': 48,
                'likes': 8,
                'comments': 2
            },
            {
                'title': 'Bug Report: Login Issue',
                'content': 'Experiencing issues with login on mobile devices.',
                'post_type': PostType.FEEDBACK,
                'tags': ['Bug', 'Mobile', 'Authentication'],
                'hours_ago': 3,
                'likes': 5,
                'comments': 2
            },
            {
                'title': 'Deep Learning with TensorFlow',
                'content': 'Building neural networks with TensorFlow 2.0 and Keras.',
                'post_type': PostType.BLOG,
                'tags': ['Deep Learning', 'TensorFlow', 'AI', 'Python'],
                'hours_ago': 8,
                'likes': 22,
                'comments': 7
            }
        ]
        
        created_count = 0
        for post_data in posts_data:
            # Check if post already exists
            existing = Post.query.filter_by(title=post_data['title']).first()
            if not existing:
                # Calculate created_at based on hours_ago
                created_at = datetime.utcnow() - timedelta(hours=post_data['hours_ago'])
                
                post = Post(
                    title=post_data.get('title'),
                    content=post_data['content'],
                    post_type=post_data['post_type'],
                    tags=post_data['tags'],
                    author_id=test_user.id,
                    created_at=created_at,
                    likes_count=post_data['likes'],
                    comments_count=post_data['comments'],
                    read_time=5
                )
                db.session.add(post)
                created_count += 1
        
        if created_count > 0:
            db.session.commit()
            print(f"✓ Created {created_count} sample posts")
        else:
            print("✓ Sample posts already exist")
        
        print("\n✅ Sample posts created successfully!")


def test_feed_ranking():
    """Test the feed ranking engine"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*60)
        print("TESTING FEED RANKING ENGINE")
        print("="*60)
        
        # Get test user
        test_user = User.query.filter_by(email='test@example.com').first()
        if not test_user:
            print("❌ Test user not found")
            return
        
        print(f"\nUser: {test_user.name}")
        
        # Get user profile
        profile = UserProfile.query.filter_by(user_id=test_user.id).first()
        if profile:
            print(f"Skills: {', '.join(profile.skills or [])}")
            print(f"Interests: {', '.join(profile.interests or [])}")
        else:
            print("No profile found")
        
        print("\n" + "-"*60)
        print("RANKED FEED (Top 10)")
        print("-"*60)
        
        # Get ranked feed with score breakdown
        feed = FeedRankingEngine.rank_feed(
            user_id=test_user.id,
            limit=10,
            include_scores=True
        )
        
        if not feed:
            print("No posts found")
            return
        
        for i, post in enumerate(feed, 1):
            print(f"\n{i}. {post['title']}")
            print(f"   Type: {post['post_type']}")
            print(f"   Rank Score: {post['rank_score']}%")
            
            if 'score_breakdown' in post:
                breakdown = post['score_breakdown']
                print(f"   └─ Recency: {breakdown['recency_score']}% ({breakdown['hours_since_post']}h ago)")
                print(f"   └─ Engagement: {breakdown['engagement_score']}% ({post['likes_count']} likes, {post['comments_count']} comments)")
                print(f"   └─ Relevance: {breakdown['relevance_score']}%")
            
            if post.get('tags'):
                print(f"   Tags: {', '.join(post['tags'][:3])}")
        
        print("\n" + "-"*60)
        print("TRENDING POSTS (Last 24 hours)")
        print("-"*60)
        
        # Get trending posts
        trending = FeedRankingEngine.get_trending_posts(limit=5)
        
        if trending:
            for i, post in enumerate(trending, 1):
                print(f"\n{i}. {post['title']}")
                print(f"   Trending Score: {post['trending_score']} (engagement/hour)")
                print(f"   Age: {post['hours_old']} hours")
                print(f"   Engagement: {post['likes_count']} likes, {post['comments_count']} comments")
        else:
            print("\nNo trending posts in the last 24 hours")
        
        print("\n" + "-"*60)
        print("FEED STATISTICS")
        print("-"*60)
        
        # Get feed stats
        stats = FeedRankingEngine.get_feed_stats(test_user.id)
        print(f"\nTotal Posts: {stats['total_posts']}")
        print(f"Blog Posts: {stats['blog_posts']}")
        print(f"Feedback Posts: {stats['feedback_posts']}")
        print(f"Recent Posts (24h): {stats['recent_posts_24h']}")
        print(f"Has Profile: {stats['has_profile']}")
        print(f"Personalization Enabled: {stats['personalization_enabled']}")
        
        print("\n" + "="*60)
        print("✅ TEST COMPLETE")
        print("="*60)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Test feed ranking engine')
    parser.add_argument('--create-posts', action='store_true', help='Create sample posts')
    parser.add_argument('--test', action='store_true', help='Test feed ranking')
    
    args = parser.parse_args()
    
    if args.create_posts:
        create_sample_posts()
    
    if args.test:
        test_feed_ranking()
    
    if not args.create_posts and not args.test:
        # Run both by default
        create_sample_posts()
        test_feed_ranking()
