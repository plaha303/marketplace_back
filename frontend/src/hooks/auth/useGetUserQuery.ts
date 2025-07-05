import { useAppSelector } from "@/store/hooks/hooks";
import { authService } from "@/utils/packages/auth";
import { useQuery } from "@tanstack/react-query";

function useGetUserQuery() {
  const isAuthInitialized = useAppSelector(state => state.token.isAuthInitialized);
  const isAccessToken = useAppSelector(state => state.token.accessToken);

  const {data, isPending: getUserProfilePending } = useQuery({
    queryKey: ['user'],
    queryFn: () => authService.getUser(),
    enabled: isAuthInitialized && !!isAccessToken,
    refetchOnWindowFocus: false,
    retry: false,
  })

  const getUserProfile = data?.data;

  return {getUserProfile, getUserProfilePending}
}

export default useGetUserQuery;