import { useAppDispatch } from "@/store/hooks/hooks";
import { useMutation } from "@tanstack/react-query";
import { EmailConfirm } from "../API/EmailConfirm";
import { closeAuthModal } from "@/store/authModalSlice";
import { toast } from "react-toastify";


function useEmailConfirmMutation() {
  const dispatch = useAppDispatch();

  const {mutate: emailConfirm, isPending: emailConfirmPending, isError, error} = useMutation({
    mutationFn: EmailConfirm,
    onSuccess: () => {
      console.log('email confirm ok')
      toast.success('You have successfully confirm your email')
      dispatch(closeAuthModal())
    },
    onError: (error, variables, context) => {
      console.log('error: ', error)
    }
  })

  return {emailConfirm, emailConfirmPending, isError, error}
}

export default useEmailConfirmMutation;