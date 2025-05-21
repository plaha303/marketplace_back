import { AxiosError } from "axios";
import { ApiError } from "./type/interface";

export function normalizeApiError(error: unknown): ApiError {
  if(error instanceof AxiosError) {
    const row = error.response?.data

    const message = typeof row === 'string' ? row : row?.message ?? row?.error?.message ?? 'Server error';

    const fieldErrors =  row && typeof row === 'object' && row.data && typeof row.data === 'object' 
    ? Object.fromEntries(Object.entries(row.data).filter(([_, v]) => typeof v === "string")) as Record<string, string>
    : undefined;

    return {message, statusCode: error.response?.status, original: row, fieldErrors}
  }

  if(error instanceof Error) {
    return {message: error.message, original: error}
  }

  return {message: 'Unknow Error', original: error}
}