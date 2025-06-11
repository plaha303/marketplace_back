import { BrowserRouter, Route, RouterProvider, Routes } from "react-router";
import { Provider } from "react-redux"
import Layout from "./layout/Layout/Layout";
import Home from "./pages/Home/Home";
import Support from "./pages/Support/Support";
import NotFound from "./pages/NotFound/NotFound"
import store from "./store/store";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { setQueryClientInstance } from "./utils/helpers/getQueryClient";
import { Bounce, ToastContainer } from "react-toastify";
import { routers } from "./routers/routers";

function App() {
	const queryClient = new QueryClient();
	setQueryClientInstance(queryClient);
	
	return (
		<>
			<QueryClientProvider client={queryClient}>
				<Provider store={store}>
					<RouterProvider router={routers} />
				</Provider>
			</QueryClientProvider>

			<ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick={false}
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="colored"
        transition={Bounce}
        />
		</>
	)
}

export default App
