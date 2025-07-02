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
    <div>
       <Header/>
       <main className="main">
          <Suspense fallback={<div>Loading...</div>}>
            <Outlet />
          </Suspense>
       </main>
       <Footer />
    </div>
  );
}

export default ProtectedRoute;