import {useMutation} from "@tanstack/react-query"
import { authService } from "@/utils/packages/auth";
import { SignUpRequestDTO } from "@/utils/packages/auth/type/interfaces";


function useSignUpMutation()  {
  const {mutate: mutateSignUp, isPending: mutateSignUpPenging, isError, error} = useMutation({
    mutationFn: (data: SignUpRequestDTO) => authService.signUpAuth(data),
    onSuccess: () => {
      console.log('useSignUpMutation work');
    },
    onError: (error) => {
      console.log('useSignUpMutation error: ', error)
    },
  })

  return {mutateSignUp, mutateSignUpPenging, isError, error}
}

export default useSignUpMutation;