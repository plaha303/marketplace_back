import { createBrowserRouter } from "react-router";
import AppRoute from "./enums/routers-enums";
import Layout from "@/layout/Layout/Layout";
import NotFound from "@/pages/NotFound/NotFound";
import Home from "@/pages/Home/Home";
import Support from "@/pages/Support/Support";
import ProtectedRoute from "@/layout/ProtectedRoute/ProtectedRoute";
import UserProfile from "@/pages/UserProfile/UserProfile";
import LogInPage from "@/pages/LogInPage/LogInPage";

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
        path: AppRoute.REGISTRATION,
        element: <LogInPage />
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