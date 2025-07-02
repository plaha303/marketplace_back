import { useAppDispatch } from "@/store/hooks/hooks";
import { setToken } from "@/store/slices/tokenSlice";
import { authService } from "@/utils/packages/auth";
import { LogInRequestDTO } from "@/utils/packages/auth/type/interfaces";
import { useMutation } from "@tanstack/react-query";
import { toast } from "react-toastify";


function useLogInMutation() {
  const dispatch = useAppDispatch();

  const {mutate: mutateLogIn, isPending: mutateLoginPending, isError, error} = useMutation({
    mutationFn: (data: LogInRequestDTO) => authService.logInAuth(data),
    onSuccess: (data) => {
      toast.success('You have successfully logged in')
      console.log('Log in success')
      console.log('Log in success', data)
      if(data?.success) {
        dispatch(setToken(data?.access))
      }
    },
    onError: (error) => {
      console.log('useLogInMutation error: ', error)
    },
  })

  return {mutateLogIn, mutateLoginPending, isError, error}
}

export default useLogInMutation;