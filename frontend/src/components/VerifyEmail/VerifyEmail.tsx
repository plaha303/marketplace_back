import { useNavigate, useParams } from "react-router";
import useVerifyEmailQuery from "./hook/useVerifyEmailQuery";
import { useEffect } from "react";
import AppRoute from "@/routers/enums/routers-enums";
import { CustomError } from "@/utils/packages/auth/type/interfaces";

function VerifyEmail() {
  const { uid, token } = useParams();
  const navigate = useNavigate();

  console.log('re', uid, token)

  const data = {
    uid: uid || '',
    token: token || '',
  }
  const {verifyEmailResponse, isPending, isError, error} = useVerifyEmailQuery(data);

  useEffect(() => {
    if(verifyEmailResponse?.success) {
      const timeout = setTimeout(() => {
        navigate(AppRoute.LOGIN); 
      }, 5000)

      return () => clearTimeout(timeout)
    }

  }, [verifyEmailResponse, navigate])

  if (isPending) return <div>Підтвердження email...</div>;
  if (isError) {
    const customError = error as CustomError;
    const fieldError = customError?.fieldErrors?.non_field_errors;
    const generalMessage = customError?.message ?? 'Невідома помилка';

    return (
      <div>
        <p>Помилка підтвердження email:</p>
        <p style={{ color: 'red' }}>
          {fieldError || generalMessage}
        </p>
      </div>
    );

  };

  return (
    <div>Email успішно підтверджено. Відбувається перехід на сторінку Log in</div>
  );
}

export default VerifyEmail;