
import React from 'react';
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Bell, Menu, Search } from 'lucide-react';
import { Input } from "@/components/ui/input";
import { ThemeToggle } from './ThemeToggle';

interface DashboardHeaderProps {
  onMenuClick: () => void;
}

export const DashboardHeader = ({ onMenuClick }: DashboardHeaderProps) => {
  return (
    <header className="border-b border-border h-16 flex items-center px-4 md:px-6 sticky top-0 z-30 bg-background">
      <Button 
        variant="ghost" 
        size="icon"
        className="lg:hidden mr-2"
        onClick={onMenuClick}
      >
        <Menu className="h-6 w-6" />
      </Button>
      
      <div className="w-full flex items-center justify-between">
        <div className="relative w-full max-w-md hidden md:flex">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            type="search"
            placeholder="Buscar..."
            className="pl-8 bg-background w-full"
          />
        </div>
        
        <div className="flex items-center ml-auto gap-4">
          <ThemeToggle />
          
          <Button
            variant="ghost"
            size="icon"
            className="relative rounded-full"
          >
            <Bell className="h-5 w-5" />
            <span className="absolute top-0 right-0 h-2 w-2 rounded-full bg-red-500" />
          </Button>

          <Avatar className="h-8 w-8">
            <AvatarImage src="https://api.dicebear.com/7.x/adventurer/svg?seed=Felix" alt="Avatar" />
            <AvatarFallback>BM</AvatarFallback>
          </Avatar>
        </div>
      </div>
    </header>
  );
};
