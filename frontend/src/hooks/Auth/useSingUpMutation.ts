import {useMutation} from "@tanstack/react-query"
import { SingUp } from "../../api/Auth/SingUp"
import { useDispatch } from "react-redux"
import { openAuthModal, setCodeSent } from "../../store/authModalSlice";

function useSingUpMutation()  {
  const dispatch = useDispatch();

  const {mutate: mutateSingUp, isPending: mutateSingUpPenging, isError, error} = useMutation({
    mutationFn: SingUp,
    onSuccess: () => {
      console.log('useSingUpMutation work');
      dispatch(openAuthModal('EmailConfirm'));
      dispatch(setCodeSent(true))
    },
    onError: (error) => {
      console.log('error: ', error)
    },
  })

  return {mutateSingUp, mutateSingUpPenging, isError, error}
}

export default useSingUpMutation;