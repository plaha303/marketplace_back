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
import EmailConfirm from "@/components/EmailConfirm/EmailConfirm";


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
      // {
      //   path: AppRoute.CONFIRM_EMAIL,
      //   element: <EmailConfirm />
      // },
      {
        path: AppRoute.RESET_PASSWORD,
        element: <ForgotPasswordPage />
      },
      {
        element: <ProtectedRoute />,
        children: [
          {
            path: AppRoute.PROFILE,
            element: <UserProfile/>
          }
        ]
      }
    ]
  }
])