// pages/HomePage.jsx
import React from 'react';
import Header from '../layout/Header';
import Footer from '../layout/Footer';
import ProfileSection from '../sections/ProfileSection';
import StoriesBar from '../sections/StoriesBar';
import NewFriends from '../sections/NewFriends';
import RightSidebar from '../sections/RightSidebar';
import NewPost from '../sections/NewPost';
import PostList from '../sections/PostList';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-[#eeede8] text-[#1a1a1a] font-sans">
      <Header />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left column */}
          <div className="hidden lg:block lg:col-span-3 space-y-6">
            <ProfileSection />
            <NewFriends />
          </div>

          {/* Central column */}
          <div className="lg:col-span-6 space-y-8">
            <StoriesBar />
            <NewPost />
            <PostList />
          </div>

          {/* Right column */}
          <div className="hidden lg:block lg:col-span-3">
            <RightSidebar />
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}