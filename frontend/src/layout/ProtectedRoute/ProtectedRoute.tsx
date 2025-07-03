import { Suspense } from "react";
import Footer from "../Footer/Footer";
import Header from "../Header/Header";
import { Navigate, Outlet } from "react-router";
import { useAppSelector } from "@/store/hooks/hooks";
import AppRoute from "@/routers/enums/routers-enums";

function ProtectedRoute() {
  const accessToken = useAppSelector(state => state.token.accessToken);
  const isAuthInitialized = useAppSelector(state => state.token.isAuthInitialized);

  if (!isAuthInitialized) {
    return <div className="container px-4 mx-auto">Loading...</div>
  }

  if(!accessToken) {
    return <Navigate to={AppRoute.ROOT} replace></Navigate>
  }
 
  return (
    <div className="flex flex-col min-h-screen">
      <Header/>
      <main className="main flex-1">
        <Suspense fallback={<div>Loading...</div>}>
          <Outlet />
        </Suspense>
      </main>
      <Footer />
    </div>
  );
}

export default ProtectedRoute;