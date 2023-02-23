import React from 'react';
import ReactDOM from 'react-dom/client';
import HomePage from './js/views/HomePage';
import DemoPage from './js/views/DemoPage';
import PageWrapper from './js/views/PageWrapper';
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import './scss/index.scss';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<PageWrapper />}>
          <Route index element={<HomePage />} />
          <Route path="demo" element={<DemoPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
