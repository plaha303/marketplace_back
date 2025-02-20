import { BrowserRouter, Route, Routes } from "react-router";
import Layout from "./layout/Layout/Layout";
import Home from "./pages/Home/Home";
import Support from "./pages/Support/Support";


function App() {
	return (
		<BrowserRouter>
			<Routes>
				<Route element={<Layout />}>
					<Route index element={<Home />} />
					<Route path="/support" element={<Support />} />
				</Route>
			</Routes>
		</BrowserRouter>
	)
}

export default App
