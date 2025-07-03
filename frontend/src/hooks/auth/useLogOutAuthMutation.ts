import AppRoute from "@/routers/enums/routers-enums";
import { clearToken, setAuthInitialized } from "@/store/slices/tokenSlice";
import { authService } from "@/utils/packages/auth";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router";
import { toast } from "react-toastify";

function useLogOutAuthMutation() {
  const dispatch = useDispatch();
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const {mutate: logOut, isPending} = useMutation({
    mutationFn: () => authService.logOutAuth(),
    onSuccess: (data) => {
      console.log('logOut', data),
      toast.success('Log Out successfully')

      navigate(AppRoute.ROOT, { replace: true });

      queryClient.removeQueries({ queryKey: ['user'] });
      dispatch(clearToken());
      dispatch(setAuthInitialized(false));
    },
    onError: (error) => {
      console.log('log out error', error)
    }
  })

  return {logOut, isPending}
}

export default useLogOutAuthMutation;