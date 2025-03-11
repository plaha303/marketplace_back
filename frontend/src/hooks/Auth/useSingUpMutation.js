import {useMutation} from "@tanstack/react-query"
import { SingUp } from "../../api/Auth/SingUp"
import { useDispatch } from "react-redux"
import { openAuthModal } from "../../store/authModalSlice";

function useSingUpMutation() {
  const dispatch = useDispatch();

  const {mutate: mutateSingUp, isPending: mutateSingUpPenging} = useMutation({
    mutationFn: SingUp,
    onSuccess: () => {
      console.log('useSingUpMutation work');
      dispatch(openAuthModal());
    },
    onError: (error, variables, context) => {
      console.log(`rolling back optimistic update with id ${context.id}`)
    },
  })

  return {mutateSingUp, mutateSingUpPenging}
}

export default useSingUpMutation;