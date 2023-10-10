import React from 'react'
import ReactDOM from 'react-dom/client'
import {createBrowserRouter, RouterProvider} from 'react-router-dom';
import App from './App.jsx'
import './index.css'
import LoginPage from './components/LoginPage.jsx';
import ErrorPage from './components/ErrorPage.jsx';
import ShopPage from './components/ShopPage.jsx'
import { canonicalProductsLoader, sessionLoader } from './loaders.js';
import CareersPage from './components/CareersPage.jsx';
import ApplyPage from './components/ApplyPage.jsx';
import CareersOutlet from './components/CareersOutlet.jsx';

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    loader: sessionLoader,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "login",
        element: <LoginPage />,
      },
      {
        path: "shop",
        element: <ShopPage />,
        loader: canonicalProductsLoader,
      },
      {
        path: "careers",
        element: <CareersOutlet />,
        children: [
          {
            path: "open", 
            element: <CareersPage />
          },
          {
            path: "apply", 
            element: <ApplyPage />
          },
        ]
      }
    ]
  }])

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
