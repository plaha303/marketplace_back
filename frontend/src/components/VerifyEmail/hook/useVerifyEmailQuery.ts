import { authService } from "@/utils/packages/auth";
import { VerifyEmailRequestDTO } from "@/utils/packages/auth/type/interfaces";
import { useQuery } from "@tanstack/react-query";


function useVerifyEmailQuery(data: VerifyEmailRequestDTO) {
  const {data: verifyEmailResponse, isPending, isError, error} = useQuery({
    queryKey: ['verifyEmailKey', data],
    queryFn: () => authService.verifyEmailAuth(data),
    enabled: !!data?.uid && !!data?.token
  })

  return {verifyEmailResponse, isPending, isError, error}
}

export default useVerifyEmailQuery;