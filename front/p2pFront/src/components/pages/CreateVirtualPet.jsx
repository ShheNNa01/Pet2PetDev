'use client'

import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronLeft, ChevronRight, ArrowLeft } from 'lucide-react'
import { Button } from "../ui/button"
import { Input } from "../ui/input"
import  Label  from "../ui/label"

const pets = [
  { id: 1, name: 'Dog', image: '/placeholder.svg?height=400&width=400' },
  { id: 2, name: 'Cat', image: '/placeholder.svg?height=400&width=400' },
  { id: 3, name: 'Rabbit', image: '/placeholder.svg?height=400&width=400' },
  { id: 4, name: 'Hamster', image: '/placeholder.svg?height=400&width=400' },
  { id: 5, name: 'Bird', image: '/placeholder.svg?height=400&width=400' },
]

export default function CreateVirtualPet() {
  const [currentPet, setCurrentPet] = useState(2)
  const [showForm, setShowForm] = useState(false)
  const [petName, setPetName] = useState('')

  const nextPet = () => {
    setCurrentPet((prev) => (prev + 1) % pets.length)
  }

  const prevPet = () => {
    setCurrentPet((prev) => (prev - 1 + pets.length) % pets.length)
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-r from-blue-100 to-purple-100 overflow-hidden">
      <div className="w-full max-w-6xl p-8">
        <AnimatePresence mode="wait">
          {!showForm ? (
            <motion.div
              key="carousel"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0, x: -300 }}
              className="flex flex-col items-center"
            >
              <h1 className="text-4xl font-bold mb-12 text-gray-800">Selecciona tu mascota virtual</h1>
              <div className="relative w-full h-96 mb-8">
                {pets.map((pet, index) => {
                  const offset = ((index - currentPet + pets.length) % pets.length) - Math.floor(pets.length / 2)
                  return (
                    <motion.div
                      key={pet.id}
                      className="absolute top-0 left-0 w-full h-full flex justify-center items-center"
                      initial={{ opacity: 0, x: offset * 100 }}
                      animate={{
                        opacity: offset === 0 ? 1 : 0.5,
                        x: offset * 300,
                        scale: offset === 0 ? 1 : 0.8,
                        zIndex: offset === 0 ? 1 : 0,
                      }}
                      transition={{ duration: 0.5 }}
                    >
                      <img
                        src={pet.image}
                        alt={pet.name}
                        className="w-64 h-64 object-cover rounded-full shadow-xl"
                      />
                    </motion.div>
                  )
                })}
              </div>
              <div className="flex justify-between w-full mb-8">
                <Button onClick={prevPet} variant="outline" size="icon" className="rounded-full p-3">
                  <ChevronLeft className="h-6 w-6" />
                </Button>
                <Button onClick={nextPet} variant="outline" size="icon" className="rounded-full p-3">
                  <ChevronRight className="h-6 w-6" />
                </Button>
              </div>
              <Button onClick={() => setShowForm(true)} className="px-8 py-3 text-lg">
                Select {pets[currentPet].name}
              </Button>
            </motion.div>
          ) : (
            <motion.div
              key="form"
              initial={{ opacity: 0, x: 300 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 300 }}
              className="flex flex-col items-center bg-white p-8 rounded-xl shadow-2xl"
            >
              <Button
                onClick={() => setShowForm(false)}
                variant="ghost"
                className="self-start mb-4"
              >
                <ArrowLeft className="mr-2 h-4 w-4" /> Back to selection
              </Button>
              <h2 className="text-3xl font-bold mb-6 text-gray-800">Customize Your {pets[currentPet].name}</h2>
              <img
                src={pets[currentPet].image}
                alt={pets[currentPet].name}
                className="w-40 h-40 object-cover rounded-full mb-6 shadow-lg"
              />
              <div className="w-full max-w-md">
                <Label htmlFor="petName" className="text-lg mb-2">Pet Name</Label>
                <Input
                  id="petName"
                  type="text"
                  value={petName}
                  onChange={(e) => setPetName(e.target.value)}
                  placeholder="Enter your pet's name"
                  className="mb-6 text-lg p-3"
                />
                <Button 
                  onClick={() => alert(`You've selected a ${pets[currentPet].name} named ${petName}!`)}
                  className="w-full py-3 text-lg"
                >
                  Confirm Selection
                </Button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}