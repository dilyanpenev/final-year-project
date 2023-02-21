import React from 'react';
import ReactDOM from 'react-dom/client';
import HomePage from './js/views/HomePage';
import PageWrapper from './js/views/PageWrapper';
import './scss/index.scss';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <PageWrapper>
      <HomePage />
    </PageWrapper>
  </React.StrictMode>
);
