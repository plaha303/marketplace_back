import axios from "axios";

export async function EmailConfirm() {
  const BASE_URL = import.meta.env.VITE_BASE_URL;
  try {
    const response = await axios.post(`${BASE_URL}/`)
  } catch (error) {
    
  }
}