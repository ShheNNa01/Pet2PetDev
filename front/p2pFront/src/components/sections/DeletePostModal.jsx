import React from 'react';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogDescription,
    DialogFooter,
} from "../ui/dialog";
import { Button } from "../ui/button";
import { toast } from '../ui/use-toast';

const DeletePostModal = ({ isOpen, onClose, onConfirm, isDeleting }) => {
    const handleConfirm = async () => {
        try {
            await onConfirm();
            toast({
                title: "Publicación eliminada",
                description: "La publicación se ha eliminado correctamente",
                variant: "success",
            });
            onClose();
        } catch (error) {
            console.error('Error detallado en DeletePostModal:', error);
            
            // Mensaje personalizado basado en el tipo de error
            const errorMessage = error.response?.data?.message || error.message || "Error desconocido";
            
            toast({
                title: "Error al eliminar",
                description: errorMessage,
                variant: "destructive",
            });
        }
    };

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>¿Eliminar publicación?</DialogTitle>
                    <DialogDescription>
                        Esta acción no se puede deshacer. La publicación será eliminada permanentemente.
                    </DialogDescription>
                </DialogHeader>
                <DialogFooter className="gap-2 sm:gap-0">
                    <Button
                        variant="outline"
                        onClick={onClose}
                        disabled={isDeleting}
                    >
                        Cancelar
                    </Button>
                    <Button
                        variant="destructive"
                        onClick={handleConfirm}
                        disabled={isDeleting}
                        className="bg-red-500 hover:bg-red-600"
                    >
                        {isDeleting ? 'Eliminando...' : 'Eliminar'}
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
};

export default DeletePostModal;