import { BrowserRouter, Route, RouterProvider, Routes } from "react-router";
import Layout from "./layout/Layout/Layout";
import Home from "./pages/Home/Home";
import Support from "./pages/Support/Support";
import NotFound from "./pages/NotFound/NotFound"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { setQueryClientInstance } from "./utils/helpers/getQueryClient";
import { Bounce, ToastContainer } from "react-toastify";
import { routers } from "./routers/routers";
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import useGetUserQuery from "./hooks/auth/useGetUserQuery";
import { useInitAuth } from "./hooks/auth/useInitAuth";

	function InitAuth() {
		useInitAuth();
		return null
	}

function App() {
	const queryClient = new QueryClient();
	setQueryClientInstance(queryClient);

	return (
		<>
			<QueryClientProvider client={queryClient}>
				<ReactQueryDevtools initialIsOpen={false} />
				<InitAuth />
				<RouterProvider router={routers} />
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
