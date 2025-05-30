import { useMutation } from "@tanstack/react-query";
import { LogIn } from "../API/LogIn";
import { toast } from "react-toastify";


function useLogInMutation() {
  const {mutate: mutateLogIn, isPending: mutateLoginPending, isError, error} = useMutation({
    mutationFn: LogIn,
    onSuccess: () => {
      toast.success('You have successfully logged in')
      console.log('Log in success')
    },
  })

  return {mutateLogIn, mutateLoginPending, isError, error}
}

export default useLogInMutation;