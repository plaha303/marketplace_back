import { authService } from "@/utils/packages/auth";
import { LogInRequestDTO } from "@/utils/packages/auth/type/interfaces";
import { useMutation } from "@tanstack/react-query";
import { toast } from "react-toastify";


function useLogInMutation() {
  const {mutate: mutateLogIn, isPending: mutateLoginPending, isError, error} = useMutation({
    mutationFn: (data: LogInRequestDTO) => authService.logInAuth(data),
    onSuccess: () => {
      toast.success('You have successfully logged in')
      console.log('Log in success')
    },
    onError: (error) => {
      console.log('useLogInMutation error: ', error)
    },
  })

  return {mutateLogIn, mutateLoginPending, isError, error}
}

export default useLogInMutation;