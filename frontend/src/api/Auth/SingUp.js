import axios from "axios"

export async function SingUp(data) {
  console.log('SingUp', data)
  const BASE_URL = import.meta.env.VITE_BASE_URL;

  try {
    const response = await axios.post(`${BASE_URL}/api/auth/register/`, data);
    console.log('response', response)
    return response.data
  } catch (error) {
    throw error.response?.data || { message: "Невідома помилка" };
  }
  
}