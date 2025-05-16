import axios from "axios";

interface LogInProps {
  email: string,
  password: string
}

export async function LogIn(data: LogInProps) {
  const BASE_URL = import.meta.env.VITE_BASE_URL;

  try {
    const response = await axios.post(`${BASE_URL}/api/auth/login/`, data);

    return response.data
  } catch (error:unknown) {
    if(axios.isAxiosError(error)) {
      throw error.response?.data
    }
    throw { message: "Невідома помилка" };
  }
}
