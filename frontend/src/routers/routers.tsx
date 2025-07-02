import { createBrowserRouter } from "react-router";
import AppRoute from "./enums/routers-enums";
import Layout from "@/layout/Layout/Layout";
import NotFound from "@/pages/NotFound/NotFound";
import Home from "@/pages/Home/Home";
import Support from "@/pages/Support/Support";
import ProtectedRoute from "@/layout/ProtectedRoute/ProtectedRoute";
import UserProfile from "@/pages/UserProfile/UserProfile";
import LogInPage from "@/pages/LogInPage/LogInPage";
import SignUpPage from "@/pages/SignUpPage/SignUpPage";
import ForgotPasswordPage from "@/pages/ForgotPasswordPage/ForgotPasswordPage";
import SendConfirmLetter from "@/components/SendConfirmLetter/SendConfirmLetter";
import VerifyEmail from "@/components/VerifyEmail/VerifyEmail";
import UserOrders from "@/pages/UserOrders/UserOrders";
import UserFavorite from "@/pages/UserFavorite/UserFavorite";
import UserNotification from "@/pages/UserNotification/UserNotification";
import UserSettings from "@/pages/UserSettings/UserSettings";
import UserGoods from "@/pages/UserGoods/UserGoods";
import UserReviews from "@/pages/UserReviews/UserReviews";
import UserMaster from "@/pages/UserMaster/UserMaster";



export const routers = createBrowserRouter([
  {
    path: AppRoute.ROOT,
    element: <Layout />,
    errorElement: <NotFound />,
    children: [
      {
        path: AppRoute.ROOT,
        element: <Home />
      },
      {
        path: AppRoute.SUPPORT,
        element: <Support />
      },
      {
        path: AppRoute.LOGIN,
        element: <LogInPage />
      },
      {
        path: AppRoute.REGISTRATION,
        element: <SignUpPage />
      },
      {
        path: AppRoute.VERIFYEMAIL,
        element: <VerifyEmail />
      },
      {
        path: AppRoute.SENDCONFIRMLETTER,
        element: <SendConfirmLetter />
      },
      {
        path: AppRoute.RESET_PASSWORD,
        element: <ForgotPasswordPage />
      },
    ],
  },
  {
    element: <ProtectedRoute />,
    children: [
      {
        path: AppRoute.MASTER,
        element: <UserProfile/>
      },
      {
        path: AppRoute.PROFILE,
        element: <UserProfile/>
      },
      {
        path: AppRoute.ORDERS,
        element: <UserOrders/>
      },
      {
        path: AppRoute.FAVORITE,
        element: <UserFavorite />
      },
      {
        path: AppRoute.NOTIFICATION,
        element: <UserNotification />
      },
      {
        path: AppRoute.SETTINGS,
        element: <UserSettings />
      },
      {
        path: AppRoute.GOODS,
        element: <UserGoods />
      },
      {
        path: AppRoute.REVIEWS,
        element: <UserReviews />
      },
      {
        path: AppRoute.MASTER,
        element: <UserMaster />
      },
    ]
  }
])