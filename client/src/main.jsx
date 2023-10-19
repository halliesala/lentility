import React from 'react'
import ReactDOM from 'react-dom/client'
import {createBrowserRouter, RouterProvider} from 'react-router-dom';
import App from './App.jsx'
import './index.css'
import LoginPage from './components/LoginPage.jsx';
import ErrorPage from './components/ErrorPage.jsx';
import ShopPage from './components/ShopPage.jsx'
import { canonicalProductsLoader, sessionLoader, cartLoader, supplierAccountsLoader, ordersLoader, checkoutLoader, addressesLoader, usersLoader } from './loaders.js';
import CareersPage from './components/CareersPage.jsx';
import ApplyPage from './components/ApplyPage.jsx';
import CareersOutlet from './components/CareersOutlet.jsx';
import SignUpPage from './components/SignUpPage.jsx';
import CartPage from './components/CartPage.jsx';
import CheckoutPage from './components/CheckoutPage.jsx';
import Logout from './components/Logout.jsx';
import AccountOutlet from './components/AccountOutlet.jsx';
import ManageVendorsPage from './components/ManageVendorsPage.jsx';
import OrdersPage from './components/OrdersPage.jsx';
import AddressesPage from './components/AddressesPage.jsx';
import PaymentMethods from './components/PaymentMethods.jsx';
import DataPage from './components/DataPage.jsx';
import ManageUsers from './components/ManageUsers.jsx';

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
        path: "logout",
        element: <Logout />,
      },
      {
        path: "signup",
        element: <SignUpPage />,
      },
      {
        path: "shop",
        element: <ShopPage />,
        loader: canonicalProductsLoader,
      },
      {
        path: "cart",
        element: <CartPage />,
        loader: cartLoader,
      },
      {
        path: "checkout",
        element: <CheckoutPage />,
        loader: checkoutLoader,
      },
      {
        path: "account",
        element: <AccountOutlet />,
        children: [
          {
            path: "vendors",
            element: <ManageVendorsPage />,
            loader: supplierAccountsLoader,
          },
          {
            path: "users",
            element: <ManageUsers />,
            loader: usersLoader
          },
          {
            path: "orders",
            element: <OrdersPage />,
            loader: ordersLoader,
          },
          {
            path: "addresses",
            element: <AddressesPage />,
            loader: addressesLoader,
          },
          {
            path: "paymentmethods",
            element: <PaymentMethods />,
          },
          {
            path: "stats",
            element: <DataPage />
          }
        ]
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
