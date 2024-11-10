// components/sections/ProfileSection.jsx
import { Card, CardContent, CardHeader } from "../ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import { Button } from "../ui/button";

export default function ProfileSection() {
    const userProfile = {
        username: "Firulais",
        avatar: "/placeholder.svg?height=96&width=96",
        description: "Amante de los juguetes y las siestas al sol",
    };

    return (
        <Card className="bg-white shadow-sm rounded-lg overflow-hidden">
        <CardContent className="pt-6">
            <div className="flex flex-col items-center space-y-4">
            <Avatar className="h-24 w-24 ring-2 ring-[#509ca2]/20">
                <AvatarImage src={userProfile.avatar} alt={userProfile.username} />
                <AvatarFallback>{userProfile.username[0]}</AvatarFallback>
            </Avatar>
            <div className="text-center">
                <h3 className="text-xl font-semibold">{userProfile.username}</h3>
                <p className="text-sm text-gray-500 mt-1">{userProfile.description}</p>
            </div>
            <Button className="w-full bg-[#509ca2] hover:bg-[#509ca2]/90">
                Editar perfil
            </Button>
            </div>
        </CardContent>
        </Card>
    );
}