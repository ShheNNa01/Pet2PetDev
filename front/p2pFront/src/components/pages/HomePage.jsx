import React, { useState, useCallback } from 'react';
import Header from '../layout/Header';
import Footer from '../layout/Footer';
import ProfileSection from '../sections/ProfileSection';
import StoriesBar from '../sections/StoriesBar';
import NewFriends from '../sections/NewFriends';
import RightSidebar from '../sections/RightSidebar';
import NewPost from '../sections/NewPost';
import PostList from '../sections/PostList';
import { usePet } from '../context/PetContext';

export default function HomePage() {
  const { currentPet } = usePet();
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleRefresh = useCallback(() => {
    console.log("Triggering refresh in HomePage"); // Debug
    setRefreshTrigger(prev => prev + 1);
}, []);


  return (
    <div className="min-h-screen bg-[#eeede8] text-[#1a1a1a] font-sans">
      <Header />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <div className="hidden lg:block lg:col-span-3 space-y-6">
            <ProfileSection />
            <NewFriends />
          </div>
          <div className="lg:col-span-6 space-y-8">
            {/* <StoriesBar /> */}
            {currentPet ? (
              <NewPost
                activePetId={currentPet.id}
                onPostCreated={handleRefresh}
                petAvatar={currentPet.image_url}
                petName={currentPet.name}
              />
            ) : (
              <div className="bg-white p-4 rounded-lg shadow-sm text-center">
                <p className="text-gray-500">
                  Necesitas registrar una mascota para poder publicar
                </p>
              </div>
            )}
            <PostList 
              refreshTrigger={refreshTrigger}
              onPostDeleted={handleRefresh}
            />
          </div>
          <div className="hidden lg:block lg:col-span-3">
            <RightSidebar />
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}