import { Suspense } from "react";
import Footer from "../Footer/Footer";
import Header from "../Header/Header";
import { Outlet } from "react-router";

function ProtectedRoute() {
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