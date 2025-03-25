
import React from 'react';
import { Sidebar } from './Sidebar';
import { cn } from '@/lib/utils';

interface MobileNavProps {
  isOpen: boolean;
  onClose: () => void;
}

export function MobileNav({ isOpen, onClose }: MobileNavProps) {
  return (
    <div 
      className={cn(
        "fixed inset-0 z-50 lg:hidden",
        isOpen ? "block" : "hidden"
      )}
    >
      <div 
        className="absolute inset-0 bg-foreground/20 backdrop-blur-sm"
        onClick={onClose}
        aria-hidden="true"
      />
      <div className="absolute inset-y-0 left-0 max-w-xs w-full flex animate-slide-in">
        <Sidebar isMobile onCloseMobile={onClose} className="w-full" />
      </div>
    </div>
  );
}
