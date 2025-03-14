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
      if (error.response?.data?.errors) {
        return error.response.errors;
      }
    },
  })

  return {mutateSingUp, mutateSingUpPenging}
}

export default useSingUpMutation;