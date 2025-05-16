import axios from "axios";

interface EmailConfirmProps {
  code: string
}

export async function EmailConfirm(code: EmailConfirmProps) {
  console.log('qwer', code)
  const BASE_URL = import.meta.env.VITE_BASE_URL;

  try {
    const response = await axios.post(`${BASE_URL}/api/auth/verify-email/`, {code});

    return response.data
  } catch (error) {
    if(axios.isAxiosError(error)) {
      throw error.response?.data;
    }
    throw {message: 'An unknown error'}
  }
}
