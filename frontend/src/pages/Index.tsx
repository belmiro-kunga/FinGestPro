
import React, { useState } from 'react';
import { Sidebar } from '../components/Sidebar';
import { DashboardHeader as PageHeader } from '../components/DashboardHeader';
import { MobileNav } from '../components/MobileNav';
import DashboardHeader from '../components/dashboard/DashboardHeader';
import MetricsGrid from '../components/dashboard/MetricsGrid';
import ChartsGrid from '../components/dashboard/ChartsGrid';
import DataTabs from '../components/dashboard/DataTabs';
import BottomSection from '../components/dashboard/BottomSection';

const Dashboard = () => {
  const [mobileNavOpen, setMobileNavOpen] = useState(false);

  return (
    <div className="flex min-h-screen bg-background">
      <div className="hidden lg:block">
        <Sidebar />
      </div>

      <MobileNav isOpen={mobileNavOpen} onClose={() => setMobileNavOpen(false)} />

      <div className="flex-1 flex flex-col max-w-full">
        <PageHeader onMenuClick={() => setMobileNavOpen(true)} />

        <main className="flex-1 p-4 md:p-6 overflow-auto">
          <div className="mx-auto max-w-7xl space-y-8">
            <DashboardHeader />
            <MetricsGrid />
            <ChartsGrid />
            <DataTabs />
            <BottomSection />
          </div>
        </main>
      </div>
    </div>
  );
};

export default Dashboard;
