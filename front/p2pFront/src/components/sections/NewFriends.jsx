// components/sections/NewFriends.jsx
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { UserPlus } from 'lucide-react';

export default function NewFriends() {
    const newFriends = ["Max", "Luna", "Rocky", "Bella"];

    return (
        <Card className="bg-white shadow-sm rounded-lg overflow-hidden">
        <CardHeader>
            <h2 className="text-[#d55b49] text-xl font-semibold">Nuevos Amigos</h2>
        </CardHeader>
        <CardContent>
            <ul className="space-y-4">
            {newFriends.map((friend) => (
                <li key={friend} className="flex items-center justify-between group">
                <div className="flex items-center gap-3">
                    <Avatar className="h-8 w-8">
                    <AvatarImage src={`/placeholder.svg?height=32&width=32&text=${friend[0]}`} />
                    <AvatarFallback className="bg-gray-100">
                        {friend[0]}
                    </AvatarFallback>
                    </Avatar>
                    <span className="text-sm">{friend}</span>
                </div>
                <Button
                    variant="outline"
                    size="sm"
                    className="h-7 px-3 border-[#509ca2] text-[#509ca2] hover:bg-[#509ca2]/5 text-xs font-normal"
                >
                    <UserPlus className="h-3.5 w-3.5 mr-1.5" />
                    Seguir
                </Button>
                </li>
            ))}
            </ul>
        </CardContent>
        </Card>
    );
}