import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { DashboardPage } from './pages/DashboardPage';
import { SourcesPage } from './pages/SourcesPage';
import { SourceDetailPage } from './pages/SourceDetailPage';
import { RunsPage } from './pages/RunsPage';
import { RunDetailsPage } from './pages/RunDetailsPage';
import { HealingPage } from './pages/HealingPage';
import { InsightsPage } from './pages/InsightsPage';
import { AskPage } from './pages/AskPage';
import { SettingsPage } from './pages/SettingsPage';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<DashboardPage />} />
          <Route path="sources" element={<SourcesPage />} />
          <Route path="sources/:id" element={<SourceDetailPage />} />
          <Route path="runs" element={<RunsPage />} />
          <Route path="runs/:id" element={<RunDetailsPage />} />
          <Route path="healing" element={<HealingPage />} />
          <Route path="insights" element={<InsightsPage />} />
          <Route path="ask" element={<AskPage />} />
          <Route path="settings" element={<SettingsPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App;
