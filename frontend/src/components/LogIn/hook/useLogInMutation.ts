import { authService } from "@/utils/packages/auth";
import { useMutation } from "@tanstack/react-query";
import { toast } from "react-toastify";


function useLogInMutation() {
  const {mutate: mutateLogIn, isPending: mutateLoginPending, isError, error} = useMutation({
    mutationFn: authService.logInAuth,
    onSuccess: () => {
      toast.success('You have successfully logged in')
      console.log('Log in success')
    },
  })

  return {mutateLogIn, mutateLoginPending, isError, error}
}

export default useLogInMutation;