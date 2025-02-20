import { Outlet } from "react-router";
import Header from "../Header/Header";
import Footer from "../Footer/Footer";

function Layout() {
  return (
    <>
      <Header />
        <main className="main">
          <div className="container mx-auto">
            <Outlet />
          </div>
        </main>
      <Footer />
    </>
  );
}

export default Layout;