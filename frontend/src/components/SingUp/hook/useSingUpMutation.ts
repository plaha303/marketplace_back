import { useAppDispatch } from "@/store/hooks/hooks";
import {useMutation} from "@tanstack/react-query"
import { SingUp } from "../API/SingUp";
import { openAuthModal, setCodeSent } from "@/store/authModalSlice";


function useSingUpMutation()  {
  const dispatch = useAppDispatch();

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