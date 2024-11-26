import React from 'react';
import { 
    Facebook, 
    Twitter, 
    Linkedin, 
    Send, 
    MessageSquare, // Cambiado de WhatsApp a MessageSquare
    Link as LinkIcon
} from 'lucide-react';

const ShareButtons = ({ onShare, className = "" }) => {
    const socialButtons = [
        { icon: Facebook, label: 'Facebook', platform: 'facebook' },
        { icon: Twitter, label: 'Twitter/X', platform: 'twitter' },
        { icon: MessageSquare, label: 'WhatsApp', platform: 'whatsapp' }, // Usando MessageSquare para WhatsApp
        { icon: Send, label: 'Telegram', platform: 'telegram' },
        { icon: Linkedin, label: 'LinkedIn', platform: 'linkedin' },
        { icon: LinkIcon, label: 'Copiar link', platform: 'copy' }
    ];

    return (
        <div className={`grid grid-cols-3 gap-4 p-4 ${className}`}>
            {socialButtons.map(({ icon: Icon, label, platform }) => (
                <button
                    key={platform}
                    onClick={() => onShare(platform)}
                    className="flex flex-col items-center justify-center p-3 rounded-lg
                             hover:bg-gray-100 transition-colors"
                >
                    <Icon className="h-6 w-6 mb-2 text-gray-600" />
                    <span className="text-sm text-gray-600">{label}</span>
                </button>
            ))}
        </div>
    );
};

export default ShareButtons;