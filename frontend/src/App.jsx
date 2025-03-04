import { BrowserRouter, Route, Routes } from "react-router";
import { Provider } from "react-redux"
import Layout from "./layout/Layout/Layout";
import Home from "./pages/Home/Home";
import Support from "./pages/Support/Support";
import { store } from "./store/store";


function App() {
	return (
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
	)
}

export default App
