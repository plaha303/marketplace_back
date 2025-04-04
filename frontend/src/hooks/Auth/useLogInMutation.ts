import { useMutation } from "@tanstack/react-query";
import { LogIn } from "../../api/Auth/LogIn";

function useLogInMutation() {
  const {mutate: mutateLogIn, isPending: mutateLoginPending, isError, error} = useMutation({
    mutationFn: LogIn,
    onSuccess: () => {
      console.log('Log in success')
    },
    onError: (error) => {
      console.error("Ошибка входа:", error);
    },
  })

  return {mutateLogIn, mutateLoginPending, isError, error}
}

export default useLogInMutation;