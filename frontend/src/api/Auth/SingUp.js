import axios from "axios"

export async function SingUp({username, email, password, password2}) {
  const BASE_URL = import.meta.env.VITE_BASE_URL;

  const response = await axios.post(`${BASE_URL}/api/auth/register/`, {username, email, password, password2});

  return response.data
}