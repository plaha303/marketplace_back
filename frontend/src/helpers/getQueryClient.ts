import { QueryClient } from "@tanstack/react-query";

let queryClient: QueryClient;

export function setQueryClientInstance(client: QueryClient) {
  queryClient = client;
}

export function getQueryClient() {
  return queryClient;
}