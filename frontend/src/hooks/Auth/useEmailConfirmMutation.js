import { useMutation } from "@tanstack/react-query";
import {EmailConfirm} from "../../api/Auth/EmailConfirm"
import { useDispatch } from "react-redux";
import { closeAuthModal } from "../../store/authModalSlice";

function useEmailConfirmMutation() {
  const dispatch = useDispatch();

  const {mutate: emailConfirm, isPending: emailConfirmPending, isError, error} = useMutation({
    mutationFn: EmailConfirm,
    onSuccess: () => {
      console.log('email confirm ok')
      dispatch(closeAuthModal())
    },
    onError: (error, variables, context) => {
      cconsole.log('error: ', error)
    }
  })

  return {emailConfirm, emailConfirmPending, isError, error}
}

export default useEmailConfirmMutation;