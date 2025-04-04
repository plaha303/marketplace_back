import { BrowserRouter, Route, Routes } from "react-router";
import { Provider } from "react-redux"
import Layout from "./layout/Layout/Layout";
import Home from "./pages/Home/Home";
import Support from "./pages/Support/Support";
import store from "./store/store";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";


function App() {
	const queryClient = new QueryClient();
	return (
		<QueryClientProvider client={queryClient}>
			<Provider store={store}>
				<BrowserRouter>
					<Routes>
						<Route element={<Layout />}>
							<Route index element={<Home />} />
							<Route path="/support" element={<Support />} />
						</Route>
					</Routes>
				</BrowserRouter>
			</Provider>
		</QueryClientProvider>
	)
}

export default App
