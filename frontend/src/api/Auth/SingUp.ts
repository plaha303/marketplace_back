import axios from "axios"

interface SingUpProps {
  userName: string,
  email: string,
  password: string,
  password2: string,
}


export async function SingUp(data: SingUpProps) {
  console.log('SingUp', data)
  const BASE_URL = import.meta.env.VITE_BASE_URL;

  try {
    const response = await axios.post(`${BASE_URL}/api/auth/register/`, data);

    return response.data
  } catch (error:unknown) {
    if(axios.isAxiosError(error)) {
      throw error.response?.data;
    }
    throw { message: "Невідома помилка" };
  }
  
}