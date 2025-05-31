import { isAxiosError } from "axios";
import { ApiError } from "./type/interface";

export function normalizeApiError(error: unknown): ApiError {
  if(isAxiosError(error)) {
    const row = error.response?.data;

    console.log('row', row)

    const message = typeof row === 'string'
      ? (row.startsWith('<!DOCTYPE html') ? 'Server error' : row)
      : row?.message ?? row?.error?.message ?? 'Server error';

    const possibleFieldErrors = row && typeof row === 'object' ? row?.data || row?.errors || row?.error?.errors : undefined;

    console.log('possibleFieldErrors err', possibleFieldErrors)

    const fieldErrors =
  possibleFieldErrors && typeof possibleFieldErrors === 'object'
    ? Object.fromEntries(
        Object.entries(possibleFieldErrors)
          .filter(([_, v]) => Array.isArray(v) && typeof v[0] === 'string')
          .map(([key, value]) => [key, (value as string[])[0]])
      ) as Record<string, string>
    : undefined;

    return {message, statusCode: error.response?.status, original: row, fieldErrors}
  }

  if(error instanceof Error) {
    return {message: error.message, original: error}
  }

  return {message: 'Unknow Error', original: error}
}